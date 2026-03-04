#!/usr/bin/env python3
"""
Compile knowledge graph data into static JSON files for the Astro site.

Queries Neo4j and exports pre-built JSON views that the static site
can consume without any database connection at runtime.

Usage:
    python3 scripts/compile_site_data.py
    python3 scripts/compile_site_data.py --output site/src/data
"""

import argparse
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "core" / "scripts"))

from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


# ── Helpers ──────────────────────────────────────────────────────────

def write_json(path: Path, data):
    """Write JSON with consistent formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)


def slugify(text: str) -> str:
    """Convert text to URL-safe slug."""
    import re
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')


# ── Query functions ──────────────────────────────────────────────────

def query_overview(session) -> dict:
    """Global stats for the homepage."""
    stats = {}

    # Node counts by label
    counts_query = """
        MATCH (c:Concept) WITH count(c) AS concepts
        MATCH (cl:ConceptCluster) WITH concepts, count(cl) AS clusters
        MATCH (d:Domain) WITH concepts, clusters, count(d) AS domains
        MATCH (o:Objective) WITH concepts, clusters, domains, count(o) AS objectives
        MATCH (s:Subject) WITH concepts, clusters, domains, objectives, count(s) AS subjects
        MATCH (ks:KeyStage) WITH concepts, clusters, domains, objectives, subjects, count(ks) AS key_stages
        MATCH (tl:ThinkingLens) WITH concepts, clusters, domains, objectives, subjects, key_stages, count(tl) AS lenses
        MATCH (dl:DifficultyLevel) WITH concepts, clusters, domains, objectives, subjects, key_stages, lenses, count(dl) AS difficulty_levels
        RETURN concepts, clusters, domains, objectives, subjects, key_stages, lenses, difficulty_levels
    """
    r = session.run(counts_query).single()
    stats['concepts'] = r['concepts']
    stats['clusters'] = r['clusters']
    stats['domains'] = r['domains']
    stats['objectives'] = r['objectives']
    stats['subjects'] = r['subjects']
    stats['key_stages_count'] = r['key_stages']
    stats['thinking_lenses'] = r['lenses']
    stats['difficulty_levels'] = r['difficulty_levels']

    # Prerequisite count
    prereq_query = """
        MATCH ()-[r:PREREQUISITE_OF]->() RETURN count(r) AS count
    """
    stats['prerequisites'] = session.run(prereq_query).single()['count']

    # Key stages with year info
    ks_query = """
        MATCH (ks:KeyStage)
        OPTIONAL MATCH (ks)-[:HAS_YEAR]->(y:Year)
        WITH ks, collect(y) AS years
        OPTIONAL MATCH (ks)-[:HAS_YEAR]->(:Year)-[:HAS_PROGRAMME]->(:Programme)
                        -[:HAS_DOMAIN]->(:Domain)-[:HAS_CONCEPT]->(c:Concept)
        WITH ks, years, count(DISTINCT c) AS concept_count
        RETURN ks.key_stage_id AS id, ks.name AS name,
               [y IN years | y.year_id] AS year_ids,
               concept_count
        ORDER BY ks.key_stage_id
    """
    stats['key_stages'] = []
    for r in session.run(ks_query):
        year_ids = sorted(r['year_ids'], key=lambda y: (
            0 if y == 'EYFS' else int(y.replace('Y', '')) if y.startswith('Y') else 99
        ))
        stats['key_stages'].append({
            'id': r['id'],
            'name': r['name'],
            'year_ids': year_ids,
            'concept_count': r['concept_count'],
        })

    return stats


def query_subjects(session) -> list[dict]:
    """All subjects with year/domain breakdown and delivery modes."""
    query = """
        MATCH (s:Subject)<-[:FOR_SUBJECT]-(p:Programme)<-[:HAS_PROGRAMME]-(y:Year)
              <-[:HAS_YEAR]-(ks:KeyStage)
        WITH s, y, ks,
             collect(DISTINCT p) AS progs
        UNWIND progs AS p
        MATCH (p)-[:HAS_DOMAIN]->(d:Domain)
        OPTIONAL MATCH (d)-[:HAS_CONCEPT]->(c:Concept)
        WITH s, y, ks, d, count(DISTINCT c) AS concept_count
        OPTIONAL MATCH (d)-[:HAS_CLUSTER]->(cl:ConceptCluster)
        WITH s, y, ks, d, concept_count, count(DISTINCT cl) AS cluster_count
        RETURN s.name AS subject_name, s.subject_id AS subject_id,
               ks.key_stage_id AS key_stage_id,
               y.year_id AS year_id, y.year_number AS year_number,
               d.domain_id AS domain_id, d.name AS domain_name,
               concept_count, cluster_count
        ORDER BY s.name, y.year_number, d.domain_id
    """
    records = session.run(query).data()

    # Group by subject
    subjects_map = {}
    for r in records:
        sid = r['subject_id']
        if sid not in subjects_map:
            subjects_map[sid] = {
                'subject_id': sid,
                'name': r['subject_name'],
                'slug': slugify(r['subject_name']),
                'key_stages': [],
                'years': {},
                'total_concepts': 0,
                'total_domains': 0,
                'total_clusters': 0,
            }
        subj = subjects_map[sid]
        ks = r['key_stage_id']
        if ks not in subj['key_stages']:
            subj['key_stages'].append(ks)

        yid = r['year_id']
        if yid not in subj['years']:
            subj['years'][yid] = {
                'year_id': yid,
                'year_number': r['year_number'],
                'key_stage': ks,
                'domains': [],
            }
        subj['years'][yid]['domains'].append({
            'domain_id': r['domain_id'],
            'name': r['domain_name'],
            'concept_count': r['concept_count'],
            'cluster_count': r['cluster_count'],
        })
        subj['total_concepts'] += r['concept_count']
        subj['total_domains'] += 1
        subj['total_clusters'] += r['cluster_count']

    # Convert years dict to sorted list
    for subj in subjects_map.values():
        subj['years'] = sorted(subj['years'].values(),
                                key=lambda y: y['year_number'] or 0)

    return sorted(subjects_map.values(), key=lambda s: s['name'])


def query_delivery_modes(session) -> dict:
    """Delivery mode breakdown for the dashboard."""
    # Overall summary
    summary_query = """
        MATCH (c:Concept)-[dv:DELIVERABLE_VIA {primary: true}]->(dm:DeliveryMode)
        RETURN dm.mode_id AS mode_id, dm.name AS mode_name,
               dm.display_color AS color,
               count(c) AS count
        ORDER BY dm.mode_id
    """
    summary = session.run(summary_query).data()

    # By subject
    by_subject_query = """
        MATCH (s:Subject)<-[:FOR_SUBJECT]-(:Programme)-[:HAS_DOMAIN]->(:Domain)
              -[:HAS_CONCEPT]->(c:Concept)
              -[dv:DELIVERABLE_VIA {primary: true}]->(dm:DeliveryMode)
        RETURN s.name AS subject, dm.mode_id AS mode_id, dm.name AS mode_name,
               count(DISTINCT c) AS count
        ORDER BY subject, dm.mode_id
    """
    by_subject_raw = session.run(by_subject_query).data()
    by_subject = defaultdict(lambda: {'subject': '', 'modes': {}})
    for r in by_subject_raw:
        subj = r['subject']
        by_subject[subj]['subject'] = subj
        by_subject[subj]['modes'][r['mode_id']] = {
            'name': r['mode_name'],
            'count': r['count'],
        }

    # By key stage
    by_ks_query = """
        MATCH (ks:KeyStage)-[:HAS_YEAR]->(:Year)-[:HAS_PROGRAMME]->(:Programme)
              -[:HAS_DOMAIN]->(:Domain)-[:HAS_CONCEPT]->(c:Concept)
              -[dv:DELIVERABLE_VIA {primary: true}]->(dm:DeliveryMode)
        RETURN ks.key_stage_id AS key_stage, dm.mode_id AS mode_id,
               dm.name AS mode_name, count(DISTINCT c) AS count
        ORDER BY key_stage, dm.mode_id
    """
    by_ks_raw = session.run(by_ks_query).data()
    by_ks = defaultdict(lambda: {'key_stage': '', 'modes': {}})
    for r in by_ks_raw:
        ks = r['key_stage']
        by_ks[ks]['key_stage'] = ks
        by_ks[ks]['modes'][r['mode_id']] = {
            'name': r['mode_name'],
            'count': r['count'],
        }

    # Teaching requirements
    req_query = """
        MATCH (tr:TeachingRequirement)
        OPTIONAL MATCH (c:Concept)-[:HAS_TEACHING_REQUIREMENT]->(tr)
        WITH tr, count(c) AS concept_count
        OPTIONAL MATCH (tr)-[:IMPLIES_MINIMUM_MODE]->(dm:DeliveryMode)
        RETURN tr.requirement_id AS id, tr.name AS name,
               tr.category AS category, tr.description AS description,
               concept_count, dm.name AS implies_mode
        ORDER BY tr.category, tr.name
    """
    requirements = session.run(req_query).data()

    # DeliveryMode definitions
    modes_query = """
        MATCH (dm:DeliveryMode)
        RETURN dm.mode_id AS id, dm.name AS name, dm.description AS description,
               dm.display_color AS color
        ORDER BY dm.mode_id
    """
    modes = session.run(modes_query).data()

    return {
        'modes': modes,
        'summary': summary,
        'by_subject': sorted(by_subject.values(), key=lambda x: x['subject']),
        'by_key_stage': sorted(by_ks.values(), key=lambda x: x['key_stage']),
        'requirements': requirements,
    }


def query_domain_detail(session, domain_id: str) -> dict:
    """Complete domain data including concepts, clusters, and metadata."""
    # Domain info
    domain_query = """
        MATCH (d:Domain {domain_id: $did})
        OPTIONAL MATCH (d)<-[:HAS_DOMAIN]-(p:Programme)-[:FOR_SUBJECT]->(s:Subject)
        OPTIONAL MATCH (p)<-[:HAS_PROGRAMME]-(y:Year)<-[:HAS_YEAR]-(ks:KeyStage)
        RETURN d.domain_id AS domain_id, d.name AS name,
               d.description AS description, d.curriculum_context AS curriculum_context,
               s.name AS subject, s.subject_id AS subject_id,
               y.year_id AS year_id, y.year_number AS year_number,
               ks.key_stage_id AS key_stage, ks.name AS key_stage_name
    """
    dr_rows = session.run(domain_query, did=domain_id).data()
    if not dr_rows:
        return None
    dr = dr_rows[0]

    domain = {
        'domain_id': dr['domain_id'],
        'name': dr['name'],
        'description': dr['description'],
        'curriculum_context': dr['curriculum_context'],
        'subject': dr['subject'],
        'subject_id': dr['subject_id'],
        'subject_slug': slugify(dr['subject'] or ''),
        'year_id': dr['year_id'],
        'year_number': dr['year_number'],
        'key_stage': dr['key_stage'],
        'key_stage_name': dr['key_stage_name'],
    }

    # Concepts with difficulty levels, representation stages, delivery modes, vocabulary
    concepts_query = """
        MATCH (d:Domain {domain_id: $did})-[:HAS_CONCEPT]->(c:Concept)
        OPTIONAL MATCH (c)-[:HAS_DIFFICULTY_LEVEL]->(dl:DifficultyLevel)
        OPTIONAL MATCH (c)-[:HAS_REPRESENTATION_STAGE]->(rs:RepresentationStage)
        OPTIONAL MATCH (c)-[dv:DELIVERABLE_VIA {primary: true}]->(dm:DeliveryMode)
        OPTIONAL MATCH (c)-[ut:USES_TERM]->(vt:VocabularyTerm)
        WITH c,
             collect(DISTINCT properties(dl)) AS dls,
             collect(DISTINCT properties(rs)) AS rss,
             collect(DISTINCT {
                term_id: vt.term_id, term: vt.term, definition: vt.definition,
                tier: vt.tier, word_class: vt.word_class,
                introduced: ut.introduced, importance: ut.importance
             }) AS vocab_terms,
             dm, dv
        RETURN c.concept_id AS concept_id, c.name AS name,
               c.description AS description, c.concept_type AS concept_type,
               c.teaching_weight AS teaching_weight, c.is_keystone AS is_keystone,
               c.teaching_guidance AS teaching_guidance,
               c.key_vocabulary AS key_vocabulary,
               c.common_misconceptions AS common_misconceptions,
               dls, rss,
               [v IN vocab_terms WHERE v.term_id IS NOT NULL | v] AS vocabulary_terms,
               dm.mode_id AS delivery_mode_id, dm.name AS delivery_mode_name,
               dv.confidence AS delivery_confidence, dv.rationale AS delivery_rationale
        ORDER BY c.concept_id
    """
    concepts = []
    seen_concepts = set()
    for r in session.run(concepts_query, did=domain_id):
        cid = r['concept_id']
        if cid in seen_concepts:
            continue
        seen_concepts.add(cid)

        difficulty_levels = sorted(
            [dl for dl in r['dls'] if dl],
            key=lambda x: x.get('level_number', 0)
        )
        representation_stages = sorted(
            [rs for rs in r['rss'] if rs],
            key=lambda x: x.get('stage_number', 0)
        )

        vocabulary_terms = sorted(
            r.get('vocabulary_terms', []),
            key=lambda x: x.get('term', '')
        )

        concepts.append({
            'concept_id': cid,
            'name': r['name'],
            'description': r['description'],
            'concept_type': r['concept_type'],
            'teaching_weight': r['teaching_weight'],
            'is_keystone': r['is_keystone'],
            'teaching_guidance': r['teaching_guidance'],
            'key_vocabulary': r['key_vocabulary'],
            'common_misconceptions': r['common_misconceptions'],
            'difficulty_levels': difficulty_levels,
            'representation_stages': representation_stages,
            'vocabulary_terms': vocabulary_terms,
            'delivery_mode': {
                'mode_id': r['delivery_mode_id'],
                'name': r['delivery_mode_name'],
                'confidence': r['delivery_confidence'],
                'rationale': r['delivery_rationale'],
            } if r['delivery_mode_id'] else None,
        })
    domain['concepts'] = concepts

    # Clusters with thinking lenses
    clusters_query = """
        MATCH (d:Domain {domain_id: $did})-[:HAS_CLUSTER]->(cl:ConceptCluster)
        OPTIONAL MATCH (cl)-[:GROUPS]->(c:Concept)
        OPTIONAL MATCH (cl)-[al:APPLIES_LENS]->(tl:ThinkingLens)
        OPTIONAL MATCH (cl)-[:SEQUENCED_AFTER]->(prev:ConceptCluster)
        WITH cl,
             collect(DISTINCT c.concept_id) AS concept_ids,
             collect(DISTINCT {
                name: tl.name, rank: al.rank,
                rationale: al.rationale, key_question: tl.key_question
             }) AS lenses,
             collect(DISTINCT prev.cluster_id) AS after_ids
        RETURN cl.cluster_id AS cluster_id, cl.name AS name,
               cl.cluster_type AS cluster_type, cl.rationale AS rationale,
               cl.is_curated AS is_curated,
               cl.teaching_weeks AS teaching_weeks,
               cl.lesson_count AS lesson_count,
               cl.thinking_lens_primary AS thinking_lens_primary,
               concept_ids,
               [l IN lenses WHERE l.name IS NOT NULL | l] AS thinking_lenses,
               after_ids
        ORDER BY cl.cluster_id
    """
    clusters = []
    for r in session.run(clusters_query, did=domain_id):
        lenses = sorted(
            r['thinking_lenses'],
            key=lambda x: x.get('rank', 99)
        )
        clusters.append({
            'cluster_id': r['cluster_id'],
            'name': r['name'],
            'cluster_type': r['cluster_type'],
            'rationale': r['rationale'],
            'is_curated': r['is_curated'],
            'teaching_weeks': r['teaching_weeks'],
            'lesson_count': r['lesson_count'],
            'thinking_lens_primary': r['thinking_lens_primary'],
            'concept_ids': r['concept_ids'],
            'thinking_lenses': lenses,
            'sequenced_after': r['after_ids'],
        })
    domain['clusters'] = clusters

    # Prerequisites from outside this domain
    prereq_query = """
        MATCH (d:Domain {domain_id: $did})-[:HAS_CONCEPT]->(c:Concept)
              <-[:PREREQUISITE_OF]-(prereq:Concept)
        WHERE NOT EXISTS {
            MATCH (d)-[:HAS_CONCEPT]->(prereq)
        }
        OPTIONAL MATCH (prereq)<-[:HAS_CONCEPT]-(pd:Domain)
        RETURN DISTINCT prereq.concept_id AS prereq_id,
               prereq.name AS prereq_name,
               pd.domain_id AS from_domain_id, pd.name AS from_domain_name,
               c.concept_id AS target_id, c.name AS target_name
        ORDER BY prereq.concept_id
    """
    domain['prerequisites'] = session.run(prereq_query, did=domain_id).data()

    # ── Per-subject ontology (study/unit suggestions) ─────────────────
    suggestions_query = """
        MATCH (d:Domain {domain_id: $did})-[:HAS_SUGGESTION]->(s)
        OPTIONAL MATCH (s)-[:DELIVERS_VIA]->(c:Concept)<-[:HAS_CONCEPT]-(d)
        WITH s, labels(s) AS lbls, collect(DISTINCT c.concept_id) AS cids
        OPTIONAL MATCH (s)-[:USES_TEMPLATE]->(vt:VehicleTemplate)
        OPTIONAL MATCH (s)-[:CROSS_CURRICULAR]->(s2)
        OPTIONAL MATCH (s)-[:FOREGROUNDS]->(dc:DisciplinaryConcept)
        OPTIONAL MATCH (s)-[:USES_SOURCE]->(hs:HistoricalSource)
        OPTIONAL MATCH (s)-[:USES_ENQUIRY_TYPE]->(et:EnquiryType)
        OPTIONAL MATCH (s)-[:SURFACES_MISCONCEPTION]->(m:Misconception)
        OPTIONAL MATCH (s)-[:IN_GENRE]->(g:Genre)
        OPTIONAL MATCH (s)-[:LOCATED_IN]->(gp:GeoPlace)
        OPTIONAL MATCH (s)-[:CONTRASTS_WITH]->(gc:GeoContrast)
        RETURN s.name AS name,
               [l IN lbls WHERE l <> 'Node'][0] AS type,
               s.description AS description,
               s.pedagogical_rationale AS pedagogical_rationale,
               s.period AS period,
               s.key_figures AS key_figures,
               s.enquiry_question AS enquiry_question,
               s.enquiry_focus AS enquiry_focus,
               s.writing_outcome AS writing_outcome,
               s.variables AS variables,
               cids AS concept_ids,
               vt.name AS template_name,
               collect(DISTINCT CASE WHEN s2 IS NOT NULL
                   THEN {target_name: s2.name, hook: '', strength: ''}
                   END) AS cross_curricular_raw,
               collect(DISTINCT dc.name) AS disciplinary_concepts,
               collect(DISTINCT hs.name) AS sources,
               collect(DISTINCT et.name) AS enquiry_types,
               collect(DISTINCT m.name) AS misconceptions,
               collect(DISTINCT g.name) AS genres,
               collect(DISTINCT gp.name) AS places,
               collect(DISTINCT gc.name) AS contrasts
        ORDER BY s.name
    """
    suggestions = []
    for r in session.run(suggestions_query, did=domain_id):
        s = {
            'name': r['name'],
            'type': r['type'],
            'description': r['description'],
            'pedagogical_rationale': r['pedagogical_rationale'],
            'concept_ids': r['concept_ids'] or [],
            'template_name': r['template_name'],
            'cross_curricular': [
                x for x in (r['cross_curricular_raw'] or [])
                if x is not None
            ],
        }
        # Subject-specific properties (only include when present)
        if r['period']:
            s['period'] = r['period']
        if r['key_figures']:
            s['key_figures'] = r['key_figures'] if isinstance(r['key_figures'], list) else [r['key_figures']]
        if r.get('disciplinary_concepts'):
            dcs = [x for x in r['disciplinary_concepts'] if x]
            if dcs:
                s['disciplinary_concepts'] = dcs
        if r.get('sources'):
            srcs = [x for x in r['sources'] if x]
            if srcs:
                s['sources'] = srcs
        if r['enquiry_question']:
            s['enquiry_question'] = r['enquiry_question']
        if r['enquiry_focus']:
            s['enquiry_type'] = r['enquiry_focus']
        if r.get('enquiry_types'):
            ets = [x for x in r['enquiry_types'] if x]
            if ets:
                s['enquiry_type'] = ets[0]
        if r.get('misconceptions'):
            ms = [x for x in r['misconceptions'] if x]
            if ms:
                s['misconceptions'] = ms
        if r['writing_outcome']:
            s['writing_outcome'] = r['writing_outcome']
        if r.get('genres'):
            gs = [x for x in r['genres'] if x]
            if gs:
                s['genre'] = gs[0]
        if r.get('places'):
            ps = [x for x in r['places'] if x]
            if ps:
                s['place'] = ps[0]
        if r.get('contrasts'):
            cs = [x for x in r['contrasts'] if x]
            if cs:
                s['contrast'] = cs[0]
        if r['variables']:
            s['variables'] = r['variables']
        suggestions.append(s)
    domain['suggestions'] = suggestions

    # ── SEND support (access barriers + strategies per concept) ───────
    send_query = """
        MATCH (d:Domain {domain_id: $did})-[:HAS_CONCEPT]->(c:Concept)
              -[har:HAS_ACCESS_REQUIREMENT]->(ar:AccessRequirement)
        OPTIONAL MATCH (ss:SupportStrategy)-[m:MITIGATES]->(ar)
        RETURN c.concept_id AS concept_id, c.name AS concept_name,
               ar.access_req_id AS access_req_id, ar.name AS barrier_name,
               ar.category AS barrier_category,
               har.level AS level, har.rationale AS rationale,
               collect(DISTINCT CASE WHEN ss IS NOT NULL THEN {
                   support_id: ss.support_id,
                   name: ss.name,
                   tier: ss.tier,
                   construct_risk: ss.construct_risk,
                   strength: m.strength
               } END) AS strategies
        ORDER BY c.concept_id, ar.access_req_id
    """
    send_rows = session.run(send_query, did=domain_id).data()

    # Build per-concept barriers and domain-level summary
    concept_barriers_map = {}
    barrier_counts = defaultdict(int)
    strategy_usage = defaultdict(lambda: {'name': '', 'tier': '', 'count': 0})

    for r in send_rows:
        cid = r['concept_id']
        if cid not in concept_barriers_map:
            concept_barriers_map[cid] = {
                'concept_id': cid,
                'concept_name': r['concept_name'],
                'barriers': [],
            }
        concept_barriers_map[cid]['barriers'].append({
            'access_req_id': r['access_req_id'],
            'name': r['barrier_name'],
            'level': r['level'],
            'rationale': r['rationale'],
        })
        barrier_counts[r['barrier_name']] += 1

        for strat in (r['strategies'] or []):
            if strat is not None:
                sid = strat['support_id']
                strategy_usage[sid]['name'] = strat['name']
                strategy_usage[sid]['tier'] = strat['tier']
                strategy_usage[sid]['count'] += 1

    concept_barriers = sorted(concept_barriers_map.values(),
                               key=lambda x: x['concept_id'])
    domain['concept_barriers'] = concept_barriers

    # Domain-level SEND summary
    top_strategies = sorted(
        [{'name': v['name'], 'tier': v['tier'], 'mitigates_count': v['count']}
         for v in strategy_usage.values()],
        key=lambda x: -x['mitigates_count']
    )[:8]

    domain['send_summary'] = {
        'concepts_with_barriers': len(concept_barriers_map),
        'total_concepts': len(domain['concepts']),
        'barrier_counts': dict(barrier_counts),
        'top_strategies': top_strategies,
    } if concept_barriers_map else None

    return domain


def query_all_domains(session) -> list[dict]:
    """Get all domain IDs for iteration."""
    query = """
        MATCH (d:Domain)
        RETURN d.domain_id AS domain_id
        ORDER BY d.domain_id
    """
    return [r['domain_id'] for r in session.run(query)]


def query_thinking_lenses(session) -> list[dict]:
    """All thinking lenses with usage stats."""
    query = """
        MATCH (tl:ThinkingLens)
        OPTIONAL MATCH (cl:ConceptCluster)-[al:APPLIES_LENS]->(tl)
        WITH tl, count(cl) AS cluster_count,
             count(CASE WHEN al.rank = 1 THEN 1 END) AS primary_count
        OPTIONAL MATCH (tl)-[pf:PROMPT_FOR]->(ks:KeyStage)
        WITH tl, cluster_count, primary_count,
             collect({
                key_stage: ks.key_stage_id,
                agent_prompt: pf.agent_prompt,
                question_stems: pf.question_stems
             }) AS ks_prompts
        RETURN tl.lens_id AS id, tl.name AS name,
               tl.description AS description,
               tl.key_question AS key_question,
               tl.agent_prompt AS agent_prompt,
               tl.display_color AS color,
               cluster_count, primary_count,
               ks_prompts
        ORDER BY primary_count DESC
    """
    return session.run(query).data()


def query_learner_profiles(session) -> list[dict]:
    """All year learner profiles."""
    query = """
        MATCH (y:Year)
        OPTIONAL MATCH (y)-[:HAS_CONTENT_GUIDELINE]->(cg:ContentGuideline)
        OPTIONAL MATCH (y)-[:HAS_PEDAGOGY_PROFILE]->(pp:PedagogyProfile)
        OPTIONAL MATCH (y)-[:HAS_FEEDBACK_PROFILE]->(fp:FeedbackProfile)
        OPTIONAL MATCH (y)-[:SUPPORTS_INTERACTION]->(it:InteractionType)
        WITH y, properties(cg) AS content, properties(pp) AS pedagogy,
             properties(fp) AS feedback,
             collect(DISTINCT {
                name: it.name, category: it.category,
                description: it.description,
                input_method: it.input_method,
                visual_complexity: it.visual_complexity
             }) AS interactions
        RETURN y.year_id AS year_id, y.year_number AS year_number,
               y.name AS year_name, y.age_range AS age_range,
               content, pedagogy, feedback,
               [i IN interactions WHERE i.name IS NOT NULL | i] AS interactions
        ORDER BY y.year_number
    """
    return session.run(query).data()


def query_prerequisite_graph(session) -> dict:
    """Prerequisite chains for visualization."""
    query = """
        MATCH (c1:Concept)-[:PREREQUISITE_OF]->(c2:Concept)
        RETURN c1.concept_id AS source, c1.name AS source_name,
               c2.concept_id AS target, c2.name AS target_name
    """
    edges = session.run(query).data()

    # Get concept metadata for all involved concepts
    concept_ids = set()
    for e in edges:
        concept_ids.add(e['source'])
        concept_ids.add(e['target'])

    nodes_query = """
        MATCH (c:Concept) WHERE c.concept_id IN $cids
        OPTIONAL MATCH (c)<-[:HAS_CONCEPT]-(d:Domain)
                        <-[:HAS_DOMAIN]-(:Programme)-[:FOR_SUBJECT]->(s:Subject)
        RETURN c.concept_id AS id, c.name AS name,
               s.name AS subject, d.name AS domain
    """
    nodes = session.run(nodes_query, cids=list(concept_ids)).data()

    return {
        'nodes': nodes,
        'edges': edges,
    }


def query_search_index(session) -> list[dict]:
    """Build search index for client-side search."""
    # Concepts
    concepts_query = """
        MATCH (c:Concept)<-[:HAS_CONCEPT]-(d:Domain)
              <-[:HAS_DOMAIN]-(p:Programme)-[:FOR_SUBJECT]->(s:Subject)
        OPTIONAL MATCH (p)<-[:HAS_PROGRAMME]-(y:Year)
                       <-[:HAS_YEAR]-(ks:KeyStage)
        OPTIONAL MATCH (c)-[dv:DELIVERABLE_VIA {primary: true}]->(dm:DeliveryMode)
        RETURN DISTINCT c.concept_id AS id, c.name AS name,
               c.description AS description,
               c.concept_type AS type,
               c.is_keystone AS is_keystone,
               c.teaching_weight AS teaching_weight,
               s.name AS subject,
               y.year_id AS year_id,
               ks.key_stage_id AS key_stage,
               d.domain_id AS domain_id,
               d.name AS domain_name,
               dm.mode_id AS delivery_mode
        ORDER BY c.concept_id
    """
    entries = []
    for r in session.run(concepts_query):
        entries.append({
            'id': r['id'],
            'name': r['name'],
            'description': r['description'] or '',
            'type': 'concept',
            'concept_type': r['type'],
            'is_keystone': r['is_keystone'],
            'subject': r['subject'],
            'year_id': r['year_id'],
            'key_stage': r['key_stage'],
            'domain_id': r['domain_id'],
            'domain_name': r['domain_name'],
            'delivery_mode': r['delivery_mode'],
        })

    # Domains
    domains_query = """
        MATCH (d:Domain)<-[:HAS_DOMAIN]-(p:Programme)-[:FOR_SUBJECT]->(s:Subject)
        OPTIONAL MATCH (p)<-[:HAS_PROGRAMME]-(y:Year)
                       <-[:HAS_YEAR]-(ks:KeyStage)
        RETURN DISTINCT d.domain_id AS id, d.name AS name,
               d.description AS description,
               s.name AS subject,
               y.year_id AS year_id,
               ks.key_stage_id AS key_stage
        ORDER BY d.domain_id
    """
    for r in session.run(domains_query):
        entries.append({
            'id': r['id'],
            'name': r['name'],
            'description': r['description'] or '',
            'type': 'domain',
            'subject': r['subject'],
            'year_id': r['year_id'],
            'key_stage': r['key_stage'],
        })

    # Study suggestions (ontology nodes)
    studies_query = """
        MATCH (d:Domain)-[:HAS_SUGGESTION]->(s)
        OPTIONAL MATCH (d)<-[:HAS_DOMAIN]-(:Programme)-[:FOR_SUBJECT]->(subj:Subject)
        OPTIONAL MATCH (d)<-[:HAS_DOMAIN]-(:Programme)<-[:HAS_PROGRAMME]-(y:Year)
                       <-[:HAS_YEAR]-(ks:KeyStage)
        RETURN DISTINCT s.name AS name,
               [l IN labels(s) WHERE l <> 'Node'][0] AS type,
               s.description AS description,
               subj.name AS subject,
               y.year_id AS year_id,
               ks.key_stage_id AS key_stage,
               d.domain_id AS domain_id
        ORDER BY s.name
    """
    for r in session.run(studies_query):
        entries.append({
            'id': slugify(r['name'] or ''),
            'name': r['name'],
            'description': r['description'] or '',
            'type': 'study',
            'subject': r['subject'],
            'year_id': r['year_id'],
            'key_stage': r['key_stage'],
            'domain_id': r['domain_id'],
        })

    return entries


# ── Main ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Compile graph data for static site')
    parser.add_argument('--output', type=str,
                        default=str(PROJECT_ROOT / 'site' / 'src' / 'data'),
                        help='Output directory for JSON files')
    args = parser.parse_args()
    out = Path(args.output)

    print(f"Connecting to Neo4j: {NEO4J_URI}")
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    start = time.time()

    try:
        with driver.session() as session:
            # 1. Overview stats
            print("  Compiling overview stats...")
            overview = query_overview(session)
            write_json(out / 'overview.json', overview)

            # 2. Subjects
            print("  Compiling subjects...")
            subjects = query_subjects(session)
            write_json(out / 'subjects.json', subjects)

            # 3. Delivery modes
            print("  Compiling delivery modes...")
            delivery = query_delivery_modes(session)
            write_json(out / 'delivery.json', delivery)

            # 4. Domain details
            print("  Compiling domains...")
            domain_ids = query_all_domains(session)
            print(f"    {len(domain_ids)} domains to compile")
            domains_dir = out / 'domains'
            for i, did in enumerate(domain_ids, 1):
                domain = query_domain_detail(session, did)
                if domain:
                    write_json(domains_dir / f'{did}.json', domain)
                if i % 50 == 0:
                    print(f"    {i}/{len(domain_ids)} domains compiled")
            print(f"    {len(domain_ids)}/{len(domain_ids)} domains compiled")

            # 5. Thinking lenses
            print("  Compiling thinking lenses...")
            lenses = query_thinking_lenses(session)
            write_json(out / 'lenses.json', lenses)

            # 6. Learner profiles
            print("  Compiling learner profiles...")
            profiles = query_learner_profiles(session)
            write_json(out / 'profiles.json', profiles)

            # 7. Prerequisite graph
            print("  Compiling prerequisite graph...")
            prereq_graph = query_prerequisite_graph(session)
            write_json(out / 'prerequisites.json', prereq_graph)

            # 8. Search index (includes planners if manifest exists)
            print("  Compiling search index...")
            search_index = query_search_index(session)

            # Add planners to search index if manifest exists
            manifest_path = out / 'planners_manifest.json'
            if manifest_path.exists():
                print("  Adding planners to search index...")
                planners = json.loads(manifest_path.read_text(encoding='utf-8'))
                for p in planners:
                    search_index.append({
                        'id': p['study_id'],
                        'name': p['title'],
                        'description': f"{p['subject']} {p['key_stage']} — {p.get('study_type', '')} — {p.get('duration', '')}".strip(' —'),
                        'type': 'planner',
                        'subject': p['subject'],
                        'key_stage': p['key_stage'],
                        'year_id': ', '.join(p.get('year_groups', [])),
                        'folder': p['folder'],
                        'slug': p['slug'],
                    })
                print(f"    {len(planners)} planners added to search index")

            write_json(out / 'search_index.json', search_index)

    finally:
        driver.close()

    elapsed = time.time() - start
    file_count = sum(1 for _ in out.rglob('*.json'))
    print(f"\nDone: {file_count} JSON files written to {out}")
    print(f"Time: {elapsed:.1f}s")


if __name__ == '__main__':
    main()

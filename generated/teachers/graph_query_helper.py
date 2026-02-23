#!/usr/bin/env python3
"""Pull full teaching context from Neo4j for simulated teacher planning.

Surfaces ALL graph layers relevant to teaching:
  - UK Curriculum: domains, concepts, prerequisites, CO_TEACHES, clusters, objectives
  - Content Vehicles: choosable teaching packs with resources, definitions, assessment
  - Topics: case studies and teaching units (Geography, History)
  - Assessment: KS2 ContentDomainCodes (what is formally tested)
  - Epistemic Skills: disciplinary thinking skills with progression chains
  - Learner Profiles: content guidelines, pedagogy, feedback, interaction types, techniques

Intentionally excludes:
  - CASE Standards (US standards — not relevant for UK teacher planning)
  - SourceDocument / visualization metadata (provenance, not teaching content)

Usage:
  python3 graph_query_helper.py MA-Y3-D001 MA-Y3-D002 -o output.md
"""
import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "core" / "scripts"))

from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


def query_domain_context(session, domain_id):
    """Pull full context for one domain."""
    sections = []

    # ── Domain metadata ──────────────────────────────────────────────
    rec = session.run("""
        MATCH (d:Domain {domain_id: $did})
        OPTIONAL MATCH (p:Programme)-[:HAS_DOMAIN]->(d)
        RETURN d.domain_name AS name, d.description AS desc,
               d.curriculum_context AS ctx, d.structure_type AS stype,
               p.subject_name AS subject, p.key_stage AS ks, p.age_range AS age
    """, did=domain_id).single()
    if not rec:
        return f"\n## Domain {domain_id} — NOT FOUND\n"

    sections.append(f"\n## Domain: {domain_id} — {rec['name']}")
    sections.append(f"**Subject:** {rec['subject']} | **Key Stage:** {rec['ks']} | **Age:** {rec['age']} | **Structure:** {rec['stype']}")
    if rec['ctx']:
        sections.append(f"\n### Curriculum Context\n{rec['ctx']}")

    # ── Concepts with enrichment ─────────────────────────────────────
    concepts = list(session.run("""
        MATCH (d:Domain {domain_id: $did})-[:HAS_CONCEPT]->(c:Concept)
        RETURN c.concept_id AS id, c.concept_name AS name,
               c.description AS desc, c.concept_type AS ctype,
               c.complexity_level AS complexity, c.teaching_weight AS tw,
               c.is_keystone AS keystone,
               c.prerequisite_fan_out AS fan_out,
               c.teaching_guidance AS guidance,
               c.common_misconceptions AS misconceptions,
               c.key_vocabulary AS vocab
        ORDER BY c.concept_id
    """, did=domain_id))

    sections.append(f"\n### Concepts ({len(concepts)})")
    for c in concepts:
        ks_flag = " **[KEYSTONE]**" if c['keystone'] else ""
        sections.append(f"\n#### {c['id']} — {c['name']}{ks_flag}")
        fan_out_info = f" | Fan-out: {c['fan_out']}" if c['fan_out'] else ""
        sections.append(f"Type: {c['ctype']} | Complexity: {c['complexity']} | Teaching weight: {c['tw']}{fan_out_info}")
        sections.append(f"\n{c['desc']}")
        if c['guidance']:
            sections.append(f"\n**Teaching guidance:** {c['guidance']}")
        if c['misconceptions']:
            sections.append(f"\n**Common misconceptions:** {c['misconceptions']}")
        if c['vocab']:
            sections.append(f"\n**Key vocabulary:** {c['vocab']}")

    # ── Prerequisites (within domain) ────────────────────────────────
    prereqs = list(session.run("""
        MATCH (d:Domain {domain_id: $did})-[:HAS_CONCEPT]->(c1:Concept)
              -[:PREREQUISITE_OF]->(c2:Concept)<-[:HAS_CONCEPT]-(d)
        RETURN c1.concept_id AS src, c1.concept_name AS src_name,
               c2.concept_id AS tgt, c2.concept_name AS tgt_name
    """, did=domain_id))
    if prereqs:
        sections.append(f"\n### Prerequisites (within domain)")
        for p in prereqs:
            sections.append(f"- {p['src']} ({p['src_name']}) → {p['tgt']} ({p['tgt_name']})")

    # ── External prerequisites ───────────────────────────────────────
    ext_prereqs = list(session.run("""
        MATCH (d:Domain {domain_id: $did})-[:HAS_CONCEPT]->(c2:Concept)
              <-[:PREREQUISITE_OF]-(c1:Concept)
        WHERE NOT (d)-[:HAS_CONCEPT]->(c1)
        RETURN c1.concept_id AS src, c1.concept_name AS src_name,
               c2.concept_id AS tgt, c2.concept_name AS tgt_name
        LIMIT 20
    """, did=domain_id))
    if ext_prereqs:
        sections.append(f"\n### External Prerequisites (from other domains)")
        for p in ext_prereqs:
            sections.append(f"- {p['src']} ({p['src_name']}) → {p['tgt']} ({p['tgt_name']})")

    # ── CO_TEACHES (within domain) ───────────────────────────────────
    co_teaches = list(session.run("""
        MATCH (d:Domain {domain_id: $did})-[:HAS_CONCEPT]->(c1:Concept)
              -[r:CO_TEACHES]->(c2:Concept)<-[:HAS_CONCEPT]-(d)
        RETURN c1.concept_id AS src, c2.concept_id AS tgt, r.reason AS reason
    """, did=domain_id))
    if co_teaches:
        sections.append(f"\n### CO_TEACHES relationships (within domain)")
        for ct in co_teaches:
            sections.append(f"- {ct['src']} ↔ {ct['tgt']} ({ct['reason']})")

    # ── Cross-domain CO_TEACHES ──────────────────────────────────────
    cross_domain = list(session.run("""
        MATCH (d:Domain {domain_id: $did})-[:HAS_CONCEPT]->(c1:Concept)
              -[r:CO_TEACHES]->(c2:Concept)
        WHERE NOT (d)-[:HAS_CONCEPT]->(c2)
        OPTIONAL MATCH (d2:Domain)-[:HAS_CONCEPT]->(c2)
        RETURN c1.concept_id AS src, c1.concept_name AS src_name,
               c2.concept_id AS tgt, c2.concept_name AS tgt_name,
               r.reason AS reason, r.rationale AS rationale,
               d2.domain_id AS tgt_domain, d2.domain_name AS tgt_domain_name
        UNION
        MATCH (d:Domain {domain_id: $did})-[:HAS_CONCEPT]->(c2:Concept)
              <-[r:CO_TEACHES]-(c1:Concept)
        WHERE NOT (d)-[:HAS_CONCEPT]->(c1)
        OPTIONAL MATCH (d2:Domain)-[:HAS_CONCEPT]->(c1)
        RETURN c1.concept_id AS src, c1.concept_name AS src_name,
               c2.concept_id AS tgt, c2.concept_name AS tgt_name,
               r.reason AS reason, r.rationale AS rationale,
               d2.domain_id AS tgt_domain, d2.domain_name AS tgt_domain_name
    """, did=domain_id))
    if cross_domain:
        sections.append(f"\n### Cross-Domain CO_TEACHES ({len(cross_domain)} connections)")
        sections.append("These are curated connections to concepts in other domains. Use the rationale to understand WHY these concepts connect.\n")
        for cd in cross_domain:
            sections.append(f"- **{cd['src']}** ({cd['src_name']}) ↔ **{cd['tgt']}** ({cd['tgt_name']})")
            sections.append(f"  Domain: {cd['tgt_domain']} ({cd['tgt_domain_name']})")
            sections.append(f"  Reason: {cd['reason']}")
            if cd['rationale']:
                sections.append(f"  Rationale: {cd['rationale']}")

    # ── ConceptClusters ──────────────────────────────────────────────
    clusters = list(session.run("""
        MATCH (d:Domain {domain_id: $did})-[:HAS_CLUSTER]->(cc:ConceptCluster)
        OPTIONAL MATCH (cc)-[:GROUPS]->(c:Concept)
        WITH cc, collect(c.concept_id) AS concept_ids, collect(c.concept_name) AS concept_names
        OPTIONAL MATCH (cc)-[:SEQUENCED_AFTER]->(prev:ConceptCluster)
        RETURN cc.cluster_id AS cid, cc.cluster_name AS cname,
               cc.cluster_type AS ctype, cc.is_keystone_cluster AS keystone,
               cc.rationale AS rationale, cc.inspired_by AS inspired_by,
               cc.is_curated AS curated,
               concept_ids, concept_names,
               prev.cluster_id AS after_cluster
        ORDER BY cc.cluster_id
    """, did=domain_id))
    if clusters:
        sections.append(f"\n### ConceptClusters ({len(clusters)})")
        for cl in clusters:
            curated_flag = " [CURATED]" if cl['curated'] else ""
            ks_flag = " [KEYSTONE]" if cl['keystone'] else ""
            sections.append(f"\n**{cl['cid']}** — {cl['cname']}{curated_flag}{ks_flag}")
            sections.append(f"Type: {cl['ctype']}")
            if cl['after_cluster']:
                sections.append(f"Sequenced after: {cl['after_cluster']}")
            concepts_list = [f"{cid} ({cname})" for cid, cname in zip(cl['concept_ids'], cl['concept_names'])]
            sections.append(f"Concepts: {', '.join(concepts_list)}")
            if cl['rationale']:
                sections.append(f"Rationale: {cl['rationale']}")
            if cl['inspired_by']:
                sections.append(f"Inspired by: {cl['inspired_by']}")

    # ── Thinking Lenses per cluster ─────────────────────────────────
    if clusters:
        cluster_ids = [cl['cid'] for cl in clusters]
        lenses = list(session.run("""
            MATCH (cc:ConceptCluster)-[al:APPLIES_LENS]->(tl:ThinkingLens)
            WHERE cc.cluster_id IN $cids
            RETURN cc.cluster_id  AS cluster_id,
                   tl.name        AS lens_name,
                   tl.key_question AS key_question,
                   tl.agent_prompt AS agent_prompt,
                   al.rank        AS rank,
                   al.rationale   AS rationale
            ORDER BY cc.cluster_id, al.rank
        """, cids=cluster_ids))
        if lenses:
            # Group by cluster
            from collections import defaultdict
            lens_by_cluster = defaultdict(list)
            for l in lenses:
                lens_by_cluster[l['cluster_id']].append(l)
            sections.append(f"\n### Thinking Lenses")
            sections.append("Cognitive framing for each cluster — the primary lens (rank 1) is the recommended framing.")
            for cid in cluster_ids:
                cls_lenses = lens_by_cluster.get(cid, [])
                if cls_lenses:
                    sections.append(f"\n**{cid}:**")
                    for l in cls_lenses:
                        primary_tag = " (primary)" if l['rank'] == 1 else ""
                        sections.append(f"- **{l['lens_name']}**{primary_tag}: {l['key_question']}")
                        if l['rationale']:
                            sections.append(f"  Why: {l['rationale']}")
                        if l['agent_prompt']:
                            sections.append(f"  AI instruction: {l['agent_prompt']}")

    # ── Objectives with Concept links ────────────────────────────────
    objectives = list(session.run("""
        MATCH (d:Domain {domain_id: $did})-[:CONTAINS]->(o:Objective)
        OPTIONAL MATCH (o)-[:TEACHES]->(c:Concept)
        WITH o, collect(c.concept_id) AS concept_ids
        RETURN o.objective_id AS id, o.objective_text AS text,
               o.is_statutory AS statutory, concept_ids
        ORDER BY o.objective_id
        LIMIT 40
    """, did=domain_id))
    if objectives:
        sections.append(f"\n### Objectives ({len(objectives)})")
        for o in objectives:
            stat = " [statutory]" if o['statutory'] else ""
            concepts_str = f" → {', '.join(o['concept_ids'])}" if o['concept_ids'] else ""
            sections.append(f"- {o['id']}{stat}: {o['text']}{concepts_str}")

    # ── Topics ───────────────────────────────────────────────────────
    topics = list(session.run("""
        MATCH (d:Domain {domain_id: $did})-[:HAS_CONCEPT]->(c:Concept)<-[:TEACHES]-(t:Topic)
        WITH t, collect(DISTINCT c.concept_id) AS concept_ids
        RETURN t.topic_id AS id, t.topic_name AS name, t.topic_type AS ttype,
               t.is_prescribed AS prescribed, t.is_optional AS optional,
               t.curriculum_note AS note, concept_ids
        ORDER BY t.topic_id
    """, did=domain_id))
    if topics:
        sections.append(f"\n### Topics ({len(topics)})")
        sections.append("These are teaching topics (case studies, units, exemplars) that address concepts in this domain.\n")
        for t in topics:
            prescribed_flag = " [prescribed]" if t['prescribed'] else ""
            optional_flag = " [optional]" if t['optional'] else ""
            sections.append(f"#### {t['id']} — {t['name']}{prescribed_flag}{optional_flag}")
            sections.append(f"Type: {t['ttype']} | Concepts: {', '.join(t['concept_ids'])}")
            if t['note']:
                sections.append(f"NC note: {t['note']}")

    # ── Content Vehicles (teaching packs) ────────────────────────────
    vehicles = list(session.run("""
        MATCH (d:Domain {domain_id: $did})-[:HAS_VEHICLE]->(cv:ContentVehicle)
        OPTIONAL MATCH (cv)-[:DELIVERS]->(c:Concept)
        WITH cv, collect(c.concept_id) AS concept_ids
        OPTIONAL MATCH (cv)-[:IMPLEMENTS]->(t:Topic)
        RETURN cv.vehicle_id AS id, cv.name AS name, cv.vehicle_type AS vtype,
               cv.description AS desc, cv.definitions AS defs,
               cv.assessment_guidance AS assessment,
               cv.success_criteria AS criteria,
               concept_ids,
               t.topic_id AS topic_id, t.topic_name AS topic_name,
               cv.period AS period, cv.key_figures AS key_figures,
               cv.sources AS sources, cv.perspectives AS perspectives,
               cv.location AS location, cv.data_points AS data_points,
               cv.themes AS themes,
               cv.enquiry_type AS enquiry_type, cv.equipment AS equipment,
               cv.expected_outcome AS expected_outcome,
               cv.genre AS genre, cv.suggested_texts AS suggested_texts,
               cv.writing_outcome AS writing_outcome, cv.grammar_focus AS grammar_focus,
               cv.cpa_stage AS cpa_stage, cv.manipulatives AS manipulatives,
               cv.representations AS representations, cv.common_errors AS common_errors
        ORDER BY cv.vehicle_id
    """, did=domain_id))
    if vehicles:
        sections.append(f"\n### Content Vehicles — Teaching Packs ({len(vehicles)})")
        sections.append("These are choosable teaching packs that deliver concepts in this domain. Teachers select the pack that fits their class.\n")
        for v in vehicles:
            sections.append(f"#### {v['id']} — {v['name']} ({v['vtype']})")
            sections.append(f"{v['desc']}")
            sections.append(f"Delivers: {', '.join(v['concept_ids'])}")
            if v['topic_id']:
                sections.append(f"Implements topic: {v['topic_id']} ({v['topic_name']})")
            # Subject-specific properties
            if v['period']:
                sections.append(f"Period: {v['period']}")
            if v['key_figures']:
                sections.append(f"Key figures: {', '.join(v['key_figures'])}")
            if v['sources']:
                sections.append(f"Sources: {', '.join(v['sources'])}")
            if v['perspectives']:
                sections.append(f"Perspectives: {', '.join(v['perspectives'])}")
            if v['location']:
                sections.append(f"Location: {v['location']}")
            if v['data_points']:
                sections.append(f"Data: {', '.join(v['data_points'])}")
            if v['themes']:
                sections.append(f"Themes: {', '.join(v['themes'])}")
            if v['enquiry_type']:
                sections.append(f"Enquiry type: {v['enquiry_type']}")
            if v['equipment']:
                sections.append(f"Equipment: {', '.join(v['equipment'])}")
            if v['expected_outcome']:
                sections.append(f"Expected outcome: {v['expected_outcome']}")
            if v['genre']:
                sections.append(f"Genre: {v['genre']}")
            if v['suggested_texts']:
                sections.append(f"Suggested texts: {', '.join(v['suggested_texts'])}")
            if v['writing_outcome']:
                sections.append(f"Writing outcome: {v['writing_outcome']}")
            if v['grammar_focus']:
                sections.append(f"Grammar focus: {', '.join(v['grammar_focus'])}")
            if v['cpa_stage']:
                sections.append(f"CPA stage: {v['cpa_stage']}")
            if v['manipulatives']:
                sections.append(f"Manipulatives: {', '.join(v['manipulatives'])}")
            if v['representations']:
                sections.append(f"Representations: {', '.join(v['representations'])}")
            if v['common_errors']:
                sections.append(f"Common errors: {', '.join(v['common_errors'])}")
            if v['defs']:
                sections.append(f"Key vocabulary: {', '.join(v['defs'])}")
            if v['assessment']:
                sections.append(f"Assessment: {v['assessment']}")
            if v['criteria']:
                sections.append(f"Success criteria: {'; '.join(v['criteria'])}")

    # ── Assessment — KS2 Content Domain Codes ────────────────────────
    assessments = list(session.run("""
        MATCH (d:Domain {domain_id: $did})-[:HAS_CONCEPT]->(c:Concept)
              <-[:ASSESSES_CONCEPT]-(cdc:ContentDomainCode)
        WITH cdc, collect(DISTINCT c.concept_id) AS concept_ids
        RETURN cdc.code_id AS code_id, cdc.code AS code,
               cdc.description AS desc, cdc.strand_name AS strand,
               concept_ids
        ORDER BY cdc.code
    """, did=domain_id))
    if not assessments:
        # Fall back to domain-level assessment links
        assessments = list(session.run("""
            MATCH (cdc:ContentDomainCode)-[:ASSESSES_DOMAIN]->(d:Domain {domain_id: $did})
            RETURN cdc.code_id AS code_id, cdc.code AS code,
                   cdc.description AS desc, cdc.strand_name AS strand,
                   [] AS concept_ids
            ORDER BY cdc.code
        """, did=domain_id))
    if assessments:
        sections.append(f"\n### Assessment — Content Domain Codes ({len(assessments)})")
        sections.append("These test framework codes map to concepts in this domain. Use them to understand what is formally assessed.\n")
        for a in assessments:
            concepts_str = f" → {', '.join(a['concept_ids'])}" if a['concept_ids'] else ""
            sections.append(f"- **{a['code']}**: {a['desc']}{concepts_str}")

    # ── Concept-level Disciplinary Skill Links ────────────────────────
    skill_links = list(session.run("""
        MATCH (d:Domain {domain_id: $did})-[:HAS_CONCEPT]->(c:Concept)
              -[r:DEVELOPS_SKILL]->(s)
        WHERE r.level = 'concept'
        RETURN c.concept_id AS concept_id, c.concept_name AS concept_name,
               s.skill_id AS skill_id, s.skill_name AS skill_name,
               labels(s)[0] AS skill_type,
               r.enquiry_type AS enquiry_type, r.rationale AS rationale
        ORDER BY c.concept_id, s.skill_id
    """, did=domain_id))
    if skill_links:
        sections.append(f"\n### Disciplinary Skills per Concept ({len(skill_links)} links)")
        sections.append("These show which specific disciplinary skills each concept develops.\n")
        by_concept = {}
        for sl in skill_links:
            by_concept.setdefault(sl['concept_id'], []).append(sl)
        for cid, links in by_concept.items():
            cname = links[0]['concept_name']
            sections.append(f"**{cid}** ({cname}):")
            for sl in links:
                eq = f" [{sl['enquiry_type']}]" if sl['enquiry_type'] else ""
                sections.append(f"  - {sl['skill_id']} ({sl['skill_name']}){eq}")

    return "\n".join(sections)


# ─────────────────────────────────────────────────────────────────────
# Programme-level: Epistemic Skills (called once, not per domain)
# ─────────────────────────────────────────────────────────────────────

def query_epistemic_skills(session, domain_ids):
    """Pull epistemic skills with progression chains (deduplicated across domains)."""
    skills = list(session.run("""
        UNWIND $dids AS did
        MATCH (p:Programme)-[:HAS_DOMAIN]->(d:Domain {domain_id: did})
        MATCH (p)-[:DEVELOPS_SKILL]->(s)
        WHERE s.key_stage = p.key_stage
        OPTIONAL MATCH (prev_s)-[:PROGRESSION_OF]->(s)
        OPTIONAL MATCH (s)-[:PROGRESSION_OF]->(next_s)
        RETURN DISTINCT labels(s)[0] AS skill_type, s.skill_id AS id,
               s.skill_name AS name, s.description AS desc, s.strand AS strand,
               prev_s.skill_id AS builds_on, next_s.skill_id AS leads_to
        ORDER BY s.skill_id
    """, dids=domain_ids))
    if not skills:
        return ""

    sections = []
    by_type = {}
    for s in skills:
        by_type.setdefault(s['skill_type'], []).append(s)

    for skill_type, type_skills in by_type.items():
        sections.append(f"\n## Epistemic Skills — {skill_type} ({len(type_skills)})")
        sections.append("These disciplinary thinking skills should be woven through all teaching.\n")
        for s in type_skills:
            strand_info = f" [{s['strand']}]" if s['strand'] else ""
            progression_parts = []
            if s['builds_on']:
                progression_parts.append(f"builds on {s['builds_on']}")
            if s['leads_to']:
                progression_parts.append(f"leads to {s['leads_to']}")
            progression = f" ({', '.join(progression_parts)})" if progression_parts else ""
            sections.append(f"- **{s['id']}** {s['name']}{strand_info}: {s['desc']}{progression}")

    return "\n".join(sections)


# ─────────────────────────────────────────────────────────────────────
# Year-level: Learner Profile (content, pedagogy, feedback, interactions, techniques)
# ─────────────────────────────────────────────────────────────────────

def query_learner_profile(session, key_stage, year_id=None):
    """Pull full learner profile using actual graph property names.

    Args:
        key_stage: e.g. "KS1", "KS2"
        year_id: specific year e.g. "Y2", "Y5". If None, defaults to
                 first year of key stage (fallback only).
    """
    ks_to_years = {
        "KS1": ["Y1", "Y2"], "KS2": ["Y3", "Y4", "Y5", "Y6"],
        "KS3": ["Y7", "Y8", "Y9"], "KS4": ["Y10", "Y11"]
    }
    years = ks_to_years.get(key_stage, [])
    if not years:
        return ""

    if year_id and year_id in years:
        pass  # use the explicit year_id
    elif year_id:
        print(f"  WARNING: --year {year_id} not in {key_stage} ({years}), using {years[0]}")
        year_id = years[0]
    else:
        year_id = years[0]
    sections = [f"\n## Learner Profile ({key_stage}, from {year_id})"]

    # ── Content Guidelines ───────────────────────────────────────────
    cg = session.run("""
        MATCH (y:Year {year_id: $yid})-[:HAS_CONTENT_GUIDELINE]->(cg:ContentGuideline)
        RETURN cg.reading_level_description AS reading,
               cg.lexile_min AS lexile_min, cg.lexile_max AS lexile_max,
               cg.flesch_kincaid_grade_max AS fk_grade,
               cg.max_sentence_length_words AS max_sentence,
               cg.avg_sentence_length_words AS avg_sentence,
               cg.vocabulary_level AS vocab_level,
               cg.vocabulary_notes AS vocab_notes,
               cg.academic_vocabulary_ok AS academic_vocab,
               cg.tts_required AS tts_required,
               cg.tts_available AS tts_available,
               cg.tts_notes AS tts_notes,
               cg.sentence_structure AS sentence_structure,
               cg.number_range AS number_range,
               cg.agent_content_prompt AS agent_prompt
    """, yid=year_id).single()
    if cg:
        sections.append(f"\n### Content Guidelines")
        if cg['reading']:
            sections.append(f"**Reading level:** {cg['reading']}")
        if cg['lexile_min'] is not None:
            sections.append(f"**Lexile range:** {cg['lexile_min']}–{cg['lexile_max']}")
        if cg['fk_grade'] is not None:
            sections.append(f"**Flesch-Kincaid grade max:** {cg['fk_grade']}")
        if cg['max_sentence'] is not None:
            sections.append(f"**Sentence length:** max {cg['max_sentence']} words, avg {cg['avg_sentence']} words")
        if cg['vocab_level']:
            sections.append(f"**Vocabulary level:** {cg['vocab_level']}")
        if cg['vocab_notes']:
            sections.append(f"**Vocabulary notes:** {cg['vocab_notes']}")
        if cg['academic_vocab'] is not None:
            sections.append(f"**Academic vocabulary:** {'OK to use with scaffolding' if cg['academic_vocab'] else 'Avoid — use everyday language'}")
        if cg['tts_required'] is not None:
            tts = "Required (default on)" if cg['tts_required'] else "Available on request"
            sections.append(f"**Text-to-speech:** {tts}")
        if cg['tts_notes']:
            sections.append(f"**TTS notes:** {cg['tts_notes']}")
        if cg['sentence_structure']:
            sections.append(f"**Sentence structure:** {cg['sentence_structure']}")
        if cg['number_range']:
            sections.append(f"**Number range:** {cg['number_range']}")
        if cg['agent_prompt']:
            sections.append(f"\n**Agent content instructions:** {cg['agent_prompt']}")

    # ── Pedagogy Profile ─────────────────────────────────────────────
    pp = session.run("""
        MATCH (y:Year {year_id: $yid})-[:HAS_PEDAGOGY_PROFILE]->(pp:PedagogyProfile)
        RETURN pp.session_length_min_minutes AS session_min,
               pp.session_length_max_minutes AS session_max,
               pp.activities_per_session AS activities,
               pp.hint_tiers_max AS hint_tiers,
               pp.hint_tier_notes AS hint_notes,
               pp.productive_failure_appropriate AS pf_ok,
               pp.productive_failure_notes AS pf_notes,
               pp.worked_examples_required AS worked_ex,
               pp.worked_example_style AS worked_ex_style,
               pp.scaffolding_level AS scaffolding,
               pp.prerequisite_gating_required AS prereq_gating,
               pp.metacognitive_prompts AS metacog,
               pp.mastery_threshold_correct_in_window AS mastery_n,
               pp.mastery_window_days AS mastery_days,
               pp.mastery_success_rate_percent AS mastery_pct,
               pp.interleaving_appropriate AS interleaving,
               pp.spacing_appropriate AS spacing,
               pp.spacing_interval_days_min AS spacing_min,
               pp.spacing_interval_days_max AS spacing_max,
               pp.agent_pedagogy_prompt AS agent_prompt
    """, yid=year_id).single()
    if pp:
        sections.append(f"\n### Pedagogy Profile")
        if pp['session_min'] is not None:
            sections.append(f"**Session length:** {pp['session_min']}–{pp['session_max']} minutes, {pp['activities']} activities")
        if pp['scaffolding']:
            sections.append(f"**Scaffolding level:** {pp['scaffolding']}")
        if pp['hint_tiers'] is not None:
            sections.append(f"**Hint tiers:** max {pp['hint_tiers']}")
        if pp['hint_notes']:
            sections.append(f"**Hint notes:** {pp['hint_notes']}")
        if pp['worked_ex'] is not None:
            style = f" ({pp['worked_ex_style']})" if pp['worked_ex_style'] else ""
            sections.append(f"**Worked examples:** {'Required' if pp['worked_ex'] else 'Optional'}{style}")
        if pp['pf_ok'] is not None:
            sections.append(f"**Productive failure:** {'Appropriate' if pp['pf_ok'] else 'Not yet appropriate'}")
        if pp['pf_notes']:
            sections.append(f"**PF notes:** {pp['pf_notes']}")
        if pp['prereq_gating'] is not None:
            sections.append(f"**Prerequisite gating:** {'Required' if pp['prereq_gating'] else 'Optional'}")
        if pp['metacog'] is not None:
            sections.append(f"**Metacognitive prompts:** {'Yes' if pp['metacog'] else 'Not yet appropriate'}")
        if pp['mastery_n'] is not None:
            sections.append(f"**Mastery threshold:** {pp['mastery_n']} correct in {pp['mastery_days']} days ({pp['mastery_pct']}%)")
        if pp['spacing'] is not None:
            sections.append(f"**Spacing:** {'Yes' if pp['spacing'] else 'No'} ({pp['spacing_min']}–{pp['spacing_max']} day intervals)")
        if pp['interleaving'] is not None:
            sections.append(f"**Interleaving:** {'Appropriate' if pp['interleaving'] else 'Not yet appropriate'}")
        if pp['agent_prompt']:
            sections.append(f"\n**Agent pedagogy instructions:** {pp['agent_prompt']}")

    # ── Feedback Profile ─────────────────────────────────────────────
    fp = session.run("""
        MATCH (y:Year {year_id: $yid})-[:HAS_FEEDBACK_PROFILE]->(fp:FeedbackProfile)
        RETURN fp.feedback_style AS style,
               fp.ai_tone AS tone,
               fp.ai_voice_style AS voice,
               fp.normalize_struggle AS normalize,
               fp.positive_error_framing AS positive_errors,
               fp.post_error_style AS post_error,
               fp.immediate_feedback AS immediate,
               fp.counter_misconceptions_explicit AS counter_misconceptions,
               fp.metacognitive_reflection AS metacog,
               fp.metacognitive_examples AS metacog_examples,
               fp.feedback_example_correct AS example_correct,
               fp.feedback_example_incorrect AS example_incorrect,
               fp.avoid_phrases AS avoid_phrases,
               fp.gamification_safe AS gamification,
               fp.progress_bars_safe AS progress_bars,
               fp.leaderboards_safe AS leaderboards,
               fp.visible_streaks_safe AS streaks,
               fp.unexpected_delight_safe AS delight,
               fp.delight_frequency AS delight_freq,
               fp.delight_notes AS delight_notes,
               fp.agent_feedback_prompt AS agent_prompt
    """, yid=year_id).single()
    if fp:
        sections.append(f"\n### Feedback Profile")
        if fp['tone']:
            sections.append(f"**AI tone:** {fp['tone']}")
        if fp['voice']:
            sections.append(f"**Voice style:** {fp['voice']}")
        if fp['style']:
            sections.append(f"**Feedback style:** {fp['style']}")
        if fp['immediate'] is not None:
            sections.append(f"**Immediate feedback:** {'Yes' if fp['immediate'] else 'Delayed'}")
        if fp['normalize'] is not None:
            sections.append(f"**Normalise struggle:** {'Yes' if fp['normalize'] else 'No'}")
        if fp['positive_errors'] is not None:
            sections.append(f"**Positive error framing:** {'Yes' if fp['positive_errors'] else 'No'}")
        if fp['post_error']:
            sections.append(f"**Post-error approach:** {fp['post_error']}")
        if fp['counter_misconceptions'] is not None:
            sections.append(f"**Counter misconceptions explicitly:** {'Yes' if fp['counter_misconceptions'] else 'Not yet'}")
        if fp['metacog'] is not None:
            sections.append(f"**Metacognitive reflection:** {'Yes' if fp['metacog'] else 'Not yet'}")
        if fp['metacog_examples']:
            sections.append(f"**Metacognitive examples:** {fp['metacog_examples']}")
        # Gamification safety
        gamification_parts = []
        if fp['gamification'] is not None and not fp['gamification']:
            gamification_parts.append("gamification unsafe")
        if fp['progress_bars'] is not None and not fp['progress_bars']:
            gamification_parts.append("no progress bars")
        if fp['leaderboards'] is not None and not fp['leaderboards']:
            gamification_parts.append("no leaderboards")
        if fp['streaks'] is not None and not fp['streaks']:
            gamification_parts.append("no visible streaks")
        if gamification_parts:
            sections.append(f"**Gamification safety:** {', '.join(gamification_parts)}")
        if fp['delight'] is not None and fp['delight']:
            sections.append(f"**Surprise/delight:** Yes ({fp['delight_freq']}). {fp['delight_notes'] or ''}")
        if fp['example_correct']:
            sections.append(f"**Example feedback (correct):** \"{fp['example_correct']}\"")
        if fp['example_incorrect']:
            sections.append(f"**Example feedback (incorrect):** \"{fp['example_incorrect']}\"")
        if fp['avoid_phrases']:
            sections.append(f"**Avoid phrases:** {fp['avoid_phrases']}")
        if fp['agent_prompt']:
            sections.append(f"\n**Agent feedback instructions:** {fp['agent_prompt']}")

    # ── Interaction Types ────────────────────────────────────────────
    interactions = list(session.run("""
        MATCH (y:Year {year_id: $yid})-[r:SUPPORTS_INTERACTION]->(it:InteractionType)
        RETURN it.interaction_id AS id, it.name AS name, it.category AS category,
               it.description AS desc, it.input_method AS input,
               it.visual_complexity AS complexity,
               it.requires_literacy AS literacy, it.requires_numeracy AS numeracy,
               r.primary AS is_primary,
               it.agent_prompt AS agent_prompt
        ORDER BY r.primary DESC, it.interaction_id
    """, yid=year_id))
    if interactions:
        primary = [i for i in interactions if i['is_primary']]
        secondary = [i for i in interactions if not i['is_primary']]
        sections.append(f"\n### Interaction Types ({len(interactions)} total, {len(primary)} primary)")
        if primary:
            sections.append("\n**Primary (recommended for this year group):**")
            for i in primary:
                sections.append(f"- **{i['name']}** ({i['category']}, {i['input']}): {i['desc']}")
        if secondary:
            sections.append("\n**Secondary (available but not primary):**")
            for i in secondary:
                sections.append(f"- {i['name']} ({i['category']}, {i['input']}): {i['desc']}")

    # ── Pedagogy Techniques ──────────────────────────────────────────
    techniques = list(session.run("""
        MATCH (y:Year {year_id: $yid})-[:HAS_PEDAGOGY_PROFILE]->(pp:PedagogyProfile)
              -[:USES_TECHNIQUE]->(pt:PedagogyTechnique)
        OPTIONAL MATCH (pp)-[intro:INTRODUCES_TECHNIQUE]->(pt)
        RETURN pt.technique_id AS id, pt.name AS name,
               pt.description AS desc, pt.evidence_base AS evidence,
               pt.how_to_implement AS how_to,
               intro IS NOT NULL AS new_this_year
        ORDER BY pt.technique_id
    """, yid=year_id))
    if techniques:
        sections.append(f"\n### Pedagogy Techniques ({len(techniques)})")
        for t in techniques:
            new_flag = " **[NEW this year]**" if t['new_this_year'] else ""
            sections.append(f"\n**{t['name']}**{new_flag}")
            sections.append(f"{t['desc']}")
            if t['evidence']:
                sections.append(f"Evidence: {t['evidence']}")
            if t['how_to']:
                sections.append(f"Implementation: {t['how_to']}")

    return "\n".join(sections)


# ─────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────

def _infer_year_from_domain_ids(domain_ids):
    """Try to extract a year from domain ID prefixes like MA-Y2-D001."""
    import re
    years = set()
    for did in domain_ids:
        m = re.search(r'-Y(\d+)-', did)
        if m:
            years.add(f"Y{m.group(1)}")
    if len(years) == 1:
        return years.pop()
    if len(years) > 1:
        # Multiple years — pick the highest (most specific to what they're teaching)
        return sorted(years, key=lambda y: int(y[1:]))[-1]
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("domain_ids", nargs="+")
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--year", help="Specific year ID (e.g. Y2, Y5) for learner profile. "
                        "If omitted, inferred from domain IDs or defaults to first year of KS.")
    args = parser.parse_args()

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    try:
        with driver.session() as session:
            parts = ["# Teaching Context (from Graph)\n"]
            ks = None
            for did in args.domain_ids:
                parts.append(query_domain_context(session, did))
                if not ks:
                    rec = session.run("""
                        MATCH (p:Programme)-[:HAS_DOMAIN]->(d:Domain {domain_id: $did})
                        RETURN p.key_stage AS ks
                    """, did=did).single()
                    if rec:
                        ks = rec['ks']

            parts.append(query_epistemic_skills(session, args.domain_ids))

            if ks:
                year_id = args.year or _infer_year_from_domain_ids(args.domain_ids)
                parts.append(query_learner_profile(session, ks, year_id=year_id))

            Path(args.output).write_text("\n".join(parts))
            print(f"Written to {args.output} ({len(parts)} sections)")
    finally:
        driver.close()


if __name__ == "__main__":
    main()

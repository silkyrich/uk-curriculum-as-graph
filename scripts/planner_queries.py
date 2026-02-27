#!/usr/bin/env python3
"""
Query layer for teacher planner generation.

Fetches complete study context from Neo4j for any study node type
(HistoryStudy, ScienceEnquiry, EnglishUnit, GeoStudy, Art/Music/DT/Computing/Generic).

Falls back to JSON data files when graph relationships are missing.
"""

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ── Neo4j config ─────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "core" / "scripts"))
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

DATA_DIR = PROJECT_ROOT / "layers" / "topic-suggestions" / "data"

# ── Study node type registry ─────────────────────────────────────────

STUDY_NODES = {
    'HistoryStudy':              {'id_field': 'study_id',      'data_dir': 'history_studies',    'array_key': 'studies',    'subject': 'History'},
    'GeoStudy':                  {'id_field': 'study_id',      'data_dir': 'geo_studies',        'array_key': 'studies',    'subject': 'Geography'},
    'ScienceEnquiry':            {'id_field': 'enquiry_id',    'data_dir': 'science_enquiries',  'array_key': 'enquiries',  'subject': 'Science'},
    'EnglishUnit':               {'id_field': 'unit_id',       'data_dir': 'english_units',      'array_key': 'units',      'subject': 'English'},
    'ArtTopicSuggestion':        {'id_field': 'suggestion_id', 'data_dir': 'art_studies',        'array_key': None,         'subject': 'Art and Design'},
    'MusicTopicSuggestion':      {'id_field': 'suggestion_id', 'data_dir': 'music_studies',      'array_key': None,         'subject': 'Music'},
    'DTTopicSuggestion':         {'id_field': 'suggestion_id', 'data_dir': 'dt_studies',         'array_key': None,         'subject': 'Design and Technology'},
    'ComputingTopicSuggestion':  {'id_field': 'suggestion_id', 'data_dir': 'computing_studies',  'array_key': None,         'subject': 'Computing'},
    'TopicSuggestion':           {'id_field': 'suggestion_id', 'data_dir': 'generic_studies',    'array_key': None,         'subject': None},
}

def _extract_key_stage(study_id: str) -> str:
    """Extract key stage from a study ID like 'HS-KS2-001', 'TS-AD-KS1-002', or 'EU-EN-Y5-003'."""
    import re
    # Direct KS reference
    m = re.search(r'(KS\d)', study_id, re.IGNORECASE)
    if m:
        return m.group(1).upper()
    # Year group reference (English units use Y1-Y11)
    m = re.search(r'Y(\d+)', study_id, re.IGNORECASE)
    if m:
        year = int(m.group(1))
        if year <= 2:
            return 'KS1'
        elif year <= 6:
            return 'KS2'
        elif year <= 9:
            return 'KS3'
        else:
            return 'KS4'
    return ''


# Properties that are relationships, not node properties (skip in rendering)
RELATIONSHIP_FIELDS = {
    'delivers_via', 'uses_template', 'domain_ids', 'in_genre', 'studies_text',
    'foregrounds', 'uses_source_ids', 'chronologically_follows',
    'thematically_linked_to', 'contrasts_with', 'builds_on', 'complements',
    'locations', 'uses_enquiry_type', 'surfaces_misconception', 'progresses_to',
    'grammar_sequence_after', 'text_complexity_after', 'source_concepts',
    'develops_skill', 'prerequisite_misconception_ids', 'cross_curricular_hooks',
    'cross_curricular_links',
}

DISPLAY_FIELDS = {
    'display_category', 'display_color', 'display_icon', 'display_size',
}


@dataclass
class StudyContext:
    """Complete context for rendering a teacher planner."""
    study: dict                               # All study node properties
    label: str                                # HistoryStudy, ScienceEnquiry, etc.
    study_id: str                             # Canonical ID value
    subject: str                              # Human-readable subject name
    key_stage: str                            # KS1, KS2, KS3, KS4

    concepts: list = field(default_factory=list)
    thinking_lenses: list = field(default_factory=list)
    templates: list = field(default_factory=list)
    references: dict = field(default_factory=dict)
    cross_curricular: list = field(default_factory=list)
    source_documents: list = field(default_factory=list)
    follows: str | None = None
    leads_to: str | None = None
    epistemic_skills: list = field(default_factory=list)
    prerequisites: list = field(default_factory=list)
    assessment_codes: list = field(default_factory=list)
    learner_profile: dict = field(default_factory=dict)


# ── JSON fallback helpers ────────────────────────────────────────────

def _load_json_studies(label: str) -> dict:
    """Load all study nodes from JSON files for a given label. Returns {id: props}."""
    meta = STUDY_NODES[label]
    data_path = DATA_DIR / meta['data_dir']
    result = {}
    if not data_path.exists():
        return result

    for fp in sorted(data_path.glob('*.json')):
        with open(fp) as f:
            raw = json.load(f)
        # Handle wrapped vs bare arrays
        if isinstance(raw, list):
            items = raw
        elif meta['array_key'] and meta['array_key'] in raw:
            items = raw[meta['array_key']]
        elif 'studies' in raw:
            items = raw['studies']
        elif 'enquiries' in raw:
            items = raw['enquiries']
        elif 'units' in raw:
            items = raw['units']
        else:
            items = raw if isinstance(raw, list) else []
        for item in items:
            sid = item.get(meta['id_field'])
            if sid:
                result[sid] = item
    return result


def _load_reference_nodes(ref_type: str) -> dict:
    """Load reference nodes from JSON. Returns {id: props}."""
    ref_dirs = {
        'HistoricalSource':     ('history_sources',              'source_id',         'sources'),
        'DisciplinaryConcept':  ('history_disciplinary_concepts', 'concept_id',       'disciplinary_concepts'),
        'GeoPlace':             ('geo_places',                   'place_id',          'places'),
        'GeoContrast':          ('geo_contrasts',                'contrast_id',       'contrasts'),
        'EnquiryType':          ('science_enquiry_types',        'enquiry_type_id',   None),
        'Misconception':        ('science_misconceptions',       'misconception_id',  None),
        'Genre':                ('english_genres',               'genre_id',          'genres'),
        'SetText':              ('english_set_texts',            'set_text_id',       'set_texts'),
    }
    if ref_type not in ref_dirs:
        return {}
    dir_name, id_field, array_key = ref_dirs[ref_type]
    data_path = DATA_DIR / dir_name
    result = {}
    if not data_path.exists():
        return result
    for fp in sorted(data_path.glob('*.json')):
        with open(fp) as f:
            raw = json.load(f)
        if isinstance(raw, list):
            items = raw
        elif array_key and array_key in raw:
            items = raw[array_key]
        else:
            items = raw if isinstance(raw, list) else []
        for item in items:
            rid = item.get(id_field)
            if rid:
                result[rid] = item
    return result


# ── Graph queries ────────────────────────────────────────────────────

def _get_id_field(label: str) -> str:
    return STUDY_NODES[label]['id_field']


def query_all_study_ids(session) -> list[dict]:
    """Get all study node IDs with their label, subject, and key stage."""
    results = []
    for label, meta in STUDY_NODES.items():
        id_field = meta['id_field']
        query = f"""
            MATCH (ts:{label})
            RETURN ts.{id_field} AS study_id, ts.name AS name,
                   ts.key_stage AS key_stage, ts.subject AS subject,
                   '{label}' AS label
            ORDER BY ts.key_stage, ts.name
        """
        records = session.run(query).data()
        for r in records:
            r['label'] = label
            r['id_field'] = id_field
            # Derive subject from metadata if not on node
            if not r.get('subject'):
                r['subject'] = meta['subject'] or 'General'
            # Derive key_stage from study ID if not on node
            if not r.get('key_stage'):
                r['key_stage'] = _extract_key_stage(r['study_id'])
            results.append(r)
    return results


def query_study_node(session, label: str, study_id: str) -> dict | None:
    """Fetch a single study node with all properties."""
    id_field = _get_id_field(label)
    query = f"""
        MATCH (ts:{label} {{{id_field}: $sid}})
        RETURN properties(ts) AS props, labels(ts) AS labels
    """
    records = session.run(query, sid=study_id).data()
    if not records:
        return None
    return records[0]['props']


def query_concepts(session, label: str, study_id: str) -> list[dict]:
    """Fetch concepts delivered by this study, with difficulty levels and CPA stages."""
    id_field = _get_id_field(label)
    query = f"""
        MATCH (ts:{label} {{{id_field}: $sid}})-[dv:DELIVERS_VIA]->(c:Concept)
        OPTIONAL MATCH (c)-[:HAS_DIFFICULTY_LEVEL]->(dl:DifficultyLevel)
        OPTIONAL MATCH (c)-[:HAS_REPRESENTATION_STAGE]->(rs:RepresentationStage)
        WITH c, dv.primary AS is_primary,
             collect(DISTINCT properties(dl)) AS dls,
             collect(DISTINCT properties(rs)) AS rss
        RETURN properties(c) AS concept, is_primary, dls, rss
        ORDER BY is_primary DESC, c.concept_id
    """
    records = session.run(query, sid=study_id).data()
    concepts = []
    for r in records:
        c = r['concept']
        c['is_primary'] = r['is_primary']
        # Sort difficulty levels by level_number
        c['difficulty_levels'] = sorted(
            [dl for dl in r['dls'] if dl],
            key=lambda x: x.get('level_number', 0)
        )
        # Sort representation stages by stage_number
        c['representation_stages'] = sorted(
            [rs for rs in r['rss'] if rs],
            key=lambda x: x.get('stage_number', 0)
        )
        concepts.append(c)
    return concepts


def query_thinking_lenses(session, domain_ids: list[str], key_stage: str) -> list[dict]:
    """Fetch thinking lenses for clusters in the given domains."""
    if not domain_ids:
        return []
    query = """
        MATCH (d:Domain)-[:HAS_CLUSTER]->(cc:ConceptCluster)-[al:APPLIES_LENS]->(tl:ThinkingLens)
        WHERE d.domain_id IN $dids
        OPTIONAL MATCH (tl)-[pf:PROMPT_FOR]->(ks:KeyStage {key_stage_id: $ks})
        RETURN DISTINCT tl.name AS lens_name,
               tl.key_question AS key_question,
               coalesce(pf.agent_prompt, tl.agent_prompt) AS agent_prompt,
               pf.question_stems AS question_stems,
               min(al.rank) AS best_rank,
               collect(DISTINCT al.rationale) AS rationales
        ORDER BY best_rank
    """
    records = session.run(query, dids=domain_ids, ks=key_stage).data()
    lenses = []
    for r in records:
        lenses.append({
            'lens_name': r['lens_name'],
            'key_question': r['key_question'],
            'agent_prompt': r['agent_prompt'],
            'question_stems': r['question_stems'] or [],
            'rank': r['best_rank'],
            'rationale': r['rationales'][0] if r['rationales'] else '',
        })
    return lenses


def query_vehicle_templates(session, template_ids: list[str], key_stage: str) -> list[dict]:
    """Fetch vehicle templates with age-banded prompts."""
    if not template_ids:
        return []
    query = """
        MATCH (vt:VehicleTemplate)
        WHERE vt.template_id IN $tids
        OPTIONAL MATCH (vt)-[tf:TEMPLATE_FOR]->(ks:KeyStage {key_stage_id: $ks})
        RETURN properties(vt) AS vt_props,
               tf.agent_prompt AS ks_agent_prompt,
               tf.question_stems AS ks_question_stems
    """
    records = session.run(query, tids=template_ids, ks=key_stage).data()
    templates = []
    for r in records:
        vt = r['vt_props']
        vt['ks_agent_prompt'] = r['ks_agent_prompt']
        vt['ks_question_stems'] = r['ks_question_stems'] or []
        templates.append(vt)
    return templates


def query_references(session, label: str, study_id: str) -> dict:
    """Fetch subject-specific reference nodes linked to this study."""
    id_field = _get_id_field(label)
    refs = {}

    if label == 'HistoryStudy':
        # Disciplinary concepts
        q = f"""
            MATCH (ts:{label} {{{id_field}: $sid}})-[r:FOREGROUNDS]->(dc:DisciplinaryConcept)
            RETURN properties(dc) AS props, r.rank AS rank, r.ks_guidance AS ks_guidance
            ORDER BY r.rank
        """
        records = session.run(q, sid=study_id).data()
        refs['disciplinary_concepts'] = [
            {**r['props'], 'rank': r['rank'], 'ks_guidance': r['ks_guidance']}
            for r in records
        ]
        # Historical sources
        q = f"""
            MATCH (ts:{label} {{{id_field}: $sid}})-[:USES_SOURCE]->(hs:HistoricalSource)
            RETURN properties(hs) AS props
        """
        refs['sources'] = [r['props'] for r in session.run(q, sid=study_id).data()]

    elif label == 'ScienceEnquiry':
        q = f"""
            MATCH (ts:{label} {{{id_field}: $sid}})-[:USES_ENQUIRY_TYPE]->(et:EnquiryType)
            RETURN properties(et) AS props
        """
        refs['enquiry_types'] = [r['props'] for r in session.run(q, sid=study_id).data()]
        q = f"""
            MATCH (ts:{label} {{{id_field}: $sid}})-[:SURFACES_MISCONCEPTION]->(m:Misconception)
            RETURN properties(m) AS props
        """
        refs['misconceptions'] = [r['props'] for r in session.run(q, sid=study_id).data()]

    elif label == 'EnglishUnit':
        q = f"""
            MATCH (ts:{label} {{{id_field}: $sid}})-[:IN_GENRE]->(g:Genre)
            RETURN properties(g) AS props
        """
        refs['genres'] = [r['props'] for r in session.run(q, sid=study_id).data()]
        q = f"""
            MATCH (ts:{label} {{{id_field}: $sid}})-[:STUDIES_TEXT]->(st:SetText)
            RETURN properties(st) AS props
        """
        refs['set_texts'] = [r['props'] for r in session.run(q, sid=study_id).data()]

    elif label == 'GeoStudy':
        q = f"""
            MATCH (ts:{label} {{{id_field}: $sid}})-[:LOCATED_IN]->(gp:GeoPlace)
            RETURN properties(gp) AS props
        """
        refs['places'] = [r['props'] for r in session.run(q, sid=study_id).data()]
        q = f"""
            MATCH (ts:{label} {{{id_field}: $sid}})-[:CONTRASTS_WITH]->(gc:GeoContrast)
            RETURN properties(gc) AS props
        """
        refs['contrasts'] = [r['props'] for r in session.run(q, sid=study_id).data()]

    return refs


LABEL_TO_SUBJECT = {
    'HistoryStudy': 'History', 'GeoStudy': 'Geography',
    'ScienceEnquiry': 'Science', 'EnglishUnit': 'English',
    'ArtTopicSuggestion': 'Art and Design', 'MusicTopicSuggestion': 'Music',
    'DTTopicSuggestion': 'Design and Technology',
    'ComputingTopicSuggestion': 'Computing', 'TopicSuggestion': 'General',
}


def query_cross_curricular(session, label: str, study_id: str) -> list[dict]:
    """Fetch cross-curricular links from graph."""
    id_field = _get_id_field(label)
    query = f"""
        MATCH (ts:{label} {{{id_field}: $sid}})-[cc:CROSS_CURRICULAR]->(target)
        RETURN target.name AS target_name,
               target.subject AS target_subject,
               cc.hook AS hook,
               cc.strength AS strength,
               labels(target)[0] AS target_label
    """
    results = session.run(query, sid=study_id).data()
    # Derive subject from target label when not set on node
    for r in results:
        if not r.get('target_subject') or r['target_subject'] in ('None', ''):
            r['target_subject'] = LABEL_TO_SUBJECT.get(r.get('target_label', ''), '')
    return results


def query_sequencing(session, label: str, study_id: str) -> tuple[str | None, str | None]:
    """Fetch what comes before and after this study."""
    id_field = _get_id_field(label)
    follows = None
    leads_to = None

    if label == 'HistoryStudy':
        # CHRONOLOGICALLY_FOLLOWS is a graph relationship
        q = f"""
            MATCH (ts:{label} {{{id_field}: $sid}})-[:CHRONOLOGICALLY_FOLLOWS]->(prev:{label})
            RETURN prev.name AS name LIMIT 1
        """
        records = session.run(q, sid=study_id).data()
        if records:
            follows = records[0]['name']
        # Check what follows this (reverse direction)
        q = f"""
            MATCH (next:{label})-[:CHRONOLOGICALLY_FOLLOWS]->(ts:{label} {{{id_field}: $sid}})
            RETURN next.name AS name LIMIT 1
        """
        records = session.run(q, sid=study_id).data()
        if records:
            leads_to = records[0]['name']

    elif label == 'GeoStudy':
        # BUILDS_ON is a graph relationship
        q = f"""
            MATCH (ts:{label} {{{id_field}: $sid}})-[:BUILDS_ON]->(prev:{label})
            RETURN prev.name AS name LIMIT 1
        """
        records = session.run(q, sid=study_id).data()
        if records:
            follows = records[0]['name']

    elif label == 'EnglishUnit':
        # Check for sequencing relationships
        q = f"""
            MATCH (ts:{label} {{{id_field}: $sid}})-[:GRAMMAR_SEQUENCE_AFTER]->(prev:{label})
            RETURN prev.name AS name LIMIT 1
        """
        records = session.run(q, sid=study_id).data()
        if records:
            follows = records[0]['name']
        # What follows this
        q = f"""
            MATCH (next:{label})-[:GRAMMAR_SEQUENCE_AFTER]->(ts:{label} {{{id_field}: $sid}})
            RETURN next.name AS name LIMIT 1
        """
        records = session.run(q, sid=study_id).data()
        if records:
            leads_to = records[0]['name']

    return follows, leads_to


def query_prerequisites(session, label: str, study_id: str) -> list[dict]:
    """Fetch prerequisite concepts for concepts delivered by this study.

    Returns concepts from earlier years/key stages that pupils should already
    know, grouped by the target concept they feed into.
    """
    id_field = _get_id_field(label)
    query = f"""
        MATCH (ts:{label} {{{id_field}: $sid}})-[:DELIVERS_VIA]->(c:Concept)
              <-[:PREREQUISITE_OF]-(prereq:Concept)
        WHERE prereq.concept_id <> c.concept_id
        RETURN DISTINCT prereq.concept_id AS prereq_id,
               prereq.name AS prereq_name,
               prereq.description AS prereq_description,
               c.concept_id AS target_id,
               c.name AS target_name
        ORDER BY prereq.concept_id
    """
    return session.run(query, sid=study_id).data()


def query_assessment_codes(session, concept_ids: list[str]) -> list[dict]:
    """Fetch KS2 ContentDomainCodes that assess these concepts."""
    if not concept_ids:
        return []
    query = """
        MATCH (cdc:ContentDomainCode)-[:ASSESSES_CONCEPT]->(c:Concept)
        WHERE c.concept_id IN $cids
        RETURN DISTINCT cdc.code_id AS code_id,
               cdc.name AS name,
               cdc.description AS description,
               c.concept_id AS concept_id,
               c.name AS concept_name
        ORDER BY cdc.code_id
    """
    return session.run(query, cids=concept_ids).data()


def query_learner_profile(session, year_codes: list[str]) -> dict:
    """Fetch PedagogyProfile, ContentGuideline, and FeedbackProfile for year groups.

    Returns the profile for the first (youngest) year group found, since
    planners should scaffold to the least-advanced learners in the cohort.
    """
    if not year_codes:
        return {}
    query = """
        UNWIND $ycs AS yc
        MATCH (y:Year {year_id: yc})
        OPTIONAL MATCH (y)-[:HAS_PEDAGOGY_PROFILE]->(pp:PedagogyProfile)
        OPTIONAL MATCH (y)-[:HAS_CONTENT_GUIDELINE]->(cg:ContentGuideline)
        OPTIONAL MATCH (y)-[:HAS_FEEDBACK_PROFILE]->(fp:FeedbackProfile)
        RETURN y.year_id AS year_id,
               properties(pp) AS pedagogy,
               properties(cg) AS content,
               properties(fp) AS feedback
        LIMIT 1
    """
    records = session.run(query, ycs=year_codes).data()
    if not records:
        return {}
    r = records[0]
    return {
        'year_id': r['year_id'],
        'pedagogy': r.get('pedagogy') or {},
        'content': r.get('content') or {},
        'feedback': r.get('feedback') or {},
    }


def query_source_documents(session, key_stage: str, subject: str = '',
                           domain_ids: list[str] | None = None,
                           concept_ids: list[str] | None = None) -> list[dict]:
    """Fetch source documents, preferring exact curriculum links over broad name matches.

    Priority order:
      1. SourceDocument linked to Programmes covering the study's domains
      2. SourceDocument linked directly from delivered concepts
      3. Subject + key stage name match
      4. Subject-only name match
      5. Key-stage-only fallback
    """
    if domain_ids:
        query = """
            MATCH (d:Domain)<-[:HAS_DOMAIN]-(p:Programme)-[:SOURCED_FROM]->(sd:SourceDocument)
            WHERE d.domain_id IN $dids
            RETURN properties(sd) AS props, count(DISTINCT d) AS hits
            ORDER BY hits DESC, props.name
        """
        records = session.run(query, dids=domain_ids).data()
        if records:
            return [r['props'] for r in records]

    if concept_ids:
        query = """
            MATCH (c:Concept)-[:SOURCED_FROM]->(sd:SourceDocument)
            WHERE c.concept_id IN $cids
            RETURN properties(sd) AS props, count(DISTINCT c) AS hits
            ORDER BY hits DESC, props.name
        """
        records = session.run(query, cids=concept_ids).data()
        if records:
            return [r['props'] for r in records]

    if subject:
        # Prefer programme-of-study style documents over test frameworks.
        query = """
            MATCH (:Curriculum)-[:HAS_DOCUMENT]->(sd:SourceDocument)
            WHERE sd.name CONTAINS $subject AND sd.name CONTAINS $ks
            RETURN properties(sd) AS props,
                   CASE
                       WHEN sd.name CONTAINS 'Programme of Study' THEN 0
                       WHEN sd.name CONTAINS 'Programme' THEN 1
                       WHEN sd.name CONTAINS 'National Curriculum' THEN 2
                       WHEN sd.name CONTAINS 'Test Framework' THEN 9
                       ELSE 5
                   END AS priority
            ORDER BY priority, sd.name
        """
        records = session.run(query, subject=subject, ks=key_stage).data()
        if records:
            return [r['props'] for r in records]

        # Fallback: subject only (for documents without KS in name)
        query = """
            MATCH (:Curriculum)-[:HAS_DOCUMENT]->(sd:SourceDocument)
            WHERE sd.name CONTAINS $subject
            RETURN properties(sd) AS props,
                   CASE
                       WHEN sd.name CONTAINS 'Programme of Study' THEN 0
                       WHEN sd.name CONTAINS 'Programme' THEN 1
                       WHEN sd.name CONTAINS 'National Curriculum' THEN 2
                       WHEN sd.name CONTAINS 'Test Framework' THEN 9
                       ELSE 5
                   END AS priority
            ORDER BY priority, sd.name
        """
        records = session.run(query, subject=subject).data()
        if records:
            return [r['props'] for r in records]

    # Last resort: match by key stage only
    query = """
        MATCH (:Curriculum)-[:HAS_DOCUMENT]->(sd:SourceDocument)
        WHERE sd.name CONTAINS $ks
        RETURN properties(sd) AS props
    """
    records = session.run(query, ks=key_stage).data()
    return [r['props'] for r in records]


def query_epistemic_skills(session, domain_ids: list[str]) -> list[dict]:
    """Fetch epistemic skills for these domains. Prefers concept-level links, falls back to programme."""
    if not domain_ids:
        return []
    # First try concept-level DEVELOPS_SKILL (curated, more specific)
    query = """
        UNWIND $dids AS did
        MATCH (d:Domain {domain_id: did})-[:CONTAINS]->(:Objective)-[:TEACHES]->(c:Concept)
              -[r:DEVELOPS_SKILL]->(s)
        RETURN DISTINCT s.name AS name, s.description AS description,
               labels(s)[0] AS skill_type
        LIMIT 8
    """
    results = session.run(query, dids=domain_ids).data()
    if results:
        return results
    # Fallback: programme-level skills (broader, cap at 6)
    query = """
        UNWIND $dids AS did
        MATCH (d:Domain {domain_id: did})<-[:HAS_DOMAIN]-(p:Programme)-[r:DEVELOPS_SKILL]->(s)
        RETURN DISTINCT s.name AS name, s.description AS description,
               labels(s)[0] AS skill_type
        LIMIT 6
    """
    return session.run(query, dids=domain_ids).data()


# ── JSON fallback for references ─────────────────────────────────────

def _fallback_references(study_json: dict, label: str) -> dict:
    """Extract reference data from raw JSON when graph rels are missing."""
    refs = {}

    if label == 'HistoryStudy':
        # Sources
        source_ids = study_json.get('uses_source_ids', [])
        if source_ids:
            all_sources = _load_reference_nodes('HistoricalSource')
            refs['sources'] = [all_sources[sid] for sid in source_ids if sid in all_sources]
        # Disciplinary concepts
        foregrounds = study_json.get('foregrounds', [])
        if foregrounds:
            all_dc = _load_reference_nodes('DisciplinaryConcept')
            refs['disciplinary_concepts'] = []
            for fg in foregrounds:
                slug = fg.get('disciplinary_concept_slug', '')
                # Find by slug match
                for dc_id, dc in all_dc.items():
                    if dc.get('slug') == slug or dc.get('concept_id') == slug:
                        refs['disciplinary_concepts'].append({
                            **dc, 'rank': fg.get('rank'), 'ks_guidance': fg.get('ks_guidance')
                        })
                        break

    elif label == 'ScienceEnquiry':
        enquiry_types = study_json.get('uses_enquiry_type', [])
        if enquiry_types:
            all_et = _load_reference_nodes('EnquiryType')
            refs['enquiry_types'] = [
                all_et[et['enquiry_type_id']]
                for et in enquiry_types
                if et.get('enquiry_type_id') in all_et
            ]
        misconceptions = study_json.get('surfaces_misconception', [])
        if misconceptions:
            all_m = _load_reference_nodes('Misconception')
            refs['misconceptions'] = [
                all_m[m['misconception_id']]
                for m in misconceptions
                if m.get('misconception_id') in all_m
            ]

    elif label == 'EnglishUnit':
        genres = study_json.get('in_genre', [])
        if genres:
            all_g = _load_reference_nodes('Genre')
            refs['genres'] = [
                all_g[g['genre_id']]
                for g in genres
                if g.get('genre_id') in all_g
            ]
        texts = study_json.get('studies_text', study_json.get('set_texts', []))
        if texts:
            all_st = _load_reference_nodes('SetText')
            refs['set_texts'] = [
                all_st[t['set_text_id']] if isinstance(t, dict) else all_st.get(t, {})
                for t in texts
                if (isinstance(t, dict) and t.get('set_text_id') in all_st) or
                   (isinstance(t, str) and t in all_st)
            ]

    elif label == 'GeoStudy':
        locations = study_json.get('locations', [])
        if locations:
            all_gp = _load_reference_nodes('GeoPlace')
            refs['places'] = [all_gp[loc] for loc in locations if loc in all_gp]
        contrasts = study_json.get('contrasts_with', [])
        if contrasts:
            all_gc = _load_reference_nodes('GeoContrast')
            refs['contrasts'] = [all_gc[c] for c in contrasts if c in all_gc]

    return refs


def _fallback_cross_curricular(study_json: dict) -> list[dict]:
    """Extract cross-curricular links from raw JSON."""
    links = study_json.get('cross_curricular_links', [])
    # ID prefix → subject mapping for fallback
    _PREFIX_SUBJECT = {
        'HS': 'History', 'GE': 'Geography', 'SE': 'Science',
        'EU': 'English', 'TS-AD': 'Art and Design', 'TS-MU': 'Music',
        'TS-DT': 'Design and Technology', 'TS-CO': 'Computing',
    }
    result = []
    for link in links:
        tid = link.get('target_id', '')
        # Derive subject from target ID prefix
        subj = ''
        for prefix, s in _PREFIX_SUBJECT.items():
            if tid.startswith(prefix):
                subj = s
                break
        result.append({
            'target_name': link.get('target_name', tid),
            'target_subject': subj,
            'hook': link.get('hook', ''),
            'strength': link.get('strength', ''),
        })
    return result


# ── Main query function ──────────────────────────────────────────────

def _query_domain_ids(session, label: str, study_id: str) -> list[str]:
    """Get domain IDs from HAS_SUGGESTION relationship (Domain → Study)."""
    id_field = _get_id_field(label)
    query = f"""
        MATCH (d:Domain)-[:HAS_SUGGESTION]->(ts:{label} {{{id_field}: $sid}})
        RETURN d.domain_id AS domain_id
    """
    return [r['domain_id'] for r in session.run(query, sid=study_id).data()
            if r.get('domain_id')]


def _query_template_ids(session, label: str, study_id: str) -> list[str]:
    """Get template IDs from USES_TEMPLATE relationship (Study → VehicleTemplate)."""
    id_field = _get_id_field(label)
    query = f"""
        MATCH (ts:{label} {{{id_field}: $sid}})-[:USES_TEMPLATE]->(vt:VehicleTemplate)
        RETURN vt.template_id AS template_id
    """
    return [r['template_id'] for r in session.run(query, sid=study_id).data()
            if r.get('template_id')]


def fetch_study_context(session, label: str, study_id: str) -> StudyContext | None:
    """Fetch complete context for a single study node."""
    # Q1: Study node
    study = query_study_node(session, label, study_id)
    if not study:
        return None

    id_field = _get_id_field(label)
    key_stage = study.get('key_stage', '') or _extract_key_stage(study_id)
    subject = study.get('subject', STUDY_NODES[label]['subject'] or 'General')

    # Domain IDs: try node property first, then graph relationship, then JSON fallback
    domain_ids = study.get('domain_ids', [])
    if isinstance(domain_ids, str):
        try:
            domain_ids = json.loads(domain_ids)
        except (json.JSONDecodeError, TypeError):
            domain_ids = [domain_ids] if domain_ids else []
    if not domain_ids:
        domain_ids = _query_domain_ids(session, label, study_id)
    if not domain_ids:
        # JSON fallback
        all_json = _load_json_studies(label)
        study_json = all_json.get(study_id, {})
        domain_ids = study_json.get('domain_ids', [])

    # Template IDs: try node property, then graph relationship, then JSON fallback
    template_ref = study.get('uses_template', [])
    if isinstance(template_ref, str):
        template_ids = [template_ref]
    elif isinstance(template_ref, list):
        template_ids = template_ref
    else:
        template_ids = []
    if not template_ids:
        template_ids = _query_template_ids(session, label, study_id)
    if not template_ids:
        all_json = _load_json_studies(label)
        study_json = all_json.get(study_id, {})
        tpl = study_json.get('uses_template', [])
        if isinstance(tpl, str):
            template_ids = [tpl]
        elif isinstance(tpl, list):
            template_ids = tpl

    # Q2: Concepts + difficulty levels + representation stages
    concepts = query_concepts(session, label, study_id)

    # Q3: Thinking lenses (via domain_ids)
    thinking_lenses = query_thinking_lenses(session, domain_ids, key_stage)

    # Q4: Vehicle templates
    templates = query_vehicle_templates(session, template_ids, key_stage)

    # Q5: Subject-specific references (graph, then JSON fallback)
    references = query_references(session, label, study_id)

    # JSON fallback for references if graph returned empty
    if not any(references.values()):
        all_json = _load_json_studies(label)
        study_json = all_json.get(study_id, {})
        if study_json:
            fallback_refs = _fallback_references(study_json, label)
            for k, v in fallback_refs.items():
                if v and not references.get(k):
                    references[k] = v

    # Q6: Cross-curricular links (graph, then JSON fallback)
    cross_curricular = query_cross_curricular(session, label, study_id)
    if not cross_curricular:
        all_json = _load_json_studies(label)
        study_json = all_json.get(study_id, {})
        if study_json:
            cross_curricular = _fallback_cross_curricular(study_json)

    # Q7: Sequencing
    follows, leads_to = query_sequencing(session, label, study_id)

    concept_ids = [c.get('concept_id') for c in concepts if c.get('concept_id')]

    # Source documents (prefer exact domain/programme links)
    source_documents = query_source_documents(
        session, key_stage, subject, domain_ids=domain_ids, concept_ids=concept_ids
    )

    # Epistemic skills
    epistemic_skills = query_epistemic_skills(session, domain_ids)

    # Prerequisites (what pupils should already know)
    prerequisites = query_prerequisites(session, label, study_id)

    # KS2 assessment codes (ContentDomainCodes)
    assessment_codes = query_assessment_codes(session, concept_ids) if key_stage == 'KS2' else []

    # Learner profile (pedagogy, content guideline, feedback)
    year_groups = study.get('year_groups', [])
    if isinstance(year_groups, str):
        try:
            year_groups = json.loads(year_groups)
        except (json.JSONDecodeError, TypeError):
            year_groups = [year_groups] if year_groups else []
    learner_profile = query_learner_profile(session, year_groups) if year_groups else {}

    return StudyContext(
        study=study,
        label=label,
        study_id=study_id,
        subject=subject,
        key_stage=key_stage,
        concepts=concepts,
        thinking_lenses=thinking_lenses,
        templates=templates,
        references=references,
        cross_curricular=cross_curricular,
        source_documents=source_documents,
        follows=follows,
        leads_to=leads_to,
        epistemic_skills=epistemic_skills,
        prerequisites=prerequisites,
        assessment_codes=assessment_codes,
        learner_profile=learner_profile,
    )


# ── Utility helpers ──────────────────────────────────────────────────

def slugify(text: str) -> str:
    """Convert study name to filesystem-safe slug."""
    import re
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s-]+', '_', text)
    text = text.strip('_')
    return text


def subject_slug(subject: str) -> str:
    """Convert subject name to folder-friendly slug."""
    mapping = {
        'History': 'history',
        'Geography': 'geography',
        'Science': 'science',
        'English': 'english',
        'Art and Design': 'art',
        'Music': 'music',
        'Design and Technology': 'dt',
        'Computing': 'computing',
        'Religious Studies': 'rs',
        'Citizenship': 'citizenship',
    }
    return mapping.get(subject, slugify(subject))


def output_folder(subject: str, key_stage: str) -> str:
    """Generate folder name like 'history_ks2'."""
    return f"{subject_slug(subject)}_{key_stage.lower()}"


if __name__ == '__main__':
    """Quick test: list all study nodes."""
    from neo4j import GraphDatabase
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    try:
        with driver.session() as session:
            studies = query_all_study_ids(session)
            print(f"Found {len(studies)} study nodes:\n")
            by_subject = {}
            for s in studies:
                subj = s['subject']
                by_subject.setdefault(subj, []).append(s)
            for subj in sorted(by_subject.keys()):
                items = by_subject[subj]
                print(f"  {subj} ({len(items)}):")
                for item in items[:3]:
                    print(f"    {item['study_id']}: {item['name']} ({item['key_stage']})")
                if len(items) > 3:
                    print(f"    ... and {len(items) - 3} more")
    finally:
        driver.close()

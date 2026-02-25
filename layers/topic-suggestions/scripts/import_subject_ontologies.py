#!/usr/bin/env python3
"""
Import per-subject ontology nodes and relationships.

Each intellectual discipline has its own node types expressing how its concepts
should be taught. This replaces the universal TopicSuggestion wrapper for the
"big 5" subjects (History, Geography, Science, English, Maths) while keeping
typed TopicSuggestion labels for foundation subjects.

Import order:
  Phase 1: Reference nodes (no inter-dependencies)
  Phase 2: Study/unit nodes (reference nodes must exist first)
  Phase 3: Cross-references between nodes (all nodes must exist)

Usage:
  python3 layers/topic-suggestions/scripts/import_subject_ontologies.py
  python3 layers/topic-suggestions/scripts/import_subject_ontologies.py --clear
"""

import json
import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / "core" / "scripts"))

from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

DATA_DIR = PROJECT_ROOT / "layers" / "topic-suggestions" / "data"

# ─── Node type configurations ────────────────────────────────────────────────
# (label, data_subdir, id_field, array_key_in_wrapper_or_None)
# array_key=None means the JSON file is a plain array [...].
# array_key="studies" means the file is { ..., "studies": [...] }.

REFERENCE_NODES = [
    ("DisciplinaryConcept", "history_disciplinary_concepts", "concept_id", "disciplinary_concepts"),
    ("HistoricalSource", "history_sources", "source_id", "sources"),
    ("GeoPlace", "geo_places", "place_id", "places"),
    ("GeoContrast", "geo_contrasts", "contrast_id", "contrasts"),
    ("EnquiryType", "science_enquiry_types", "enquiry_type_id", None),
    ("Misconception", "science_misconceptions", "misconception_id", None),
    ("Genre", "english_genres", "genre_id", "genres"),
    ("SetText", "english_set_texts", "set_text_id", "set_texts"),
    ("MathsManipulative", "maths_manipulatives", "manipulative_id", None),
    ("MathsRepresentation", "maths_representations", "representation_id", None),
    ("MathsContext", "maths_contexts", "context_id", None),
    ("ReasoningPromptType", "maths_reasoning", "prompt_type_id", None),
]

STUDY_NODES = [
    ("HistoryStudy", "history_studies", "study_id", "studies"),
    ("GeoStudy", "geo_studies", "study_id", "studies"),
    ("ScienceEnquiry", "science_enquiries", "enquiry_id", "enquiries"),
    ("EnglishUnit", "english_units", "unit_id", "units"),
    # Foundation subjects — use typed TopicSuggestion labels
    ("ArtTopicSuggestion", "art_studies", "suggestion_id", None),
    ("MusicTopicSuggestion", "music_studies", "suggestion_id", None),
    ("DTTopicSuggestion", "dt_studies", "suggestion_id", None),
    ("ComputingTopicSuggestion", "computing_studies", "suggestion_id", None),
    ("TopicSuggestion", "generic_studies", "suggestion_id", None),
]

# Fields that encode relationships (not stored as node properties)
RELATIONSHIP_FIELDS = {
    "delivers_via", "uses_template", "domain_ids", "in_genre", "studies_text",
    "foregrounds", "uses_source_ids", "chronologically_follows",
    "thematically_linked_to", "contrasts_with", "builds_on", "complements",
    "locations", "uses_enquiry_type", "surfaces_misconception", "progresses_to",
    "grammar_sequence_after", "text_complexity_after",
    "source_concepts", "develops_skill", "prerequisite_misconception_ids",
    "cross_curricular_hooks", "cross_curricular_links",
    # Wrapper metadata fields (not node properties)
    "genre_progressions", "genre_affinities",
    # File-level metadata keys
    "metadata", "version", "subject", "key_stage", "authored_by",
    "authored_date", "note", "node_label",
}

ALL_LABELS = [cfg[0] for cfg in REFERENCE_NODES + STUDY_NODES]


class SubjectOntologyImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            "nodes_created": 0,
            "delivers_via": 0,
            "uses_template": 0,
            "has_suggestion": 0,
            "foregrounds": 0,
            "uses_source": 0,
            "chronologically_follows": 0,
            "located_in": 0,
            "contrasts_with": 0,
            "uses_enquiry_type": 0,
            "surfaces_misconception": 0,
            "in_genre": 0,
            "studies_text": 0,
            "progresses_to": 0,
            "builds_on": 0,
            "prerequisite_misconception": 0,
            "genre_progressions": 0,
            "genre_affinities": 0,
            "concept_link": 0,
            "develops_skill": 0,
            "cross_curricular": 0,
            "errors": [],
        }

    def close(self):
        self.driver.close()

    # ─── File loading ─────────────────────────────────────────────────────────

    def _load_items(self, filepath, array_key):
        """Load items from a JSON file, handling all 3 wrapper formats."""
        with open(filepath) as f:
            data = json.load(f)

        if isinstance(data, list):
            return data

        if array_key and array_key in data:
            return data[array_key]

        # Try to find the first list value (skip metadata-like keys)
        for key, val in data.items():
            if isinstance(val, list) and val and isinstance(val[0], dict):
                return val

        self.stats["errors"].append(f"{filepath.name}: could not find items array")
        return []

    def _load_all_files(self, data_subdir, array_key):
        """Load items from all JSON files in a data subdirectory."""
        subdir = DATA_DIR / data_subdir
        if not subdir.exists():
            return []

        all_items = []
        for f in sorted(subdir.glob("*.json")):
            all_items.extend(self._load_items(f, array_key))
        return all_items

    # ─── Node creation ────────────────────────────────────────────────────────

    def _serialize_props(self, item, id_field):
        """Prepare node properties: exclude relationship fields, serialize nested objects."""
        props = {}
        for key, val in item.items():
            if key in RELATIONSHIP_FIELDS:
                continue
            if val is None:
                continue
            # Neo4j can store string[], int[] natively but not object[]
            if isinstance(val, list) and val and isinstance(val[0], dict):
                props[key] = json.dumps(val)
            elif isinstance(val, dict):
                props[key] = json.dumps(val)
            else:
                props[key] = val
        return props

    def _merge_node(self, session, label, id_field, item):
        """MERGE a single node."""
        node_id = item.get(id_field)
        if not node_id:
            self.stats["errors"].append(f"Missing {id_field} in {label} item")
            return None

        props = self._serialize_props(item, id_field)
        set_parts = ", ".join(f"n.{k} = ${k}" for k in props.keys())
        query = f"""
            MERGE (n:{label} {{{id_field}: ${id_field}}})
            SET {set_parts}
        """
        session.run(query, **props)
        self.stats["nodes_created"] += 1
        return node_id

    def _import_node_group(self, session, label, data_subdir, id_field, array_key):
        """Import all nodes of one type from all files in a subdirectory."""
        items = self._load_all_files(data_subdir, array_key)
        if not items:
            return []

        print(f"\n  {label}: {len(items)} items from {data_subdir}/")
        ids = []
        for item in items:
            nid = self._merge_node(session, label, id_field, item)
            if nid:
                ids.append(nid)
        print(f"    created {len(ids)} nodes")
        return ids

    # ─── Shared relationships ─────────────────────────────────────────────────

    def _create_delivers_via(self, session, label, id_field, items):
        """Create DELIVERS_VIA relationships to Concept nodes."""
        for item in items:
            node_id = item.get(id_field)
            if not node_id:
                continue
            for ref in (item.get("delivers_via") or []):
                concept_id = ref if isinstance(ref, str) else ref.get("concept_id", "")
                primary = False if isinstance(ref, str) else ref.get("primary", False)
                if concept_id:
                    session.run(f"""
                        MATCH (n:{label} {{{id_field}: $nid}})
                        MATCH (c:Concept {{concept_id: $cid}})
                        MERGE (n)-[r:DELIVERS_VIA]->(c)
                        SET r.primary = $primary
                    """, nid=node_id, cid=concept_id, primary=primary)
                    self.stats["delivers_via"] += 1

    def _create_uses_template(self, session, label, id_field, items):
        """Create USES_TEMPLATE relationships to VehicleTemplate nodes."""
        for item in items:
            node_id = item.get(id_field)
            if not node_id:
                continue
            templates = (item.get("uses_template") or [])
            # Handle string (single) or list
            if isinstance(templates, str):
                templates = [templates]
            for tid in templates:
                session.run(f"""
                    MATCH (n:{label} {{{id_field}: $nid}})
                    MATCH (vt:VehicleTemplate {{template_id: $tid}})
                    MERGE (n)-[:USES_TEMPLATE]->(vt)
                """, nid=node_id, tid=tid)
                self.stats["uses_template"] += 1

    def _create_has_suggestion(self, session, label, id_field, items):
        """Create HAS_SUGGESTION relationships from Domain nodes."""
        for item in items:
            node_id = item.get(id_field)
            if not node_id:
                continue
            for domain_id in (item.get("domain_ids") or []):
                session.run(f"""
                    MATCH (d:Domain {{domain_id: $did}})
                    MATCH (n:{label} {{{id_field}: $nid}})
                    MERGE (d)-[:HAS_SUGGESTION]->(n)
                """, did=domain_id, nid=node_id)
                self.stats["has_suggestion"] += 1

    # ─── History relationships ────────────────────────────────────────────────

    def _create_history_rels(self, session, items):
        """Create History-specific relationships."""
        for item in items:
            sid = item.get("study_id")
            if not sid:
                continue

            # FOREGROUNDS -> DisciplinaryConcept
            for fg in (item.get("foregrounds") or []):
                slug = fg.get("disciplinary_concept_slug")
                if slug:
                    session.run("""
                        MATCH (hs:HistoryStudy {study_id: $sid})
                        MATCH (dc:DisciplinaryConcept {slug: $slug})
                        MERGE (hs)-[r:FOREGROUNDS]->(dc)
                        SET r.rank = $rank, r.ks_guidance = $guidance
                    """, sid=sid, slug=slug,
                        rank=fg.get("rank", 1),
                        guidance=fg.get("ks_guidance", ""))
                    self.stats["foregrounds"] += 1

            # USES_SOURCE -> HistoricalSource
            for src_id in (item.get("uses_source_ids") or []):
                session.run("""
                    MATCH (hs:HistoryStudy {study_id: $sid})
                    MATCH (src:HistoricalSource {source_id: $srcid})
                    MERGE (hs)-[:USES_SOURCE]->(src)
                """, sid=sid, srcid=src_id)
                self.stats["uses_source"] += 1

            # CHRONOLOGICALLY_FOLLOWS -> HistoryStudy
            follows = item.get("chronologically_follows")
            if follows:
                session.run("""
                    MATCH (a:HistoryStudy {study_id: $sid})
                    MATCH (b:HistoryStudy {study_id: $fid})
                    MERGE (a)-[:CHRONOLOGICALLY_FOLLOWS]->(b)
                """, sid=sid, fid=follows)
                self.stats["chronologically_follows"] += 1

    # ─── Geography relationships ──────────────────────────────────────────────

    def _create_geo_rels(self, session, studies, contrasts):
        """Create Geography-specific relationships."""
        for item in studies:
            sid = item.get("study_id")
            if not sid:
                continue

            # LOCATED_IN -> GeoPlace
            for place_id in (item.get("locations") or []):
                session.run("""
                    MATCH (gs:GeoStudy {study_id: $sid})
                    MATCH (gp:GeoPlace {place_id: $pid})
                    MERGE (gs)-[:LOCATED_IN]->(gp)
                """, sid=sid, pid=place_id)
                self.stats["located_in"] += 1

            # BUILDS_ON -> GeoStudy
            for ref_id in (item.get("builds_on") or []):
                session.run("""
                    MATCH (a:GeoStudy {study_id: $sid})
                    MATCH (b:GeoStudy {study_id: $rid})
                    MERGE (a)-[:BUILDS_ON]->(b)
                """, sid=sid, rid=ref_id)
                self.stats["builds_on"] += 1

            # CONTRASTS_WITH -> GeoContrast
            for cid in (item.get("contrasts_with") or []):
                session.run("""
                    MATCH (gs:GeoStudy {study_id: $sid})
                    MATCH (gc:GeoContrast {contrast_id: $cid})
                    MERGE (gs)-[:CONTRASTS_WITH]->(gc)
                """, sid=sid, cid=cid)
                self.stats["contrasts_with"] += 1

        # GeoContrast place/study links
        for item in contrasts:
            cid = item.get("contrast_id")
            if not cid:
                continue
            for field, label, id_field in [
                ("place_a_id", "GeoPlace", "place_id"),
                ("place_b_id", "GeoPlace", "place_id"),
            ]:
                ref = item.get(field)
                if ref:
                    session.run(f"""
                        MATCH (gc:GeoContrast {{contrast_id: $cid}})
                        MATCH (t:{label} {{{id_field}: $ref}})
                        MERGE (gc)-[:INVOLVES_PLACE]->(t)
                    """, cid=cid, ref=ref)
                    self.stats["contrasts_with"] += 1

            for field in ("study_a_id", "study_b_id"):
                ref = item.get(field)
                if ref:
                    session.run("""
                        MATCH (gc:GeoContrast {contrast_id: $cid})
                        MATCH (gs:GeoStudy {study_id: $ref})
                        MERGE (gc)-[:INVOLVES_STUDY]->(gs)
                    """, cid=cid, ref=ref)
                    self.stats["contrasts_with"] += 1

    # ─── Science relationships ────────────────────────────────────────────────

    def _create_science_rels(self, session, enquiries, misconceptions, enquiry_types):
        """Create Science-specific relationships."""
        for item in enquiries:
            eid = item.get("enquiry_id")
            if not eid:
                continue

            # USES_ENQUIRY_TYPE -> EnquiryType
            for ref in (item.get("uses_enquiry_type") or []):
                etid = ref.get("enquiry_type_id") if isinstance(ref, dict) else ref
                rank = ref.get("rank", 1) if isinstance(ref, dict) else 1
                if etid:
                    session.run("""
                        MATCH (se:ScienceEnquiry {enquiry_id: $eid})
                        MATCH (et:EnquiryType {enquiry_type_id: $etid})
                        MERGE (se)-[r:USES_ENQUIRY_TYPE]->(et)
                        SET r.rank = $rank
                    """, eid=eid, etid=etid, rank=rank)
                    self.stats["uses_enquiry_type"] += 1

            # SURFACES_MISCONCEPTION -> Misconception
            for ref in (item.get("surfaces_misconception") or []):
                mid = ref.get("misconception_id") if isinstance(ref, dict) else ref
                likelihood = ref.get("likelihood", "moderate") if isinstance(ref, dict) else "moderate"
                if mid:
                    session.run("""
                        MATCH (se:ScienceEnquiry {enquiry_id: $eid})
                        MATCH (m:Misconception {misconception_id: $mid})
                        MERGE (se)-[r:SURFACES_MISCONCEPTION]->(m)
                        SET r.likelihood = $likelihood
                    """, eid=eid, mid=mid, likelihood=likelihood)
                    self.stats["surfaces_misconception"] += 1

            # PROGRESSES_TO -> ScienceEnquiry
            for ref in (item.get("progresses_to") or []):
                target = ref.get("enquiry_id") if isinstance(ref, dict) else ref
                rationale = ref.get("rationale", "") if isinstance(ref, dict) else ""
                if target:
                    session.run("""
                        MATCH (a:ScienceEnquiry {enquiry_id: $eid})
                        MATCH (b:ScienceEnquiry {enquiry_id: $tid})
                        MERGE (a)-[r:PROGRESSES_TO]->(b)
                        SET r.rationale = $rationale
                    """, eid=eid, tid=target, rationale=rationale)
                    self.stats["progresses_to"] += 1

        # Misconception prerequisite chains
        for item in misconceptions:
            mid = item.get("misconception_id")
            for prereq in (item.get("prerequisite_misconception_ids") or []):
                session.run("""
                    MATCH (a:Misconception {misconception_id: $mid})
                    MATCH (b:Misconception {misconception_id: $pid})
                    MERGE (a)-[:PREREQUISITE_MISCONCEPTION]->(b)
                """, mid=mid, pid=prereq)
                self.stats["prerequisite_misconception"] += 1

        # EnquiryType -> WorkingScientifically (develops_skill)
        for item in enquiry_types:
            etid = item.get("enquiry_type_id")
            for ref in (item.get("develops_skill") or []):
                skill_id = ref.get("skill_id") if isinstance(ref, dict) else ref
                strength = ref.get("strength", "supporting") if isinstance(ref, dict) else "supporting"
                if skill_id:
                    session.run("""
                        MATCH (et:EnquiryType {enquiry_type_id: $etid})
                        MATCH (ws:WorkingScientifically {skill_id: $sid})
                        MERGE (et)-[r:DEVELOPS_SKILL]->(ws)
                        SET r.strength = $strength
                    """, etid=etid, sid=skill_id, strength=strength)
                    self.stats["develops_skill"] += 1

    # ─── English relationships ────────────────────────────────────────────────

    def _create_english_rels(self, session, units, genres_data):
        """Create English-specific relationships."""
        for item in units:
            uid = item.get("unit_id")
            if not uid:
                continue

            # IN_GENRE -> Genre
            for ref in (item.get("in_genre") or []):
                gid = ref.get("genre_id") if isinstance(ref, dict) else ref
                role = ref.get("role", "primary") if isinstance(ref, dict) else "primary"
                if gid:
                    session.run("""
                        MATCH (eu:EnglishUnit {unit_id: $uid})
                        MATCH (g:Genre {genre_id: $gid})
                        MERGE (eu)-[r:IN_GENRE]->(g)
                        SET r.role = $role
                    """, uid=uid, gid=gid, role=role)
                    self.stats["in_genre"] += 1

            # STUDIES_TEXT -> SetText
            for stid in (item.get("studies_text") or []):
                session.run("""
                    MATCH (eu:EnglishUnit {unit_id: $uid})
                    MATCH (st:SetText {set_text_id: $stid})
                    MERGE (eu)-[:STUDIES_TEXT]->(st)
                """, uid=uid, stid=stid)
                self.stats["studies_text"] += 1

            # GRAMMAR_SEQUENCE_AFTER -> EnglishUnit
            after = item.get("grammar_sequence_after")
            if after:
                session.run("""
                    MATCH (a:EnglishUnit {unit_id: $uid})
                    MATCH (b:EnglishUnit {unit_id: $aid})
                    MERGE (a)-[:GRAMMAR_SEQUENCE_AFTER]->(b)
                """, uid=uid, aid=after)

            # TEXT_COMPLEXITY_AFTER -> EnglishUnit
            after = item.get("text_complexity_after")
            if after:
                session.run("""
                    MATCH (a:EnglishUnit {unit_id: $uid})
                    MATCH (b:EnglishUnit {unit_id: $aid})
                    MERGE (a)-[:TEXT_COMPLEXITY_AFTER]->(b)
                """, uid=uid, aid=after)

        # Genre progressions and affinities (from genres.json top-level arrays)
        genres_file = DATA_DIR / "english_genres" / "genres.json"
        if genres_file.exists():
            with open(genres_file) as f:
                gdata = json.load(f)

            for prog in (gdata.get("genre_progressions") or []):
                session.run("""
                    MATCH (a:Genre {genre_id: $from_id})
                    MATCH (b:Genre {genre_id: $to_id})
                    MERGE (a)-[r:PROGRESSES_TO]->(b)
                    SET r.from_ks = $from_ks, r.to_ks = $to_ks,
                        r.progression_note = $note
                """, from_id=prog["from_genre_id"], to_id=prog["to_genre_id"],
                    from_ks=prog.get("from_ks", ""), to_ks=prog.get("to_ks", ""),
                    note=prog.get("progression_note", ""))
                self.stats["genre_progressions"] += 1

            for aff in (gdata.get("genre_affinities") or []):
                session.run("""
                    MATCH (a:Genre {genre_id: $id1})
                    MATCH (b:Genre {genre_id: $id2})
                    MERGE (a)-[r:SHARES_AFFINITY_WITH]->(b)
                    SET r.affinity_note = $note
                """, id1=aff["genre_id_1"], id2=aff["genre_id_2"],
                    note=aff.get("affinity_note", ""))
                self.stats["genre_affinities"] += 1

    # ─── Maths relationships ─────────────────────────────────────────────────

    def _create_maths_rels(self, session, manipulatives, representations,
                           contexts, reasoning_types):
        """Create Maths-specific relationships (source_concepts -> Concept)."""
        for item in manipulatives:
            mid = item.get("manipulative_id")
            if not mid:
                continue
            for cid in (item.get("source_concepts") or []):
                session.run("""
                    MATCH (mm:MathsManipulative {manipulative_id: $mid})
                    MATCH (c:Concept {concept_id: $cid})
                    MERGE (mm)-[:USED_FOR_CONCEPT]->(c)
                """, mid=mid, cid=cid)
                self.stats["concept_link"] += 1

        for item in representations:
            rid = item.get("representation_id")
            if not rid:
                continue
            for cid in (item.get("source_concepts") or []):
                session.run("""
                    MATCH (mr:MathsRepresentation {representation_id: $rid})
                    MATCH (c:Concept {concept_id: $cid})
                    MERGE (mr)-[:USED_FOR_CONCEPT]->(c)
                """, rid=rid, cid=cid)
                self.stats["concept_link"] += 1

        for item in contexts:
            cxid = item.get("context_id")
            if not cxid:
                continue
            for cid in (item.get("source_concepts") or []):
                session.run("""
                    MATCH (mc:MathsContext {context_id: $cxid})
                    MATCH (c:Concept {concept_id: $cid})
                    MERGE (mc)-[:USED_FOR_CONCEPT]->(c)
                """, cxid=cxid, cid=cid)
                self.stats["concept_link"] += 1

        for item in reasoning_types:
            ptid = item.get("prompt_type_id")
            if not ptid:
                continue
            for cid in (item.get("source_concepts") or []):
                session.run("""
                    MATCH (rpt:ReasoningPromptType {prompt_type_id: $ptid})
                    MATCH (c:Concept {concept_id: $cid})
                    MERGE (rpt)-[:USED_FOR_CONCEPT]->(c)
                """, ptid=ptid, cid=cid)
                self.stats["concept_link"] += 1

    # ─── Cross-curricular relationships ─────────────────────────────────────

    def _create_cross_curricular_rels(self, session, study_data):
        """Create CROSS_CURRICULAR relationships from cross_curricular_links."""
        # Build lookup: node_id -> (label, id_field)
        id_to_label = {}
        for label, _subdir, id_field, _array_key in STUDY_NODES:
            for item in study_data.get(label, []):
                nid = item.get(id_field)
                if nid:
                    id_to_label[nid] = (label, id_field)

        for label, _subdir, id_field, _array_key in STUDY_NODES:
            for item in study_data.get(label, []):
                source_id = item.get(id_field)
                if not source_id:
                    continue
                for link in (item.get("cross_curricular_links") or []):
                    target_id = link.get("target_id")
                    hook = link.get("hook", "")
                    strength = link.get("strength", "moderate")
                    if not target_id:
                        continue
                    target_info = id_to_label.get(target_id)
                    if not target_info:
                        self.stats["errors"].append(
                            f"CROSS_CURRICULAR: target {target_id} not found "
                            f"(from {source_id})")
                        continue
                    target_label, target_id_field = target_info
                    session.run(f"""
                        MATCH (a:{label} {{{id_field}: $source_id}})
                        MATCH (b:{target_label} {{{target_id_field}: $target_id}})
                        MERGE (a)-[r:CROSS_CURRICULAR]->(b)
                        SET r.hook = $hook, r.strength = $strength
                    """, source_id=source_id, target_id=target_id,
                        hook=hook, strength=strength)
                    self.stats["cross_curricular"] += 1

    # ─── Clear ────────────────────────────────────────────────────────────────

    def clear(self):
        """Delete all per-subject ontology nodes and their relationships."""
        total = 0
        with self.driver.session() as session:
            for label in ALL_LABELS:
                result = session.run(
                    f"MATCH (n:{label}) DETACH DELETE n RETURN count(n) AS deleted"
                )
                deleted = result.single()["deleted"]
                if deleted > 0:
                    print(f"  Cleared {deleted} {label} nodes")
                    total += deleted
        print(f"  Total cleared: {total} nodes")

    # ─── Main run ─────────────────────────────────────────────────────────────

    def run(self, clear=False):
        print("=" * 60)
        print("Import: Per-Subject Ontology Nodes")
        print("=" * 60)

        if clear:
            print("\n--clear: removing existing ontology nodes...")
            self.clear()

        with self.driver.session() as session:
            # ── Phase 1: Reference nodes ──────────────────────────────────
            print("\n── Phase 1: Reference Nodes ──")
            ref_data = {}
            for label, subdir, id_field, array_key in REFERENCE_NODES:
                items = self._load_all_files(subdir, array_key)
                if items:
                    print(f"\n  {label}: {len(items)} items from {subdir}/")
                    for item in items:
                        self._merge_node(session, label, id_field, item)
                    print(f"    created {len(items)} nodes")
                ref_data[label] = items

            # ── Phase 2: Study/unit nodes ─────────────────────────────────
            print("\n── Phase 2: Study / Unit Nodes ──")
            study_data = {}
            for label, subdir, id_field, array_key in STUDY_NODES:
                items = self._load_all_files(subdir, array_key)
                if items:
                    print(f"\n  {label}: {len(items)} items from {subdir}/")
                    for item in items:
                        self._merge_node(session, label, id_field, item)
                    print(f"    created {len(items)} nodes")
                study_data[label] = items

            # ── Phase 3: Relationships ────────────────────────────────────
            print("\n── Phase 3: Relationships ──")

            # Shared relationships for all study/unit types
            for label, subdir, id_field, array_key in STUDY_NODES:
                items = study_data.get(label, [])
                if not items:
                    continue
                print(f"\n  {label} relationships:")
                self._create_delivers_via(session, label, id_field, items)
                self._create_uses_template(session, label, id_field, items)
                self._create_has_suggestion(session, label, id_field, items)

            # Subject-specific relationships
            print("\n  History-specific relationships:")
            self._create_history_rels(session, study_data.get("HistoryStudy", []))

            print("\n  Geography-specific relationships:")
            self._create_geo_rels(
                session,
                study_data.get("GeoStudy", []),
                ref_data.get("GeoContrast", []),
            )

            print("\n  Science-specific relationships:")
            self._create_science_rels(
                session,
                study_data.get("ScienceEnquiry", []),
                ref_data.get("Misconception", []),
                ref_data.get("EnquiryType", []),
            )

            print("\n  English-specific relationships:")
            self._create_english_rels(
                session,
                study_data.get("EnglishUnit", []),
                ref_data.get("Genre", []),
            )

            print("\n  Maths-specific relationships:")
            self._create_maths_rels(
                session,
                ref_data.get("MathsManipulative", []),
                ref_data.get("MathsRepresentation", []),
                ref_data.get("MathsContext", []),
                ref_data.get("ReasoningPromptType", []),
            )

            # Cross-curricular links (study-to-study across subjects)
            print("\n  Cross-curricular relationships:")
            self._create_cross_curricular_rels(session, study_data)

        # ── Report ────────────────────────────────────────────────────────
        print(f"\n{'=' * 60}")
        print("IMPORT COMPLETE")
        print("=" * 60)
        for k, v in self.stats.items():
            if k == "errors":
                continue
            if v > 0:
                print(f"  {k}: {v}")
        if self.stats["errors"]:
            print(f"\n  ERRORS ({len(self.stats['errors'])}):")
            for err in self.stats["errors"][:30]:
                print(f"    {err}")
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Import per-subject ontology nodes and relationships"
    )
    parser.add_argument(
        "--clear", action="store_true",
        help="Delete existing ontology nodes before importing"
    )
    args = parser.parse_args()

    importer = SubjectOntologyImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    try:
        importer.run(clear=args.clear)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        importer.close()


if __name__ == "__main__":
    main()

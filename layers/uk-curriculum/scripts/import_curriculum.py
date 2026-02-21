#!/usr/bin/env python3
"""
Import UK Curriculum extractions into Neo4j
Graph Model v3.0 - Programme-based model with SourceDocument traceability

New graph structure:
  Curriculum -[HAS_KEY_STAGE]-> KeyStage -[HAS_YEAR]-> Year -[HAS_PROGRAMME]-> Programme
  Programme -[FOR_SUBJECT]-> Subject
  Programme -[HAS_DOMAIN]-> Domain -[CONTAINS]-> Objective -[TEACHES]-> Concept
  Programme -[SOURCED_FROM]-> SourceDocument
  Curriculum -[HAS_DOCUMENT]-> SourceDocument
  Concept -[SOURCED_FROM]-> SourceDocument

Loads JSON files from /data/extractions/ directory and metadata from
/data/curriculum-documents/metadata.json
"""

from neo4j import GraphDatabase
import json
import os
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "core" / "scripts"))
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
LAYER_ROOT = Path(__file__).parent.parent
EXTRACTIONS_DIR = LAYER_ROOT / "data" / "extractions"
METADATA_FILE = PROJECT_ROOT / "core" / "data" / "curriculum-documents" / "metadata.json"

# Core subjects as defined by the National Curriculum
CORE_SUBJECTS = {"Mathematics", "English", "Science"}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def year_to_age_range(year_num):
    """Map a year group number to its age range string."""
    ages = {
        1: "5-6",
        2: "6-7",
        3: "7-8",
        4: "8-9",
        5: "9-10",
        6: "10-11",
        7: "11-12",
        8: "12-13",
        9: "13-14",
        10: "14-15",
        11: "15-16",
    }
    return ages.get(int(year_num) if str(year_num).isdigit() else -1, "unknown")


def coerce_years(years):
    """
    Coerce a list of year values (possibly strings like 'Year 1') to integers.
    Returns a sorted list of integers.
    """
    result = []
    for y in years:
        if isinstance(y, int):
            result.append(y)
        elif isinstance(y, str):
            # Handle 'Year 1', 'Year 2', '1', '2', etc.
            digits = ''.join(c for c in y if c.isdigit())
            if digits:
                result.append(int(digits))
    return sorted(result)


def years_to_age_range(years):
    """Derive an age range string covering all years in a list."""
    int_years = coerce_years(years) if years else []
    if not int_years:
        return "unknown"
    min_year = min(int_years)
    max_year = max(int_years)
    start = year_to_age_range(min_year)
    end = year_to_age_range(max_year)
    start_age = start.split("-")[0] if "-" in start else start
    end_age = end.split("-")[1] if "-" in end else end
    return f"{start_age}-{end_age}"


def make_programme_id(subject_name, years, key_stage):
    """
    Build a unique programme_id from subject + years or key_stage.

    Single year  -> "PROG-Mathematics-Y1"
    Multi year (full KS) -> "PROG-Mathematics-KS1"
    Multi year (partial) -> "PROG-Mathematics-Y3-Y4"
    """
    safe_subject = subject_name.replace(" ", "")
    ks_year_map = {
        "KS1": [1, 2],
        "KS2": [3, 4, 5, 6],
        "KS3": [7, 8, 9],
        "KS4": [10, 11],
    }
    sorted_years = sorted(years) if years else []
    if len(sorted_years) == 1:
        return f"PROG-{safe_subject}-Y{sorted_years[0]}"
    # Check if the years exactly match a full key stage
    for ks, ks_years in ks_year_map.items():
        if sorted_years == ks_years:
            return f"PROG-{safe_subject}-{ks}"
    # Partial or unusual range
    year_str = "-Y".join(str(y) for y in sorted_years)
    return f"PROG-{safe_subject}-Y{year_str}"


def infer_key_stage(years):
    """Infer the key stage from a list of year group numbers."""
    if not years:
        return "Unknown"
    min_y = min(years)
    max_y = max(years)
    if max_y <= 2:
        return "KS1"
    if min_y >= 3 and max_y <= 6:
        return "KS2"
    if min_y >= 7 and max_y <= 9:
        return "KS3"
    if min_y >= 10 and max_y <= 11:
        return "KS4"
    # Spans multiple key stages - use the dominant one
    ks1_count = sum(1 for y in years if y <= 2)
    ks2_count = sum(1 for y in years if 3 <= y <= 6)
    ks3_count = sum(1 for y in years if 7 <= y <= 9)
    ks4_count = sum(1 for y in years if 10 <= y <= 11)
    counts = {"KS1": ks1_count, "KS2": ks2_count, "KS3": ks3_count, "KS4": ks4_count}
    return max(counts, key=counts.get)


_CONCEPT_TYPE_MAP = {
    # Invalid values found in extractions -> nearest valid value
    "concept":        "knowledge",   # LLM wrote the word "concept" as the type
    "language":       "knowledge",   # language concepts are declarative knowledge
    "representation": "knowledge",   # representational knowledge
}
VALID_CONCEPT_TYPES = {"knowledge", "skill", "process", "attitude", "content"}

def _normalize_concept_type(raw):
    """Map non-standard concept_type values to the nearest valid enum value."""
    if raw in VALID_CONCEPT_TYPES:
        return raw
    mapped = _CONCEPT_TYPE_MAP.get(raw)
    if mapped:
        return mapped
    print(f"    ! Unknown concept_type '{raw}' — defaulting to 'knowledge'")
    return "knowledge"


_STRUCTURE_TYPE_MAP = {
    # Invalid values found in extractions -> nearest valid value
    "skills":      "process",    # skill-oriented domains are process domains
    "analytical":  "conceptual", # analytical reasoning is conceptual
}
VALID_STRUCTURE_TYPES = {
    "sequential", "hierarchical", "mixed", "exploratory",
    "conceptual", "applied", "knowledge",
    "process", "developmental", "thematic",  # legitimate types added after review
}

def _normalize_structure_type(raw):
    """Map non-standard structure_type values to the nearest valid enum value."""
    if raw in VALID_STRUCTURE_TYPES:
        return raw
    mapped = _STRUCTURE_TYPE_MAP.get(raw)
    if mapped:
        return mapped
    print(f"    ! Unknown structure_type '{raw}' — defaulting to 'mixed'")
    return "mixed"


def normalize_concept_id(raw_id):
    """
    Normalize concept IDs: replace known underscore-prefix patterns with hyphens
    for graph consistency.
    """
    return raw_id.replace("DT_KS1_", "DT-KS1-").replace("PE_KS1_", "PE-KS1-")


def load_metadata():
    """
    Load and index metadata.json for efficient source URL lookup.

    Returns a dict keyed by (subject_name, frozenset_of_key_stages) -> document entry.
    Also returns a flat list of all subject_documents.
    """
    with open(METADATA_FILE, "r") as f:
        raw = json.load(f)

    subject_docs = raw.get("sources", {}).get("subject_documents", [])

    # Build lookup index: (subject, frozenset(key_stages)) -> doc
    lookup = {}
    for doc in subject_docs:
        subject = doc.get("subject", "")
        ks_list = doc.get("key_stages", [])
        key = (subject, frozenset(ks_list))
        lookup[key] = doc

    return lookup, subject_docs


def get_source_doc_info(metadata_lookup, subject_name, key_stage):
    """
    Look up source document information for a given (subject, key_stage) pair.

    Tries an exact key_stage match first, then falls back to any document
    that covers the requested key_stage.

    Returns a dict with source_url, publication_url, dfe_reference and doc entry,
    or empty strings/None if not found.
    """
    # Exact match
    key = (subject_name, frozenset([key_stage]))
    if key in metadata_lookup:
        doc = metadata_lookup[key]
        return {
            "source_url": doc.get("source_url", ""),
            "publication_url": doc.get("publication_page", ""),
            "dfe_reference": doc.get("reference", ""),
            "doc": doc,
        }

    # Multi-KS documents (e.g., KS1-2 documents covering both KS1 and KS2)
    for (subj, ks_set), doc in metadata_lookup.items():
        if subj == subject_name and key_stage in ks_set:
            return {
                "source_url": doc.get("source_url", ""),
                "publication_url": doc.get("publication_page", ""),
                "dfe_reference": doc.get("reference", ""),
                "doc": doc,
            }

    return {"source_url": "", "publication_url": "", "dfe_reference": "", "doc": None}


def make_document_id(doc):
    """Build a document_id string from a metadata subject_document entry."""
    subject = doc.get("subject", "Unknown").replace(" ", "")
    ks_list = doc.get("key_stages", [])
    ks_str = "-".join(ks_list)
    return f"DOC-{subject}-{ks_str}"


class CurriculumImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.metadata_lookup, self.all_subject_docs = load_metadata()
        self.stats = {
            "curricula": 0,
            "key_stages": 0,
            "years": 0,
            "subjects": 0,
            "source_documents": 0,
            "programmes": 0,
            "domains": 0,
            "objectives": 0,
            "concepts": 0,
            "prerequisites": 0,
            "appears_in_year": 0,
            "applies_to": 0,
            "has_concept": 0,
        }

    def close(self):
        self.driver.close()

    # -------------------------------------------------------------------------
    # Foundational nodes
    # -------------------------------------------------------------------------

    def create_curriculum(self, session):
        """Create the root Curriculum node."""
        query = """
        MERGE (c:Curriculum {curriculum_id: $curriculum_id})
        SET c.name = $name,
            c.country = $country
        REMOVE c.version, c.last_updated
        RETURN c
        """
        result = session.run(
            query,
            curriculum_id="uk-national-curriculum",
            name="UK National Curriculum",
            country="England",
        )
        if result.single():
            self.stats["curricula"] += 1
            print("  + Created Curriculum node")

    def create_key_stages(self, session):
        """Create KeyStage nodes and link to Curriculum."""
        key_stages = [
            {"key_stage_id": "KS1", "name": "Key Stage 1", "years": [1, 2], "age_range": "5-7"},
            {"key_stage_id": "KS2", "name": "Key Stage 2", "years": [3, 4, 5, 6], "age_range": "7-11"},
            {"key_stage_id": "KS3", "name": "Key Stage 3", "years": [7, 8, 9], "age_range": "11-14"},
            {"key_stage_id": "KS4", "name": "Key Stage 4", "years": [10, 11], "age_range": "14-16"},
        ]

        query = """
        MATCH (c:Curriculum {curriculum_id: 'uk-national-curriculum'})
        MERGE (ks:KeyStage {key_stage_id: $key_stage_id})
        SET ks.name = $name,
            ks.years = $years,
            ks.age_range = $age_range
        MERGE (c)-[:HAS_KEY_STAGE]->(ks)
        RETURN ks
        """

        for ks in key_stages:
            result = session.run(query, **ks)
            if result.single():
                self.stats["key_stages"] += 1
                print(f"  + Created KeyStage: {ks['key_stage_id']}")

    def create_years(self, session):
        """Create Year nodes and link to KeyStages."""
        years_data = [
            # KS1
            {"year_id": "Y1", "year_number": 1, "age_range": "5-6", "key_stage": "KS1"},
            {"year_id": "Y2", "year_number": 2, "age_range": "6-7", "key_stage": "KS1"},
            # KS2
            {"year_id": "Y3", "year_number": 3, "age_range": "7-8", "key_stage": "KS2"},
            {"year_id": "Y4", "year_number": 4, "age_range": "8-9", "key_stage": "KS2"},
            {"year_id": "Y5", "year_number": 5, "age_range": "9-10", "key_stage": "KS2"},
            {"year_id": "Y6", "year_number": 6, "age_range": "10-11", "key_stage": "KS2"},
            # KS3
            {"year_id": "Y7", "year_number": 7, "age_range": "11-12", "key_stage": "KS3"},
            {"year_id": "Y8", "year_number": 8, "age_range": "12-13", "key_stage": "KS3"},
            {"year_id": "Y9", "year_number": 9, "age_range": "13-14", "key_stage": "KS3"},
            # KS4
            {"year_id": "Y10", "year_number": 10, "age_range": "14-15", "key_stage": "KS4"},
            {"year_id": "Y11", "year_number": 11, "age_range": "15-16", "key_stage": "KS4"},
        ]

        query = """
        MATCH (ks:KeyStage {key_stage_id: $key_stage})
        MERGE (y:Year {year_id: $year_id})
        SET y.year_number = $year_number,
            y.age_range = $age_range,
            y.key_stage = $key_stage
        MERGE (ks)-[:HAS_YEAR]->(y)
        RETURN y
        """

        for year in years_data:
            result = session.run(query, **year)
            if result.single():
                self.stats["years"] += 1

        print(f"  + Created {self.stats['years']} Year nodes")

    # -------------------------------------------------------------------------
    # SourceDocument nodes
    # -------------------------------------------------------------------------

    def create_source_documents(self, session):
        """
        Create SourceDocument nodes from metadata.json and link them to
        the root Curriculum node via HAS_DOCUMENT.
        """
        query = """
        MATCH (c:Curriculum {curriculum_id: 'uk-national-curriculum'})
        MERGE (sd:SourceDocument {document_id: $document_id})
        SET sd.title = $title,
            sd.subject = $subject,
            sd.key_stages = $key_stages,
            sd.url = $url,
            sd.publication_page = $publication_page,
            sd.dfe_reference = $dfe_reference,
            sd.published = $published,
            sd.last_updated = $last_updated,
            sd.pages = $pages,
            sd.local_file = $local_file
        MERGE (c)-[:HAS_DOCUMENT]->(sd)
        RETURN sd
        """

        for doc in self.all_subject_docs:
            document_id = make_document_id(doc)
            subject = doc.get("subject", "")
            ks_list = doc.get("key_stages", [])

            # Derive a human-readable title
            ks_str = "/".join(ks_list)
            title = f"{subject} ({ks_str}) - National Curriculum Programme of Study"

            result = session.run(
                query,
                document_id=document_id,
                title=title,
                subject=subject,
                key_stages=ks_list,
                url=doc.get("source_url", ""),
                publication_page=doc.get("publication_page", ""),
                dfe_reference=doc.get("reference", ""),
                published=doc.get("published", ""),
                last_updated=doc.get("last_updated", ""),
                pages=doc.get("pages", 0),
                local_file=doc.get("local_file", ""),
            )

            if result.single():
                self.stats["source_documents"] += 1

        print(f"  + Created {self.stats['source_documents']} SourceDocument nodes")

    # -------------------------------------------------------------------------
    # Main subject import (Programme-based model)
    # -------------------------------------------------------------------------

    def import_subject(self, session, data):
        """Import a single subject extraction using the v3.0 Programme model."""
        metadata = data.get("metadata", {})
        subject_name = metadata.get("subject", "Unknown")

        # ---- Resolve key_stage and years_covered ----------------------------
        raw_key_stage = metadata.get("key_stage") or ""
        raw_key_stages = metadata.get("key_stages", [])

        years_covered = coerce_years(
            metadata.get("years_covered") or metadata.get("year_groups", [])
        )
        if not years_covered:
            if raw_key_stage == "KS1":
                years_covered = [1, 2]
            elif raw_key_stage == "KS2":
                years_covered = [3, 4, 5, 6]
            elif raw_key_stage == "KS3":
                years_covered = [7, 8, 9]
            elif raw_key_stage == "KS4":
                years_covered = [10, 11]
            else:
                for ks in raw_key_stages:
                    if ks == "KS1":
                        years_covered += [1, 2]
                    elif ks == "KS2":
                        years_covered += [3, 4, 5, 6]
                    elif ks == "KS3":
                        years_covered += [7, 8, 9]
                    elif ks == "KS4":
                        years_covered += [10, 11]
                years_covered = sorted(set(years_covered))

        # Determine canonical key_stage for this extraction file
        if raw_key_stage:
            key_stage = raw_key_stage
        elif raw_key_stages:
            key_stage = raw_key_stages[0]
        else:
            key_stage = infer_key_stage(years_covered)

        programme_id = make_programme_id(subject_name, years_covered, key_stage)
        is_core = subject_name in CORE_SUBJECTS

        print(f"\n  Importing: {subject_name} {key_stage} -> {programme_id}")

        # ---- Source document lookup -----------------------------------------
        src = get_source_doc_info(self.metadata_lookup, subject_name, key_stage)
        source_url = src["source_url"]
        publication_url = src["publication_url"]
        dfe_reference = src["dfe_reference"] or metadata.get("document_reference", "")
        src_doc = src["doc"]

        # ---- A. Subject node (master, subject_id = plain subject name) ------
        key_stages_covered = sorted(set(
            raw_key_stages if raw_key_stages else ([key_stage] if key_stage else [])
        ))

        subject_query = """
        MERGE (s:Subject {subject_id: $subject_id})
        SET s.name = $name,
            s.description = $description,
            s.is_core_subject = $is_core_subject,
            s.statutory = $statutory,
            s.key_stages_covered = $key_stages_covered,
            s.subject_type = $subject_type
        RETURN s
        """
        result = session.run(
            subject_query,
            subject_id=subject_name,
            name=subject_name,
            description="",
            is_core_subject=is_core,
            statutory=True,
            key_stages_covered=key_stages_covered,
            subject_type="core" if is_core else "foundation",
        )
        if result.single():
            self.stats["subjects"] += 1
            print(f"    + Subject node: {subject_name}")

        # ---- B. Programme node (Subject × Year instantiation) ---------------
        age_range = years_to_age_range(years_covered) if years_covered else "unknown"

        programme_query = """
        MERGE (p:Programme {programme_id: $programme_id})
        SET p.name = $name,
            p.subject_name = $subject_name,
            p.years = $years,
            p.key_stage = $key_stage,
            p.age_range = $age_range,
            p.is_core_subject = $is_core_subject,
            p.structure_rating = $structure_rating,
            p.extraction_date = $extraction_date,
            p.source_url = $source_url,
            p.publication_url = $publication_url,
            p.dfe_reference = $dfe_reference,
            p.curriculum_name = $curriculum_name
        RETURN p
        """

        years_label = (
            f"Year {years_covered[0]}"
            if len(years_covered) == 1
            else f"{key_stage}"
        )
        result = session.run(
            programme_query,
            programme_id=programme_id,
            name=f"{subject_name} {years_label}",
            subject_name=subject_name,
            years=sorted(years_covered),
            key_stage=key_stage,
            age_range=age_range,
            is_core_subject=is_core,
            structure_rating=metadata.get("structure_rating", 0),
            extraction_date=metadata.get("extraction_date", "2026-02-16"),
            source_url=source_url,
            publication_url=publication_url,
            dfe_reference=dfe_reference,
            curriculum_name="UK National Curriculum 2014",
        )
        if result.single():
            self.stats["programmes"] += 1
            print(f"    + Programme node: {programme_id}")

        # Link Programme -> Subject
        session.run(
            """
            MATCH (p:Programme {programme_id: $programme_id})
            MATCH (s:Subject {subject_id: $subject_id})
            MERGE (p)-[:FOR_SUBJECT]->(s)
            """,
            programme_id=programme_id,
            subject_id=subject_name,
        )

        # Link Programme -> SourceDocument
        if src_doc:
            document_id = make_document_id(src_doc)
            session.run(
                """
                MATCH (p:Programme {programme_id: $programme_id})
                MATCH (sd:SourceDocument {document_id: $document_id})
                MERGE (p)-[:SOURCED_FROM]->(sd)
                """,
                programme_id=programme_id,
                document_id=document_id,
            )

        # Link Year -> Programme (for every year this programme covers)
        for year_num in years_covered:
            session.run(
                """
                MATCH (y:Year {year_number: $year_number})
                MATCH (p:Programme {programme_id: $programme_id})
                MERGE (y)-[:HAS_PROGRAMME]->(p)
                """,
                year_number=year_num,
                programme_id=programme_id,
            )

        # ---- C. Domain nodes (Programme -[HAS_DOMAIN]-> Domain) -------------
        # Build domain name lookup for objective source_reference
        domain_name_lookup = {
            d.get("domain_id", ""): (d.get("domain_name") or d.get("name") or d.get("domain_id", ""))
            for d in data.get("domains", [])
        }

        for domain in data.get("domains", []):
            domain_name = (
                domain.get("domain_name")
                or domain.get("name")
                or domain.get("domain_id")
            )

            domain_query = """
            MATCH (p:Programme {programme_id: $programme_id})
            MERGE (d:Domain {domain_id: $domain_id})
            SET d.domain_name = $domain_name,
                d.description = $description,
                d.curriculum_context = $curriculum_context,
                d.is_cross_cutting = $is_cross_cutting,
                d.structure_type = $structure_type,
                d.source_reference = $source_reference
            MERGE (p)-[:HAS_DOMAIN]->(d)
            RETURN d
            """

            result = session.run(
                domain_query,
                programme_id=programme_id,
                domain_id=domain["domain_id"],
                domain_name=domain_name,
                description=domain.get("description", ""),
                curriculum_context=domain.get("curriculum_context", ""),
                is_cross_cutting=domain.get("is_cross_cutting", False),
                structure_type=_normalize_structure_type(domain.get("structure_type", "mixed")),
                source_reference=f"National Curriculum 2014, {dfe_reference} — {subject_name} {key_stage} Programme of Study: {domain_name}",
            )

            if result.single():
                self.stats["domains"] += 1

        print(f"    + {len(data.get('domains', []))} domains")

        # ---- D. Objective nodes (enhanced with key_stage and year_groups) ---
        for objective in data.get("objectives", []):
            obj_text = (objective.get("objective_text")
                        or objective.get("statement")
                        or objective.get("text")  # some extractions use "text" key
                        or "")
            is_stat = objective.get("is_statutory")
            if is_stat is None:
                is_stat = objective.get("statutory", True)

            domain_name_for_obj = domain_name_lookup.get(objective.get("domain_id", ""), "")
            statutory_label = "Statutory Requirement" if is_stat else "Non-statutory Guidance"
            obj_source_reference = f"National Curriculum 2014, {dfe_reference} — {subject_name} {key_stage} Programme of Study: {domain_name_for_obj} [{statutory_label}]"

            obj_query = """
            MATCH (d:Domain {domain_id: $domain_id})
            MERGE (o:Objective {objective_id: $objective_id})
            SET o.objective_text = $objective_text,
                o.non_statutory_guidance = $non_statutory_guidance,
                o.examples = $examples,
                o.is_statutory = $is_statutory,
                o.source_reference = $source_reference
            MERGE (d)-[:CONTAINS]->(o)
            RETURN o
            """

            result = session.run(
                obj_query,
                domain_id=objective.get("domain_id", ""),
                objective_id=objective["objective_id"],
                objective_text=obj_text,
                non_statutory_guidance=objective.get("non_statutory_guidance", ""),
                examples=objective.get("examples", ""),
                is_statutory=is_stat,
                source_reference=obj_source_reference,
            )

            if result.single():
                self.stats["objectives"] += 1

        print(f"    + {len(data.get('objectives', []))} objectives")

        # ---- E. Concept nodes (enhanced with source traceability) -----------
        year_introduced = min(years_covered) if years_covered else None

        for concept in data.get("concepts", []):
            concept_name = (
                concept.get("concept_name")
                or concept.get("name")
                or concept.get("label")
                or concept.get("concept_id")
            )
            description = concept.get("description") or concept.get("definition", "")

            raw_id = concept["concept_id"]
            normalized_id = normalize_concept_id(raw_id)

            # Normalize concept_type to valid enum values
            raw_concept_type = concept["concept_type"]
            concept_type = _normalize_concept_type(raw_concept_type)

            concept_query = """
            MERGE (c:Concept {concept_id: $concept_id})
            SET c.concept_name = $concept_name,
                c.description = $description,
                c.teaching_guidance = $teaching_guidance,
                c.key_vocabulary = $key_vocabulary,
                c.common_misconceptions = $common_misconceptions,
                c.concept_type = $concept_type,
                c.complexity_level = $complexity_level,
                c.is_cross_cutting = $is_cross_cutting,
                c.source_reference = $source_reference
            RETURN c
            """

            result = session.run(
                concept_query,
                concept_id=normalized_id,
                concept_name=concept_name,
                description=description,
                teaching_guidance=concept.get("teaching_guidance", ""),
                key_vocabulary=concept.get("key_vocabulary", ""),
                common_misconceptions=concept.get("common_misconceptions", ""),
                concept_type=concept_type,
                complexity_level=concept["complexity_level"],
                is_cross_cutting=concept.get("is_cross_cutting", False),
                source_reference=f"National Curriculum 2014, {dfe_reference} — {subject_name} {key_stage} Programme of Study",
            )

            if result.single():
                self.stats["concepts"] += 1

            # Link Programme -> Concept (so concepts are reachable from the hierarchy)
            session.run(
                """
                MATCH (p:Programme {programme_id: $programme_id})
                MATCH (c:Concept {concept_id: $concept_id})
                MERGE (p)-[:HAS_CONCEPT]->(c)
                """,
                programme_id=programme_id,
                concept_id=normalized_id,
            )

            # Link Domain -> Concept (using domain_id on the concept)
            concept_domain_id = concept.get("domain_id")
            if concept_domain_id:
                session.run(
                    """
                    MATCH (d:Domain {domain_id: $domain_id})
                    MATCH (c:Concept {concept_id: $concept_id})
                    MERGE (d)-[:HAS_CONCEPT]->(c)
                    """,
                    domain_id=concept_domain_id,
                    concept_id=normalized_id,
                )

            # Link Concept -> SourceDocument
            if src_doc:
                document_id = make_document_id(src_doc)
                session.run(
                    """
                    MATCH (c:Concept {concept_id: $concept_id})
                    MATCH (sd:SourceDocument {document_id: $document_id})
                    MERGE (c)-[:SOURCED_FROM]->(sd)
                    """,
                    concept_id=normalized_id,
                    document_id=document_id,
                )

        print(f"    + {len(data.get('concepts', []))} concepts")

        # ---- F. Prerequisite relationships ----------------------------------
        prereq_list = (
            data.get("prerequisite_relationships")
            or data.get("prerequisites")
            or data.get("prerequisite_relations", [])
        )

        for prereq in prereq_list:
            prerequisite_id = prereq.get("prerequisite_concept") or prereq.get("source_concept_id")
            dependent_id = prereq.get("dependent_concept") or prereq.get("target_concept_id")

            if prerequisite_id:
                prerequisite_id = normalize_concept_id(prerequisite_id)
            if dependent_id:
                dependent_id = normalize_concept_id(dependent_id)

            if not (prerequisite_id and dependent_id):
                continue

            prereq_query = """
            MATCH (c1:Concept {concept_id: $prerequisite})
            MATCH (c2:Concept {concept_id: $dependent})
            MERGE (c1)-[r:PREREQUISITE_OF]->(c2)
            SET r.confidence = $confidence,
                r.relationship_type = $relationship_type,
                r.strength = $strength,
                r.rationale = $rationale
            RETURN r
            """

            result = session.run(
                prereq_query,
                prerequisite=prerequisite_id,
                dependent=dependent_id,
                confidence=prereq.get("confidence", "inferred"),
                relationship_type=prereq.get("relationship_type", "developmental"),
                strength=prereq.get("strength", 0.5),
                rationale=prereq.get("rationale", ""),
            )

            if result.single():
                self.stats["prerequisites"] += 1

        print(f"    + {len(prereq_list)} prerequisites")

    # -------------------------------------------------------------------------
    # Main entry point
    # -------------------------------------------------------------------------

    def import_all_extractions(self):
        """Import all JSON files from extractions directory."""
        print("\n" + "=" * 60)
        print("IMPORTING CURRICULUM DATA (v3.0 - Programme model)")
        print("=" * 60)

        with self.driver.session() as session:
            # Create foundational / structural nodes
            print("\nCreating foundational nodes...")
            self.create_curriculum(session)
            self.create_key_stages(session)
            self.create_years(session)

            # Create SourceDocument nodes from metadata.json
            print("\nCreating SourceDocument nodes from metadata.json...")
            self.create_source_documents(session)

            # Import subjects / programmes from extraction files
            print("\nImporting subjects (creating Programme nodes)...")

            for subdir in ["primary", "secondary"]:
                extraction_path = EXTRACTIONS_DIR / subdir
                if not extraction_path.exists():
                    print(f"  ! Directory not found: {extraction_path}")
                    continue

                for json_file in sorted(extraction_path.glob("*.json")):
                    try:
                        with open(json_file, "r") as f:
                            data = json.load(f)
                        self.import_subject(session, data)
                    except Exception as e:
                        print(f"  ! Error importing {json_file.name}: {e}")

        # Print summary
        print("\n" + "=" * 60)
        print("IMPORT SUMMARY")
        print("=" * 60)
        for key, value in self.stats.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        print("=" * 60)


def main():
    """Main execution."""
    print("UK Curriculum Knowledge Graph - Data Importer (v3.0)")
    print(f"Extractions directory: {EXTRACTIONS_DIR}")
    print(f"Metadata file:        {METADATA_FILE}")

    importer = CurriculumImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        importer.import_all_extractions()
    except Exception as e:
        print(f"\nImport failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        importer.close()

    print("\nImport complete!")


if __name__ == "__main__":
    main()

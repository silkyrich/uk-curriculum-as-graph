#!/usr/bin/env python3
"""
Import EYFS (Early Years Foundation Stage) into Neo4j.

Graph structure mirrors the UK Curriculum model (Option A):
  Curriculum -[HAS_KEY_STAGE]-> KeyStage{EYFS} -[HAS_YEAR]-> Year{EYFS}
  Year{EYFS} -[PRECEDES]-> Year{Y1}
  Year{EYFS} -[HAS_PROGRAMME]-> Programme -[FOR_SUBJECT]-> Subject
  Programme -[HAS_DOMAIN]-> Domain -[CONTAINS]-> Objective -[TEACHES]-> Concept
  Concept -[PREREQUISITE_OF]-> Concept  (includes EYFS→KS1 cross-stage links)

Loads 7 extraction JSON files from layers/eyfs/data/extractions/

Usage:
  python3 layers/eyfs/scripts/import_eyfs.py
  python3 layers/eyfs/scripts/import_eyfs.py --clear   # delete EYFS nodes first
"""

import json
import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / "core" / "scripts"))

from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

EXTRACTIONS_DIR = PROJECT_ROOT / "layers" / "eyfs" / "data" / "extractions"

CORE_SUBJECTS = {"Mathematics", "English", "Science"}

VALID_CONCEPT_TYPES = {
    "declarative", "procedural", "conceptual", "process", "skill", "social",
}


def _normalize_concept_type(raw):
    if not raw:
        return "declarative"
    norm = raw.lower().strip()
    if norm in VALID_CONCEPT_TYPES:
        return norm
    # Common aliases
    if norm in ("knowledge", "fact"):
        return "declarative"
    if norm in ("technique", "method"):
        return "procedural"
    if norm in ("idea", "principle", "concept"):
        return "conceptual"
    return "declarative"


class EYFSImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            "key_stages": 0,
            "years": 0,
            "subjects": 0,
            "programmes": 0,
            "domains": 0,
            "objectives": 0,
            "concepts": 0,
            "prerequisites": 0,
        }

    def close(self):
        self.driver.close()

    # -------------------------------------------------------------------------
    # Structural setup
    # -------------------------------------------------------------------------

    def create_eyfs_structure(self, session):
        """Create EYFS KeyStage, Year node, and PRECEDES link to Y1."""

        # EYFS KeyStage — linked to existing Curriculum root
        session.run("""
            MATCH (c:Curriculum {curriculum_id: 'uk-national-curriculum'})
            MERGE (ks:KeyStage {key_stage_id: 'EYFS'})
            SET ks.name         = 'Early Years Foundation Stage',
                ks.years        = [0],
                ks.age_range    = '4-5',
                ks.display_category = 'UK Curriculum',
                ks.display_color    = '#D97706',
                ks.display_icon     = 'child_care',
                ks.name             = 'Early Years Foundation Stage'
            MERGE (c)-[:HAS_KEY_STAGE]->(ks)
        """)
        self.stats["key_stages"] += 1
        print("  + KeyStage: EYFS")

        # EYFS Year node (year_number: 0 = Reception, before Y1)
        session.run("""
            MATCH (ks:KeyStage {key_stage_id: 'EYFS'})
            MERGE (y:Year {year_id: 'EYFS'})
            SET y.year_number   = 0,
                y.age_range     = '4-5',
                y.key_stage     = 'EYFS',
                y.name          = 'Reception',
                y.display_category = 'UK Curriculum',
                y.display_color    = '#D97706',
                y.display_icon     = 'child_care'
            MERGE (ks)-[:HAS_YEAR]->(y)
        """)
        self.stats["years"] += 1
        print("  + Year: EYFS (Reception, year_number: 0)")

        # EYFS Year PRECEDES Y1
        session.run("""
            MATCH (eyfs:Year {year_id: 'EYFS'})
            MATCH (y1:Year {year_id: 'Y1'})
            MERGE (eyfs)-[:PRECEDES]->(y1)
        """)
        print("  + EYFS -[PRECEDES]-> Y1")

    # -------------------------------------------------------------------------
    # Clear (optional)
    # -------------------------------------------------------------------------

    def clear_eyfs_nodes(self, session):
        """Remove all EYFS nodes and relationships. Use before re-import."""
        print("\nClearing EYFS nodes...")

        # Delete concepts with EY/CL/PSED/PD/LIT/EYMA/UW/EAD prefixes
        result = session.run("""
            MATCH (c:Concept)
            WHERE c.concept_id STARTS WITH 'EY'
               OR c.concept_id STARTS WITH 'CL-R-'
               OR c.concept_id STARTS WITH 'PSED-R-'
               OR c.concept_id STARTS WITH 'PD-R-'
               OR c.concept_id STARTS WITH 'LIT-R-'
               OR c.concept_id STARTS WITH 'EYMA-R-'
               OR c.concept_id STARTS WITH 'UW-R-'
               OR c.concept_id STARTS WITH 'EAD-R-'
            DETACH DELETE c
            RETURN count(c) as deleted
        """)
        rec = result.single()
        print(f"  Deleted {rec['deleted'] if rec else 0} EYFS Concept nodes")

        # Delete objectives, domains, programmes, subjects for EYFS
        session.run("""
            MATCH (o:Objective)
            WHERE o.objective_id STARTS WITH 'CL-R-'
               OR o.objective_id STARTS WITH 'PSED-R-'
               OR o.objective_id STARTS WITH 'PD-R-'
               OR o.objective_id STARTS WITH 'LIT-R-'
               OR o.objective_id STARTS WITH 'EYMA-R-'
               OR o.objective_id STARTS WITH 'UW-R-'
               OR o.objective_id STARTS WITH 'EAD-R-'
            DETACH DELETE o
        """)

        session.run("""
            MATCH (d:Domain)
            WHERE d.domain_id STARTS WITH 'CL-R-'
               OR d.domain_id STARTS WITH 'PSED-R-'
               OR d.domain_id STARTS WITH 'PD-R-'
               OR d.domain_id STARTS WITH 'LIT-R-'
               OR d.domain_id STARTS WITH 'EYMA-R-'
               OR d.domain_id STARTS WITH 'UW-R-'
               OR d.domain_id STARTS WITH 'EAD-R-'
            DETACH DELETE d
        """)

        session.run("""
            MATCH (p:Programme {key_stage: 'EYFS'})
            DETACH DELETE p
        """)

        # Remove EYFS-specific subjects (only those with no non-EYFS programmes)
        session.run("""
            MATCH (s:Subject)
            WHERE s.subject_id IN [
              'Communication and Language',
              'Personal, Social and Emotional Development',
              'Physical Development',
              'Literacy',
              'Understanding the World',
              'Expressive Arts and Design'
            ]
            AND NOT EXISTS {
              MATCH (s)<-[:FOR_SUBJECT]-(p:Programme)
              WHERE p.key_stage <> 'EYFS'
            }
            DETACH DELETE s
        """)

        session.run("""
            MATCH (y:Year {year_id: 'EYFS'}) DETACH DELETE y
        """)
        session.run("""
            MATCH (ks:KeyStage {key_stage_id: 'EYFS'}) DETACH DELETE ks
        """)
        print("  EYFS nodes cleared.")

    # -------------------------------------------------------------------------
    # Per-extraction import (Pass 1 — nodes)
    # -------------------------------------------------------------------------

    def import_extraction(self, session, data):
        """Import a single EYFS extraction file (nodes only, no prerequisites)."""
        metadata = data.get("metadata", {})
        subject_name = metadata.get("subject", "Unknown")
        key_stage = "EYFS"
        dfe_reference = metadata.get("document_reference", "DfE EYFS Statutory Framework 2024")
        structure_rating = metadata.get("structure_rating", 7)
        extraction_date = metadata.get("extraction_date", "2026-02-22")
        is_core = subject_name in CORE_SUBJECTS

        programme_id = f"PROG-{subject_name.replace(' ', '')}-EYFS"

        print(f"\n  Importing: {subject_name} → {programme_id}")

        # ---- Subject node ----
        session.run("""
            MERGE (s:Subject {subject_id: $subject_id})
            SET s.name                = $name,
                s.description         = $description,
                s.is_core_subject     = $is_core,
                s.statutory           = true,
                s.key_stages_covered  = ['EYFS'],
                s.subject_type        = $subject_type,
                s.area_type           = $area_type,
                s.display_category    = 'UK Curriculum',
                s.display_color       = '#D97706',
                s.display_icon        = 'child_care'
        """,
            subject_id=subject_name,
            name=subject_name,
            description=metadata.get("notes", ""),
            is_core=is_core,
            subject_type="core" if is_core else "foundation",
            area_type=metadata.get("area_type", "specific"),
        )
        self.stats["subjects"] += 1

        # ---- Programme node ----
        session.run("""
            MERGE (p:Programme {programme_id: $programme_id})
            SET p.name             = $name,
                p.subject_name     = $subject_name,
                p.years            = [0],
                p.key_stage        = 'EYFS',
                p.age_range        = '4-5',
                p.is_core_subject  = $is_core,
                p.structure_rating = $structure_rating,
                p.extraction_date  = $extraction_date,
                p.dfe_reference    = $dfe_reference,
                p.curriculum_name  = 'EYFS Statutory Framework 2024',
                p.display_category = 'UK Curriculum',
                p.display_color    = '#D97706',
                p.display_icon     = 'child_care',
                p.name             = $name
        """,
            programme_id=programme_id,
            name=f"{subject_name} Reception",
            subject_name=subject_name,
            is_core=is_core,
            structure_rating=structure_rating,
            extraction_date=extraction_date,
            dfe_reference=dfe_reference,
        )
        self.stats["programmes"] += 1

        # Programme -> Subject
        session.run("""
            MATCH (p:Programme {programme_id: $programme_id})
            MATCH (s:Subject {subject_id: $subject_id})
            MERGE (p)-[:FOR_SUBJECT]->(s)
        """, programme_id=programme_id, subject_id=subject_name)

        # EYFS Year -> Programme
        session.run("""
            MATCH (y:Year {year_id: 'EYFS'})
            MATCH (p:Programme {programme_id: $programme_id})
            MERGE (y)-[:HAS_PROGRAMME]->(p)
        """, programme_id=programme_id)
        print(f"    + Programme: {programme_id}")

        # ---- Domain nodes ----
        for domain in data.get("domains", []):
            domain_name = (
                domain.get("domain_name") or domain.get("name") or domain.get("domain_id")
            )
            session.run("""
                MATCH (p:Programme {programme_id: $programme_id})
                MERGE (d:Domain {domain_id: $domain_id})
                SET d.domain_name       = $domain_name,
                    d.description       = $description,
                    d.curriculum_context= $curriculum_context,
                    d.is_cross_cutting  = $is_cross_cutting,
                    d.structure_type    = $structure_type,
                    d.source_reference  = $source_reference,
                    d.display_category  = 'UK Curriculum',
                    d.display_color     = '#D97706',
                    d.display_icon      = 'child_care',
                    d.name              = $domain_name
                MERGE (p)-[:HAS_DOMAIN]->(d)
            """,
                programme_id=programme_id,
                domain_id=domain["domain_id"],
                domain_name=domain_name,
                description=domain.get("description", ""),
                curriculum_context=domain.get("curriculum_context", ""),
                is_cross_cutting=domain.get("is_cross_cutting", False),
                structure_type=domain.get("structure_type", "hierarchical"),
                source_reference=f"EYFS Statutory Framework 2024 — {subject_name}: {domain_name}",
            )
            self.stats["domains"] += 1

        print(f"    + {len(data.get('domains', []))} domains")

        # ---- Objective nodes ----
        for objective in data.get("objectives", []):
            obj_text = (
                objective.get("objective_text")
                or objective.get("statement")
                or objective.get("text", "")
            )
            session.run("""
                MATCH (d:Domain {domain_id: $domain_id})
                MERGE (o:Objective {objective_id: $objective_id})
                SET o.objective_text          = $objective_text,
                    o.non_statutory_guidance  = $non_statutory_guidance,
                    o.examples                = $examples,
                    o.is_statutory            = $is_statutory,
                    o.source_reference        = $source_reference,
                    o.display_category        = 'UK Curriculum',
                    o.name                    = $objective_text
                MERGE (d)-[:CONTAINS]->(o)
            """,
                domain_id=objective.get("domain_id", ""),
                objective_id=objective["objective_id"],
                objective_text=obj_text,
                non_statutory_guidance=objective.get("non_statutory_guidance", ""),
                examples=objective.get("examples", ""),
                is_statutory=objective.get("is_statutory", True),
                source_reference=f"EYFS Statutory Framework 2024 — {subject_name}",
            )
            self.stats["objectives"] += 1

        print(f"    + {len(data.get('objectives', []))} objectives")

        # ---- Concept nodes ----
        for concept in data.get("concepts", []):
            concept_name = (
                concept.get("concept_name")
                or concept.get("name")
                or concept.get("concept_id")
            )
            concept_type = _normalize_concept_type(concept.get("concept_type", "declarative"))

            session.run("""
                MERGE (c:Concept {concept_id: $concept_id})
                SET c.concept_name         = $concept_name,
                    c.description          = $description,
                    c.teaching_guidance    = $teaching_guidance,
                    c.key_vocabulary       = $key_vocabulary,
                    c.common_misconceptions= $common_misconceptions,
                    c.concept_type         = $concept_type,
                    c.complexity_level     = $complexity_level,
                    c.is_cross_cutting     = $is_cross_cutting,
                    c.teaching_weight      = $teaching_weight,
                    c.co_teach_hints       = $co_teach_hints,
                    c.source_reference     = $source_reference,
                    c.display_category     = 'UK Curriculum',
                    c.display_color        = '#D97706',
                    c.display_icon         = 'child_care',
                    c.name                 = $concept_name
            """,
                concept_id=concept["concept_id"],
                concept_name=concept_name,
                description=concept.get("description", ""),
                teaching_guidance=concept.get("teaching_guidance", ""),
                key_vocabulary=concept.get("key_vocabulary", ""),
                common_misconceptions=concept.get("common_misconceptions", ""),
                concept_type=concept_type,
                complexity_level=concept.get("complexity_level", 1),
                is_cross_cutting=concept.get("is_cross_cutting", False),
                teaching_weight=concept.get("teaching_weight", 1),
                co_teach_hints=concept.get("co_teach_hints", []),
                source_reference=f"EYFS Statutory Framework 2024 — {subject_name}",
            )
            self.stats["concepts"] += 1

            # Domain -> Concept
            if concept.get("domain_id"):
                session.run("""
                    MATCH (d:Domain {domain_id: $domain_id})
                    MATCH (c:Concept {concept_id: $concept_id})
                    MERGE (d)-[:HAS_CONCEPT]->(c)
                """, domain_id=concept["domain_id"], concept_id=concept["concept_id"])

            # Programme -> Concept
            session.run("""
                MATCH (p:Programme {programme_id: $programme_id})
                MATCH (c:Concept {concept_id: $concept_id})
                MERGE (p)-[:HAS_CONCEPT]->(c)
            """, programme_id=programme_id, concept_id=concept["concept_id"])

        print(f"    + {len(data.get('concepts', []))} concepts")

    # -------------------------------------------------------------------------
    # Pass 2 — prerequisites
    # -------------------------------------------------------------------------

    def import_prerequisites(self, session, data):
        """Second pass — create PREREQUISITE_OF relationships (incl. cross-stage EYFS→KS1)."""
        prereq_list = (
            data.get("prerequisite_relationships")
            or data.get("prerequisites")
            or []
        )

        created = 0
        for prereq in prereq_list:
            src_id = prereq.get("prerequisite_concept") or prereq.get("source_concept_id")
            dep_id = prereq.get("dependent_concept") or prereq.get("target_concept_id")

            if not (src_id and dep_id):
                continue

            result = session.run("""
                MATCH (c1:Concept {concept_id: $src})
                MATCH (c2:Concept {concept_id: $dep})
                MERGE (c1)-[r:PREREQUISITE_OF]->(c2)
                SET r.confidence        = $confidence,
                    r.relationship_type = $relationship_type,
                    r.strength          = $strength,
                    r.rationale         = $rationale
                RETURN r
            """,
                src=src_id,
                dep=dep_id,
                confidence=prereq.get("confidence", "curated"),
                relationship_type=prereq.get("relationship_type", "developmental"),
                strength=prereq.get("strength", 0.8),
                rationale=prereq.get("rationale", ""),
            )

            if result.single():
                self.stats["prerequisites"] += 1
                created += 1

        return created

    # -------------------------------------------------------------------------
    # Main entry point
    # -------------------------------------------------------------------------

    def run(self, clear=False):
        print("=" * 60)
        print("EYFS Import")
        print("=" * 60)

        extraction_files = sorted(EXTRACTIONS_DIR.glob("*_EYFS_extracted.json"))
        if not extraction_files:
            print(f"\nNo EYFS extraction files found in {EXTRACTIONS_DIR}")
            print("Expected pattern: *_EYFS_extracted.json")
            sys.exit(1)

        print(f"\nFound {len(extraction_files)} extraction files:")
        for f in extraction_files:
            print(f"  {f.name}")

        # Load all data first
        all_data = []
        for path in extraction_files:
            with open(path) as f:
                all_data.append(json.load(f))

        with self.driver.session() as session:
            if clear:
                self.clear_eyfs_nodes(session)

            print("\nCreating EYFS structural nodes...")
            self.create_eyfs_structure(session)

            print("\n── Pass 1: Nodes ──")
            for data in all_data:
                self.import_extraction(session, data)

            print("\n── Pass 2: Prerequisites ──")
            total_prereqs = 0
            for data in all_data:
                prereq_list = data.get("prerequisite_relationships") or data.get("prerequisites") or []
                if prereq_list:
                    created = self.import_prerequisites(session, data)
                    subject = data.get("metadata", {}).get("subject", "?")
                    cross_stage = sum(
                        1 for p in prereq_list
                        if not (
                            (p.get("prerequisite_concept", "") or "").startswith(
                                ("CL-R-", "PSED-R-", "PD-R-", "LIT-R-", "EYMA-R-", "UW-R-", "EAD-R-")
                            )
                            and (p.get("dependent_concept", "") or "").startswith(
                                ("CL-R-", "PSED-R-", "PD-R-", "LIT-R-", "EYMA-R-", "UW-R-", "EAD-R-")
                            )
                        )
                    )
                    print(f"  {subject}: {created} prereqs ({cross_stage} cross-stage EYFS→KS1)")
                    total_prereqs += created

        print("\n" + "=" * 60)
        print("EYFS Import Summary")
        print("=" * 60)
        for k, v in self.stats.items():
            if v:
                print(f"  {k}: {v}")
        print(f"\n✅ Done. {total_prereqs} prerequisite relationships created.")


def main():
    parser = argparse.ArgumentParser(description="Import EYFS into Neo4j")
    parser.add_argument("--clear", action="store_true",
                        help="Delete existing EYFS nodes before importing")
    args = parser.parse_args()

    importer = EYFSImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
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

#!/usr/bin/env python3
"""
Import DeliveryMode and TeachingRequirement nodes, then link Concepts via
DELIVERABLE_VIA and HAS_TEACHING_REQUIREMENT relationships.

Creates:
  :DeliveryMode nodes (4) — the four delivery channels
  :TeachingRequirement nodes (15) — atomic pedagogical requirements
  (:Concept)-[:DELIVERABLE_VIA {primary, confidence, rationale}]->(:DeliveryMode)
  (:Concept)-[:HAS_TEACHING_REQUIREMENT]->(:TeachingRequirement)
  (:TeachingRequirement)-[:IMPLIES_MINIMUM_MODE]->(:DeliveryMode)

Idempotent: uses MERGE on node IDs so it's safe to rerun.

Usage:
  python3 layers/uk-curriculum/scripts/import_delivery_modes.py
  python3 layers/uk-curriculum/scripts/import_delivery_modes.py --clear
"""

import json
import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / "core" / "scripts"))

from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

DATA_DIR = PROJECT_ROOT / "layers" / "uk-curriculum" / "data" / "delivery_modes"
DEFINITIONS_DIR = DATA_DIR  # definitions live alongside the per-subject files

VALID_MODES = {"ai_direct", "ai_facilitated", "guided_materials", "specialist_teacher"}
MODE_IDS = {"ai_direct": "DM-AI", "ai_facilitated": "DM-AF", "guided_materials": "DM-GM", "specialist_teacher": "DM-ST"}


class DeliveryModeImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            "dm_nodes": 0,
            "tr_nodes": 0,
            "implies_rels": 0,
            "files": 0,
            "concepts_linked": 0,
            "deliverable_via_rels": 0,
            "teaching_req_rels": 0,
            "skipped_missing_concept": 0,
        }

    def close(self):
        self.driver.close()

    def clear(self, session):
        """Delete all DeliveryMode and TeachingRequirement nodes and relationships."""
        result = session.run("""
            MATCH (dm:DeliveryMode) DETACH DELETE dm
            RETURN count(dm) AS deleted
        """)
        deleted = result.single()["deleted"]
        print(f"  Deleted {deleted} DeliveryMode nodes.")

        result = session.run("""
            MATCH (tr:TeachingRequirement) DETACH DELETE tr
            RETURN count(tr) AS deleted
        """)
        deleted = result.single()["deleted"]
        print(f"  Deleted {deleted} TeachingRequirement nodes.")

    def import_delivery_mode_definitions(self, session):
        """Create the 4 DeliveryMode nodes."""
        defpath = DEFINITIONS_DIR / "delivery_mode_definitions.json"
        with open(defpath) as f:
            modes = json.load(f)

        print(f"\n  Creating {len(modes)} DeliveryMode nodes...")
        for mode in modes:
            session.run("""
                MERGE (dm:DeliveryMode {mode_id: $mode_id})
                SET dm.name              = $name,
                    dm.short_name        = $short_name,
                    dm.description       = $description,
                    dm.agent_prompt      = $agent_prompt,
                    dm.human_role        = $human_role,
                    dm.platform_capability = $platform_capability,
                    dm.display_order     = $display_order,
                    dm.display_category  = 'Delivery Readiness',
                    dm.display_color     = '#10B981',
                    dm.display_icon      = 'settings_input_antenna'
            """,
                mode_id=mode["mode_id"],
                name=mode["name"],
                short_name=mode["short_name"],
                description=mode["description"],
                agent_prompt=mode["agent_prompt"],
                human_role=mode["human_role"],
                platform_capability=mode["platform_capability"],
                display_order=mode["display_order"],
            )
            self.stats["dm_nodes"] += 1
            print(f"    {mode['mode_id']}: {mode['name']}")

    def import_teaching_requirement_definitions(self, session):
        """Create the 15 TeachingRequirement nodes and IMPLIES_MINIMUM_MODE rels."""
        defpath = DEFINITIONS_DIR / "teaching_requirement_definitions.json"
        with open(defpath) as f:
            reqs = json.load(f)

        print(f"\n  Creating {len(reqs)} TeachingRequirement nodes...")
        for req in reqs:
            session.run("""
                MERGE (tr:TeachingRequirement {requirement_id: $requirement_id})
                SET tr.name              = $name,
                    tr.category          = $category,
                    tr.description       = $description,
                    tr.examples          = $examples,
                    tr.display_category  = 'Delivery Readiness',
                    tr.display_color     = '#10B981',
                    tr.display_icon      = 'checklist'
            """,
                requirement_id=req["requirement_id"],
                name=req["name"],
                category=req["category"],
                description=req["description"],
                examples=req.get("examples", []),
            )
            self.stats["tr_nodes"] += 1

            # Create IMPLIES_MINIMUM_MODE relationship
            min_mode = req["implies_minimum_mode"]
            session.run("""
                MATCH (tr:TeachingRequirement {requirement_id: $req_id})
                MATCH (dm:DeliveryMode {mode_id: $mode_id})
                MERGE (tr)-[:IMPLIES_MINIMUM_MODE]->(dm)
            """,
                req_id=req["requirement_id"],
                mode_id=min_mode,
            )
            self.stats["implies_rels"] += 1
            print(f"    {req['requirement_id']}: {req['name']} -> {min_mode}")

    def import_concept_classifications(self, session, path):
        """Import one per-subject delivery mode JSON file."""
        with open(path) as f:
            entries = json.load(f)

        print(f"\n  Loading {path.name}: {len(entries)} concepts")
        self.stats["files"] += 1

        for entry in entries:
            concept_id = entry["concept_id"]
            primary_mode = entry["primary_mode"]
            primary_mode_id = entry["primary_mode_id"]
            confidence = entry["confidence"]
            rationale = entry["rationale"]
            alternative_modes = entry.get("alternative_modes", [])
            teaching_reqs = entry.get("teaching_requirements", [])
            notes = entry.get("notes", "")

            # Verify concept exists
            exists = session.run(
                "MATCH (c:Concept {concept_id: $cid}) RETURN c.concept_id AS id",
                cid=concept_id,
            ).single()

            if not exists:
                self.stats["skipped_missing_concept"] += 1
                continue

            self.stats["concepts_linked"] += 1

            # Create primary DELIVERABLE_VIA relationship
            session.run("""
                MATCH (c:Concept {concept_id: $cid})
                MATCH (dm:DeliveryMode {mode_id: $mode_id})
                MERGE (c)-[r:DELIVERABLE_VIA]->(dm)
                SET r.primary    = true,
                    r.confidence = $confidence,
                    r.rationale  = $rationale,
                    r.notes      = $notes
            """,
                cid=concept_id,
                mode_id=primary_mode_id,
                confidence=confidence,
                rationale=rationale,
                notes=notes,
            )
            self.stats["deliverable_via_rels"] += 1

            # Create alternative DELIVERABLE_VIA relationships
            for alt_mode in alternative_modes:
                alt_mode_id = MODE_IDS.get(alt_mode, alt_mode)
                session.run("""
                    MATCH (c:Concept {concept_id: $cid})
                    MATCH (dm:DeliveryMode {mode_id: $mode_id})
                    MERGE (c)-[r:DELIVERABLE_VIA]->(dm)
                    SET r.primary    = false,
                        r.confidence = $confidence,
                        r.rationale  = 'Alternative delivery mode'
                """,
                    cid=concept_id,
                    mode_id=alt_mode_id,
                    confidence=confidence,
                )
                self.stats["deliverable_via_rels"] += 1

            # Create HAS_TEACHING_REQUIREMENT relationships
            for tr_id in teaching_reqs:
                session.run("""
                    MATCH (c:Concept {concept_id: $cid})
                    MATCH (tr:TeachingRequirement {requirement_id: $tr_id})
                    MERGE (c)-[:HAS_TEACHING_REQUIREMENT]->(tr)
                """,
                    cid=concept_id,
                    tr_id=tr_id,
                )
                self.stats["teaching_req_rels"] += 1

    def import_all(self, clear=False):
        """Run the full import."""
        with self.driver.session() as session:
            if clear:
                print("\nClearing existing delivery mode data...")
                self.clear(session)

            # Step 1: Create DeliveryMode nodes
            self.import_delivery_mode_definitions(session)

            # Step 2: Create TeachingRequirement nodes + IMPLIES_MINIMUM_MODE
            self.import_teaching_requirement_definitions(session)

            # Step 3: Import per-subject classifications
            print("\n  Importing concept classifications...")
            # Glob all JSON files except the definition files
            definition_files = {
                "delivery_mode_definitions.json",
                "teaching_requirement_definitions.json",
            }
            for path in sorted(DATA_DIR.glob("*.json")):
                if path.name not in definition_files:
                    self.import_concept_classifications(session, path)

        self._print_stats()

    def _print_stats(self):
        print("\n" + "=" * 60)
        print("IMPORT SUMMARY")
        print("=" * 60)
        print(f"  DeliveryMode nodes:        {self.stats['dm_nodes']}")
        print(f"  TeachingRequirement nodes:  {self.stats['tr_nodes']}")
        print(f"  IMPLIES_MINIMUM_MODE rels:  {self.stats['implies_rels']}")
        print(f"  Files processed:            {self.stats['files']}")
        print(f"  Concepts linked:            {self.stats['concepts_linked']}")
        print(f"  DELIVERABLE_VIA rels:       {self.stats['deliverable_via_rels']}")
        print(f"  HAS_TEACHING_REQUIREMENT:   {self.stats['teaching_req_rels']}")
        if self.stats['skipped_missing_concept']:
            print(f"  WARN: Skipped (missing concept): {self.stats['skipped_missing_concept']}")
        print("\nDone.")


def main():
    parser = argparse.ArgumentParser(description="Import delivery mode classifications into Neo4j")
    parser.add_argument("--clear", action="store_true", help="Clear existing delivery mode data before import")
    args = parser.parse_args()

    print("=" * 60)
    print("Delivery Mode Importer")
    print("=" * 60)
    print(f"\nConnecting to Neo4j at {NEO4J_URI}...")

    importer = DeliveryModeImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    try:
        importer.import_all(clear=args.clear)
    finally:
        importer.close()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Import RepresentationStage nodes from representation_stages/*.json.

Creates :RepresentationStage nodes and (:Concept)-[:HAS_REPRESENTATION_STAGE]->(:RepresentationStage)
relationships. Each stage encodes a CPA (Concrete-Pictorial-Abstract) progression step for a
primary maths concept — describing the resources, activities, and transition cues for each stage.

Idempotent: uses MERGE on stage_id so it's safe to rerun.

Usage:
  python3 layers/uk-curriculum/scripts/import_representation_stages.py
  python3 layers/uk-curriculum/scripts/import_representation_stages.py --clear
"""

import json
import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / "core" / "scripts"))

from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

DATA_DIR = PROJECT_ROOT / "layers" / "uk-curriculum" / "data" / "representation_stages"

VALID_STAGES = {"concrete", "pictorial", "abstract"}


class RepresentationStageImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            "files": 0,
            "concepts": 0,
            "stages_created": 0,
            "relationships": 0,
            "skipped_missing_concept": 0,
        }

    def close(self):
        self.driver.close()

    def clear(self, session):
        """Delete all RepresentationStage nodes and relationships."""
        result = session.run("""
            MATCH (rs:RepresentationStage) DETACH DELETE rs
            RETURN count(rs) AS deleted
        """)
        deleted = result.single()["deleted"]
        print(f"  Deleted {deleted} existing RepresentationStage nodes.")

    def import_file(self, session, path):
        """Import one representation_stages JSON file."""
        with open(path) as f:
            entries = json.load(f)

        print(f"\n  Loading {path.name}: {len(entries)} concepts")
        self.stats["files"] += 1

        for entry in entries:
            concept_id = entry["concept_id"]
            stages = entry.get("stages", [])

            if not stages:
                continue

            # Verify concept exists
            exists = session.run(
                "MATCH (c:Concept {concept_id: $cid}) RETURN c.concept_id AS id",
                cid=concept_id,
            ).single()

            if not exists:
                print(f"    WARN: Concept {concept_id} not found — skipping {len(stages)} stages")
                self.stats["skipped_missing_concept"] += len(stages)
                continue

            self.stats["concepts"] += 1

            for stage in stages:
                stage_number = stage["stage_number"]
                stage_id = f"{concept_id}-RS{stage_number:02d}"
                stage_name = stage["stage"]

                if stage_name not in VALID_STAGES:
                    print(f"    WARN: {stage_id} has invalid stage '{stage_name}' — skipping")
                    continue

                # Truncate description for display name (max 60 chars)
                description = stage["description"]
                name = description[:60] + "..." if len(description) > 60 else description

                session.run("""
                    MERGE (rs:RepresentationStage {stage_id: $stage_id})
                    SET rs.stage_number      = $stage_number,
                        rs.stage             = $stage_name,
                        rs.description       = $description,
                        rs.resources         = $resources,
                        rs.example_activity  = $example_activity,
                        rs.transition_cue    = $transition_cue,
                        rs.name              = $name,
                        rs.display_category  = 'UK Curriculum',
                        rs.display_color     = '#06B6D4',
                        rs.display_icon      = 'view_carousel'
                """,
                    stage_id=stage_id,
                    stage_number=stage_number,
                    stage_name=stage_name,
                    description=description,
                    resources=stage.get("resources", []),
                    example_activity=stage.get("example_activity", ""),
                    transition_cue=stage.get("transition_cue", ""),
                    name=name,
                )
                self.stats["stages_created"] += 1

                # Link Concept -> RepresentationStage
                session.run("""
                    MATCH (c:Concept {concept_id: $concept_id})
                    MATCH (rs:RepresentationStage {stage_id: $stage_id})
                    MERGE (c)-[:HAS_REPRESENTATION_STAGE]->(rs)
                """,
                    concept_id=concept_id,
                    stage_id=stage_id,
                )
                self.stats["relationships"] += 1

            print(f"    {concept_id}: {len(stages)} stages")

    def run(self, clear=False):
        print("=" * 60)
        print("Import: RepresentationStage nodes (CPA framework)")
        print("=" * 60)

        if not DATA_DIR.exists():
            print(f"\nNo data directory: {DATA_DIR}")
            sys.exit(1)

        json_files = sorted(DATA_DIR.glob("*.json"))
        if not json_files:
            print(f"\nNo JSON files in {DATA_DIR}")
            sys.exit(1)

        print(f"\nFound {len(json_files)} representation stage files:")
        for f in json_files:
            print(f"  {f.name}")

        with self.driver.session() as session:
            if clear:
                print("\nClearing existing RepresentationStage nodes...")
                self.clear(session)

            for path in json_files:
                self.import_file(session, path)

        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        for k, v in self.stats.items():
            print(f"  {k}: {v}")
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Import RepresentationStage nodes (CPA framework)")
    parser.add_argument("--clear", action="store_true",
                        help="Delete existing RepresentationStage nodes before importing")
    args = parser.parse_args()

    importer = RepresentationStageImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
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

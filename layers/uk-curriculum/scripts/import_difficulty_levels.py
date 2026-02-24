#!/usr/bin/env python3
"""
Import DifficultyLevel nodes from difficulty_levels/*.json.

Creates :DifficultyLevel nodes and (:Concept)-[:HAS_DIFFICULTY_LEVEL]->(:DifficultyLevel)
relationships. Each level encodes what a specific difficulty tier looks like for a concept —
grounding the abstract complexity into concrete, assessable tasks.

Idempotent: uses MERGE on level_id so it's safe to rerun.

Usage:
  python3 layers/uk-curriculum/scripts/import_difficulty_levels.py
  python3 layers/uk-curriculum/scripts/import_difficulty_levels.py --clear
"""

import json
import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / "core" / "scripts"))

from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

DATA_DIR = PROJECT_ROOT / "layers" / "uk-curriculum" / "data" / "difficulty_levels"

VALID_LABELS = {"entry", "developing", "expected", "greater_depth", "emerging", "secure", "mastery"}


class DifficultyLevelImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            "files": 0,
            "concepts": 0,
            "levels_created": 0,
            "relationships": 0,
            "skipped_missing_concept": 0,
        }

    def close(self):
        self.driver.close()

    def clear(self, session):
        """Delete all DifficultyLevel nodes and relationships."""
        result = session.run("""
            MATCH (dl:DifficultyLevel) DETACH DELETE dl
            RETURN count(dl) AS deleted
        """)
        deleted = result.single()["deleted"]
        print(f"  Deleted {deleted} existing DifficultyLevel nodes.")

    def import_file(self, session, path):
        """Import one difficulty_levels JSON file."""
        with open(path) as f:
            entries = json.load(f)

        print(f"\n  Loading {path.name}: {len(entries)} concepts")
        self.stats["files"] += 1

        for entry in entries:
            concept_id = entry["concept_id"]
            levels = entry.get("levels", [])

            if not levels:
                continue

            # Verify concept exists
            exists = session.run(
                "MATCH (c:Concept {concept_id: $cid}) RETURN c.concept_id AS id",
                cid=concept_id,
            ).single()

            if not exists:
                print(f"    WARN: Concept {concept_id} not found — skipping {len(levels)} levels")
                self.stats["skipped_missing_concept"] += len(levels)
                continue

            self.stats["concepts"] += 1

            for level in levels:
                level_number = level["level_number"]
                level_id = f"{concept_id}-DL{level_number:02d}"
                label = level["label"]

                if label not in VALID_LABELS:
                    print(f"    WARN: {level_id} has invalid label '{label}' — skipping")
                    continue

                # Truncate description for display name (max 60 chars)
                description = level["description"]
                name = description[:60] + "…" if len(description) > 60 else description

                session.run("""
                    MERGE (dl:DifficultyLevel {level_id: $level_id})
                    SET dl.level_number      = $level_number,
                        dl.label             = $label,
                        dl.description       = $description,
                        dl.example_task      = $example_task,
                        dl.example_response  = $example_response,
                        dl.common_errors     = $common_errors,
                        dl.name              = $name,
                        dl.display_category  = 'UK Curriculum',
                        dl.display_color     = '#F59E0B',
                        dl.display_icon      = 'signal_cellular_alt'
                """,
                    level_id=level_id,
                    level_number=level_number,
                    label=label,
                    description=description,
                    example_task=level.get("example_task", ""),
                    example_response=level.get("example_response", ""),
                    common_errors=level.get("common_errors", []),
                    name=name,
                )
                self.stats["levels_created"] += 1

                # Link Concept -> DifficultyLevel
                session.run("""
                    MATCH (c:Concept {concept_id: $concept_id})
                    MATCH (dl:DifficultyLevel {level_id: $level_id})
                    MERGE (c)-[:HAS_DIFFICULTY_LEVEL]->(dl)
                """,
                    concept_id=concept_id,
                    level_id=level_id,
                )
                self.stats["relationships"] += 1

            print(f"    ✓ {concept_id}: {len(levels)} levels")

    def run(self, clear=False):
        print("=" * 60)
        print("Import: DifficultyLevel nodes")
        print("=" * 60)

        if not DATA_DIR.exists():
            print(f"\nNo data directory: {DATA_DIR}")
            sys.exit(1)

        json_files = sorted(DATA_DIR.glob("*.json"))
        if not json_files:
            print(f"\nNo JSON files in {DATA_DIR}")
            sys.exit(1)

        print(f"\nFound {len(json_files)} difficulty level files:")
        for f in json_files:
            print(f"  {f.name}")

        with self.driver.session() as session:
            if clear:
                print("\nClearing existing DifficultyLevel nodes...")
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
    parser = argparse.ArgumentParser(description="Import DifficultyLevel nodes")
    parser.add_argument("--clear", action="store_true",
                        help="Delete existing DifficultyLevel nodes before importing")
    args = parser.parse_args()

    importer = DifficultyLevelImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
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

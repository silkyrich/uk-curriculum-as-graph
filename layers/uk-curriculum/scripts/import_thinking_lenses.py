#!/usr/bin/env python3
"""
Import ThinkingLens nodes from thinking_lenses.json.

Creates one :ThinkingLens node per lens definition with all properties
including agent_prompt, display styling, and provenance fields.

Cluster -> ThinkingLens links (APPLIES_LENS relationships) are created by
generate_concept_clusters.py, not here.

Usage:
  python3 layers/uk-curriculum/scripts/import_thinking_lenses.py
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / "core" / "scripts"))

from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

THINKING_LENSES_FILE = (
    PROJECT_ROOT
    / "layers"
    / "uk-curriculum"
    / "data"
    / "thinking_lenses"
    / "thinking_lenses.json"
)


class ThinkingLensImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def run(self):
        with open(THINKING_LENSES_FILE) as f:
            lenses = json.load(f)

        print("=" * 60)
        print("Import: ThinkingLens nodes")
        print("=" * 60)
        print(f"\nLoading {len(lenses)} lens definitions from {THINKING_LENSES_FILE.name}")

        created = 0
        with self.driver.session() as session:
            for lens in lenses:
                session.execute_write(self._merge_lens, lens)
                created += 1
                print(f"  ✓ {lens['lens_id']} — {lens['lens_name']}")

        print(f"\nDone. {created} ThinkingLens nodes created/updated.")

    @staticmethod
    def _merge_lens(tx, lens):
        tx.run("""
            MERGE (tl:ThinkingLens {lens_id: $lens_id})
            SET tl.lens_name          = $lens_name,
                tl.description        = $description,
                tl.key_question       = $key_question,
                tl.inspired_by        = $inspired_by,
                tl.agent_prompt       = $agent_prompt,
                tl.display_category   = 'UK Curriculum',
                tl.display_color      = '#7C3AED',
                tl.display_icon       = 'psychology',
                tl.name               = $lens_name
        """,
            lens_id=lens["lens_id"],
            lens_name=lens["lens_name"],
            description=lens["description"],
            key_question=lens["key_question"],
            inspired_by=lens.get("inspired_by", ""),
            agent_prompt=lens.get("agent_prompt", ""),
        )


def main():
    importer = ThinkingLensImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    try:
        importer.run()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        importer.close()


if __name__ == "__main__":
    main()

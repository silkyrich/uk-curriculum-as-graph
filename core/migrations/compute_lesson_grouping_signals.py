#!/usr/bin/env python3
"""
Migration: Compute lesson-grouping signals on Concept nodes.

Post-import migration that computes topology-dependent properties and
materialises CO_TEACHES relationships so the clustering script can work
from in-graph data alone.

Steps:
  1. is_keystone (bool) + prerequisite_fan_out (int) — derived from
     PREREQUISITE_OF fan-out (keystone threshold >= 3).
  2. CO_TEACHES from co_teach_hints — extracted hints stored on Concept
     nodes during import are turned into explicit relationships.
  3. CO_TEACHES from inverse-operation heuristic — concepts in the same
     domain whose names contain classic inverse pairs (addition/subtraction,
     encoding/decoding, etc.) are linked with source='inferred'.

Safe to run multiple times (MERGE prevents duplicates, SET overwrites).
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "core" / "scripts"))

from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


def run_migration():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    with driver.session() as session:
        # ── Step 1: Compute is_keystone and prerequisite_fan_out ──────────
        print("\n--- Step 1: Keystone detection ---")

        result = session.run("""
            MATCH (c:Concept)
            OPTIONAL MATCH (c)-[:PREREQUISITE_OF]->(dep:Concept)
            WITH c, count(dep) AS fan_out
            SET c.is_keystone = (fan_out >= 3),
                c.prerequisite_fan_out = fan_out
            RETURN count(c) AS updated,
                   sum(CASE WHEN fan_out >= 3 THEN 1 ELSE 0 END) AS keystones
        """)
        row = result.single()
        print(f"  Concepts updated: {row['updated']}")
        print(f"  Keystones (fan_out >= 3): {row['keystones']}")

        # ── Step 2: CO_TEACHES from co_teach_hints ───────────────────────
        print("\n--- Step 2: CO_TEACHES from co_teach_hints ---")

        result = session.run("""
            MATCH (c:Concept)
            WHERE c.co_teach_hints IS NOT NULL AND size(c.co_teach_hints) > 0
            UNWIND c.co_teach_hints AS hint_id
            MATCH (target:Concept {concept_id: hint_id})
            MERGE (c)-[r:CO_TEACHES]->(target)
            SET r.reason = 'extracted', r.strength = 0.8, r.source = 'extracted'
            RETURN count(r) AS created
        """)
        row = result.single()
        print(f"  CO_TEACHES relationships (extracted): {row['created']}")

        # ── Step 3: CO_TEACHES from inverse-operation heuristic ──────────
        print("\n--- Step 3: CO_TEACHES from inverse-operation pairs ---")

        result = session.run("""
            MATCH (d:Domain)-[:HAS_CONCEPT]->(c1:Concept)
            MATCH (d)-[:HAS_CONCEPT]->(c2:Concept)
            WHERE c1 <> c2
              AND elementId(c1) < elementId(c2)
              AND (   (c1.concept_name CONTAINS 'addition' AND c2.concept_name CONTAINS 'subtraction')
                   OR (c1.concept_name CONTAINS 'multiplication' AND c2.concept_name CONTAINS 'division')
                   OR (c1.concept_name CONTAINS 'expanding' AND c2.concept_name CONTAINS 'factorising')
                   OR (c1.concept_name CONTAINS 'encoding' AND c2.concept_name CONTAINS 'decoding')
              )
            MERGE (c1)-[r:CO_TEACHES]->(c2)
            SET r.reason = 'inverse_operations', r.strength = 0.9, r.source = 'inferred'
            RETURN count(r) AS created
        """)
        row = result.single()
        print(f"  CO_TEACHES relationships (inferred): {row['created']}")

        # ── Summary ──────────────────────────────────────────────────────
        print("\n--- Summary ---")
        result = session.run("""
            MATCH ()-[r:CO_TEACHES]->()
            RETURN count(r) AS total,
                   sum(CASE WHEN r.source = 'extracted' THEN 1 ELSE 0 END) AS extracted,
                   sum(CASE WHEN r.source = 'inferred' THEN 1 ELSE 0 END) AS inferred
        """)
        row = result.single()
        print(f"  Total CO_TEACHES: {row['total']} (extracted: {row['extracted']}, inferred: {row['inferred']})")

    driver.close()
    print("\nMigration complete.")


if __name__ == "__main__":
    print("=" * 60)
    print("MIGRATION: Compute lesson-grouping signals")
    print("=" * 60)
    run_migration()

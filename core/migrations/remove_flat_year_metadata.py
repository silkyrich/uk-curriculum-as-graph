#!/usr/bin/env python3
"""
Migration: Remove flat year metadata properties from Year nodes.

These flat properties were added by add_year_metadata.py (Feb 2026) and are
superseded by the structured learner-profiles layer nodes:
  interaction_modes    → (Year)-[:SUPPORTS_INTERACTION]->(InteractionType)
  interface_style      → ContentGuideline.reading_level_description
  input_primary        → SUPPORTS_INTERACTION {primary: true}
  input_secondary      → SUPPORTS_INTERACTION {primary: false}
  ui_density           → PedagogyProfile.scaffolding_level
  ai_prompt_guidance   → ContentGuideline.agent_content_prompt

Properties KEPT on Year nodes:
  age_min, age_max     — simple factual reference

Safe to run multiple times (idempotent REMOVE).
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "core" / "scripts"))

from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from neo4j import GraphDatabase


PROPERTIES_TO_REMOVE = [
    "interaction_modes",
    "interface_style",
    "input_primary",
    "input_secondary",
    "ui_density",
    "ai_prompt_guidance",
]


def run_migration():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    with driver.session() as session:
        # Check how many Year nodes have these properties
        result = session.run(
            "MATCH (y:Year) WHERE y.ai_prompt_guidance IS NOT NULL RETURN count(y) AS n"
        )
        count = result.single()["n"]
        print(f"Year nodes with flat metadata properties: {count}")

        if count == 0:
            print("Nothing to migrate — flat properties already removed.")
            driver.close()
            return

        # Build REMOVE clause
        remove_clause = ", ".join(f"y.{p}" for p in PROPERTIES_TO_REMOVE)
        cypher = f"MATCH (y:Year) REMOVE {remove_clause} RETURN count(y) AS updated"

        result = session.run(cypher)
        updated = result.single()["updated"]
        print(f"Removed flat metadata properties from {updated} Year nodes.")
        print(f"Properties removed: {', '.join(PROPERTIES_TO_REMOVE)}")
        print("Properties retained: age_min, age_max")

    driver.close()
    print("\nMigration complete.")


if __name__ == "__main__":
    print("=" * 60)
    print("MIGRATION: Remove flat Year metadata properties")
    print("=" * 60)
    run_migration()

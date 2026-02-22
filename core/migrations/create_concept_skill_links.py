#!/usr/bin/env python3
"""
Migration: Create concept-level DEVELOPS_SKILL relationships from curated JSON files.

Reads human-curated concept→skill link definitions from
layers/uk-curriculum/data/concept_skill_links/*.json and MERGEs
DEVELOPS_SKILL relationships from Concept nodes to epistemic skill nodes
(WorkingScientifically, GeographicalSkill, HistoricalThinking, etc.).

These complement the existing Programme-level DEVELOPS_SKILL relationships
by adding concept granularity — enabling queries like "which WS skills does
this specific concept develop?" rather than just "which skills does this
whole programme develop?"

Safe to run multiple times (MERGE prevents duplicates, SET overwrites properties).
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "core" / "scripts"))

from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

CONCEPT_SKILL_DIR = PROJECT_ROOT / "layers" / "uk-curriculum" / "data" / "concept_skill_links"

# Map skill_type from JSON to Neo4j node label
SKILL_TYPE_TO_LABEL = {
    "WorkingScientifically": "WorkingScientifically",
    "GeographicalSkill": "GeographicalSkill",
    "HistoricalThinking": "HistoricalThinking",
    "ReadingSkill": "ReadingSkill",
    "MathematicalReasoning": "MathematicalReasoning",
    "ComputationalThinking": "ComputationalThinking",
}


def load_curated_links():
    """Load all curated concept-skill link files and validate."""
    all_links = []
    stats = {}

    for json_path in sorted(CONCEPT_SKILL_DIR.glob("*.json")):
        with open(json_path) as f:
            data = json.load(f)

        subject = data.get("subject", json_path.stem)
        skill_type = data.get("skill_type")
        links = data.get("links", [])

        if skill_type not in SKILL_TYPE_TO_LABEL:
            print(f"  WARNING: {json_path.name} has unknown skill_type '{skill_type}' — skipping")
            continue

        for i, link in enumerate(links):
            if not link.get("concept_id") or not link.get("skill_id"):
                print(f"  WARNING: {json_path.name} link #{i} missing concept_id or skill_id — skipping")
                continue

            link["subject"] = subject
            link["skill_label"] = SKILL_TYPE_TO_LABEL[skill_type]
            all_links.append(link)

        stats[subject] = len(links)
        print(f"  Loaded {len(links)} links from {json_path.name} ({skill_type})")

    return all_links, stats


def run_migration():
    print("\n--- Loading curated concept-skill link definitions ---")
    all_links, stats = load_curated_links()

    if not all_links:
        print("\n  No links to create. Done.")
        return

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    with driver.session() as session:
        # ── Step 1: Verify all referenced IDs exist ──────────────────────
        print("\n--- Step 1: Verifying concept and skill IDs exist ---")

        concept_ids = {link["concept_id"] for link in all_links}
        skill_ids = {link["skill_id"] for link in all_links}

        # Check concepts
        result = session.run("""
            UNWIND $ids AS cid
            OPTIONAL MATCH (c:Concept {concept_id: cid})
            RETURN cid, c IS NOT NULL AS exists
        """, ids=list(concept_ids))
        missing_concepts = [r["cid"] for r in result if not r["exists"]]

        # Check skills (try all possible labels)
        missing_skills = []
        for sid in skill_ids:
            result = session.run("""
                OPTIONAL MATCH (s {skill_id: $sid})
                WHERE s:WorkingScientifically OR s:GeographicalSkill OR s:HistoricalThinking
                      OR s:ReadingSkill OR s:MathematicalReasoning OR s:ComputationalThinking
                RETURN s IS NOT NULL AS exists
            """, sid=sid)
            rec = result.single()
            if not rec or not rec["exists"]:
                missing_skills.append(sid)

        if missing_concepts:
            print(f"  WARNING: {len(missing_concepts)} concept IDs not found:")
            for cid in sorted(missing_concepts):
                print(f"    - {cid}")

        if missing_skills:
            print(f"  WARNING: {len(missing_skills)} skill IDs not found:")
            for sid in sorted(missing_skills):
                print(f"    - {sid}")

        # Filter out links with missing IDs
        missing_set = set(missing_concepts) | set(missing_skills)
        valid_links = [
            link for link in all_links
            if link["concept_id"] not in missing_set and link["skill_id"] not in missing_set
        ]
        print(f"  Verified: {len(valid_links)} valid links (of {len(all_links)} total)")

        # ── Step 2: Create DEVELOPS_SKILL relationships ──────────────────
        print("\n--- Step 2: Creating concept-level DEVELOPS_SKILL relationships ---")

        created = 0
        subject_counts = {}

        for link in valid_links:
            # Use label-specific query for type safety
            label = link["skill_label"]
            result = session.run(f"""
                MATCH (c:Concept {{concept_id: $concept_id}})
                MATCH (s:{label} {{skill_id: $skill_id}})
                MERGE (c)-[r:DEVELOPS_SKILL]->(s)
                SET r.source = 'curated',
                    r.rationale = $rationale,
                    r.enquiry_type = $enquiry_type,
                    r.level = 'concept'
                RETURN type(r) AS rtype
            """,
                concept_id=link["concept_id"],
                skill_id=link["skill_id"],
                rationale=link.get("rationale", ""),
                enquiry_type=link.get("enquiry_type"),
            )
            if result.single():
                created += 1
                subj = link["subject"]
                subject_counts[subj] = subject_counts.get(subj, 0) + 1

        print(f"  DEVELOPS_SKILL relationships created/updated: {created}")

        # ── Summary ──────────────────────────────────────────────────────
        print("\n--- Summary ---")
        print(f"  By subject:")
        for subj, count in sorted(subject_counts.items()):
            print(f"    {subj}: {count}")

        # Total DEVELOPS_SKILL stats
        result = session.run("""
            MATCH ()-[r:DEVELOPS_SKILL]->()
            RETURN count(r) AS total,
                   sum(CASE WHEN r.level = 'concept' THEN 1 ELSE 0 END) AS concept_level,
                   sum(CASE WHEN r.level IS NULL THEN 1 ELSE 0 END) AS programme_level
        """)
        row = result.single()
        print(f"\n  Total DEVELOPS_SKILL: {row['total']}")
        print(f"    programme-level: {row['programme_level']}")
        print(f"    concept-level:   {row['concept_level']}")

    driver.close()
    print("\nMigration complete.")


if __name__ == "__main__":
    print("=" * 60)
    print("MIGRATION: Create concept-level DEVELOPS_SKILL from curated links")
    print("=" * 60)
    run_migration()

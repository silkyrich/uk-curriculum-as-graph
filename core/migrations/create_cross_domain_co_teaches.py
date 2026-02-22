#!/usr/bin/env python3
"""
Migration: Create cross-domain CO_TEACHES relationships from curated JSON files.

Reads human-curated cross-domain link definitions from
layers/uk-curriculum/data/cross_domain_links/*.json and MERGEs CO_TEACHES
relationships in the graph with source='curated' and cross_domain=true.

Safe to run multiple times (MERGE prevents duplicates, SET overwrites properties).

Reason taxonomy:
  - parallel_concept: same principle in different domain (commutativity, inverse ops)
  - feeds_into: one concept's output is another's input (reading analysis -> writing)
  - shared_context: benefit from same teaching context/exemplar
  - continuous_narrative: continuous teaching sequence across domain boundary
  - prerequisite_gap: should be a prerequisite but isn't captured
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "core" / "scripts"))

from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

CROSS_DOMAIN_DIR = PROJECT_ROOT / "layers" / "uk-curriculum" / "data" / "cross_domain_links"

VALID_REASONS = {
    "parallel_concept", "feeds_into", "shared_context",
    "continuous_narrative", "prerequisite_gap",
}


def load_curated_links():
    """Load all curated cross-domain link files and validate."""
    all_links = []
    stats = {}

    for json_path in sorted(CROSS_DOMAIN_DIR.glob("*.json")):
        with open(json_path) as f:
            data = json.load(f)

        subject_group = data.get("subject_group", json_path.stem)
        links = data.get("links", [])

        # Validate each link
        for i, link in enumerate(links):
            for field in ("source", "target", "reason", "rationale"):
                if not link.get(field):
                    print(f"  WARNING: {json_path.name} link #{i} missing '{field}' — skipping")
                    continue

            if link["reason"] not in VALID_REASONS:
                print(f"  WARNING: {json_path.name} link #{i} has unknown reason '{link['reason']}' — skipping")
                continue

            link["subject_group"] = subject_group
            all_links.append(link)

        stats[subject_group] = len(links)
        print(f"  Loaded {len(links)} links from {json_path.name}")

    return all_links, stats


def run_migration():
    print("\n--- Loading curated cross-domain link definitions ---")
    all_links, stats = load_curated_links()

    if not all_links:
        print("\n  No links to create. Done.")
        return

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    with driver.session() as session:
        # ── Step 1: Verify all referenced concepts exist ───────────────
        print("\n--- Step 1: Verifying concept IDs exist ---")

        concept_ids = set()
        for link in all_links:
            concept_ids.add(link["source"])
            concept_ids.add(link["target"])

        result = session.run("""
            UNWIND $ids AS cid
            OPTIONAL MATCH (c:Concept {concept_id: cid})
            RETURN cid, c IS NOT NULL AS exists
        """, ids=list(concept_ids))

        missing = [r["cid"] for r in result if not r["exists"]]
        if missing:
            print(f"  WARNING: {len(missing)} concept IDs not found in graph:")
            for cid in sorted(missing):
                print(f"    - {cid}")
            # Filter out links with missing concepts
            all_links = [
                link for link in all_links
                if link["source"] not in missing and link["target"] not in missing
            ]
            print(f"  Proceeding with {len(all_links)} valid links")
        else:
            print(f"  All {len(concept_ids)} concept IDs verified")

        # ── Step 2: Create CO_TEACHES relationships ────────────────────
        print("\n--- Step 2: Creating cross-domain CO_TEACHES relationships ---")

        created = 0
        reason_counts = {}

        for link in all_links:
            result = session.run("""
                MATCH (src:Concept {concept_id: $source})
                MATCH (tgt:Concept {concept_id: $target})
                MERGE (src)-[r:CO_TEACHES]->(tgt)
                SET r.reason = $reason,
                    r.strength = $strength,
                    r.source = 'curated',
                    r.rationale = $rationale,
                    r.cross_domain = true,
                    r.subject_group = $subject_group
                RETURN type(r) AS rtype
            """,
                source=link["source"],
                target=link["target"],
                reason=link["reason"],
                strength=link.get("strength", 0.8),
                rationale=link["rationale"],
                subject_group=link["subject_group"],
            )
            if result.single():
                created += 1
                reason = link["reason"]
                reason_counts[reason] = reason_counts.get(reason, 0) + 1

        print(f"  CO_TEACHES relationships created/updated: {created}")

        # ── Summary ────────────────────────────────────────────────────
        print("\n--- Summary ---")
        print(f"  By subject group:")
        for group, count in sorted(stats.items()):
            print(f"    {group}: {count}")

        print(f"  By reason:")
        for reason, count in sorted(reason_counts.items()):
            print(f"    {reason}: {count}")

        # Total CO_TEACHES stats
        result = session.run("""
            MATCH ()-[r:CO_TEACHES]->()
            RETURN count(r) AS total,
                   sum(CASE WHEN r.source = 'extracted' THEN 1 ELSE 0 END) AS extracted,
                   sum(CASE WHEN r.source = 'inferred' THEN 1 ELSE 0 END) AS inferred,
                   sum(CASE WHEN r.source = 'curated' THEN 1 ELSE 0 END) AS curated
        """)
        row = result.single()
        print(f"\n  Total CO_TEACHES: {row['total']}")
        print(f"    extracted: {row['extracted']}")
        print(f"    inferred:  {row['inferred']}")
        print(f"    curated:   {row['curated']}")

    driver.close()
    print("\nMigration complete.")


if __name__ == "__main__":
    print("=" * 60)
    print("MIGRATION: Create cross-domain CO_TEACHES from curated links")
    print("=" * 60)
    run_migration()

#!/usr/bin/env python3
"""
Migration: Add missing source_url/dfe_reference to KS4 Programme nodes
and create SourceDocument nodes with SOURCED_FROM links.

The 17 KS4 subjects added in the initial KS4 extraction batch were
imported without source_url or dfe_reference because metadata.json
had no KS4-specific subject document entries at the time.

This migration:
  1. Reads the KS4 entries now present in metadata.json
  2. Sets source_url, publication_url, and dfe_reference on each KS4 Programme
  3. Creates the corresponding SourceDocument node (MERGE — idempotent)
  4. Creates the SOURCED_FROM relationship (MERGE — idempotent)

Safe to run multiple times.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "core" / "scripts"))

import json
from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


METADATA_FILE = PROJECT_ROOT / "core" / "data" / "curriculum-documents" / "metadata.json"


def load_ks4_docs():
    """Return KS4-only subject document entries from metadata.json."""
    with open(METADATA_FILE) as f:
        raw = json.load(f)
    return [
        d for d in raw.get("sources", {}).get("subject_documents", [])
        if d.get("key_stages") == ["KS4"]
    ]


def doc_id(doc):
    """Build document_id from a subject_document entry."""
    subject = doc.get("subject", "Unknown").replace(" ", "")
    ks_str = "-".join(doc.get("key_stages", []))
    return f"DOC-{subject}-{ks_str}"


def run_migration():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    ks4_docs = load_ks4_docs()
    print(f"KS4 subject documents to process: {len(ks4_docs)}")

    with driver.session() as session:
        programmes_updated = 0
        source_docs_created = 0
        links_created = 0

        for doc in ks4_docs:
            subject = doc["subject"]
            source_url = doc.get("source_url", "")
            publication_url = doc.get("publication_page", "")
            dfe_ref = doc.get("reference", "")
            document_id = doc_id(doc)
            title = f"{subject} (KS4) — GCSE Subject Content"

            # ── 1. Update Programme node ──────────────────────────────────
            result = session.run("""
                MATCH (p:Programme {key_stage: 'KS4', subject_name: $subject})
                SET p.source_url = $source_url,
                    p.publication_url = $publication_url,
                    p.dfe_reference = $dfe_reference
                RETURN count(p) AS updated
            """, subject=subject, source_url=source_url,
                publication_url=publication_url, dfe_reference=dfe_ref)
            n = result.single()["updated"]
            programmes_updated += n
            if n:
                print(f"  Updated Programme: {subject} KS4")
            else:
                print(f"  WARN: No Programme found for '{subject}' KS4")

            # ── 2. Create SourceDocument node ─────────────────────────────
            result = session.run("""
                MERGE (sd:SourceDocument {document_id: $document_id})
                ON CREATE SET
                    sd.title = $title,
                    sd.url = $source_url,
                    sd.dfe_reference = $dfe_reference,
                    sd.key_stages = ['KS4'],
                    sd.subject = $subject,
                    sd.display_category = 'UK Curriculum',
                    sd.display_color = '#6B7280',
                    sd.display_icon = 'description',
                    sd.display_size = 1,
                    sd.name = $title
                RETURN count(sd) AS created
            """, document_id=document_id, title=title,
                source_url=source_url, dfe_reference=dfe_ref, subject=subject)
            created = result.single()["created"]
            source_docs_created += created

            # ── 3. Link Programme -[:SOURCED_FROM]-> SourceDocument ───────
            result = session.run("""
                MATCH (p:Programme {key_stage: 'KS4', subject_name: $subject})
                MATCH (sd:SourceDocument {document_id: $document_id})
                MERGE (p)-[r:SOURCED_FROM]->(sd)
                RETURN count(r) AS links
            """, subject=subject, document_id=document_id)
            links = result.single()["links"]
            links_created += links

        print(f"\nSummary:")
        print(f"  Programmes updated:     {programmes_updated}")
        print(f"  SourceDocuments merged: {source_docs_created} created (0 = already existed)")
        print(f"  SOURCED_FROM links:     {links_created}")

    driver.close()
    print("\nMigration complete.")


if __name__ == "__main__":
    print("=" * 60)
    print("MIGRATION: Fix KS4 Programme metadata")
    print("=" * 60)
    run_migration()

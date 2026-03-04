#!/usr/bin/env python3
"""
Import Vocabulary layer nodes and relationships.

Creates:
  :VocabularyTerm nodes (~3,000) — curriculum vocabulary with definitions

Relationships:
  (:Concept)-[:USES_TERM {introduced, importance}]->(:VocabularyTerm)
  (:VocabularyTerm)-[:REFINES]->(:VocabularyTerm)
  (:VocabularyTerm)-[:RELATED_TO {relationship}]->(:VocabularyTerm)
  (:VocabularyTerm)-[:SAME_SPELLING_AS]->(:VocabularyTerm)

Idempotent: uses MERGE on node IDs so it's safe to rerun.

Usage:
  python3 layers/vocabulary/scripts/import_vocabulary.py
  python3 layers/vocabulary/scripts/import_vocabulary.py --clear
"""

import json
import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / "core" / "scripts"))

from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
TERMS_DIR = DATA_DIR / "terms"
RELS_DIR = DATA_DIR / "relationships"

VALID_TIERS = {1, 2, 3}
VALID_IMPORTANCE = {"core", "supporting", "extension"}
VALID_WORD_CLASSES = {"noun", "verb", "adjective", "adverb", "phrase", ""}
VALID_RELATIONSHIP_TYPES = {"synonym", "antonym", "hypernym", "meronym", "see_also"}


class VocabularyImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            "term_nodes": 0,
            "uses_term_rels": 0,
            "refines_rels": 0,
            "related_to_rels": 0,
            "same_spelling_rels": 0,
            "term_files": 0,
            "skipped_missing_concept": 0,
            "skipped_missing_term": 0,
        }

    def close(self):
        self.driver.close()

    def clear(self, session):
        """Delete all Vocabulary layer nodes and relationships."""
        result = session.run("""
            MATCH (vt:VocabularyTerm) DETACH DELETE vt
            RETURN count(vt) AS deleted
        """)
        deleted = result.single()["deleted"]
        print(f"  Deleted {deleted} VocabularyTerm nodes.")

        # Also remove USES_TERM relationships from Concept nodes
        result = session.run("""
            MATCH ()-[r:USES_TERM]->()
            DELETE r
            RETURN count(r) AS deleted
        """)
        deleted = result.single()["deleted"]
        print(f"  Deleted {deleted} USES_TERM relationships.")

    def import_terms(self, session):
        """Load VocabularyTerm nodes from data/terms/*.json."""
        if not TERMS_DIR.exists():
            print(f"\n  WARN: {TERMS_DIR} not found — skipping term import")
            return

        json_files = sorted(TERMS_DIR.glob("*.json"))
        if not json_files:
            print(f"\n  No JSON files in {TERMS_DIR}")
            return

        # Cache concept existence to reduce Neo4j round-trips
        concept_cache = {}

        print(f"\n  Importing terms from {len(json_files)} files...")

        for path in json_files:
            with open(path) as f:
                data = json.load(f)

            metadata = data.get("metadata", {})
            terms = data.get("terms", [])
            self.stats["term_files"] += 1

            print(f"\n    {path.name}: {len(terms)} terms")

            for term in terms:
                term_id = term.get("term_id", "")
                if not term_id:
                    continue

                tier = term.get("tier", 3)
                if tier not in VALID_TIERS:
                    print(f"      WARN: {term_id} has invalid tier {tier}")
                    tier = 3

                word_class = term.get("word_class", "")
                if word_class and word_class not in VALID_WORD_CLASSES:
                    print(f"      WARN: {term_id} has unexpected word_class '{word_class}'")

                # Create/merge VocabularyTerm node
                session.run("""
                    MERGE (vt:VocabularyTerm {term_id: $term_id})
                    SET vt.term                 = $term,
                        vt.name                 = $term,
                        vt.definition           = $definition,
                        vt.subject              = $subject,
                        vt.word_class           = $word_class,
                        vt.tier                 = $tier,
                        vt.etymology            = $etymology,
                        vt.example_usage        = $example_usage,
                        vt.common_errors        = $common_errors,
                        vt.related_everyday_word = $related_everyday_word,
                        vt.display_category     = $display_category,
                        vt.display_color        = $display_color,
                        vt.display_icon         = $display_icon
                """,
                    term_id=term_id,
                    term=term.get("term", ""),
                    definition=term.get("definition", ""),
                    subject=term.get("subject", metadata.get("subject", "")),
                    word_class=word_class,
                    tier=tier,
                    etymology=term.get("etymology", ""),
                    example_usage=term.get("example_usage", ""),
                    common_errors=term.get("common_errors", ""),
                    related_everyday_word=term.get("related_everyday_word", ""),
                    display_category="Vocabulary Term",
                    display_color="#0EA5E9",
                    display_icon="spellcheck",
                )
                self.stats["term_nodes"] += 1

                # Create USES_TERM relationships to Concepts
                for link in term.get("concept_links", []):
                    concept_id = link.get("concept_id", "")
                    if not concept_id:
                        continue

                    # Verify concept exists (cached)
                    if concept_id not in concept_cache:
                        exists = session.run(
                            "MATCH (c:Concept {concept_id: $cid}) RETURN c.concept_id AS id",
                            cid=concept_id,
                        ).single()
                        concept_cache[concept_id] = exists is not None

                    if not concept_cache[concept_id]:
                        self.stats["skipped_missing_concept"] += 1
                        continue

                    introduced = link.get("introduced", False)
                    importance = link.get("importance", "core")
                    if importance not in VALID_IMPORTANCE:
                        importance = "core"

                    session.run("""
                        MATCH (c:Concept {concept_id: $cid})
                        MATCH (vt:VocabularyTerm {term_id: $tid})
                        MERGE (c)-[r:USES_TERM]->(vt)
                        SET r.introduced  = $introduced,
                            r.importance  = $importance
                    """,
                        cid=concept_id,
                        tid=term_id,
                        introduced=introduced,
                        importance=importance,
                    )
                    self.stats["uses_term_rels"] += 1

    def import_refinements(self, session):
        """Load REFINES relationships from data/relationships/refinements.json."""
        path = RELS_DIR / "refinements.json"
        if not path.exists():
            return

        with open(path) as f:
            data = json.load(f)

        rels = data.get("relationships", [])
        if not rels:
            return

        print(f"\n  Creating {len(rels)} REFINES relationships...")

        # Cache term existence
        term_cache = {}

        for rel in rels:
            from_id = rel.get("from_term_id", "")
            to_id = rel.get("to_term_id", "")

            for tid in (from_id, to_id):
                if tid not in term_cache:
                    exists = session.run(
                        "MATCH (vt:VocabularyTerm {term_id: $tid}) RETURN vt.term_id AS id",
                        tid=tid,
                    ).single()
                    term_cache[tid] = exists is not None

            if not term_cache.get(from_id):
                print(f"    WARN: VocabularyTerm {from_id} not found — skipping REFINES")
                self.stats["skipped_missing_term"] += 1
                continue
            if not term_cache.get(to_id):
                print(f"    WARN: VocabularyTerm {to_id} not found — skipping REFINES")
                self.stats["skipped_missing_term"] += 1
                continue

            session.run("""
                MATCH (a:VocabularyTerm {term_id: $from_id})
                MATCH (b:VocabularyTerm {term_id: $to_id})
                MERGE (a)-[:REFINES]->(b)
            """,
                from_id=from_id,
                to_id=to_id,
            )
            self.stats["refines_rels"] += 1

    def import_semantic_links(self, session):
        """Load RELATED_TO relationships from data/relationships/semantic.json."""
        path = RELS_DIR / "semantic.json"
        if not path.exists():
            return

        with open(path) as f:
            data = json.load(f)

        rels = data.get("relationships", [])
        if not rels:
            return

        print(f"\n  Creating {len(rels)} RELATED_TO relationships...")

        term_cache = {}

        for rel in rels:
            from_id = rel.get("from_term_id", "")
            to_id = rel.get("to_term_id", "")
            relationship = rel.get("relationship", "see_also")

            if relationship not in VALID_RELATIONSHIP_TYPES:
                print(f"    WARN: Invalid relationship type '{relationship}' — defaulting to see_also")
                relationship = "see_also"

            for tid in (from_id, to_id):
                if tid not in term_cache:
                    exists = session.run(
                        "MATCH (vt:VocabularyTerm {term_id: $tid}) RETURN vt.term_id AS id",
                        tid=tid,
                    ).single()
                    term_cache[tid] = exists is not None

            if not term_cache.get(from_id) or not term_cache.get(to_id):
                self.stats["skipped_missing_term"] += 1
                continue

            session.run("""
                MATCH (a:VocabularyTerm {term_id: $from_id})
                MATCH (b:VocabularyTerm {term_id: $to_id})
                MERGE (a)-[r:RELATED_TO]->(b)
                SET r.relationship = $relationship
            """,
                from_id=from_id,
                to_id=to_id,
                relationship=relationship,
            )
            self.stats["related_to_rels"] += 1

    def import_polysemy_links(self, session):
        """Load SAME_SPELLING_AS relationships from data/relationships/polysemy.json."""
        path = RELS_DIR / "polysemy.json"
        if not path.exists():
            return

        with open(path) as f:
            data = json.load(f)

        rels = data.get("relationships", [])
        if not rels:
            return

        print(f"\n  Creating {len(rels)} SAME_SPELLING_AS relationships...")

        term_cache = {}

        for rel in rels:
            from_id = rel.get("from_term_id", "")
            to_id = rel.get("to_term_id", "")

            for tid in (from_id, to_id):
                if tid not in term_cache:
                    exists = session.run(
                        "MATCH (vt:VocabularyTerm {term_id: $tid}) RETURN vt.term_id AS id",
                        tid=tid,
                    ).single()
                    term_cache[tid] = exists is not None

            if not term_cache.get(from_id) or not term_cache.get(to_id):
                self.stats["skipped_missing_term"] += 1
                continue

            session.run("""
                MATCH (a:VocabularyTerm {term_id: $from_id})
                MATCH (b:VocabularyTerm {term_id: $to_id})
                MERGE (a)-[:SAME_SPELLING_AS]->(b)
                MERGE (b)-[:SAME_SPELLING_AS]->(a)
            """,
                from_id=from_id,
                to_id=to_id,
            )
            self.stats["same_spelling_rels"] += 1

    def run(self, clear=False):
        """Orchestrate the full import."""
        with self.driver.session() as session:
            if clear:
                print("\nClearing existing Vocabulary data...")
                self.clear(session)

            # Step 1: VocabularyTerm nodes + USES_TERM relationships
            self.import_terms(session)

            # Step 2: REFINES relationships
            self.import_refinements(session)

            # Step 3: RELATED_TO relationships
            self.import_semantic_links(session)

            # Step 4: SAME_SPELLING_AS relationships
            self.import_polysemy_links(session)

        self._print_stats()

    def _print_stats(self):
        print("\n" + "=" * 60)
        print("IMPORT SUMMARY")
        print("=" * 60)
        print(f"  VocabularyTerm nodes:    {self.stats['term_nodes']}")
        print(f"  USES_TERM rels:          {self.stats['uses_term_rels']}")
        print(f"  REFINES rels:            {self.stats['refines_rels']}")
        print(f"  RELATED_TO rels:         {self.stats['related_to_rels']}")
        print(f"  SAME_SPELLING_AS rels:   {self.stats['same_spelling_rels']}")
        print(f"  Term files processed:    {self.stats['term_files']}")

        skip_keys = [k for k in self.stats if k.startswith("skipped_") and self.stats[k] > 0]
        if skip_keys:
            print()
            for k in skip_keys:
                print(f"  WARN: {k}: {self.stats[k]}")

        total_nodes = self.stats["term_nodes"]
        total_rels = (self.stats["uses_term_rels"]
                      + self.stats["refines_rels"]
                      + self.stats["related_to_rels"]
                      + self.stats["same_spelling_rels"])
        print(f"\n  Total nodes:         {total_nodes}")
        print(f"  Total relationships: {total_rels}")
        print("\nDone.")


def main():
    parser = argparse.ArgumentParser(description="Import Vocabulary layer into Neo4j")
    parser.add_argument("--clear", action="store_true",
                        help="Clear existing Vocabulary data before import")
    args = parser.parse_args()

    print("=" * 60)
    print("Vocabulary Importer")
    print("=" * 60)
    print(f"\nConnecting to Neo4j at {NEO4J_URI}...")

    importer = VocabularyImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
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

#!/usr/bin/env python3
"""
Import Topic nodes into Neo4j
Graph Model v3.3 — topic layer extension

Adds a curriculum Topic layer that bridges the high-level programme structure
and individual Concepts, capturing how the statutory curriculum organises
content into teachable units:

  Topic -[:TEACHES]-> Concept

Each Topic node carries the dual label :Topic and is sourced from
a JSON file in data/extractions/topics/.  One JSON file per subject/key-stage
grouping is expected; each file contains a list of topic records.

Supported properties
--------------------
  topic_id          — unique identifier (e.g. "HI-KS2-T01")
  topic_name        — human-readable name
  subject           — subject name (e.g. "History", "Geography")
  key_stage         — e.g. "KS2"
  topic_type        — e.g. "substantive", "thematic", "skills"
  is_prescribed     — bool: topic is statutory / prescribed by the NC
  is_optional       — bool: topic is listed as a choice/option
  choice_group      — string grouping label for optional-choice sets, or null
  curriculum_note   — free-text annotation from the NC document
  teaches_concept_ids — list of Concept.concept_id values (used for TEACHES rels)
"""

from neo4j import GraphDatabase
import json
from pathlib import Path
import sys

# Updated to use shared config
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "core" / "scripts"))
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
LAYER_ROOT = Path(__file__).parent.parent
TOPICS_DIR = LAYER_ROOT / "data" / "extractions" / "topics"


class TopicsImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            "topics_created": 0,
            "teaches_created": 0,
        }
        self.missing_concepts: list[str] = []

    def close(self):
        self.driver.close()

    # -------------------------------------------------------------------------
    # Node creation
    # -------------------------------------------------------------------------

    def create_topic_node(self, session, topic: dict) -> bool:
        """
        MERGE a :Topic node and SET all properties.
        Returns True if the node was created (or already existed and was updated).
        """
        result = session.run(
            """
            MERGE (t:Topic {topic_id: $topic_id})
            SET t.topic_name      = $topic_name,
                t.subject         = $subject,
                t.key_stage       = $key_stage,
                t.topic_type      = $topic_type,
                t.is_prescribed   = $is_prescribed,
                t.is_optional     = $is_optional,
                t.choice_group    = $choice_group,
                t.curriculum_note = $curriculum_note
            RETURN t
            """,
            topic_id=topic["topic_id"],
            topic_name=topic.get("topic_name", ""),
            subject=topic.get("subject", ""),
            key_stage=topic.get("key_stage", ""),
            topic_type=topic.get("topic_type", ""),
            is_prescribed=bool(topic.get("is_prescribed", False)),
            is_optional=bool(topic.get("is_optional", False)),
            choice_group=topic.get("choice_group"),  # may be None / null
            curriculum_note=topic.get("curriculum_note", ""),
        )
        return result.single() is not None

    # -------------------------------------------------------------------------
    # Relationship creation
    # -------------------------------------------------------------------------

    def create_teaches_relationship(self, session, topic_id: str, concept_id: str) -> bool:
        """
        MERGE a (:Topic)-[:TEACHES]->(:Concept) relationship.
        Returns True if the relationship was created; False if either node is missing.
        """
        result = session.run(
            """
            MATCH (t:Topic {topic_id: $topic_id})
            MATCH (c:Concept {concept_id: $concept_id})
            MERGE (t)-[:TEACHES]->(c)
            RETURN c.concept_id AS found
            """,
            topic_id=topic_id,
            concept_id=concept_id,
        )
        record = result.single()
        return record is not None

    # -------------------------------------------------------------------------
    # Import orchestration
    # -------------------------------------------------------------------------

    def import_file(self, json_path: Path):
        """Load one JSON file and import all topics (and their TEACHES rels) from it."""
        with open(json_path, encoding="utf-8") as fh:
            data = json.load(fh)

        # Accept either a bare list or a dict with a top-level "topics" key
        if isinstance(data, list):
            topics = data
        elif isinstance(data, dict):
            # Try common wrapper keys
            topics = data.get("topics") or data.get("data") or list(data.values())[0]
        else:
            print(f"  [SKIP] Unexpected JSON structure in {json_path.name}")
            return

        print(f"  Processing {json_path.name}: {len(topics)} topics")

        with self.driver.session() as session:
            for topic in topics:
                topic_id = topic.get("topic_id", "")
                if not topic_id:
                    print(f"    [WARN] Topic record missing topic_id — skipped: {topic}")
                    continue

                # Create / update the Topic node
                created = self.create_topic_node(session, topic)
                if created:
                    self.stats["topics_created"] += 1

                # Create TEACHES relationships
                for concept_id in topic.get("teaches_concept_ids", []):
                    if not concept_id:
                        continue
                    linked = self.create_teaches_relationship(session, topic_id, concept_id)
                    if linked:
                        self.stats["teaches_created"] += 1
                    else:
                        self.missing_concepts.append(concept_id)

    def import_all(self):
        """Find and import every JSON file in the topics extraction directory."""
        if not TOPICS_DIR.exists():
            print(f"[ERROR] Topics directory not found: {TOPICS_DIR}")
            return

        json_files = sorted(TOPICS_DIR.glob("*.json"))
        if not json_files:
            print(f"[WARN] No JSON files found in {TOPICS_DIR}")
            return

        print(f"Found {len(json_files)} JSON file(s) in {TOPICS_DIR}")
        for json_file in json_files:
            self.import_file(json_file)

    # -------------------------------------------------------------------------
    # Stats reporting
    # -------------------------------------------------------------------------

    def report(self):
        print()
        print("=" * 60)
        print("TOPIC IMPORT — SUMMARY")
        print("=" * 60)
        print(f"  Topics created/updated : {self.stats['topics_created']}")
        print(f"  TEACHES rels created   : {self.stats['teaches_created']}")
        if self.missing_concepts:
            unique_missing = sorted(set(self.missing_concepts))
            print(f"  Concept IDs not found  : {len(unique_missing)}")
            for cid in unique_missing[:20]:
                print(f"    - {cid}")
            if len(unique_missing) > 20:
                print(f"    ... and {len(unique_missing) - 20} more")
        else:
            print(f"  Concept IDs not found  : 0")
        print("=" * 60)


def main():
    print("=" * 60)
    print("UK Curriculum Knowledge Graph — Topic Importer")
    print("=" * 60)

    importer = TopicsImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    try:
        importer.import_all()
    finally:
        importer.report()
        importer.close()


if __name__ == "__main__":
    main()

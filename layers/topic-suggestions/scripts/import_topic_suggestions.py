#!/usr/bin/env python3
"""
Import TopicSuggestion nodes (all 9 typed labels) from JSON data files.

Reads subject-specific JSON files from data/topic_suggestions/ and creates
nodes with the correct label per subject:
  - HistoryTopicSuggestion
  - GeographyTopicSuggestion
  - ScienceTopicSuggestion
  - EnglishTopicSuggestion
  - MathsTopicSuggestion
  - ArtTopicSuggestion
  - MusicTopicSuggestion
  - DTTopicSuggestion
  - TopicSuggestion (generic: Computing, RS, Citizenship, Drama, PE, etc.)

Also creates relationships:
  - DELIVERS_VIA {primary: bool} -> Concept
  - USES_TEMPLATE -> VehicleTemplate
  - Domain -[:HAS_SUGGESTION]-> TopicSuggestion
  - GeographyTopicSuggestion -[:CONTRASTS_WITH]-> GeographyTopicSuggestion

Usage:
  python3 layers/topic-suggestions/scripts/import_topic_suggestions.py
  python3 layers/topic-suggestions/scripts/import_topic_suggestions.py --clear
"""

import json
import sys
from pathlib import Path
from glob import glob

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / "core" / "scripts"))

from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

DATA_DIR = PROJECT_ROOT / "layers" / "topic-suggestions" / "data" / "topic_suggestions"

# Map subject names to Neo4j node labels
SUBJECT_LABEL_MAP = {
    "History": "HistoryTopicSuggestion",
    "Geography": "GeographyTopicSuggestion",
    "Science": "ScienceTopicSuggestion",
    "Biology": "ScienceTopicSuggestion",
    "Chemistry": "ScienceTopicSuggestion",
    "Physics": "ScienceTopicSuggestion",
    "English": "EnglishTopicSuggestion",
    "English Language": "EnglishTopicSuggestion",
    "English Literature": "EnglishTopicSuggestion",
    "Mathematics": "MathsTopicSuggestion",
    "Art & Design": "ArtTopicSuggestion",
    "Music": "MusicTopicSuggestion",
    "Design & Technology": "DTTopicSuggestion",
}
# All other subjects use the generic TopicSuggestion label

VALID_SUGGESTION_TYPES = {
    "prescribed_topic", "exemplar_topic", "open_slot",
    "exemplar_figure", "exemplar_event", "exemplar_text",
    "set_text", "genre_requirement", "teacher_convention",
}

VALID_CURRICULUM_STATUSES = {"mandatory", "menu_choice", "exemplar", "convention"}


class TopicSuggestionImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            "nodes_created": 0,
            "delivers_via": 0,
            "uses_template": 0,
            "has_suggestion": 0,
            "contrasts_with": 0,
            "errors": [],
        }

    def close(self):
        self.driver.close()

    def clear(self):
        """Remove all TopicSuggestion nodes (all 9 labels) and their relationships."""
        labels = [
            "HistoryTopicSuggestion", "GeographyTopicSuggestion",
            "ScienceTopicSuggestion", "EnglishTopicSuggestion",
            "MathsTopicSuggestion", "ArtTopicSuggestion",
            "MusicTopicSuggestion", "DTTopicSuggestion",
            "TopicSuggestion",
        ]
        total_deleted = 0
        with self.driver.session() as session:
            for label in labels:
                result = session.run(
                    f"MATCH (n:{label}) DETACH DELETE n RETURN count(n) AS deleted"
                )
                deleted = result.single()["deleted"]
                if deleted > 0:
                    print(f"  Cleared {deleted} {label} nodes.")
                    total_deleted += deleted
        print(f"  Total cleared: {total_deleted} nodes.")

    def run(self, clear=False):
        print("=" * 60)
        print("Import: TopicSuggestion nodes (all 9 typed labels)")
        print("=" * 60)

        if clear:
            print("\n--clear flag: removing existing TopicSuggestion nodes...")
            self.clear()

        if not DATA_DIR.exists():
            print(f"\n  Data directory not found: {DATA_DIR}")
            print("  Create topic suggestion JSON files in data/topic_suggestions/")
            print("  (Phase 2 will generate these from existing ContentVehicle + Topic data)")
            return

        json_files = sorted(DATA_DIR.glob("*.json"))
        if not json_files:
            print(f"\n  No JSON files found in {DATA_DIR}")
            return

        print(f"\nFound {len(json_files)} data files in {DATA_DIR.name}/")

        # Pass 1: Create all nodes
        for json_file in json_files:
            self._import_file(json_file)

        # Pass 2: Create CONTRASTS_WITH for Geography (needs all nodes to exist)
        self._create_contrasts_with()

        # Report
        print(f"\n{'=' * 60}")
        print(f"IMPORT COMPLETE")
        print(f"  Nodes created:    {self.stats['nodes_created']}")
        print(f"  DELIVERS_VIA:     {self.stats['delivers_via']}")
        print(f"  USES_TEMPLATE:    {self.stats['uses_template']}")
        print(f"  HAS_SUGGESTION:   {self.stats['has_suggestion']}")
        print(f"  CONTRASTS_WITH:   {self.stats['contrasts_with']}")
        if self.stats["errors"]:
            print(f"\n  ERRORS ({len(self.stats['errors'])}):")
            for err in self.stats["errors"][:20]:
                print(f"    {err}")

    def _import_file(self, json_file):
        with open(json_file) as f:
            suggestions = json.load(f)

        print(f"\n  {json_file.name}: {len(suggestions)} suggestions")

        with self.driver.session() as session:
            for ts in suggestions:
                # Validate required fields
                suggestion_id = ts.get("suggestion_id", "")
                if not suggestion_id:
                    self.stats["errors"].append(f"{json_file.name}: missing suggestion_id")
                    continue

                subject = ts.get("subject", "")
                label = SUBJECT_LABEL_MAP.get(subject, "TopicSuggestion")

                # Validate enums
                stype = ts.get("suggestion_type", "")
                if stype not in VALID_SUGGESTION_TYPES:
                    self.stats["errors"].append(
                        f"{suggestion_id}: invalid suggestion_type '{stype}'"
                    )

                cstatus = ts.get("curriculum_status", "")
                if cstatus not in VALID_CURRICULUM_STATUSES:
                    self.stats["errors"].append(
                        f"{suggestion_id}: invalid curriculum_status '{cstatus}'"
                    )

                # Create node with correct label
                session.execute_write(self._merge_node, label, ts)
                self.stats["nodes_created"] += 1

                # Create DELIVERS_VIA relationships
                for concept_ref in ts.get("delivers_via", []):
                    concept_id = concept_ref if isinstance(concept_ref, str) else concept_ref.get("concept_id", "")
                    primary = False if isinstance(concept_ref, str) else concept_ref.get("primary", False)
                    if concept_id:
                        session.execute_write(
                            self._create_delivers_via, label, suggestion_id, concept_id, primary
                        )
                        self.stats["delivers_via"] += 1

                # Create USES_TEMPLATE relationships
                for template_id in ts.get("uses_template", []):
                    session.execute_write(
                        self._create_uses_template, label, suggestion_id, template_id
                    )
                    self.stats["uses_template"] += 1

                # Create HAS_SUGGESTION from Domain (inferred from concept domains)
                for domain_id in ts.get("domain_ids", []):
                    session.execute_write(
                        self._create_has_suggestion, label, suggestion_id, domain_id
                    )
                    self.stats["has_suggestion"] += 1

                print(f"    ✓ {suggestion_id} — {ts.get('name', '?')}")

    def _create_contrasts_with(self):
        """Create CONTRASTS_WITH relationships between Geography topic suggestions."""
        json_files = sorted(DATA_DIR.glob("geography_*.json"))
        for json_file in json_files:
            with open(json_file) as f:
                suggestions = json.load(f)
            with self.driver.session() as session:
                for ts in suggestions:
                    contrasting_id = ts.get("contrasts_with_id")
                    if contrasting_id:
                        session.execute_write(
                            self._create_contrasts_rel,
                            ts["suggestion_id"],
                            contrasting_id,
                        )
                        self.stats["contrasts_with"] += 1

    @staticmethod
    def _merge_node(tx, label, ts):
        """MERGE a TopicSuggestion node with the correct typed label."""
        # Build property SET clause from all non-relationship fields
        props = {k: v for k, v in ts.items()
                 if k not in ("delivers_via", "uses_template", "domain_ids",
                              "contrasts_with_id")}

        # Neo4j can't store nested objects directly — serialise any object[] or object props
        for key, val in list(props.items()):
            if isinstance(val, (dict, list)):
                # Lists of strings/ints are fine; lists of objects need JSON serialisation
                if isinstance(val, list) and val and isinstance(val[0], dict):
                    props[key] = json.dumps(val)
                elif isinstance(val, dict):
                    props[key] = json.dumps(val)

        # Build SET clause dynamically
        set_parts = ", ".join(f"n.{k} = ${k}" for k in props.keys())
        query = f"""
            MERGE (n:{label} {{suggestion_id: $suggestion_id}})
            SET {set_parts}
        """
        tx.run(query, **props)

    @staticmethod
    def _create_delivers_via(tx, label, suggestion_id, concept_id, primary):
        tx.run(f"""
            MATCH (ts:{label} {{suggestion_id: $suggestion_id}})
            MATCH (c:Concept {{concept_id: $concept_id}})
            MERGE (ts)-[r:DELIVERS_VIA]->(c)
            SET r.primary = $primary
        """, suggestion_id=suggestion_id, concept_id=concept_id, primary=primary)

    @staticmethod
    def _create_uses_template(tx, label, suggestion_id, template_id):
        tx.run(f"""
            MATCH (ts:{label} {{suggestion_id: $suggestion_id}})
            MATCH (vt:VehicleTemplate {{template_id: $template_id}})
            MERGE (ts)-[:USES_TEMPLATE]->(vt)
        """, suggestion_id=suggestion_id, template_id=template_id)

    @staticmethod
    def _create_has_suggestion(tx, label, suggestion_id, domain_id):
        tx.run(f"""
            MATCH (d:Domain {{domain_id: $domain_id}})
            MATCH (ts:{label} {{suggestion_id: $suggestion_id}})
            MERGE (d)-[:HAS_SUGGESTION]->(ts)
        """, suggestion_id=suggestion_id, domain_id=domain_id)

    @staticmethod
    def _create_contrasts_rel(tx, suggestion_id, contrasting_id):
        tx.run("""
            MATCH (a:GeographyTopicSuggestion {suggestion_id: $sid})
            MATCH (b:GeographyTopicSuggestion {suggestion_id: $cid})
            MERGE (a)-[:CONTRASTS_WITH]->(b)
        """, sid=suggestion_id, cid=contrasting_id)


def main():
    clear = "--clear" in sys.argv
    importer = TopicSuggestionImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    try:
        importer.run(clear=clear)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        importer.close()


if __name__ == "__main__":
    main()

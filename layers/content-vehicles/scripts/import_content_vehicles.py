#!/usr/bin/env python3
"""
Import ContentVehicle nodes into Neo4j
Graph Model v3.8 — content vehicles layer

Adds teaching packs (ContentVehicle) that deliver curriculum concepts with
rich metadata: definitions, assessment guidance, subject-specific properties.

  Domain -[:HAS_VEHICLE]-> ContentVehicle -[:DELIVERS]-> Concept
  ContentVehicle -[:IMPLEMENTS]-> Topic  (optional)

Each vehicle carries subject-specific properties (sources for History,
equipment for Science, manipulatives for Maths, etc.).

Loads JSON files from data/ directory.
"""

from neo4j import GraphDatabase
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "core" / "scripts"))
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

LAYER_ROOT = Path(__file__).parent.parent
DATA_DIR = LAYER_ROOT / "data"


class ContentVehicleImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            "vehicles_created": 0,
            "delivers_created": 0,
            "has_vehicle_created": 0,
            "implements_created": 0,
        }
        self.missing_concepts: list[str] = []
        self.missing_topics: list[str] = []
        self.missing_domains: list[str] = []

    def close(self):
        self.driver.close()

    # -------------------------------------------------------------------------
    # Node creation
    # -------------------------------------------------------------------------

    def create_vehicle_node(self, session, vehicle: dict) -> bool:
        """MERGE a :ContentVehicle node and SET all properties."""
        # Build the base property map (universal properties)
        props = {
            "vehicle_id": vehicle["vehicle_id"],
            "name": vehicle["name"],
            "vehicle_type": vehicle.get("vehicle_type", ""),
            "subject": vehicle.get("subject", ""),
            "key_stage": vehicle.get("key_stage", ""),
            "description": vehicle.get("description", ""),
            "definitions": vehicle.get("definitions", []),
            "assessment_guidance": vehicle.get("assessment_guidance", ""),
            "success_criteria": vehicle.get("success_criteria", []),
            "resources": vehicle.get("resources", []),
            "resource_types": vehicle.get("resource_types", []),
            "display_category": "Content Vehicle",
        }

        # Subject-specific properties — store all as flat properties
        # History
        for key in ["period", "key_figures", "key_events", "sources",
                     "source_types", "perspectives"]:
            if key in vehicle:
                props[key] = vehicle[key]

        # Geography
        for key in ["location", "data_points", "themes", "contrasting_with",
                     "map_types", "data_sources"]:
            if key in vehicle:
                props[key] = vehicle[key]

        # Science
        for key in ["enquiry_type", "variables_independent", "variables_dependent",
                     "variables_controlled", "equipment", "recording_format",
                     "safety_notes", "expected_outcome"]:
            if key in vehicle:
                props[key] = vehicle[key]

        # English
        for key in ["genre", "text_features", "suggested_texts", "reading_level",
                     "writing_outcome", "grammar_focus"]:
            if key in vehicle:
                props[key] = vehicle[key]

        # Maths
        for key in ["cpa_stage", "manipulatives", "representations",
                     "difficulty_levels", "common_errors"]:
            if key in vehicle:
                props[key] = vehicle[key]

        result = session.run(
            """
            MERGE (cv:ContentVehicle {vehicle_id: $props.vehicle_id})
            SET cv += $props
            RETURN cv
            """,
            props=props,
        )
        return result.single() is not None

    # -------------------------------------------------------------------------
    # Relationship creation
    # -------------------------------------------------------------------------

    def create_delivers_relationship(self, session, vehicle_id: str,
                                     concept_id: str, primary: bool = False) -> bool:
        """MERGE (:ContentVehicle)-[:DELIVERS]->(:Concept)."""
        result = session.run(
            """
            MATCH (cv:ContentVehicle {vehicle_id: $vehicle_id})
            MATCH (c:Concept {concept_id: $concept_id})
            MERGE (cv)-[r:DELIVERS]->(c)
            SET r.primary = $primary
            RETURN c.concept_id AS found
            """,
            vehicle_id=vehicle_id,
            concept_id=concept_id,
            primary=primary,
        )
        return result.single() is not None

    def create_has_vehicle_relationship(self, session, domain_id: str,
                                        vehicle_id: str) -> bool:
        """MERGE (:Domain)-[:HAS_VEHICLE]->(:ContentVehicle)."""
        result = session.run(
            """
            MATCH (d:Domain {domain_id: $domain_id})
            MATCH (cv:ContentVehicle {vehicle_id: $vehicle_id})
            MERGE (d)-[:HAS_VEHICLE]->(cv)
            RETURN cv.vehicle_id AS found
            """,
            domain_id=domain_id,
            vehicle_id=vehicle_id,
        )
        return result.single() is not None

    def create_implements_relationship(self, session, vehicle_id: str,
                                       topic_id: str) -> bool:
        """MERGE (:ContentVehicle)-[:IMPLEMENTS]->(:Topic)."""
        result = session.run(
            """
            MATCH (cv:ContentVehicle {vehicle_id: $vehicle_id})
            MATCH (t:Topic {topic_id: $topic_id})
            MERGE (cv)-[:IMPLEMENTS]->(t)
            RETURN t.topic_id AS found
            """,
            vehicle_id=vehicle_id,
            topic_id=topic_id,
        )
        return result.single() is not None

    # -------------------------------------------------------------------------
    # Domain inference
    # -------------------------------------------------------------------------

    def infer_domains_for_vehicle(self, session, vehicle_id: str,
                                  concept_ids: list[str]) -> list[str]:
        """Find which domains contain the delivered concepts, link HAS_VEHICLE."""
        records = session.run(
            """
            MATCH (d:Domain)-[:HAS_CONCEPT]->(c:Concept)
            WHERE c.concept_id IN $concept_ids
            RETURN DISTINCT d.domain_id AS domain_id
            """,
            concept_ids=concept_ids,
        )
        domain_ids = [r["domain_id"] for r in records]
        for domain_id in domain_ids:
            if self.create_has_vehicle_relationship(session, domain_id, vehicle_id):
                self.stats["has_vehicle_created"] += 1
            else:
                self.missing_domains.append(domain_id)
        return domain_ids

    # -------------------------------------------------------------------------
    # Import orchestration
    # -------------------------------------------------------------------------

    def import_file(self, json_path: Path):
        """Load one JSON file and import all vehicles from it."""
        with open(json_path, encoding="utf-8") as fh:
            data = json.load(fh)

        vehicles = data.get("vehicles", [])
        file_subject = data.get("subject", "")
        file_ks = data.get("key_stage", "")

        print(f"  Processing {json_path.name}: {len(vehicles)} vehicles ({file_subject} {file_ks})")

        with self.driver.session() as session:
            for vehicle in vehicles:
                vehicle_id = vehicle.get("vehicle_id", "")
                if not vehicle_id:
                    print(f"    [WARN] Vehicle record missing vehicle_id — skipped")
                    continue

                # Inherit subject/key_stage from file if not on vehicle
                if not vehicle.get("subject"):
                    vehicle["subject"] = file_subject
                if not vehicle.get("key_stage"):
                    vehicle["key_stage"] = file_ks

                # Create the vehicle node
                if self.create_vehicle_node(session, vehicle):
                    self.stats["vehicles_created"] += 1

                # Create DELIVERS relationships
                concept_ids = vehicle.get("delivers_concept_ids", [])
                for concept_id in concept_ids:
                    if not concept_id:
                        continue
                    if self.create_delivers_relationship(session, vehicle_id, concept_id):
                        self.stats["delivers_created"] += 1
                    else:
                        self.missing_concepts.append(concept_id)

                # Infer HAS_VEHICLE from domains of delivered concepts
                if concept_ids:
                    self.infer_domains_for_vehicle(session, vehicle_id, concept_ids)

                # Create IMPLEMENTS relationship (optional)
                topic_id = vehicle.get("implements_topic_id")
                if topic_id:
                    if self.create_implements_relationship(session, vehicle_id, topic_id):
                        self.stats["implements_created"] += 1
                    else:
                        self.missing_topics.append(topic_id)

    def import_all(self):
        """Find and import every JSON file in the data directory."""
        if not DATA_DIR.exists():
            print(f"[ERROR] Data directory not found: {DATA_DIR}")
            return

        json_files = sorted(DATA_DIR.glob("*.json"))
        if not json_files:
            print(f"[WARN] No JSON files found in {DATA_DIR}")
            return

        print(f"Found {len(json_files)} JSON file(s) in {DATA_DIR}")
        for json_file in json_files:
            self.import_file(json_file)

    # -------------------------------------------------------------------------
    # Stats reporting
    # -------------------------------------------------------------------------

    def report(self):
        print()
        print("=" * 60)
        print("CONTENT VEHICLE IMPORT — SUMMARY")
        print("=" * 60)
        print(f"  Vehicles created/updated : {self.stats['vehicles_created']}")
        print(f"  DELIVERS rels created    : {self.stats['delivers_created']}")
        print(f"  HAS_VEHICLE rels created : {self.stats['has_vehicle_created']}")
        print(f"  IMPLEMENTS rels created  : {self.stats['implements_created']}")

        if self.missing_concepts:
            unique_missing = sorted(set(self.missing_concepts))
            print(f"  Concept IDs not found    : {len(unique_missing)}")
            for cid in unique_missing[:20]:
                print(f"    - {cid}")
            if len(unique_missing) > 20:
                print(f"    ... and {len(unique_missing) - 20} more")
        else:
            print(f"  Concept IDs not found    : 0")

        if self.missing_topics:
            unique_missing = sorted(set(self.missing_topics))
            print(f"  Topic IDs not found      : {len(unique_missing)}")
            for tid in unique_missing[:10]:
                print(f"    - {tid}")
        else:
            print(f"  Topic IDs not found      : 0")

        print("=" * 60)


def main():
    print("=" * 60)
    print("UK Curriculum Knowledge Graph — Content Vehicle Importer")
    print("=" * 60)

    importer = ContentVehicleImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    try:
        importer.import_all()
    finally:
        importer.report()
        importer.close()


if __name__ == "__main__":
    main()

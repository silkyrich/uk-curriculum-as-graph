#!/usr/bin/env python3
"""
Import SEND Support layer nodes and relationships.

Creates:
  :NeedArea nodes (4) — statutory SEN need areas from the SEND Code of Practice
  :AccessRequirement nodes (~16) — specific barriers a learner may face
  :SupportStrategy nodes (~20) — evidence-based strategies to mitigate barriers

Relationships:
  (:AccessRequirement)-[:TAGGED_AS]->(:NeedArea)
  (:SupportStrategy)-[:MITIGATES {strength, notes}]->(:AccessRequirement)
  (:SupportStrategy)-[:COMMONLY_USED_FOR]->(:NeedArea)
  (:Concept)-[:HAS_ACCESS_REQUIREMENT {level, rationale, source}]->(:AccessRequirement)
  (:VehicleTemplate)-[:CAN_APPLY {default, notes}]->(:SupportStrategy)
  (:InteractionType)-[:ENABLES {quality, notes}]->(:SupportStrategy)
  (:TeachingRequirement)-[:SUPPORTED_BY {notes}]->(:SupportStrategy)

Idempotent: uses MERGE on node IDs so it's safe to rerun.

Usage:
  python3 layers/send-support/scripts/import_send_support.py
  python3 layers/send-support/scripts/import_send_support.py --clear
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

VALID_TIERS = {"universal", "targeted", "specialist"}
VALID_CONSTRUCT_RISK = {"low", "conditional", "high"}
VALID_INTENSITY = {"low", "medium", "high"}
VALID_ACCESS_LEVELS = {"low", "medium", "high"}


class SendSupportImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            "need_area_nodes": 0,
            "access_requirement_nodes": 0,
            "support_strategy_nodes": 0,
            "tagged_as_rels": 0,
            "mitigates_rels": 0,
            "commonly_used_for_rels": 0,
            "has_access_requirement_rels": 0,
            "can_apply_rels": 0,
            "enables_rels": 0,
            "supported_by_rels": 0,
            "concept_support_files": 0,
            "skipped_missing_concept": 0,
            "skipped_missing_access_req": 0,
            "skipped_missing_vehicle_template": 0,
            "skipped_missing_interaction_type": 0,
            "skipped_missing_teaching_req": 0,
        }

    def close(self):
        self.driver.close()

    def clear(self, session):
        """Delete all SEND Support layer nodes and relationships."""
        result = session.run("""
            MATCH (na:NeedArea) DETACH DELETE na
            RETURN count(na) AS deleted
        """)
        deleted = result.single()["deleted"]
        print(f"  Deleted {deleted} NeedArea nodes.")

        result = session.run("""
            MATCH (ar:AccessRequirement) DETACH DELETE ar
            RETURN count(ar) AS deleted
        """)
        deleted = result.single()["deleted"]
        print(f"  Deleted {deleted} AccessRequirement nodes.")

        result = session.run("""
            MATCH (ss:SupportStrategy) DETACH DELETE ss
            RETURN count(ss) AS deleted
        """)
        deleted = result.single()["deleted"]
        print(f"  Deleted {deleted} SupportStrategy nodes.")

        # Also remove HAS_ACCESS_REQUIREMENT relationships from Concept nodes
        result = session.run("""
            MATCH ()-[r:HAS_ACCESS_REQUIREMENT]->()
            DELETE r
            RETURN count(r) AS deleted
        """)
        deleted = result.single()["deleted"]
        print(f"  Deleted {deleted} HAS_ACCESS_REQUIREMENT relationships.")

        # Remove CAN_APPLY relationships from VehicleTemplate nodes
        result = session.run("""
            MATCH ()-[r:CAN_APPLY]->()
            DELETE r
            RETURN count(r) AS deleted
        """)
        deleted = result.single()["deleted"]
        print(f"  Deleted {deleted} CAN_APPLY relationships.")

        # Remove ENABLES relationships from InteractionType nodes
        result = session.run("""
            MATCH ()-[r:ENABLES]->()
            DELETE r
            RETURN count(r) AS deleted
        """)
        deleted = result.single()["deleted"]
        print(f"  Deleted {deleted} ENABLES relationships.")

        # Remove SUPPORTED_BY relationships from TeachingRequirement nodes
        result = session.run("""
            MATCH ()-[r:SUPPORTED_BY]->()
            DELETE r
            RETURN count(r) AS deleted
        """)
        deleted = result.single()["deleted"]
        print(f"  Deleted {deleted} SUPPORTED_BY relationships.")

    def import_need_areas(self, session):
        """Load NeedArea nodes from data/need_areas.json."""
        path = DATA_DIR / "need_areas.json"
        if not path.exists():
            print(f"\n  WARN: {path} not found — skipping NeedArea import")
            return

        with open(path) as f:
            need_areas = json.load(f)

        print(f"\n  Creating {len(need_areas)} NeedArea nodes...")
        for na in need_areas:
            session.run("""
                MERGE (na:NeedArea {need_area_id: $need_area_id})
                SET na.name             = $name,
                    na.description      = $description,
                    na.statutory_order  = $statutory_order,
                    na.display_category = $display_category,
                    na.display_color    = $display_color,
                    na.display_icon     = $display_icon
            """,
                need_area_id=na["need_area_id"],
                name=na["name"],
                description=na.get("description", ""),
                statutory_order=na.get("statutory_order", 0),
                display_category=na.get("display_category", "SEND Support"),
                display_color=na.get("display_color", "#E11D48"),
                display_icon=na.get("display_icon", "accessibility_new"),
            )
            self.stats["need_area_nodes"] += 1
            print(f"    {na['need_area_id']}: {na['name']}")

    def import_access_requirements(self, session):
        """Load AccessRequirement nodes and TAGGED_AS relationships from data/access_requirements.json."""
        path = DATA_DIR / "access_requirements.json"
        if not path.exists():
            print(f"\n  WARN: {path} not found — skipping AccessRequirement import")
            return

        with open(path) as f:
            access_reqs = json.load(f)

        print(f"\n  Creating {len(access_reqs)} AccessRequirement nodes...")
        for ar in access_reqs:
            intensity = ar.get("intensity_default", "medium")
            if intensity not in VALID_INTENSITY:
                print(f"    WARN: {ar['access_req_id']} has invalid intensity_default '{intensity}'")

            session.run("""
                MERGE (ar:AccessRequirement {access_req_id: $access_req_id})
                SET ar.name               = $name,
                    ar.category           = $category,
                    ar.description        = $description,
                    ar.intensity_default  = $intensity_default,
                    ar.construct_sensitive = $construct_sensitive,
                    ar.examples           = $examples,
                    ar.notes_for_compiler = $notes_for_compiler,
                    ar.display_category   = $display_category,
                    ar.display_color      = $display_color,
                    ar.display_icon       = $display_icon
            """,
                access_req_id=ar["access_req_id"],
                name=ar["name"],
                category=ar.get("category", ""),
                description=ar.get("description", ""),
                intensity_default=intensity,
                construct_sensitive=ar.get("construct_sensitive", False),
                examples=ar.get("examples", []),
                notes_for_compiler=ar.get("notes_for_compiler", ""),
                display_category=ar.get("display_category", "SEND Support"),
                display_color=ar.get("display_color", "#F97316"),
                display_icon=ar.get("display_icon", "warning_amber"),
            )
            self.stats["access_requirement_nodes"] += 1

            # Create TAGGED_AS relationships to NeedArea
            for need_area_id in ar.get("tagged_as", []):
                result = session.run(
                    "MATCH (na:NeedArea {need_area_id: $nid}) RETURN na.need_area_id AS id",
                    nid=need_area_id,
                ).single()
                if not result:
                    print(f"    WARN: NeedArea {need_area_id} not found for TAGGED_AS from {ar['access_req_id']}")
                    continue

                session.run("""
                    MATCH (ar:AccessRequirement {access_req_id: $ar_id})
                    MATCH (na:NeedArea {need_area_id: $na_id})
                    MERGE (ar)-[:TAGGED_AS]->(na)
                """,
                    ar_id=ar["access_req_id"],
                    na_id=need_area_id,
                )
                self.stats["tagged_as_rels"] += 1

            print(f"    {ar['access_req_id']}: {ar['name']}")

    def import_support_strategies(self, session):
        """Load SupportStrategy nodes, MITIGATES and COMMONLY_USED_FOR relationships."""
        path = DATA_DIR / "support_strategies.json"
        if not path.exists():
            print(f"\n  WARN: {path} not found — skipping SupportStrategy import")
            return

        with open(path) as f:
            data = json.load(f)

        # Support both top-level array and object with "strategies" key
        if isinstance(data, dict):
            strategies = data.get("strategies", [])
        else:
            strategies = data

        print(f"\n  Creating {len(strategies)} SupportStrategy nodes...")
        for ss in strategies:
            tier = ss.get("tier", "universal")
            if tier not in VALID_TIERS:
                print(f"    WARN: {ss['support_id']} has invalid tier '{tier}'")

            construct_risk = ss.get("construct_risk", "low")
            if construct_risk not in VALID_CONSTRUCT_RISK:
                print(f"    WARN: {ss['support_id']} has invalid construct_risk '{construct_risk}'")

            session.run("""
                MERGE (ss:SupportStrategy {support_id: $support_id})
                SET ss.name                  = $name,
                    ss.tier                  = $tier,
                    ss.description           = $description,
                    ss.requires_adult        = $requires_adult,
                    ss.construct_risk        = $construct_risk,
                    ss.blocked_when_assessing = $blocked_when_assessing,
                    ss.prompt_rules          = $prompt_rules,
                    ss.ui_implications       = $ui_implications,
                    ss.review_notes          = $review_notes,
                    ss.display_category      = $display_category,
                    ss.display_color         = $display_color,
                    ss.display_icon          = $display_icon
            """,
                support_id=ss["support_id"],
                name=ss["name"],
                tier=tier,
                description=ss.get("description", ""),
                requires_adult=ss.get("requires_adult", False),
                construct_risk=construct_risk,
                blocked_when_assessing=ss.get("blocked_when_assessing", []),
                prompt_rules=ss.get("prompt_rules", []),
                ui_implications=ss.get("ui_implications", []),
                review_notes=ss.get("review_notes", ""),
                display_category=ss.get("display_category", "SEND Support"),
                display_color=ss.get("display_color", "#22C55E"),
                display_icon=ss.get("display_icon", "support_agent"),
            )
            self.stats["support_strategy_nodes"] += 1

            # Create MITIGATES relationships to AccessRequirement
            for mit in ss.get("mitigates", []):
                ar_id = mit if isinstance(mit, str) else mit.get("access_req_id", mit.get("id", ""))
                strength = "" if isinstance(mit, str) else mit.get("strength", "")
                notes = "" if isinstance(mit, str) else mit.get("notes", "")

                result = session.run(
                    "MATCH (ar:AccessRequirement {access_req_id: $arid}) RETURN ar.access_req_id AS id",
                    arid=ar_id,
                ).single()
                if not result:
                    print(f"    WARN: AccessRequirement {ar_id} not found for MITIGATES from {ss['support_id']}")
                    self.stats["skipped_missing_access_req"] += 1
                    continue

                session.run("""
                    MATCH (ss:SupportStrategy {support_id: $ss_id})
                    MATCH (ar:AccessRequirement {access_req_id: $ar_id})
                    MERGE (ss)-[r:MITIGATES]->(ar)
                    SET r.strength = $strength,
                        r.notes    = $notes
                """,
                    ss_id=ss["support_id"],
                    ar_id=ar_id,
                    strength=strength,
                    notes=notes,
                )
                self.stats["mitigates_rels"] += 1

            # Create COMMONLY_USED_FOR relationships to NeedArea
            for na_id in ss.get("commonly_used_for", []):
                result = session.run(
                    "MATCH (na:NeedArea {need_area_id: $nid}) RETURN na.need_area_id AS id",
                    nid=na_id,
                ).single()
                if not result:
                    print(f"    WARN: NeedArea {na_id} not found for COMMONLY_USED_FOR from {ss['support_id']}")
                    continue

                session.run("""
                    MATCH (ss:SupportStrategy {support_id: $ss_id})
                    MATCH (na:NeedArea {need_area_id: $na_id})
                    MERGE (ss)-[:COMMONLY_USED_FOR]->(na)
                """,
                    ss_id=ss["support_id"],
                    na_id=na_id,
                )
                self.stats["commonly_used_for_rels"] += 1

            print(f"    {ss['support_id']}: {ss['name']} (tier={tier})")

        # Import cross-layer relationship data embedded in the strategies file
        if isinstance(data, dict):
            self._import_vehicle_template_links(session, data.get("vehicle_template_links", []))
            self._import_interaction_type_links(session, data.get("interaction_type_links", []))
            self._import_teaching_requirement_links(session, data.get("teaching_requirement_links", []))

    def _import_vehicle_template_links(self, session, links):
        """Create CAN_APPLY relationships: VehicleTemplate -> SupportStrategy."""
        if not links:
            return

        print(f"\n  Creating {len(links)} CAN_APPLY relationships (VehicleTemplate -> SupportStrategy)...")
        for link in links:
            template_id = link.get("template_id", "")
            support_id = link.get("support_id", "")
            default = link.get("default", False)
            notes = link.get("notes", "")

            # Verify VehicleTemplate exists
            result = session.run(
                "MATCH (vt:VehicleTemplate {template_id: $tid}) RETURN vt.template_id AS id",
                tid=template_id,
            ).single()
            if not result:
                print(f"    WARN: VehicleTemplate {template_id} not found — skipping CAN_APPLY")
                self.stats["skipped_missing_vehicle_template"] += 1
                continue

            # Verify SupportStrategy exists
            result = session.run(
                "MATCH (ss:SupportStrategy {support_id: $sid}) RETURN ss.support_id AS id",
                sid=support_id,
            ).single()
            if not result:
                print(f"    WARN: SupportStrategy {support_id} not found — skipping CAN_APPLY")
                continue

            session.run("""
                MATCH (vt:VehicleTemplate {template_id: $tid})
                MATCH (ss:SupportStrategy {support_id: $sid})
                MERGE (vt)-[r:CAN_APPLY]->(ss)
                SET r.default = $default,
                    r.notes   = $notes
            """,
                tid=template_id,
                sid=support_id,
                default=default,
                notes=notes,
            )
            self.stats["can_apply_rels"] += 1

    def _import_interaction_type_links(self, session, links):
        """Create ENABLES relationships: InteractionType -> SupportStrategy."""
        if not links:
            return

        print(f"\n  Creating {len(links)} ENABLES relationships (InteractionType -> SupportStrategy)...")
        for link in links:
            interaction_id = link.get("interaction_id", "")
            support_id = link.get("support_id", "")
            quality = link.get("quality", "")
            notes = link.get("notes", "")

            # Verify InteractionType exists
            result = session.run(
                "MATCH (it:InteractionType {interaction_id: $iid}) RETURN it.interaction_id AS id",
                iid=interaction_id,
            ).single()
            if not result:
                print(f"    WARN: InteractionType {interaction_id} not found — skipping ENABLES")
                self.stats["skipped_missing_interaction_type"] += 1
                continue

            # Verify SupportStrategy exists
            result = session.run(
                "MATCH (ss:SupportStrategy {support_id: $sid}) RETURN ss.support_id AS id",
                sid=support_id,
            ).single()
            if not result:
                print(f"    WARN: SupportStrategy {support_id} not found — skipping ENABLES")
                continue

            session.run("""
                MATCH (it:InteractionType {interaction_id: $iid})
                MATCH (ss:SupportStrategy {support_id: $sid})
                MERGE (it)-[r:ENABLES]->(ss)
                SET r.quality = $quality,
                    r.notes   = $notes
            """,
                iid=interaction_id,
                sid=support_id,
                quality=quality,
                notes=notes,
            )
            self.stats["enables_rels"] += 1

    def _import_teaching_requirement_links(self, session, links):
        """Create SUPPORTED_BY relationships: TeachingRequirement -> SupportStrategy."""
        if not links:
            return

        print(f"\n  Creating {len(links)} SUPPORTED_BY relationships (TeachingRequirement -> SupportStrategy)...")
        for link in links:
            requirement_id = link.get("requirement_id", "")
            support_id = link.get("support_id", "")
            notes = link.get("notes", "")

            # Verify TeachingRequirement exists
            result = session.run(
                "MATCH (tr:TeachingRequirement {requirement_id: $rid}) RETURN tr.requirement_id AS id",
                rid=requirement_id,
            ).single()
            if not result:
                print(f"    WARN: TeachingRequirement {requirement_id} not found — skipping SUPPORTED_BY")
                self.stats["skipped_missing_teaching_req"] += 1
                continue

            # Verify SupportStrategy exists
            result = session.run(
                "MATCH (ss:SupportStrategy {support_id: $sid}) RETURN ss.support_id AS id",
                sid=support_id,
            ).single()
            if not result:
                print(f"    WARN: SupportStrategy {support_id} not found — skipping SUPPORTED_BY")
                continue

            session.run("""
                MATCH (tr:TeachingRequirement {requirement_id: $rid})
                MATCH (ss:SupportStrategy {support_id: $sid})
                MERGE (tr)-[r:SUPPORTED_BY]->(ss)
                SET r.notes = $notes
            """,
                rid=requirement_id,
                sid=support_id,
                notes=notes,
            )
            self.stats["supported_by_rels"] += 1

    def import_concept_support_links(self, session):
        """Load concept->AccessRequirement links from data/concept_support_links/*.json.

        Each JSON file is a flat array of link objects:
          {"concept_id": "MA-Y3-C004", "access_req_id": "working_memory_load",
           "level": "high", "rationale": "...", "source": "curriculum_analysis"}
        """
        links_dir = DATA_DIR / "concept_support_links"
        if not links_dir.exists():
            print(f"\n  WARN: {links_dir} not found — skipping concept support links")
            return

        json_files = sorted(links_dir.glob("*.json"))
        if not json_files:
            print(f"\n  No JSON files in {links_dir}")
            return

        print(f"\n  Importing concept support links from {len(json_files)} files...")

        # Cache existence checks to reduce Neo4j round-trips
        concept_cache = {}
        ar_cache = {}

        for path in json_files:
            with open(path) as f:
                entries = json.load(f)

            print(f"\n    Loading {path.name}: {len(entries)} links")
            self.stats["concept_support_files"] += 1

            for entry in entries:
                concept_id = entry["concept_id"]
                ar_id = entry["access_req_id"]
                level = entry.get("level", "medium")
                rationale = entry.get("rationale", "")
                source = entry.get("source", "")

                if level not in VALID_ACCESS_LEVELS:
                    print(f"      WARN: {concept_id} -> {ar_id} has invalid level '{level}'")

                # Verify concept exists (cached)
                if concept_id not in concept_cache:
                    exists = session.run(
                        "MATCH (c:Concept {concept_id: $cid}) RETURN c.concept_id AS id",
                        cid=concept_id,
                    ).single()
                    concept_cache[concept_id] = exists is not None

                if not concept_cache[concept_id]:
                    print(f"      WARN: Concept {concept_id} not found — skipping")
                    self.stats["skipped_missing_concept"] += 1
                    continue

                # Verify AccessRequirement exists (cached)
                if ar_id not in ar_cache:
                    exists = session.run(
                        "MATCH (ar:AccessRequirement {access_req_id: $arid}) RETURN ar.access_req_id AS id",
                        arid=ar_id,
                    ).single()
                    ar_cache[ar_id] = exists is not None

                if not ar_cache[ar_id]:
                    print(f"      WARN: AccessRequirement {ar_id} not found — skipping link from {concept_id}")
                    self.stats["skipped_missing_access_req"] += 1
                    continue

                session.run("""
                    MATCH (c:Concept {concept_id: $cid})
                    MATCH (ar:AccessRequirement {access_req_id: $ar_id})
                    MERGE (c)-[r:HAS_ACCESS_REQUIREMENT]->(ar)
                    SET r.level     = $level,
                        r.rationale = $rationale,
                        r.source    = $source
                """,
                    cid=concept_id,
                    ar_id=ar_id,
                    level=level,
                    rationale=rationale,
                    source=source,
                )
                self.stats["has_access_requirement_rels"] += 1

    def run(self, clear=False):
        """Orchestrate the full import."""
        with self.driver.session() as session:
            if clear:
                print("\nClearing existing SEND Support data...")
                self.clear(session)

            # Step 1: NeedArea nodes (must exist before TAGGED_AS and COMMONLY_USED_FOR)
            self.import_need_areas(session)

            # Step 2: AccessRequirement nodes + TAGGED_AS relationships
            self.import_access_requirements(session)

            # Step 3: SupportStrategy nodes + MITIGATES + COMMONLY_USED_FOR + cross-layer links
            self.import_support_strategies(session)

            # Step 4: Concept -> AccessRequirement links
            self.import_concept_support_links(session)

        self._print_stats()

    def _print_stats(self):
        print("\n" + "=" * 60)
        print("IMPORT SUMMARY")
        print("=" * 60)
        print(f"  NeedArea nodes:             {self.stats['need_area_nodes']}")
        print(f"  AccessRequirement nodes:    {self.stats['access_requirement_nodes']}")
        print(f"  SupportStrategy nodes:      {self.stats['support_strategy_nodes']}")
        print(f"  TAGGED_AS rels:             {self.stats['tagged_as_rels']}")
        print(f"  MITIGATES rels:             {self.stats['mitigates_rels']}")
        print(f"  COMMONLY_USED_FOR rels:     {self.stats['commonly_used_for_rels']}")
        print(f"  HAS_ACCESS_REQUIREMENT rels:{self.stats['has_access_requirement_rels']}")
        print(f"  CAN_APPLY rels:             {self.stats['can_apply_rels']}")
        print(f"  ENABLES rels:               {self.stats['enables_rels']}")
        print(f"  SUPPORTED_BY rels:          {self.stats['supported_by_rels']}")
        print(f"  Concept link files:         {self.stats['concept_support_files']}")

        # Print warnings
        skip_keys = [k for k in self.stats if k.startswith("skipped_") and self.stats[k] > 0]
        if skip_keys:
            print()
            for k in skip_keys:
                print(f"  WARN: {k}: {self.stats[k]}")

        total_nodes = (self.stats["need_area_nodes"]
                       + self.stats["access_requirement_nodes"]
                       + self.stats["support_strategy_nodes"])
        total_rels = (self.stats["tagged_as_rels"]
                      + self.stats["mitigates_rels"]
                      + self.stats["commonly_used_for_rels"]
                      + self.stats["has_access_requirement_rels"]
                      + self.stats["can_apply_rels"]
                      + self.stats["enables_rels"]
                      + self.stats["supported_by_rels"])
        print(f"\n  Total nodes:         {total_nodes}")
        print(f"  Total relationships: {total_rels}")
        print("\nDone.")


def main():
    parser = argparse.ArgumentParser(description="Import SEND Support layer into Neo4j")
    parser.add_argument("--clear", action="store_true",
                        help="Clear existing SEND Support data before import")
    args = parser.parse_args()

    print("=" * 60)
    print("SEND Support Importer")
    print("=" * 60)
    print(f"\nConnecting to Neo4j at {NEO4J_URI}...")

    importer = SendSupportImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
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

#!/usr/bin/env python3
"""
Import epistemic skills into Neo4j
Graph Model v3.2 — epistemic skills extension

Adds a layer of discipline-specific thinking skills to the curriculum graph:
  Programme -[DEVELOPS_SKILL]-> <SkillType>
  <SkillType> -[PROGRESSION_OF]-> <SkillType>  (within the same skill type)
  ContentDomainCode -[ASSESSES_SKILL]-> ReadingSkill  (for coded reading skills)

Six skill node types are supported, each sourced from a JSON file in
data/extractions/epistemic-skills/:

  WorkingScientifically   — Science KS1/KS2/KS3 enquiry skills
  ReadingSkill            — English reading comprehension skills (with STA codes)
  HistoricalThinking      — History second-order disciplinary concepts
  MathematicalReasoning   — Mathematics fluency, reasoning and problem-solving skills
  GeographicalSkill       — Geography skills and fieldwork skills
  ComputationalThinking   — Computing computational thinking pillars

Graph model v3.2 — epistemic skills extension.
"""

from neo4j import GraphDatabase
import json
from pathlib import Path

# Updated to use shared config
# Updated to use shared config
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

PROJECT_ROOT = Path(__file__).parent.parent
EPISTEMIC_SKILLS_DIR = PROJECT_ROOT / "data" / "extractions" / "epistemic-skills"

# Optional fields that may or may not be present in a skill record
OPTIONAL_FIELDS = ("nc_verbatim", "test_code", "strand", "second_order", "paper")


class EpistemicSkillsImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            "nodes_created": 0,
            "progression_of": 0,
            "develops_skill": 0,
            "assesses_skill": 0,
        }

    def close(self):
        self.driver.close()

    # -------------------------------------------------------------------------
    # Node creation
    # -------------------------------------------------------------------------

    def create_skill_nodes(self, session, node_type, skills):
        """
        MERGE each skill node with the given node_type label.
        Core properties are always SET; optional properties are SET only when
        present and non-null in the source record.
        """
        # Build Cypher dynamically so that a single query handles all node types.
        # The label is injected as a literal because Neo4j does not support
        # parameterised labels.
        query = f"""
        MERGE (s:{node_type} {{skill_id: $skill_id}})
        SET s.skill_name = $skill_name,
            s.description = $description,
            s.key_stage = $key_stage,
            s.complexity_level = $complexity_level,
            s.source_reference = $source_reference,
            s.subject = $subject
        RETURN s
        """

        # Queries to SET individual optional properties (only called when present)
        optional_set_queries = {
            field: f"""
            MATCH (s:{node_type} {{skill_id: $skill_id}})
            SET s.{field} = $value
            """
            for field in OPTIONAL_FIELDS
        }

        for skill in skills:
            result = session.run(
                query,
                skill_id=skill["skill_id"],
                skill_name=skill["skill_name"],
                description=skill.get("description", ""),
                key_stage=skill.get("key_stage"),
                complexity_level=skill.get("complexity_level", 0),
                source_reference=skill.get("source_reference", ""),
                subject=skill.get("_subject", ""),
            )
            if result.single():
                self.stats["nodes_created"] += 1

            # SET optional fields if present and non-null
            for field in OPTIONAL_FIELDS:
                if field in skill and skill[field] is not None:
                    session.run(
                        optional_set_queries[field],
                        skill_id=skill["skill_id"],
                        value=skill[field],
                    )

    # -------------------------------------------------------------------------
    # PROGRESSION_OF relationships
    # -------------------------------------------------------------------------

    def create_progression_relationships(self, session, node_type, skills):
        """
        For each skill with a non-null progression_to value, create a
        PROGRESSION_OF relationship from that skill to the target skill.
        Both ends of the relationship are matched by skill_id on the same label.
        """
        query = f"""
        MATCH (a:{node_type} {{skill_id: $from_id}})
        MATCH (b:{node_type} {{skill_id: $to_id}})
        MERGE (a)-[:PROGRESSION_OF]->(b)
        RETURN a, b
        """

        for skill in skills:
            to_id = skill.get("progression_to")
            if not to_id:
                continue
            result = session.run(query, from_id=skill["skill_id"], to_id=to_id)
            if result.single():
                self.stats["progression_of"] += 1

    # -------------------------------------------------------------------------
    # DEVELOPS_SKILL relationships (Programme -> skill)
    # -------------------------------------------------------------------------

    def create_develops_skill_relationships(self, session, node_type, subject):
        """
        Link every Programme node whose subject_name matches the skill file's
        subject to every skill node of the given type via DEVELOPS_SKILL.
        This is done in a single Cypher query per skill type.
        """
        query = f"""
        MATCH (p:Programme)
        WHERE p.subject_name = $subject
        MATCH (s:{node_type})
        MERGE (p)-[:DEVELOPS_SKILL]->(s)
        RETURN count(p) AS matched_programmes
        """

        result = session.run(query, subject=subject)
        record = result.single()
        if record:
            self.stats["develops_skill"] += record["matched_programmes"]

    # -------------------------------------------------------------------------
    # ASSESSES_SKILL relationships (ContentDomainCode -> ReadingSkill)
    # -------------------------------------------------------------------------

    def create_assesses_skill_relationships(self, session, skills):
        """
        For ReadingSkill nodes that carry a non-null test_code, link the
        matching ContentDomainCode node (matched by its code property) to the
        skill via an ASSESSES_SKILL relationship.
        """
        query = """
        MATCH (code:ContentDomainCode {code: $test_code})
        MATCH (s:ReadingSkill {skill_id: $skill_id})
        MERGE (code)-[:ASSESSES_SKILL]->(s)
        RETURN code
        """

        for skill in skills:
            test_code = skill.get("test_code")
            if not test_code:
                continue
            result = session.run(
                query,
                test_code=test_code,
                skill_id=skill["skill_id"],
            )
            if result.single():
                self.stats["assesses_skill"] += 1
            else:
                print(f"    ! ContentDomainCode not found for test_code '{test_code}' "
                      f"(skill {skill['skill_id']})")

    # -------------------------------------------------------------------------
    # Import a single JSON file
    # -------------------------------------------------------------------------

    def import_file(self, session, data):
        """Import one epistemic-skills JSON file."""
        metadata = data.get("metadata", {})
        node_type = metadata.get("node_type", "")
        subject = metadata.get("subject", "")

        if not node_type:
            print("  ! Skipping file: missing metadata.node_type")
            return

        skills = data.get("skills", [])
        if not skills:
            print(f"  ! No skills found for node_type '{node_type}' — skipping")
            return

        print(f"\n  Importing: {node_type} ({subject}) — {len(skills)} skills")

        # Stamp each skill record with the file-level subject so the node
        # creation query can write it as a property without extra lookups.
        for skill in skills:
            skill["_subject"] = subject

        # 1. Create / merge skill nodes
        self.create_skill_nodes(session, node_type, skills)
        print(f"    + {len(skills)} {node_type} nodes merged")

        # 2. PROGRESSION_OF relationships
        self.create_progression_relationships(session, node_type, skills)

        # 3. DEVELOPS_SKILL relationships from Programme nodes
        self.create_develops_skill_relationships(session, node_type, subject)

        # 4. ASSESSES_SKILL relationships (ReadingSkill only)
        if node_type == "ReadingSkill":
            self.create_assesses_skill_relationships(session, skills)

    # -------------------------------------------------------------------------
    # Main entry point
    # -------------------------------------------------------------------------

    def import_all(self):
        print("\n" + "=" * 60)
        print("IMPORTING EPISTEMIC SKILLS DATA")
        print("=" * 60)

        if not EPISTEMIC_SKILLS_DIR.exists():
            print(f"! Epistemic skills directory not found: {EPISTEMIC_SKILLS_DIR}")
            return

        json_files = sorted(EPISTEMIC_SKILLS_DIR.glob("*.json"))
        if not json_files:
            print(f"! No JSON files found in {EPISTEMIC_SKILLS_DIR}")
            return

        with self.driver.session() as session:
            for json_file in json_files:
                try:
                    with open(json_file) as f:
                        data = json.load(f)
                    self.import_file(session, data)
                except Exception as e:
                    print(f"  ! Error importing {json_file.name}: {e}")
                    import traceback
                    traceback.print_exc()

        print("\n" + "=" * 60)
        print("IMPORT SUMMARY")
        print("=" * 60)
        for key, value in self.stats.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        print("=" * 60)


def main():
    print("UK Curriculum Knowledge Graph — Epistemic Skills Importer")
    importer = EpistemicSkillsImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    try:
        importer.import_all()
    except Exception as e:
        print(f"\nImport failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        importer.close()
    print("\nImport complete!")


if __name__ == "__main__":
    main()

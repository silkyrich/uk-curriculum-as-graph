#!/usr/bin/env python3
"""
Import VehicleTemplate nodes and TEMPLATE_FOR age-banded prompt relationships.

Creates one :VehicleTemplate node per template definition with all properties
including agent_prompt, session_structure, display styling, and provenance fields.

Also creates TEMPLATE_FOR relationships to KeyStage nodes with age-banded
agent_prompt and question_stems (mirrors ThinkingLens PROMPT_FOR pattern).

Usage:
  python3 layers/topic-suggestions/scripts/import_vehicle_templates.py
  python3 layers/topic-suggestions/scripts/import_vehicle_templates.py --clear
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / "core" / "scripts"))

from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

DATA_DIR = PROJECT_ROOT / "layers" / "topic-suggestions" / "data"
TEMPLATES_FILE = DATA_DIR / "vehicle_templates.json"
KS_PROMPTS_FILE = DATA_DIR / "vehicle_template_ks_prompts.json"


class VehicleTemplateImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def clear(self):
        """Remove all VehicleTemplate nodes and TEMPLATE_FOR relationships."""
        with self.driver.session() as session:
            result = session.run(
                "MATCH (vt:VehicleTemplate) DETACH DELETE vt RETURN count(vt) AS deleted"
            )
            deleted = result.single()["deleted"]
            print(f"  Cleared {deleted} VehicleTemplate nodes.")

    def run(self, clear=False):
        with open(TEMPLATES_FILE) as f:
            templates = json.load(f)

        print("=" * 60)
        print("Import: VehicleTemplate nodes")
        print("=" * 60)

        if clear:
            print("\n--clear flag: removing existing VehicleTemplate nodes...")
            self.clear()

        print(f"\nLoading {len(templates)} template definitions from {TEMPLATES_FILE.name}")

        created = 0
        with self.driver.session() as session:
            for tpl in templates:
                session.execute_write(self._merge_template, tpl)
                created += 1
                print(f"  ✓ {tpl['template_id']} — {tpl['name']}")

        # ── Age-banded prompts (TEMPLATE_FOR relationships) ────────────
        prompt_count = 0
        if KS_PROMPTS_FILE.exists():
            with open(KS_PROMPTS_FILE) as f:
                ks_prompts = json.load(f)
            print(f"\nLoading {len(ks_prompts)} age-banded prompts from {KS_PROMPTS_FILE.name}")
            with self.driver.session() as session:
                for entry in ks_prompts:
                    session.execute_write(self._merge_template_for, entry)
                    prompt_count += 1
            print(f"  ✓ {prompt_count} TEMPLATE_FOR relationships created/updated.")
        else:
            print(f"\n  (no {KS_PROMPTS_FILE.name} found — skipping age-banded prompts)")

        print(f"\nDone. {created} VehicleTemplate nodes, {prompt_count} TEMPLATE_FOR relationships.")

    @staticmethod
    def _merge_template(tx, tpl):
        tx.run("""
            MERGE (vt:VehicleTemplate {template_id: $template_id})
            SET vt.name                    = $name,
                vt.template_type           = $template_type,
                vt.description             = $description,
                vt.session_structure       = $session_structure,
                vt.assessment_approach     = $assessment_approach,
                vt.agent_prompt            = $agent_prompt,
                vt.typical_duration_lessons = $typical_duration_lessons,
                vt.subjects                = $subjects,
                vt.key_stages              = $key_stages,
                vt.display_category        = $display_category,
                vt.display_color           = $display_color,
                vt.display_icon            = $display_icon
        """,
            template_id=tpl["template_id"],
            name=tpl["name"],
            template_type=tpl["template_type"],
            description=tpl["description"],
            session_structure=tpl["session_structure"],
            assessment_approach=tpl["assessment_approach"],
            agent_prompt=tpl["agent_prompt"],
            typical_duration_lessons=tpl["typical_duration_lessons"],
            subjects=tpl["subjects"],
            key_stages=tpl["key_stages"],
            display_category=tpl["display_category"],
            display_color=tpl["display_color"],
            display_icon=tpl["display_icon"],
        )

    @staticmethod
    def _merge_template_for(tx, entry):
        tx.run("""
            MATCH (vt:VehicleTemplate {template_id: $template_id})
            MATCH (ks:KeyStage {key_stage_id: $key_stage})
            MERGE (vt)-[r:TEMPLATE_FOR]->(ks)
            SET r.agent_prompt   = $agent_prompt,
                r.question_stems = $question_stems
        """,
            template_id=entry["template_id"],
            key_stage=entry["key_stage"],
            agent_prompt=entry["agent_prompt"],
            question_stems=entry["question_stems"],
        )


def main():
    clear = "--clear" in sys.argv
    importer = VehicleTemplateImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
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

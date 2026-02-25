#!/usr/bin/env python3
"""
Generate ContentVehicle JSON drafts from graph data.

Reads concepts, topics, and domain context from Neo4j, then generates
rich ContentVehicle definitions per subject/key-stage combination.

Output: JSON files in layers/content-vehicles/data/ ready for human review
and import via import_content_vehicles.py.

Usage:
    python3 generate_content_vehicles.py --subject History --key-stage KS2
    python3 generate_content_vehicles.py --subject Science --key-stage KS2
    python3 generate_content_vehicles.py --list   # show available subject/KS combos
"""

from neo4j import GraphDatabase
import json
import argparse
from pathlib import Path
from datetime import date
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "core" / "scripts"))
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

LAYER_ROOT = Path(__file__).parent.parent
DATA_DIR = LAYER_ROOT / "data"

# Vehicle type mapping by subject
VEHICLE_TYPE_MAP = {
    "History": "topic_study",
    "Geography": "case_study",
    "Science": "investigation",
    "English": "text_study",
    "Mathematics": "worked_example_set",
}

# Subject-specific property templates for the generation prompt
SUBJECT_PROMPTS = {
    "History": """For each History vehicle, include:
- period: time period covered (e.g. "43 AD - 410 AD")
- key_figures: list of important people
- key_events: list of key events with dates
- sources: list of primary/secondary sources
- source_types: list matching sources (e.g. "primary written", "museum artefact")
- perspectives: list of viewpoints to explore""",

    "Geography": """For each Geography vehicle, include:
- location: specific place(s) studied
- data_points: key statistics and facts
- themes: geographical themes explored
- contrasting_with: vehicle_id of contrasting case (if applicable, else null)
- map_types: types of maps/visualisations used
- data_sources: organisations/datasets referenced""",

    "Science": """For each Science vehicle, include:
- enquiry_type: one of fair_test, observation, pattern_seeking, research, identifying_and_classifying
- variables_independent: what is changed
- variables_dependent: what is measured
- variables_controlled: list of what is kept the same
- equipment: list of equipment needed
- recording_format: how results are recorded (e.g. "table -> bar chart -> conclusion")
- safety_notes: safety considerations
- expected_outcome: what the investigation should show""",

    "English": """For each English vehicle, include:
- genre: text genre (e.g. "adventure narrative", "persuasive letter")
- text_features: list of key genre features
- suggested_texts: list of model texts (author + title)
- reading_level: target year group
- writing_outcome: what pupils produce
- grammar_focus: list of grammar features practised""",

    "Mathematics": """For each Maths vehicle, include:
- cpa_stage: progression (e.g. "concrete -> pictorial -> abstract")
- manipulatives: list of physical resources
- representations: list of visual models
- difficulty_levels: list of progression levels
- common_errors: list of typical mistakes""",
}


def query_concepts_for_subject_ks(driver, subject: str, key_stage: str) -> list[dict]:
    """Pull all concepts for a subject/KS with their domain info."""
    with driver.session() as session:
        records = session.run(
            """
            MATCH (p:Programme)-[:HAS_CONCEPT]->(c:Concept)
            MATCH (d:Domain)-[:HAS_CONCEPT]->(c)
            WHERE p.subject_name = $subject AND p.key_stage = $key_stage
            RETURN c.concept_id AS concept_id,
                   c.concept_name AS concept_name,
                   c.description AS description,
                   c.concept_type AS concept_type,
                   c.teaching_guidance AS teaching_guidance,
                   c.key_vocabulary AS key_vocabulary,
                   c.common_misconceptions AS common_misconceptions,
                   d.domain_id AS domain_id,
                   d.domain_name AS domain_name
            ORDER BY d.domain_id, c.concept_id
            """,
            subject=subject,
            key_stage=key_stage,
        )
        return [dict(r) for r in records]


def query_topics_for_subject_ks(driver, subject: str, key_stage: str) -> list[dict]:
    """Pull topics and their taught concepts for a subject/KS."""
    with driver.session() as session:
        records = session.run(
            """
            MATCH (t:Topic)
            WHERE t.subject = $subject AND t.key_stage = $key_stage
            OPTIONAL MATCH (t)-[:TEACHES]->(c:Concept)
            RETURN t.topic_id AS topic_id,
                   t.topic_name AS topic_name,
                   t.topic_type AS topic_type,
                   t.curriculum_note AS curriculum_note,
                   collect(c.concept_id) AS concept_ids
            ORDER BY t.topic_id
            """,
            subject=subject,
            key_stage=key_stage,
        )
        return [dict(r) for r in records]


def query_difficulty_levels(driver, subject: str, key_stage: str) -> dict[str, list[dict]]:
    """Pull difficulty levels for all concepts in a subject/KS, keyed by concept_id."""
    with driver.session() as session:
        records = session.run(
            """
            MATCH (p:Programme)-[:HAS_CONCEPT]->(c:Concept)
                  -[:HAS_DIFFICULTY_LEVEL]->(dl:DifficultyLevel)
            WHERE p.subject_name = $subject AND p.key_stage = $key_stage
            RETURN c.concept_id AS concept_id,
                   dl.level_number AS level_number,
                   dl.label AS label,
                   dl.description AS description,
                   dl.example_task AS example_task
            ORDER BY c.concept_id, dl.level_number
            """,
            subject=subject,
            key_stage=key_stage,
        )
        dl_map: dict[str, list[dict]] = {}
        for r in records:
            cid = r["concept_id"]
            if cid not in dl_map:
                dl_map[cid] = []
            dl_map[cid].append({
                "level_number": r["level_number"],
                "label": r["label"],
                "description": r["description"],
                "example_task": r["example_task"],
            })
        return dl_map


def query_available_combinations(driver) -> list[dict]:
    """List all subject/KS combinations that have concepts."""
    with driver.session() as session:
        records = session.run(
            """
            MATCH (p:Programme)-[:HAS_CONCEPT]->(c:Concept)
            RETURN p.subject_name AS subject, p.key_stage AS key_stage,
                   count(c) AS concept_count
            ORDER BY p.subject_name, p.key_stage
            """
        )
        return [dict(r) for r in records]


def build_generation_context(concepts: list[dict], topics: list[dict],
                             subject: str, key_stage: str,
                             difficulty_levels: dict[str, list[dict]] | None = None) -> str:
    """Build a context string for LLM generation."""
    dl_map = difficulty_levels or {}
    lines = [
        f"# Content Vehicle Generation Context",
        f"Subject: {subject}, Key Stage: {key_stage}",
        f"",
        f"## Concepts ({len(concepts)} total)",
    ]

    # Group concepts by domain
    by_domain: dict[str, list] = {}
    for c in concepts:
        did = c["domain_id"]
        if did not in by_domain:
            by_domain[did] = {"domain_name": c["domain_name"], "concepts": []}
        by_domain[did]["concepts"].append(c)

    for did, info in by_domain.items():
        lines.append(f"\n### Domain: {info['domain_name']} ({did})")
        for c in info["concepts"]:
            lines.append(f"- {c['concept_id']}: {c['concept_name']} ({c['concept_type']})")
            if c.get("description"):
                lines.append(f"  Description: {c['description'][:200]}")
            if c.get("teaching_guidance"):
                lines.append(f"  Teaching guidance: {c['teaching_guidance'][:200]}")
            # Difficulty levels for this concept
            cid = c["concept_id"]
            if cid in dl_map:
                lines.append(f"  Difficulty levels:")
                for dl in dl_map[cid]:
                    lines.append(f"    {dl['level_number']}. {dl['label'].replace('_', ' ').title()}: "
                                 f"{dl['description']} — e.g. \"{dl['example_task']}\"")

    if topics:
        lines.append(f"\n## Topics ({len(topics)} total)")
        for t in topics:
            lines.append(f"- {t['topic_id']}: {t['topic_name']}")
            if t.get("curriculum_note"):
                lines.append(f"  NC note: {t['curriculum_note'][:200]}")
            if t.get("concept_ids"):
                lines.append(f"  Teaches: {', '.join(t['concept_ids'])}")

    return "\n".join(lines)


def build_generation_prompt(context: str, subject: str, key_stage: str) -> str:
    """Build the full prompt for LLM vehicle generation."""
    vehicle_type = VEHICLE_TYPE_MAP.get(subject, "general")
    subject_specific = SUBJECT_PROMPTS.get(subject, "")

    return f"""{context}

---

# Task

Generate ContentVehicle definitions for {subject} {key_stage}.

Each vehicle should:
1. Have a clear, teacher-friendly name
2. Deliver 1-4 specific concepts (use concept_ids from above)
3. Include definitions (key vocabulary), assessment_guidance, and success_criteria
4. Include subject-specific properties as detailed below
5. Link to an existing Topic via implements_topic_id where there is a natural match
6. Where difficulty levels are provided for a concept, align the vehicle's progression
   and assessment to those levels (entry → developing → expected → greater depth)

Vehicle type: `{vehicle_type}`

{subject_specific}

## Output Format

Return a JSON array of vehicle objects. Each vehicle must have:
- vehicle_id: "{subject[:2].upper()}-{key_stage}-CV###" (sequential numbering)
- name: clear, teacher-friendly title
- vehicle_type: "{vehicle_type}"
- description: 1-2 sentences on what this pack covers
- delivers_concept_ids: list of concept IDs this vehicle delivers
- implements_topic_id: topic_id if matching a topic above, else omit
- definitions: list of key terms
- assessment_guidance: paragraph on how to assess through this vehicle
- success_criteria: list of observable outcomes
- Plus all subject-specific properties listed above

Generate vehicles that collectively cover ALL concepts listed above, with
some concepts delivered by multiple vehicles (teacher choice). Aim for
roughly 1 vehicle per 2-4 concepts.
"""


def generate_stub_json(subject: str, key_stage: str,
                       concepts: list[dict], topics: list[dict]) -> dict:
    """Generate a stub JSON file structure (without LLM — for manual completion)."""
    safe_subject = subject.lower().replace(" ", "_")

    # Determine year for the filename
    ks_year_map = {"KS1": "ks1", "KS2": "ks2", "KS3": "ks3", "KS4": "ks4"}
    ks_label = ks_year_map.get(key_stage, key_stage.lower())

    return {
        "version": "1.0",
        "subject": subject,
        "key_stage": key_stage,
        "authored_by": "llm-draft",
        "authored_date": date.today().isoformat(),
        "note": f"Content vehicles for {key_stage} {subject}. Generated stub — needs LLM completion and human review.",
        "vehicles": [],
    }


def main():
    parser = argparse.ArgumentParser(
        description="Generate ContentVehicle JSON drafts from graph data"
    )
    parser.add_argument("--subject", type=str, help="Subject name (e.g. History)")
    parser.add_argument("--key-stage", type=str, help="Key stage (e.g. KS2)")
    parser.add_argument("--list", action="store_true",
                        help="List available subject/KS combinations")
    parser.add_argument("--context-only", action="store_true",
                        help="Print generation context without generating")
    parser.add_argument("--stub", action="store_true",
                        help="Generate stub JSON (no LLM, for manual completion)")
    args = parser.parse_args()

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    try:
        if args.list:
            combos = query_available_combinations(driver)
            print(f"{'Subject':<25} {'Key Stage':<10} {'Concepts':>8}")
            print("-" * 50)
            for c in combos:
                print(f"{c['subject']:<25} {c['key_stage']:<10} {c['concept_count']:>8}")
            return

        if not args.subject or not args.key_stage:
            parser.error("--subject and --key-stage are required (or use --list)")

        concepts = query_concepts_for_subject_ks(driver, args.subject, args.key_stage)
        topics = query_topics_for_subject_ks(driver, args.subject, args.key_stage)
        dl_map = query_difficulty_levels(driver, args.subject, args.key_stage)

        dl_count = sum(len(v) for v in dl_map.values())
        print(f"Found {len(concepts)} concepts, {len(topics)} topics, "
              f"and {dl_count} difficulty levels for {args.subject} {args.key_stage}")

        context = build_generation_context(concepts, topics, args.subject, args.key_stage,
                                           difficulty_levels=dl_map)

        if args.context_only:
            print(context)
            return

        if args.stub:
            stub = generate_stub_json(args.subject, args.key_stage, concepts, topics)
            safe_name = f"{args.subject.lower().replace(' ', '_')}_{args.key_stage.lower()}.json"
            out_path = DATA_DIR / safe_name
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            with open(out_path, "w") as f:
                json.dump(stub, f, indent=2, ensure_ascii=False)
            print(f"Stub written to {out_path}")
            return

        # Full generation mode: print prompt for LLM
        prompt = build_generation_prompt(context, args.subject, args.key_stage)
        print("\n" + "=" * 60)
        print("GENERATION PROMPT (paste into Claude or use API)")
        print("=" * 60)
        print(prompt)

    finally:
        driver.close()


if __name__ == "__main__":
    main()

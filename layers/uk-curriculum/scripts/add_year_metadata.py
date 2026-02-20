#!/usr/bin/env python3
"""
Add age-appropriate interaction metadata to Year nodes in the Neo4j graph.

Properties added to each Year node:
  - age_min, age_max
  - interaction_modes (list)
  - interface_style
  - input_primary, input_secondary
  - ui_density
  - ai_prompt_guidance
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "core" / "scripts"))

from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, NEO4J_DATABASE

YEAR_METADATA = {
    "Y1": {
        "age_min": 5,
        "age_max": 6,
        "interaction_modes": ["voice", "tap"],
        "interface_style": "Large illustrated minimal text",
        "input_primary": "voice",
        "input_secondary": "tap",
        "ui_density": "minimal",
        "ai_prompt_guidance": (
            "Use simple voiced questions with large tap targets; "
            "avoid reading text aloud to the child; use pictures and sounds"
        ),
    },
    "Y2": {
        "age_min": 6,
        "age_max": 7,
        "interaction_modes": ["voice", "tap", "drag"],
        "interface_style": "Illustrated with simple sentences",
        "input_primary": "voice",
        "input_secondary": "tap",
        "ui_density": "simple",
        "ai_prompt_guidance": (
            "Combine voice prompts with simple illustrated choices; "
            "sentences should be one clause; celebrate with audio feedback"
        ),
    },
    "Y3": {
        "age_min": 7,
        "age_max": 8,
        "interaction_modes": ["voice", "typing-word"],
        "interface_style": "Less illustration more text",
        "input_primary": "voice",
        "input_secondary": "typing-word",
        "ui_density": "simple",
        "ai_prompt_guidance": (
            "Voice remains primary; accept single-word typed answers; "
            "reduce decoration and increase readable text"
        ),
    },
    "Y4": {
        "age_min": 8,
        "age_max": 9,
        "interaction_modes": ["voice", "typing-phrase"],
        "interface_style": "Transitional to text-heavy",
        "input_primary": "voice",
        "input_secondary": "typing-phrase",
        "ui_density": "transitional",
        "ai_prompt_guidance": (
            "Encourage short typed phrases; voice support still expected; "
            "sentences can be multi-clause"
        ),
    },
    "Y5": {
        "age_min": 9,
        "age_max": 10,
        "interaction_modes": ["typing", "voice"],
        "interface_style": "Text-heavy cleaner design",
        "input_primary": "typing",
        "input_secondary": "voice",
        "ui_density": "standard",
        "ai_prompt_guidance": (
            "Default to typed input; provide voice as fallback; "
            "use clean text-first UI with minimal illustration"
        ),
    },
    "Y6": {
        "age_min": 10,
        "age_max": 11,
        "interaction_modes": ["typing", "voice"],
        "interface_style": "Mature interface more density",
        "input_primary": "typing",
        "input_secondary": "voice",
        "ui_density": "standard",
        "ai_prompt_guidance": (
            "Typing is default; treat as capable readers; "
            "interface can be denser and more information-rich"
        ),
    },
    "Y7": {
        "age_min": 11,
        "age_max": 12,
        "interaction_modes": ["typing", "voice"],
        "interface_style": "Mature text interface",
        "input_primary": "typing",
        "input_secondary": "voice",
        "ui_density": "standard",
        "ai_prompt_guidance": (
            "Full text interface expected; voice optional for accessibility; "
            "can handle multi-step instructions"
        ),
    },
    "Y8": {
        "age_min": 12,
        "age_max": 13,
        "interaction_modes": ["typing"],
        "interface_style": "Dense text complex UI acceptable",
        "input_primary": "typing",
        "input_secondary": "none",
        "ui_density": "dense",
        "ai_prompt_guidance": (
            "Text-first sophisticated interface; multi-paragraph explanations acceptable; "
            "encourage analytical responses"
        ),
    },
    "Y9": {
        "age_min": 13,
        "age_max": 14,
        "interaction_modes": ["typing"],
        "interface_style": "Sophisticated adult-like interface",
        "input_primary": "typing",
        "input_secondary": "none",
        "ui_density": "dense",
        "ai_prompt_guidance": (
            "Adult-equivalent interface; nuanced explanations and "
            "debate-style prompts appropriate"
        ),
    },
    "Y10": {
        "age_min": 14,
        "age_max": 15,
        "interaction_modes": ["typing"],
        "interface_style": "Adult interface",
        "input_primary": "typing",
        "input_secondary": "none",
        "ui_density": "dense",
        "ai_prompt_guidance": (
            "Full adult interface; exam-style questioning; "
            "abstract reasoning and extended writing expected"
        ),
    },
    "Y11": {
        "age_min": 15,
        "age_max": 16,
        "interaction_modes": ["typing"],
        "interface_style": "Adult interface",
        "input_primary": "typing",
        "input_secondary": "none",
        "ui_density": "dense",
        "ai_prompt_guidance": (
            "Full adult interface; exam preparation context; "
            "formal academic language appropriate"
        ),
    },
}

CYPHER = """
MATCH (y:Year {name: $name})
SET y.age_min          = $age_min,
    y.age_max          = $age_max,
    y.interaction_modes = $interaction_modes,
    y.interface_style  = $interface_style,
    y.input_primary    = $input_primary,
    y.input_secondary  = $input_secondary,
    y.ui_density       = $ui_density,
    y.ai_prompt_guidance = $ai_prompt_guidance
RETURN y.name AS updated
"""


def main():
    print("Connecting to Neo4j...")
    driver_kwargs = {"auth": (NEO4J_USER, NEO4J_PASSWORD)}
    if NEO4J_DATABASE:
        driver_kwargs["database"] = NEO4J_DATABASE

    driver = GraphDatabase.driver(NEO4J_URI, **driver_kwargs)

    updated_count = 0
    skipped = []

    with driver.session(database=NEO4J_DATABASE) as session:
        for year_name, props in YEAR_METADATA.items():
            result = session.run(
                CYPHER,
                name=year_name,
                age_min=props["age_min"],
                age_max=props["age_max"],
                interaction_modes=props["interaction_modes"],
                interface_style=props["interface_style"],
                input_primary=props["input_primary"],
                input_secondary=props["input_secondary"],
                ui_density=props["ui_density"],
                ai_prompt_guidance=props["ai_prompt_guidance"],
            )
            record = result.single()
            if record:
                print(f"  [tick] {year_name} updated (ages {props['age_min']}-{props['age_max']})")
                updated_count += 1
            else:
                print(f"  [skip] {year_name} - no matching Year node found")
                skipped.append(year_name)

    driver.close()

    print()
    print(f"Summary: {updated_count} Year node(s) updated.")
    if skipped:
        print(f"  Skipped (not found): {', '.join(skipped)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Orchestrate import of all knowledge graph layers in the correct order

Usage:
  python3 core/scripts/import_all.py                    # Import all layers
  python3 core/scripts/import_all.py --skip-case        # Skip CASE layer
  python3 core/scripts/import_all.py --skip-oak         # Skip Oak layer
  python3 core/scripts/import_all.py --only uk-curriculum  # Only UK curriculum
"""

import sys
import subprocess
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent

# Layer import scripts in dependency order
LAYERS = {
    "uk-curriculum": {
        "name": "UK Curriculum (Foundation)",
        "script": PROJECT_ROOT / "layers" / "uk-curriculum" / "scripts" / "import_curriculum.py",
        "depends_on": [],
    },
    "assessment": {
        "name": "Assessment (Test Frameworks)",
        "script": PROJECT_ROOT / "layers" / "assessment" / "scripts" / "import_test_frameworks.py",
        "depends_on": ["uk-curriculum"],
    },
    "epistemic-skills": {
        "name": "Epistemic Skills",
        "script": PROJECT_ROOT / "layers" / "epistemic-skills" / "scripts" / "import_epistemic_skills.py",
        "depends_on": ["uk-curriculum", "assessment"],
    },
    "eyfs": {
        "name": "EYFS (Early Years Foundation Stage)",
        "script": PROJECT_ROOT / "layers" / "eyfs" / "scripts" / "import_eyfs.py",
        "depends_on": ["uk-curriculum"],
    },
    "enrichment": {
        "name": "Concept Grouping Signals (migration)",
        "script": PROJECT_ROOT / "core" / "migrations" / "compute_lesson_grouping_signals.py",
        "depends_on": ["uk-curriculum"],
    },
    "thinking-lenses": {
        "name": "Thinking Lenses",
        "script": PROJECT_ROOT / "layers" / "uk-curriculum" / "scripts" / "import_thinking_lenses.py",
        "depends_on": ["uk-curriculum"],
    },
    "concept-clusters": {
        "name": "Concept Clusters (generated)",
        "script": PROJECT_ROOT / "layers" / "uk-curriculum" / "scripts" / "generate_concept_clusters.py",
        "depends_on": ["uk-curriculum", "enrichment", "thinking-lenses"],
    },
    "difficulty-levels": {
        "name": "Difficulty Levels",
        "script": PROJECT_ROOT / "layers" / "uk-curriculum" / "scripts" / "import_difficulty_levels.py",
        "depends_on": ["uk-curriculum", "eyfs"],
    },
    "cross-domain-co-teaches": {
        "name": "Cross-Domain CO_TEACHES (migration)",
        "script": PROJECT_ROOT / "core" / "migrations" / "create_cross_domain_co_teaches.py",
        "depends_on": ["uk-curriculum", "enrichment"],
    },
    "concept-skill-links": {
        "name": "Concept-Level Skill Links (migration)",
        "script": PROJECT_ROOT / "core" / "migrations" / "create_concept_skill_links.py",
        "depends_on": ["uk-curriculum", "epistemic-skills"],
    },
    "vehicle-templates": {
        "name": "Vehicle Templates (pedagogical patterns)",
        "script": PROJECT_ROOT / "layers" / "topic-suggestions" / "scripts" / "import_vehicle_templates.py",
        "depends_on": ["uk-curriculum"],
    },
    "subject-ontologies": {
        "name": "Per-Subject Ontology Nodes",
        "script": PROJECT_ROOT / "layers" / "topic-suggestions" / "scripts" / "import_subject_ontologies.py",
        "depends_on": ["uk-curriculum", "vehicle-templates"],
    },
    "case-standards": {
        "name": "CASE Standards (US/International)",
        "script": PROJECT_ROOT / "layers" / "case-standards" / "scripts" / "import_case_standards_v2.py",
        "depends_on": ["uk-curriculum", "epistemic-skills"],
        "args": ["--import"],  # CASE script requires --import flag
    },
    "oak-content": {
        "name": "Oak National Academy Content",
        "script": PROJECT_ROOT / "layers" / "oak-content" / "scripts" / "import_oak_content.py",
        "depends_on": ["uk-curriculum"],
        "args": ["--import"],  # Oak script requires --import flag
    },
    "learner-profiles": {
        "name": "Learner Profiles (Age-Appropriate Design)",
        "script": PROJECT_ROOT / "layers" / "learner-profiles" / "scripts" / "import_learner_profiles.py",
        "depends_on": ["uk-curriculum"],
    },
    "visualization": {
        "name": "Visualization & Formatting",
        "script": PROJECT_ROOT / "layers" / "visualization" / "scripts" / "apply_formatting.py",
        "depends_on": ["uk-curriculum"],  # Runs after data layers; soft dep on all
    },
}


def run_layer_import(layer_id: str, dry_run: bool = False) -> bool:
    """Run the import script for a single layer. Returns True on success."""
    layer = LAYERS[layer_id]
    script = layer["script"]
    args = layer.get("args", [])

    print("\n" + "=" * 80)
    print(f"IMPORTING: {layer['name']}")
    print("=" * 80)

    if not script.exists():
        print(f"  ⚠️  Script not found: {script}")
        return False

    cmd = [sys.executable, str(script)] + args

    if dry_run:
        print(f"  [DRY RUN] Would run: {' '.join(cmd)}")
        return True

    print(f"  Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)

    if result.returncode == 0:
        print(f"  ✅ {layer['name']} imported successfully")
        return True
    else:
        print(f"  ❌ {layer['name']} import FAILED (exit code {result.returncode})")
        return False


def check_dependencies(layer_id: str, completed: set) -> bool:
    """Check if all dependencies for a layer have been completed."""
    layer = LAYERS[layer_id]
    for dep in layer["depends_on"]:
        if dep not in completed:
            return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Import all knowledge graph layers")
    parser.add_argument("--skip-case", action="store_true", help="Skip CASE Standards layer")
    parser.add_argument("--skip-oak", action="store_true", help="Skip Oak Content layer")
    parser.add_argument("--skip-viz", action="store_true", help="Skip Visualization & Formatting layer")
    parser.add_argument("--only", help="Only import this layer (e.g., 'uk-curriculum')")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be imported without running")

    args = parser.parse_args()

    print("=" * 80)
    print("UK CURRICULUM KNOWLEDGE GRAPH — IMPORT ALL LAYERS")
    print("=" * 80)

    # Determine which layers to import
    if args.only:
        if args.only not in LAYERS:
            print(f"❌ Unknown layer: {args.only}")
            print(f"Available layers: {', '.join(LAYERS.keys())}")
            sys.exit(1)
        layers_to_import = [args.only]
    else:
        layers_to_import = list(LAYERS.keys())
        if args.skip_case:
            layers_to_import.remove("case-standards")
        if args.skip_oak:
            layers_to_import.remove("oak-content")
        if args.skip_viz:
            layers_to_import.remove("visualization")

    print(f"\nLayers to import ({len(layers_to_import)}):")
    for layer_id in layers_to_import:
        deps = LAYERS[layer_id]["depends_on"]
        deps_str = f" (depends on: {', '.join(deps)})" if deps else ""
        print(f"  • {LAYERS[layer_id]['name']}{deps_str}")

    if args.dry_run:
        print("\n[DRY RUN MODE — no imports will be executed]\n")

    # Import layers in dependency order
    completed = set()
    failed = set()

    while layers_to_import:
        # Find a layer whose dependencies are all completed
        ready = [
            lid for lid in layers_to_import
            if check_dependencies(lid, completed)
        ]

        if not ready:
            print("\n❌ Dependency deadlock! Remaining layers:")
            for lid in layers_to_import:
                missing = [d for d in LAYERS[lid]["depends_on"] if d not in completed]
                print(f"  • {lid} — missing: {missing}")
            sys.exit(1)

        # Import the first ready layer
        layer_id = ready[0]

        success = run_layer_import(layer_id, dry_run=args.dry_run)

        layers_to_import.remove(layer_id)

        if success:
            completed.add(layer_id)
        else:
            failed.add(layer_id)
            if not args.dry_run:
                print(f"\n⚠️  {layer_id} import failed. Continue with remaining layers? (y/n)")
                response = input().strip().lower()
                if response != 'y':
                    print("\nAborting import.")
                    sys.exit(1)

    # Summary
    print("\n" + "=" * 80)
    print("IMPORT SUMMARY")
    print("=" * 80)
    print(f"✅ Completed: {len(completed)} layers")
    for lid in completed:
        print(f"   • {LAYERS[lid]['name']}")

    if failed:
        print(f"\n❌ Failed: {len(failed)} layers")
        for lid in failed:
            print(f"   • {LAYERS[lid]['name']}")
        sys.exit(1)
    else:
        print("\n🎉 All layers imported successfully!")
        print("\nNext step:")
        print("  python3 core/scripts/validate_schema.py")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Pre-import validator for topic suggestion JSON files.

Checks vocabulary completeness, statutory decomposition coverage,
assessment item mappings, and other generator-grade spec requirements.

Usage:
    python3 layers/topic-suggestions/scripts/validate_topic_suggestions.py
    python3 layers/topic-suggestions/scripts/validate_topic_suggestions.py --path layers/topic-suggestions/data/computing_studies
"""

import json
import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

VALID_TESTABLE_AS = {
    "define_and_give_example",
    "define_and_distinguish",
    "two_option_contrast",
    "label_diagram",
    "explain_in_own_words",
    "identify_and_correct",
    "evaluate_and_justify",
}

VALID_ASSESSMENT_TYPES = {
    "hinge_true_false_justify",
    "hinge_multiple_choice",
    "two_option_contrast",
    "label_diagram",
    "explain_in_own_words",
    "misconception_probe",
    "evaluate_and_justify",
}


class Issue:
    def __init__(self, severity, file, message):
        self.severity = severity  # ERROR, WARN, INFO
        self.file = file
        self.message = message

    def __str__(self):
        return f"[{self.severity}] {self.file}: {self.message}"


def _extract_entries(data, filename):
    """Extract the list of entries from either bare array or dict-wrapped format."""
    if isinstance(data, list):
        return data, []
    elif isinstance(data, dict):
        for key in ("enquiries", "studies", "units", "suggestions", "entries"):
            if key in data and isinstance(data[key], list):
                return data[key], []
        return [], [Issue("INFO", filename,
                          f"Dict-format file with keys {list(data.keys())[:5]} — no recognised array key")]
    return [], [Issue("ERROR", filename, "Expected top-level JSON array or dict")]


def validate_topic_file(path: Path) -> list[Issue]:
    """Validate a single topic suggestion JSON file."""
    issues = []
    filename = path.name

    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [Issue("ERROR", filename, f"Invalid JSON: {e}")]

    entries, parse_issues = _extract_entries(data, filename)
    if parse_issues:
        return parse_issues

    for entry in entries:
        entry_id = (
            entry.get("suggestion_id")
            or entry.get("study_id")
            or entry.get("enquiry_id")
            or entry.get("unit_id")
            or "(no id)"
        )

        # --- Vocabulary completeness ---
        vocab_mat = entry.get("vocabulary_mat")
        definitions = entry.get("definitions")

        if vocab_mat:
            for item in vocab_mat:
                term = item.get("term", "(no term)")
                defn = item.get("definition", "")
                if not defn or not defn.strip():
                    issues.append(Issue(
                        "ERROR", filename,
                        f"{entry_id}: vocabulary_mat term '{term}' has blank definition"
                    ))
                if not item.get("example_sentence"):
                    issues.append(Issue(
                        "WARN", filename,
                        f"{entry_id}: vocabulary_mat term '{term}' has no example_sentence"
                    ))
        elif definitions:
            # Old format: bare term list without definitions
            issues.append(Issue(
                "WARN", filename,
                f"{entry_id}: uses bare 'definitions' array ({len(definitions)} terms) "
                f"— upgrade to 'vocabulary_mat' with definitions and example sentences"
            ))

        # --- Statutory decomposition ---
        stat_decomp = entry.get("statutory_decomposition")
        curriculum_refs = entry.get("curriculum_reference", [])

        if stat_decomp:
            sd_ids = set()
            for sd in stat_decomp:
                sd_id = sd.get("sd_id", "(no id)")
                if sd_id in sd_ids:
                    issues.append(Issue(
                        "ERROR", filename,
                        f"{entry_id}: duplicate statutory_decomposition sd_id '{sd_id}'"
                    ))
                sd_ids.add(sd_id)

                if not sd.get("requirement"):
                    issues.append(Issue(
                        "ERROR", filename,
                        f"{entry_id}: sd_id '{sd_id}' has no requirement text"
                    ))
        elif curriculum_refs and entry.get("curriculum_status") == "mandatory":
            issues.append(Issue(
                "WARN", filename,
                f"{entry_id}: mandatory topic has curriculum_reference but no "
                f"statutory_decomposition — generator cannot verify coverage"
            ))

        # --- Assessment items ---
        assessment_items = entry.get("assessment_items")
        if assessment_items:
            for i, item in enumerate(assessment_items):
                item_type = item.get("type", "(no type)")
                if item_type not in VALID_ASSESSMENT_TYPES:
                    issues.append(Issue(
                        "WARN", filename,
                        f"{entry_id}: assessment_items[{i}] has unknown type '{item_type}'"
                    ))
                if not item.get("stem"):
                    issues.append(Issue(
                        "ERROR", filename,
                        f"{entry_id}: assessment_items[{i}] has no stem"
                    ))
                if not item.get("expected"):
                    issues.append(Issue(
                        "ERROR", filename,
                        f"{entry_id}: assessment_items[{i}] has no expected response"
                    ))

            # Check misconception coverage
            common_pitfalls = entry.get("common_pitfalls", [])
            misconception_names = {
                item.get("misconception_targeted")
                for item in assessment_items
                if item.get("misconception_targeted")
            }
            # This is INFO level — not all pitfalls are misconceptions
            if common_pitfalls and not misconception_names:
                issues.append(Issue(
                    "INFO", filename,
                    f"{entry_id}: has {len(common_pitfalls)} common_pitfalls but no "
                    f"assessment_items target any misconception"
                ))

    return issues


def validate_vehicle_template_file(path: Path) -> list[Issue]:
    """Validate the vehicle_templates.json file for quality gates."""
    issues = []
    filename = path.name

    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [Issue("ERROR", filename, f"Invalid JSON: {e}")]

    if not isinstance(data, list):
        return [Issue("ERROR", filename, "Expected top-level JSON array")]

    for entry in data:
        template_id = entry.get("template_id", "(no id)")

        quality_gates = entry.get("quality_gates")
        if quality_gates:
            if not isinstance(quality_gates, dict):
                issues.append(Issue(
                    "ERROR", filename,
                    f"{template_id}: quality_gates must be a dict"
                ))

        activity_constraints = entry.get("activity_constraints")
        if activity_constraints:
            for i, constraint in enumerate(activity_constraints):
                if not constraint.get("activity_type"):
                    issues.append(Issue(
                        "ERROR", filename,
                        f"{template_id}: activity_constraints[{i}] has no activity_type"
                    ))
                if not constraint.get("rules"):
                    issues.append(Issue(
                        "ERROR", filename,
                        f"{template_id}: activity_constraints[{i}] has no rules"
                    ))

    return issues


def main():
    parser = argparse.ArgumentParser(
        description="Validate topic suggestion JSON files"
    )
    parser.add_argument(
        "--path", default=None,
        help="Override path to scan (default: layers/topic-suggestions/data)"
    )
    parser.add_argument(
        "--errors-only", action="store_true",
        help="Show ERRORs only"
    )
    args = parser.parse_args()

    scan_path = Path(args.path) if args.path else DATA_DIR
    json_files = sorted(scan_path.rglob("*.json"))

    if not json_files:
        print(f"No JSON files found under {scan_path}")
        sys.exit(1)

    print(f"Validating {len(json_files)} topic suggestion files under {scan_path}")
    print("=" * 60)

    all_issues: list[Issue] = []
    files_with_errors = 0

    for path in json_files:
        if path.name == "vehicle_templates.json":
            file_issues = validate_vehicle_template_file(path)
        elif path.name == "vehicle_template_ks_prompts.json":
            continue  # Separate format, not validated here
        else:
            file_issues = validate_topic_file(path)

        if file_issues:
            files_with_errors += 1
        all_issues.extend(file_issues)

    # Report
    errors = [i for i in all_issues if i.severity == "ERROR"]
    warns = [i for i in all_issues if i.severity == "WARN"]
    infos = [i for i in all_issues if i.severity == "INFO"]

    if args.errors_only:
        display = errors
    else:
        display = all_issues

    for issue in display:
        print(issue)

    print()
    print("=" * 60)
    print(f"Files scanned: {len(json_files)}")
    print(f"Files with issues: {files_with_errors}")
    print(f"  ERRORs: {len(errors)}")
    print(f"  WARNs:  {len(warns)}")
    print(f"  INFOs:  {len(infos)}")

    # Summary of vocabulary_mat adoption
    vocab_mat_count = 0
    bare_definitions_count = 0
    for path in json_files:
        if path.name in ("vehicle_templates.json", "vehicle_template_ks_prompts.json"):
            continue
        try:
            with open(path) as f:
                data = json.load(f)
            entries, _ = _extract_entries(data, path.name)
            for entry in entries:
                if entry.get("vocabulary_mat"):
                    vocab_mat_count += 1
                elif entry.get("definitions"):
                    bare_definitions_count += 1
        except (json.JSONDecodeError, KeyError):
            pass

    print()
    print(f"Vocabulary mat adoption: {vocab_mat_count} upgraded, "
          f"{bare_definitions_count} still using bare definitions")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()

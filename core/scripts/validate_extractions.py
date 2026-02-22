#!/usr/bin/env python3
"""
Pre-import extraction validator.

Run this BEFORE import_curriculum.py to catch data quality issues in
the JSON extraction files. Catches problems that would otherwise only
surface after a full import+validate cycle.

Usage:
    python3 scripts/validate_extractions.py
    python3 scripts/validate_extractions.py --path data/extractions/primary
"""

import json
import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
EXTRACTIONS_DIR = PROJECT_ROOT / "data" / "extractions"

# These mirror the import script's normalization maps so we know
# what will be auto-corrected vs what is a genuine unknown.
KNOWN_CONCEPT_TYPE_FIXUPS = {"concept", "language", "representation"}
VALID_CONCEPT_TYPES = {
    "knowledge", "skill", "process", "attitude", "content",
} | KNOWN_CONCEPT_TYPE_FIXUPS

KNOWN_STRUCTURE_TYPE_FIXUPS = {"skills", "analytical"}
VALID_STRUCTURE_TYPES = {
    "sequential", "hierarchical", "mixed", "exploratory",
    "conceptual", "applied", "knowledge",
    "process", "developmental", "thematic",
} | KNOWN_STRUCTURE_TYPE_FIXUPS

VALID_PREREQ_CONFIDENCE = {"explicit", "inferred", "fuzzy", "suggested"}
VALID_PREREQ_REL_TYPES = {
    "logical", "developmental", "instructional", "temporal", "foundational",
    "cognitive", "enabling", "supportive",
}

OBJECTIVE_TEXT_KEYS = {"objective_text", "statement", "text"}


class ExtractionIssue:
    def __init__(self, severity, file, message):
        self.severity = severity  # ERROR, WARN, INFO
        self.file = file
        self.message = message

    def __str__(self):
        return f"[{self.severity}] {self.file}: {self.message}"


def validate_file(path: Path) -> list[ExtractionIssue]:
    issues = []
    filename = path.name

    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [ExtractionIssue("ERROR", filename, f"Invalid JSON: {e}")]

    metadata = data.get("metadata", {})
    subject = metadata.get("subject", "(unknown)")

    # ---- Objectives --------------------------------------------------------
    objectives = data.get("objectives", [])
    for obj in objectives:
        obj_id = obj.get("objective_id", "(no id)")

        # Check for objective text using all known key variants
        text_keys_present = [k for k in OBJECTIVE_TEXT_KEYS if obj.get(k)]
        if not text_keys_present:
            issues.append(ExtractionIssue(
                "ERROR", filename,
                f"Objective {obj_id} has no text — checked keys: "
                f"{sorted(OBJECTIVE_TEXT_KEYS)}; found keys: {sorted(obj.keys())}",
            ))
        elif "objective_text" not in obj and not obj.get("statement"):
            # Has text but under a non-standard key name — warn so we know
            alt_keys = [k for k in text_keys_present if k not in ("objective_text", "statement")]
            if alt_keys:
                issues.append(ExtractionIssue(
                    "WARN", filename,
                    f"Objective {obj_id} uses non-standard text key(s): {alt_keys} "
                    f"(import will handle, but worth knowing)",
                ))

        if obj.get("is_statutory") is None and obj.get("statutory") is None:
            issues.append(ExtractionIssue(
                "WARN", filename,
                f"Objective {obj_id} has no is_statutory field",
            ))

        if not obj.get("domain_id"):
            issues.append(ExtractionIssue(
                "ERROR", filename,
                f"Objective {obj_id} has no domain_id",
            ))

    # ---- Domains -----------------------------------------------------------
    domains = data.get("domains", [])
    domain_ids = set()
    for domain in domains:
        d_id = domain.get("domain_id", "(no id)")
        domain_ids.add(d_id)

        if not domain.get("domain_name") and not domain.get("name"):
            issues.append(ExtractionIssue(
                "WARN", filename,
                f"Domain {d_id} has no domain_name",
            ))

        struct = domain.get("structure_type")
        if struct and struct not in VALID_STRUCTURE_TYPES:
            issues.append(ExtractionIssue(
                "WARN", filename,
                f"Domain {d_id} has unknown structure_type '{struct}' "
                f"(not in valid set and not a known fixup)",
            ))

        ctx = domain.get("curriculum_context", "")
        if ctx and len(ctx) < 200:
            issues.append(ExtractionIssue(
                "WARN", filename,
                f"Domain {d_id} curriculum_context is only {len(ctx)} chars (threshold: 200)",
            ))

    # Check every objective references a real domain
    for obj in objectives:
        dom_ref = obj.get("domain_id")
        if dom_ref and dom_ref not in domain_ids:
            issues.append(ExtractionIssue(
                "ERROR", filename,
                f"Objective {obj.get('objective_id')} references domain_id '{dom_ref}' "
                f"which does not exist in this file's domains",
            ))

    # ---- Concepts ----------------------------------------------------------
    concepts = data.get("concepts", [])
    concept_ids = set()
    for concept in concepts:
        c_id = concept.get("concept_id", "(no id)")
        concept_ids.add(c_id)

        ctype = concept.get("concept_type")
        if ctype not in VALID_CONCEPT_TYPES:
            issues.append(ExtractionIssue(
                "ERROR" if ctype not in KNOWN_CONCEPT_TYPE_FIXUPS else "WARN",
                filename,
                f"Concept {c_id} has invalid concept_type '{ctype}' "
                f"({'will be auto-corrected' if ctype in KNOWN_CONCEPT_TYPE_FIXUPS else 'UNKNOWN — no fixup defined'})",
            ))

        clevel = concept.get("complexity_level")
        if clevel is None or not (1 <= int(clevel) <= 5 if str(clevel).isdigit() else False):
            issues.append(ExtractionIssue(
                "ERROR", filename,
                f"Concept {c_id} complexity_level '{clevel}' is not 1-5",
            ))

        desc = concept.get("description") or concept.get("definition", "")
        if not desc:
            issues.append(ExtractionIssue(
                "WARN", filename,
                f"Concept {c_id} has no description",
            ))
        elif len(desc) < 25:
            issues.append(ExtractionIssue(
                "WARN", filename,
                f"Concept {c_id} description is very short ({len(desc)} chars): '{desc}'",
            ))

    # ---- Enrichment completeness -------------------------------------------
    enrichment_fields = ["teaching_guidance", "key_vocabulary", "common_misconceptions"]
    bare_concepts = []
    for concept in concepts:
        c_id = concept.get("concept_id", "(no id)")
        missing_fields = []
        for field in enrichment_fields:
            val = concept.get(field)
            if not val or (isinstance(val, str) and not val.strip()) or (isinstance(val, list) and len(val) == 0):
                missing_fields.append(field)
        if missing_fields:
            bare_concepts.append((c_id, missing_fields))

    if bare_concepts:
        # Only report first 5 per file to avoid flooding output
        sample = bare_concepts[:5]
        suffix = f" (and {len(bare_concepts) - 5} more)" if len(bare_concepts) > 5 else ""
        sample_strs = ["{} [{}]".format(cid, ", ".join(mf)) for cid, mf in sample]
        issues.append(ExtractionIssue(
            "WARN", filename,
            f"{len(bare_concepts)}/{len(concepts)} concepts missing enrichment fields: "
            f"{', '.join(sample_strs)}{suffix}",
        ))

    # ---- Prerequisites -----------------------------------------------------
    prereq_key = (
        "prerequisite_relationships"
        or "prerequisites"
        or "prerequisite_relations"
    )
    prereqs = (
        data.get("prerequisite_relationships")
        or data.get("prerequisites")
        or data.get("prerequisite_relations", [])
    )
    for prereq in prereqs:
        src = prereq.get("prerequisite_concept") or prereq.get("source_concept_id")
        tgt = prereq.get("dependent_concept") or prereq.get("target_concept_id")

        if src and src not in concept_ids:
            issues.append(ExtractionIssue(
                "WARN", filename,
                f"Prerequisite references source concept '{src}' not defined in this file",
            ))
        if tgt and tgt not in concept_ids:
            issues.append(ExtractionIssue(
                "WARN", filename,
                f"Prerequisite references target concept '{tgt}' not defined in this file",
            ))

        conf = prereq.get("confidence")
        if conf and conf not in VALID_PREREQ_CONFIDENCE:
            issues.append(ExtractionIssue(
                "WARN", filename,
                f"Prerequisite confidence '{conf}' is not in the valid set",
            ))

        rel_type = prereq.get("relationship_type")
        if rel_type and rel_type not in VALID_PREREQ_REL_TYPES:
            issues.append(ExtractionIssue(
                "WARN", filename,
                f"Prerequisite relationship_type '{rel_type}' is not in the valid set",
            ))

        if src and tgt and src == tgt:
            issues.append(ExtractionIssue(
                "ERROR", filename,
                f"Self-referential prerequisite: {src} -> {tgt}",
            ))

    return issues


def main():
    parser = argparse.ArgumentParser(description="Validate curriculum extraction JSON files")
    parser.add_argument("--path", default=None, help="Override path to scan (default: data/extractions)")
    parser.add_argument("--errors-only", action="store_true", help="Show ERRORs only")
    args = parser.parse_args()

    scan_path = Path(args.path) if args.path else EXTRACTIONS_DIR
    json_files = sorted(p for p in scan_path.rglob("*.json")
                        if "test-frameworks" not in str(p) and "raw" not in str(p))

    if not json_files:
        print(f"No JSON files found under {scan_path}")
        sys.exit(1)

    print(f"Validating {len(json_files)} extraction files under {scan_path}")
    print("=" * 60)

    all_issues: list[ExtractionIssue] = []
    files_with_errors = 0
    files_clean = 0

    for path in json_files:
        issues = validate_file(path)
        visible = [i for i in issues if not args.errors_only or i.severity == "ERROR"]
        if visible:
            files_with_errors += 1
            for issue in visible:
                print(issue)
        else:
            files_clean += 1
        all_issues.extend(issues)

    n_errors = sum(1 for i in all_issues if i.severity == "ERROR")
    n_warns = sum(1 for i in all_issues if i.severity == "WARN")

    print()
    print("=" * 60)
    print(f"SUMMARY: {len(json_files)} files | "
          f"{files_clean} clean | {files_with_errors} with issues")
    print(f"         {n_errors} ERRORs | {n_warns} WARNs")
    print("=" * 60)

    if n_errors > 0:
        print("Fix ERRORs before importing — they will cause missing or corrupt data.")
        sys.exit(1)
    else:
        print("No ERRORs. Safe to import (review WARNs above if any).")
        sys.exit(0)


if __name__ == "__main__":
    main()

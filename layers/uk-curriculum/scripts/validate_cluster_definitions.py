#!/usr/bin/env python3
"""
Validate cluster_definitions/*.json files against the extraction JSONs.

Checks:
  1. All concept_ids exist in extraction files
  2. Every concept in each domain is covered exactly once
  3. No duplicate concept_ids within a domain's clusters
  4. cluster_type is valid ('introduction' or 'practice')
  5. cluster_name is a non-empty string (not just a concept list)
  6. At least one cluster per defined domain

Usage:
  python3 validate_cluster_definitions.py           # validate all
  python3 validate_cluster_definitions.py --subject mathematics  # one file
"""

import json
import sys
import argparse
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parents[3]
CLUSTER_DEFS_DIR = PROJECT_ROOT / "layers" / "uk-curriculum" / "data" / "cluster_definitions"
EXTRACTIONS_DIR  = PROJECT_ROOT / "layers" / "uk-curriculum" / "data" / "extractions"

VALID_CONTENT_TYPES = {"introduction", "practice"}

VALID_THINKING_LENSES = {
    "patterns", "cause_and_effect", "scale_proportion_quantity",
    "systems_models", "energy_matter", "structure_function",
    "stability_change", "continuity_change",
    "perspective_interpretation", "evidence_argument",
}


# ── Load ground-truth concept data from extraction files ─────────────────────

def load_all_concepts():
    """Return {domain_id: set(concept_ids)} from all extraction JSONs."""
    domain_concepts = defaultdict(set)
    for f in EXTRACTIONS_DIR.rglob("*_extracted.json"):
        with open(f) as fh:
            data = json.load(fh)
        for c in data.get("concepts", []):
            domain_concepts[c["domain_id"]].add(c["concept_id"])
    return domain_concepts


# ── Validation ────────────────────────────────────────────────────────────────

def validate_file(def_file, domain_concepts):
    with open(def_file) as f:
        data = json.load(f)

    subject_group = data.get("subject_group", def_file.stem)
    errors = []
    warnings = []
    total_domains = 0
    total_clusters = 0

    for domain_id, domain_data in data.get("domains", {}).items():
        total_domains += 1
        clusters = domain_data.get("clusters", [])
        ground_truth = domain_concepts.get(domain_id, set())

        if not clusters:
            errors.append(f"  {domain_id}: no clusters defined")
            continue

        # Track concept coverage within this domain
        seen_in_domain = set()

        for i, cluster in enumerate(clusters, 1):
            total_clusters += 1
            cname = cluster.get("cluster_name", "")
            ctype = cluster.get("cluster_type", "")
            cids  = cluster.get("concept_ids", [])
            rationale = cluster.get("rationale", "")

            # cluster_type must be introduction or practice
            if ctype not in VALID_CONTENT_TYPES:
                errors.append(
                    f"  {domain_id} cluster {i}: invalid cluster_type '{ctype}' "
                    f"(must be 'introduction' or 'practice')"
                )

            # thinking_lenses must be present with valid IDs and non-empty rationales
            lenses = cluster.get("thinking_lenses", [])
            if not lenses:
                warnings.append(
                    f"  {domain_id} cluster {i} '{cname[:40]}': no thinking_lenses set"
                )
            else:
                for j, lens_obj in enumerate(lenses, 1):
                    lens_id = lens_obj.get("lens", "")
                    rationale = lens_obj.get("rationale", "")
                    if lens_id not in VALID_THINKING_LENSES:
                        errors.append(
                            f"  {domain_id} cluster {i} lens {j}: invalid lens '{lens_id}' "
                            f"(valid: {sorted(VALID_THINKING_LENSES)})"
                        )
                    if not rationale or not rationale.strip():
                        errors.append(
                            f"  {domain_id} cluster {i} lens {j} '{lens_id}': missing rationale"
                        )
                if len(lenses) > 3:
                    warnings.append(
                        f"  {domain_id} cluster {i}: {len(lenses)} lenses — consider trimming to 3 max"
                    )

            # cluster_name must be non-empty
            if not cname or not cname.strip():
                errors.append(f"  {domain_id} cluster {i}: cluster_name is empty")
            elif len(cname) < 8:
                warnings.append(
                    f"  {domain_id} cluster {i}: cluster_name '{cname}' seems very short"
                )

            # rationale should be present
            if not rationale or not rationale.strip():
                warnings.append(
                    f"  {domain_id} cluster {i} '{cname[:40]}': no rationale provided"
                )

            # All concept_ids must exist
            if not cids:
                errors.append(f"  {domain_id} cluster {i}: concept_ids is empty")

            for cid in cids:
                if cid not in ground_truth:
                    errors.append(
                        f"  {domain_id} cluster {i}: concept_id '{cid}' not found "
                        f"in extraction files"
                    )
                if cid in seen_in_domain:
                    errors.append(
                        f"  {domain_id} cluster {i}: concept_id '{cid}' appears "
                        f"in more than one cluster"
                    )
                seen_in_domain.add(cid)

        # Every concept in the domain must be covered
        uncovered = ground_truth - seen_in_domain
        if uncovered:
            errors.append(
                f"  {domain_id}: {len(uncovered)} concept(s) not covered: "
                f"{sorted(uncovered)[:5]}{'...' if len(uncovered) > 5 else ''}"
            )

    return {
        "subject_group": subject_group,
        "errors": errors,
        "warnings": warnings,
        "total_domains": total_domains,
        "total_clusters": total_clusters,
    }


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Validate cluster definitions")
    parser.add_argument("--subject", help="Validate only this file stem (e.g. 'mathematics')")
    args = parser.parse_args()

    print("=" * 60)
    print("Validate: cluster_definitions/*.json")
    print("=" * 60)

    print("\nLoading extraction concepts...")
    domain_concepts = load_all_concepts()
    print(f"  Known domains: {len(domain_concepts)}")

    def_files = sorted(CLUSTER_DEFS_DIR.glob("*.json"))
    if args.subject:
        def_files = [f for f in def_files if f.stem == args.subject]
        if not def_files:
            print(f"No file found for subject '{args.subject}'")
            sys.exit(1)

    if not def_files:
        print("\nNo cluster definition files found yet.")
        print(f"Add files to: {CLUSTER_DEFS_DIR}")
        sys.exit(0)

    all_errors = 0
    all_warnings = 0

    for def_file in def_files:
        result = validate_file(def_file, domain_concepts)
        print(f"\n── {def_file.name} ({result['subject_group']}) ──")
        print(f"   Domains: {result['total_domains']}, Clusters: {result['total_clusters']}")

        if result["errors"]:
            print(f"   ERRORS ({len(result['errors'])}):")
            for e in result["errors"]:
                print(f"    ✗ {e}")
            all_errors += len(result["errors"])
        if result["warnings"]:
            print(f"   WARNINGS ({len(result['warnings'])}):")
            for w in result["warnings"]:
                print(f"    ⚠ {w}")
            all_warnings += len(result["warnings"])
        if not result["errors"] and not result["warnings"]:
            print("   ✓ All checks passed")

    print("\n" + "=" * 60)
    if all_errors:
        print(f"RESULT: {all_errors} error(s), {all_warnings} warning(s) — FAIL")
        sys.exit(1)
    elif all_warnings:
        print(f"RESULT: 0 errors, {all_warnings} warning(s) — PASS with warnings")
    else:
        print("RESULT: All checks passed — PASS")


if __name__ == "__main__":
    main()

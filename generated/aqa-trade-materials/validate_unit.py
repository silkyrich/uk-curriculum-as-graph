"""
validate_unit.py — Validate curriculum_unit.json joins and invariants

Checks:
  1. Concept registry completeness — every concept_id referenced exists in concepts{}
  2. Concept introduction ordering — no concept used before its introducing section
  3. Spec coverage — every spec_coverage item appears in at least one section
  4. Slide ID uniqueness
  5. Question ID uniqueness
  6. Cross-references — links_to_slide values resolve to real slide_ids
  7. Concept introduction consistency — concepts_introduced matches first use

Usage:
    python3 validate_unit.py <curriculum_unit.json>
"""

import json
import sys
from pathlib import Path
from collections import defaultdict


def validate(unit_path: str) -> bool:
    with open(unit_path) as f:
        unit = json.load(f)

    errors = []
    warnings = []
    sections = unit.get("sections", [])
    concepts = unit.get("concepts", {})
    spec_coverage = set(unit.get("spec_coverage", []))

    # ── Build indexes ──────────────────────────────────────────────────────────

    # section_index[section_id] = section_array_index
    section_index = {s["section_id"]: i for i, s in enumerate(sections)}

    # All slide IDs across all sections
    all_slide_ids = {}
    for s in sections:
        for sl in s.get("slides", []):
            sid = sl.get("slide_id")
            if sid:
                if sid in all_slide_ids:
                    errors.append(f"Duplicate slide_id: {sid}")
                all_slide_ids[sid] = s["section_id"]

    # All question IDs
    all_q_ids = {}
    for s in sections:
        for q in s.get("questions", []):
            qid = q.get("q_id")
            if qid:
                if qid in all_q_ids:
                    errors.append(f"Duplicate q_id: {qid}")
                all_q_ids[qid] = s["section_id"]

    # Spec refs used across sections
    used_spec_refs = set()
    for s in sections:
        for ref in s.get("spec_refs", []):
            used_spec_refs.add(ref)

    # ── Check 1: Concept registry ──────────────────────────────────────────────

    def check_concept_refs(refs, location):
        for cid in refs:
            if cid not in concepts:
                errors.append(f"Unknown concept_id '{cid}' in {location}")

    for i, section in enumerate(sections):
        sid = section["section_id"]

        check_concept_refs(section.get("concepts_introduced", []), f"{sid}.concepts_introduced")
        check_concept_refs(section.get("concepts_reinforced", []), f"{sid}.concepts_reinforced")

        for sl in section.get("slides", []):
            check_concept_refs(sl.get("concept_refs", []), f"{sl.get('slide_id', '?')}.concept_refs")

        for q in section.get("questions", []):
            check_concept_refs(q.get("concepts_tested", []), f"{q.get('q_id', '?')}.concepts_tested")

        teacher = section.get("teacher", {})
        check_concept_refs(teacher.get("key_concepts", []), f"{sid}.teacher.key_concepts")

    # ── Check 2: Concept introduction ordering ─────────────────────────────────

    # Map concept_id → section index where it's first introduced
    concept_introduced_at = {}
    for i, section in enumerate(sections):
        for cid in section.get("concepts_introduced", []):
            if cid not in concept_introduced_at:
                concept_introduced_at[cid] = i

    def check_intro_ordering(concept_ids, section_idx, location):
        for cid in concept_ids:
            if cid not in concept_introduced_at:
                warnings.append(
                    f"Concept '{cid}' used in {location} (section index {section_idx}) "
                    f"but never declared in any concepts_introduced — add it to section {sections[section_idx]['section_id']}"
                )
            elif concept_introduced_at[cid] > section_idx:
                intro_section = sections[concept_introduced_at[cid]]["section_id"]
                errors.append(
                    f"Concept '{cid}' used in {location} (section index {section_idx}) "
                    f"but not introduced until {intro_section} (index {concept_introduced_at[cid]}). "
                    f"Either move the introduction earlier or remove the reference."
                )

    for i, section in enumerate(sections):
        sid = section["section_id"]

        # concepts_reinforced must be introduced in an earlier section
        for cid in section.get("concepts_reinforced", []):
            if cid in concept_introduced_at and concept_introduced_at[cid] >= i:
                errors.append(
                    f"{sid}.concepts_reinforced: '{cid}' is not introduced before section index {i}"
                )

        for sl in section.get("slides", []):
            check_intro_ordering(
                sl.get("concept_refs", []), i, f"{sl.get('slide_id', '?')}.concept_refs"
            )

        for q in section.get("questions", []):
            check_intro_ordering(
                q.get("concepts_tested", []), i, f"{q.get('q_id', '?')}.concepts_tested"
            )

    # ── Check 3: Spec coverage ─────────────────────────────────────────────────

    uncovered = spec_coverage - used_spec_refs
    for ref in sorted(uncovered):
        warnings.append(f"Spec point '{ref}' declared in spec_coverage but not covered by any section")

    extra = used_spec_refs - spec_coverage
    for ref in sorted(extra):
        warnings.append(f"Section uses spec ref '{ref}' not declared in top-level spec_coverage — consider adding it")

    # ── Check 4: Cross-references ──────────────────────────────────────────────

    for section in sections:
        for q in section.get("questions", []):
            ref = q.get("links_to_slide")
            if ref and ref not in all_slide_ids:
                errors.append(f"{q.get('q_id', '?')}.links_to_slide: '{ref}' not found in any slide")

    # ── Check 5: concepts{} introduced_in_section consistency ─────────────────

    for cid, concept in concepts.items():
        declared_section = concept.get("introduced_in_section")
        if declared_section:
            actual_idx = concept_introduced_at.get(cid)
            if actual_idx is None:
                warnings.append(
                    f"Concept '{cid}' has introduced_in_section='{declared_section}' "
                    f"but is never listed in any concepts_introduced array"
                )
            else:
                actual_section = sections[actual_idx]["section_id"]
                if actual_section != declared_section:
                    warnings.append(
                        f"Concept '{cid}': introduced_in_section says '{declared_section}' "
                        f"but first concepts_introduced is in '{actual_section}'"
                    )

    # ── Report ─────────────────────────────────────────────────────────────────

    print(f"\n{'='*60}")
    print(f"Validation: {Path(unit_path).name}")
    print(f"{'='*60}")
    print(f"Sections:  {len(sections)}")
    print(f"Concepts:  {len(concepts)}")
    print(f"Slides:    {len(all_slide_ids)}")
    print(f"Questions: {len(all_q_ids)}")
    print(f"Spec refs: {len(used_spec_refs)}/{len(spec_coverage)} covered")
    print()

    if errors:
        print(f"❌ ERRORS ({len(errors)}):")
        for e in errors:
            print(f"   • {e}")
        print()

    if warnings:
        print(f"⚠  WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"   • {w}")
        print()

    if not errors and not warnings:
        print("✅ All checks passed")
    elif not errors:
        print(f"✅ No errors ({len(warnings)} warnings)")
    else:
        print(f"❌ {len(errors)} errors must be fixed before building")

    print()
    return len(errors) == 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 validate_unit.py <curriculum_unit.json>")
        sys.exit(1)
    ok = validate(sys.argv[1])
    sys.exit(0 if ok else 1)

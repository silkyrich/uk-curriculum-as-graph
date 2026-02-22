#!/usr/bin/env python3
"""
Enrich extraction JSONs with teaching_weight and co_teach_hints.

Reads all extraction JSON files under layers/uk-curriculum/data/extractions/
(primary/ and secondary/) and adds two fields to each concept:

  teaching_weight (int 1-6): Lesson span heuristic.
    - base = complexity_level
    - +1 if the concept is a keystone (referenced as prerequisite by 3+ others)
    - +1 if concept_type is "knowledge" and complexity_level >= 4
    - Clamped to [1, 6]

  co_teach_hints (list[str]): Concept IDs that should be co-taught.
    - Concepts referenced in teaching_guidance via linking phrases
    - Concepts whose name appears in another concept's teaching_guidance (same domain)
    - Concepts linked by supportive/enabling prerequisite relationships
    - Only includes IDs that exist in the same file; deduplicated and sorted

Usage:
    python3 layers/uk-curriculum/scripts/enrich_grouping_signals.py
"""

import json
import re
from collections import defaultdict
from pathlib import Path

# Phrases in teaching_guidance that signal co-teaching opportunities
LINKING_PHRASES = [
    r"connect(?:s|ed|ing)?\s+(?:this\s+)?(?:to|with)",
    r"link(?:s|ed|ing)?\s+(?:this\s+)?(?:to|with)",
    r"inverse\s+(?:of|operation)",
    r"opposite\s+(?:of|to)",
    r"contrast(?:s|ed|ing)?\s+(?:this\s+)?with",
    r"builds?\s+on",
    r"extends?\s+(?:from|to|this)",
    r"related\s+(?:to|concept)",
    r"connect(?:s|ed)?\s+(?:directly|explicitly)\s+to",
    r"doubling\s+relationship",
    r"alongside",
]

# Compiled pattern for concept ID references (e.g. MA-Y3-C001)
CONCEPT_ID_PATTERN = re.compile(r"\b([A-Z]{2,4}-(?:Y\d{1,2}|KS\d)-C\d{3})\b")

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
EXTRACTIONS_DIR = PROJECT_ROOT / "layers" / "uk-curriculum" / "data" / "extractions"


def find_extraction_files():
    """Find all extraction JSON files in primary/ and secondary/ subdirs."""
    files = []
    for subdir in ["primary", "secondary"]:
        dirpath = EXTRACTIONS_DIR / subdir
        if dirpath.exists():
            files.extend(sorted(dirpath.glob("*_extracted.json")))
    return files


def build_prerequisite_fan_out(prerequisite_relationships, all_concept_ids):
    """Count how many concepts depend on each concept (fan-out as prerequisite).

    A concept with fan-out >= 3 is a keystone concept.
    Only counts references to concepts that exist in this file.
    """
    fan_out = defaultdict(int)
    for rel in prerequisite_relationships:
        # Handle both field naming conventions
        prereq = rel.get("prerequisite_concept") or rel.get("source_concept_id", "")
        if prereq in all_concept_ids:
            fan_out[prereq] += 1
    return fan_out


def compute_teaching_weight(concept, fan_out):
    """Compute teaching_weight for a single concept.

    base = complexity_level
    +1 if keystone (fan-out >= 3)
    +1 if knowledge concept with complexity >= 4
    Clamped to [1, 6]
    """
    complexity = concept.get("complexity_level", 1)
    if not isinstance(complexity, int):
        complexity = 1
    weight = complexity

    concept_id = concept.get("concept_id", "")
    if fan_out.get(concept_id, 0) >= 3:
        weight += 1

    concept_type = concept.get("concept_type", "").lower()
    if concept_type == "knowledge" and complexity >= 4:
        weight += 1

    return max(1, min(6, weight))


def find_co_teach_hints(concept, concepts_by_id, concepts_in_domain, prerequisite_relationships):
    """Find concept IDs that should be co-taught with this concept.

    Sources:
    1. Concept IDs explicitly mentioned in teaching_guidance
    2. Linking phrases in teaching_guidance + concept name matching in same domain
    3. Supportive/enabling prerequisite relationships
    """
    concept_id = concept.get("concept_id", "")
    domain_id = concept.get("domain_id", "")
    teaching_guidance = concept.get("teaching_guidance", "") or ""
    hints = set()

    # 1. Direct concept ID references in teaching_guidance
    for match in CONCEPT_ID_PATTERN.finditer(teaching_guidance):
        ref_id = match.group(1)
        if ref_id != concept_id and ref_id in concepts_by_id:
            hints.add(ref_id)

    # 2. Check if teaching_guidance contains names of other concepts in same domain
    if teaching_guidance and domain_id:
        guidance_lower = teaching_guidance.lower()
        for other_id, other_concept in concepts_in_domain.get(domain_id, {}).items():
            if other_id == concept_id:
                continue
            other_name = other_concept.get("concept_name", "")
            if not other_name:
                continue
            # Only match substantial names (3+ chars) to avoid false positives
            if len(other_name) >= 3 and other_name.lower() in guidance_lower:
                hints.add(other_id)

    # 3. Check for linking phrases that reference other concepts
    #    Look for linking phrase followed by concept name in the guidance
    if teaching_guidance:
        guidance_lower = teaching_guidance.lower()
        has_linking_phrase = any(
            re.search(phrase, guidance_lower) for phrase in LINKING_PHRASES
        )
        if has_linking_phrase:
            # Check vocabulary overlap with same-domain concepts
            concept_vocab = set(
                w.lower() for w in re.findall(r"\b\w{4,}\b", teaching_guidance)
            )
            for other_id, other_concept in concepts_in_domain.get(domain_id, {}).items():
                if other_id == concept_id or other_id in hints:
                    continue
                other_guidance = other_concept.get("teaching_guidance", "") or ""
                other_vocab = set(
                    w.lower() for w in re.findall(r"\b\w{4,}\b", other_guidance)
                )
                # Require significant vocabulary overlap (5+ shared content words)
                # excluding very common words
                common_words = {
                    "that", "this", "with", "from", "they", "their", "them",
                    "have", "will", "been", "when", "than", "each", "more",
                    "some", "what", "also", "into", "used", "using", "pupils",
                    "should", "number", "numbers", "example", "understand",
                    "understanding", "practise", "practice"
                }
                shared = concept_vocab & other_vocab - common_words
                if len(shared) >= 5:
                    hints.add(other_id)

    # 4. Supportive or enabling prerequisite relationships
    for rel in prerequisite_relationships:
        rel_type = rel.get("relationship_type", "").lower()
        if rel_type not in ("supportive", "enabling"):
            continue
        prereq = rel.get("prerequisite_concept") or rel.get("source_concept_id", "")
        dependent = rel.get("dependent_concept") or rel.get("target_concept_id", "")
        if prereq == concept_id and dependent in concepts_by_id:
            hints.add(dependent)
        elif dependent == concept_id and prereq in concepts_by_id:
            hints.add(prereq)

    # Remove self-reference and sort
    hints.discard(concept_id)
    return sorted(hints)


def enrich_file(filepath):
    """Enrich a single extraction JSON file with teaching_weight and co_teach_hints.

    Returns (num_concepts, num_with_co_teach_hints).
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    concepts = data.get("concepts", [])
    if not concepts:
        return 0, 0

    prerequisite_relationships = data.get("prerequisite_relationships", [])

    # Build lookup structures
    all_concept_ids = {c["concept_id"] for c in concepts if "concept_id" in c}
    concepts_by_id = {c["concept_id"]: c for c in concepts if "concept_id" in c}

    # Group concepts by domain
    concepts_in_domain = defaultdict(dict)
    for c in concepts:
        cid = c.get("concept_id", "")
        did = c.get("domain_id", "")
        if cid and did:
            concepts_in_domain[did][cid] = c

    # Compute prerequisite fan-out
    fan_out = build_prerequisite_fan_out(prerequisite_relationships, all_concept_ids)

    # Enrich each concept
    num_with_hints = 0
    for concept in concepts:
        concept["teaching_weight"] = compute_teaching_weight(concept, fan_out)
        hints = find_co_teach_hints(
            concept, concepts_by_id, concepts_in_domain, prerequisite_relationships
        )
        concept["co_teach_hints"] = hints
        if hints:
            num_with_hints += 1

    # Write back
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return len(concepts), num_with_hints


def main():
    files = find_extraction_files()
    if not files:
        print(f"No extraction files found in {EXTRACTIONS_DIR}")
        return

    total_files = 0
    total_concepts = 0
    total_with_hints = 0

    print(f"Enriching extraction files in {EXTRACTIONS_DIR}")
    print(f"Found {len(files)} extraction files\n")

    for filepath in files:
        num_concepts, num_with_hints = enrich_file(filepath)
        total_files += 1
        total_concepts += num_concepts
        total_with_hints += num_with_hints
        hint_str = f" ({num_with_hints} with co_teach_hints)" if num_with_hints else ""
        print(f"  {filepath.name}: {num_concepts} concepts enriched{hint_str}")

    print(f"\n{'='*60}")
    print(f"Files processed:        {total_files}")
    print(f"Concepts enriched:      {total_concepts}")
    print(f"With co_teach_hints:    {total_with_hints}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()

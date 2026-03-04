#!/usr/bin/env python3
"""
Generate definitions for vocabulary term stubs using LLM.

Reads skeletal JSON files from layers/vocabulary/data/terms/, enriches each
term with: definition, word_class, tier, etymology, example_usage,
common_errors, related_everyday_word.

Uses concept descriptions and teaching guidance as context to generate
age-appropriate, curriculum-grounded definitions.

Usage:
    python3 layers/vocabulary/scripts/generate_definitions.py --subject Mathematics --ks KS2
    python3 layers/vocabulary/scripts/generate_definitions.py --subject Science --ks KS1
    python3 layers/vocabulary/scripts/generate_definitions.py --all
    python3 layers/vocabulary/scripts/generate_definitions.py --file mathematics_y3.json

Requires:
    ANTHROPIC_API_KEY environment variable set.
"""

import json
import os
import sys
import time
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
TERMS_DIR = Path(__file__).resolve().parents[1] / "data" / "terms"
EXTRACTIONS_DIR = PROJECT_ROOT / "layers" / "uk-curriculum" / "data" / "extractions"

# Key stage → year mapping for file selection
KS_YEARS = {
    "KS1": ["y1", "y2", "ks1"],
    "KS2": ["y3", "y4", "y5", "y6", "ks2"],
    "KS3": ["ks3"],
    "KS4": ["ks4"],
}


def load_concept_context(concept_ids: list[str]) -> dict[str, dict]:
    """Load concept descriptions and teaching guidance from extraction JSONs.

    Returns dict of concept_id -> {concept_name, description, teaching_guidance, domain_name}.
    """
    context = {}
    if not concept_ids:
        return context

    # Build a set for fast lookup
    needed = set(concept_ids)

    # Scan all extraction files
    for stage_dir in ["primary", "secondary"]:
        dir_path = EXTRACTIONS_DIR / stage_dir
        if not dir_path.exists():
            continue
        for fpath in dir_path.glob("*_extracted.json"):
            with open(fpath) as f:
                data = json.load(f)
            for domain in data.get("domains", []):
                for concept in domain.get("concepts", []):
                    cid = concept.get("concept_id", "")
                    if cid in needed:
                        context[cid] = {
                            "concept_name": concept.get("concept_name", ""),
                            "description": concept.get("description", ""),
                            "teaching_guidance": concept.get("teaching_guidance", ""),
                            "domain_name": domain.get("domain_name", ""),
                        }
                        needed.discard(cid)
            if not needed:
                break

    return context


def build_prompt(term: dict, concept_context: dict[str, dict], subject: str, year: str) -> str:
    """Build the LLM prompt for generating a vocabulary definition."""
    concept_snippets = []
    for link in term.get("concept_links", []):
        cid = link["concept_id"]
        ctx = concept_context.get(cid, {})
        if ctx:
            snippet = f"- {ctx['concept_name']} ({cid}): {ctx['description'][:200]}"
            if ctx.get("teaching_guidance"):
                snippet += f"\n  Teaching: {ctx['teaching_guidance'][:150]}"
            concept_snippets.append(snippet)

    concepts_text = "\n".join(concept_snippets) if concept_snippets else "(no concept context available)"

    prompt = f"""You are a UK primary/secondary curriculum vocabulary specialist. Generate a structured vocabulary entry for a term used in the {subject} curriculum ({year}).

TERM: {term['term']}
SUBJECT: {subject}
YEAR/KS: {year}

CURRICULUM CONCEPTS THAT USE THIS TERM:
{concepts_text}

Generate a JSON object with these fields:
- "definition": A clear, precise definition suitable for a teacher planning a lesson. Use language a teacher would recognise. 1-2 sentences max.
- "word_class": One of: "noun", "verb", "adjective", "adverb", "phrase"
- "tier": Beck's vocabulary tier: 1=everyday, 2=general academic, 3=domain-specific. Most curriculum terms are tier 3.
- "etymology": Brief origin (e.g. "From Latin 'fractus' (broken)"). Leave empty if mundane.
- "example_usage": One example sentence a child at this level might encounter or produce.
- "common_errors": One common error or misconception children have about this term. Leave empty if none obvious.
- "related_everyday_word": The everyday word this technical term replaces or refines (e.g. "part" for "fraction"). Leave empty if not applicable.

Rules:
- Definitions must be curriculum-grounded, not dictionary definitions
- Pitch to the year group: Y1 definitions simpler than Y6
- Do NOT include the term itself in the definition
- Keep etymology empty for common English words
- Return ONLY the JSON object, no explanation

JSON:"""

    return prompt


def call_llm(prompt: str) -> dict | None:
    """Call the Anthropic API to generate a definition.

    Returns parsed JSON dict or None on failure.
    """
    try:
        import anthropic
    except ImportError:
        print("ERROR: anthropic package not installed. Run: pip install anthropic")
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()

        # Parse JSON from response
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()

        return json.loads(text)

    except json.JSONDecodeError as e:
        print(f"    WARN: Failed to parse JSON: {e}")
        return None
    except Exception as e:
        print(f"    WARN: API error: {e}")
        return None


def select_files(subject: str | None, ks: str | None, specific_file: str | None) -> list[Path]:
    """Select term files to process based on filters."""
    if specific_file:
        path = TERMS_DIR / specific_file
        if path.exists():
            return [path]
        print(f"ERROR: File not found: {path}")
        sys.exit(1)

    all_files = sorted(TERMS_DIR.glob("*.json"))

    if not subject and not ks:
        return all_files

    selected = []
    for fpath in all_files:
        fname = fpath.stem.lower()

        if subject:
            subj_slug = subject.lower().replace(" ", "_")
            if not fname.startswith(subj_slug):
                continue

        if ks:
            year_suffixes = KS_YEARS.get(ks.upper(), [ks.lower()])
            if not any(fname.endswith(f"_{s}") for s in year_suffixes):
                continue

        selected.append(fpath)

    return selected


def generate_for_file(fpath: Path, dry_run: bool = False) -> dict:
    """Generate definitions for all undefined terms in a single file."""
    with open(fpath) as f:
        data = json.load(f)

    metadata = data.get("metadata", {})
    subject = metadata.get("subject", "Unknown")
    year = metadata.get("year", "Unknown")
    terms = data.get("terms", [])

    # Find terms needing definitions
    undefined = [t for t in terms if not t.get("definition")]
    if not undefined:
        print(f"  {fpath.name}: all {len(terms)} terms already defined")
        return {"file": fpath.name, "total": len(terms), "generated": 0, "failed": 0}

    print(f"  {fpath.name}: {len(undefined)}/{len(terms)} terms need definitions")

    if dry_run:
        return {"file": fpath.name, "total": len(terms), "generated": 0, "failed": 0}

    # Load concept context for all terms in this file
    all_concept_ids = []
    for t in undefined:
        for link in t.get("concept_links", []):
            all_concept_ids.append(link["concept_id"])
    concept_context = load_concept_context(all_concept_ids)

    generated = 0
    failed = 0

    for term in undefined:
        prompt = build_prompt(term, concept_context, subject, year)
        result = call_llm(prompt)

        if result:
            # Merge generated fields into term (don't overwrite existing non-empty values)
            for key in ["definition", "word_class", "tier", "etymology",
                        "example_usage", "common_errors", "related_everyday_word"]:
                if key in result and result[key]:
                    if not term.get(key):
                        term[key] = result[key]
            generated += 1
            print(f"    ✓ {term['term']}")
        else:
            failed += 1
            print(f"    ✗ {term['term']} — generation failed")

        # Rate limiting
        time.sleep(0.2)

    # Write back
    data["terms"] = terms
    data["metadata"]["term_count"] = len(terms)
    with open(fpath, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return {"file": fpath.name, "total": len(terms), "generated": generated, "failed": failed}


def main():
    parser = argparse.ArgumentParser(
        description="Generate vocabulary definitions using LLM"
    )
    parser.add_argument("--subject", help="Filter by subject (e.g. Mathematics)")
    parser.add_argument("--ks", help="Filter by key stage (e.g. KS2)")
    parser.add_argument("--file", help="Process a specific file")
    parser.add_argument("--all", action="store_true", help="Process all files")
    parser.add_argument("--dry-run", action="store_true", help="Count terms only")
    args = parser.parse_args()

    if not args.subject and not args.ks and not args.file and not args.all:
        parser.print_help()
        print("\nSpecify --subject, --ks, --file, or --all to proceed.")
        sys.exit(1)

    print("=" * 60)
    print("Vocabulary Definition Generator")
    print("=" * 60)

    files = select_files(args.subject, args.ks, args.file)
    if not files:
        print("No matching term files found.")
        sys.exit(1)

    print(f"\nProcessing {len(files)} file(s)...\n")

    results = []
    for fpath in files:
        result = generate_for_file(fpath, dry_run=args.dry_run)
        results.append(result)

    # Summary
    total_terms = sum(r["total"] for r in results)
    total_generated = sum(r["generated"] for r in results)
    total_failed = sum(r["failed"] for r in results)

    print(f"\n{'=' * 60}")
    print(f"GENERATION SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Files processed:  {len(results)}")
    print(f"  Total terms:      {total_terms}")
    print(f"  Generated:        {total_generated}")
    print(f"  Failed:           {total_failed}")
    print(f"\nDone.")


if __name__ == "__main__":
    main()

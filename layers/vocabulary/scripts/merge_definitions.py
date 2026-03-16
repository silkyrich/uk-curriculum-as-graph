#!/usr/bin/env python3
"""
Merge generated definitions into vocabulary term JSON files.

Reads a definitions JSON from stdin or file:
  { "term_id": {"definition": "...", "word_class": "noun", ...}, ... }

Merges into the target vocabulary file, only overwriting empty fields.

Usage:
    python3 merge_definitions.py <vocab_file> <definitions_json>
    cat defs.json | python3 merge_definitions.py <vocab_file> -
"""

import json
import sys
from pathlib import Path

TERMS_DIR = Path(__file__).resolve().parents[1] / "data" / "terms"

MERGE_FIELDS = ["definition", "word_class", "tier", "etymology",
                "example_usage", "common_errors", "related_everyday_word"]


def merge(vocab_path: Path, definitions: dict) -> dict:
    """Merge definitions into vocab file. Returns stats."""
    with open(vocab_path) as f:
        data = json.load(f)

    merged = 0
    skipped = 0

    for term in data.get("terms", []):
        tid = term.get("term_id", "")
        if tid not in definitions:
            continue

        defn = definitions[tid]
        updated = False
        for key in MERGE_FIELDS:
            if key in defn and defn[key]:
                if not term.get(key) or (key == "definition" and not term["definition"]):
                    term[key] = defn[key]
                    updated = True
        if updated:
            merged += 1
        else:
            skipped += 1

    with open(vocab_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return {"merged": merged, "skipped": skipped, "total": len(data.get("terms", []))}


def main():
    if len(sys.argv) < 3:
        print("Usage: merge_definitions.py <vocab_file> <definitions_json|->")
        sys.exit(1)

    vocab_file = sys.argv[1]
    defs_source = sys.argv[2]

    # Find vocab file
    vocab_path = Path(vocab_file)
    if not vocab_path.exists():
        vocab_path = TERMS_DIR / vocab_file
    if not vocab_path.exists():
        print(f"ERROR: {vocab_file} not found")
        sys.exit(1)

    # Load definitions
    if defs_source == "-":
        definitions = json.load(sys.stdin)
    else:
        with open(defs_source) as f:
            definitions = json.load(f)

    stats = merge(vocab_path, definitions)
    print(f"{vocab_path.name}: merged {stats['merged']}/{stats['total']} terms (skipped {stats['skipped']})")


if __name__ == "__main__":
    main()

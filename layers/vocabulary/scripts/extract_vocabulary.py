#!/usr/bin/env python3
"""
Extract vocabulary terms from curriculum extraction JSONs.

Parses every concept's `key_vocabulary` comma-separated string, deduplicates
across the curriculum, assigns namespaced IDs, and writes skeletal JSON files
to layers/vocabulary/data/terms/.

Each output file corresponds to one extraction source file (subject + year/KS).
Terms that appear in multiple files are assigned to the FIRST file they appear in
(by subject+year order), with subsequent files referencing the same term_id via
concept_links only.

Usage:
    python3 layers/vocabulary/scripts/extract_vocabulary.py
    python3 layers/vocabulary/scripts/extract_vocabulary.py --dry-run
    python3 layers/vocabulary/scripts/extract_vocabulary.py --stats
"""

import json
import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parents[3]
EXTRACTIONS_DIR = PROJECT_ROOT / "layers" / "uk-curriculum" / "data" / "extractions"
EYFS_EXTRACTIONS_DIR = PROJECT_ROOT / "layers" / "eyfs" / "data" / "extractions"
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "data" / "terms"

# Subject prefix mapping (must match concept_id prefixes in the curriculum)
SUBJECT_PREFIXES = {
    "Mathematics": "MA",
    "English": "EN",
    "English Language": "EN",
    "English Literature": "EN",
    "Science": "SC",
    "Biology": "SC",
    "Chemistry": "SC",
    "Physics": "SC",
    "History": "HI",
    "Geography": "GE",
    "Art and Design": "AD",
    "Art & Design": "AD",
    "Music": "MU",
    "Design and Technology": "DT",
    "Design & Technology": "DT",
    "Computing": "CO",
    "Physical Education": "PE",
    "Languages": "LA",
    "Religious Studies": "RS",
    "Religious Education": "RS",
    "Citizenship": "CI",
    "Drama": "DR",
    "Business": "BU",
    "Food Preparation and Nutrition": "FN",
    "Food Preparation & Nutrition": "FN",
    "Media Studies": "MS",
    "Communication and Language": "EY",
    "Personal, Social and Emotional Development": "EY",
    "Physical Development": "EY",
    "Literacy": "EY",
    "Understanding the World": "EY",
    "Expressive Arts and Design": "EY",
    "PSED": "EY",
}


def slugify(term: str) -> str:
    """Convert a vocabulary term to a URL-safe slug.

    Examples:
        'fraction' -> 'fraction'
        'three-digit number' -> 'three-digit-number'
        '24-hour clock' -> '24-hour-clock'
        'a.m.' -> 'am'
        '>, <, =' -> 'gt-lt-eq'
    """
    # Special symbol replacements
    term = term.replace(">=", "gte").replace("<=", "lte")
    term = term.replace(">", "gt").replace("<", "lt").replace("=", "eq")
    term = term.replace("£", "pounds").replace("°", "degrees")
    term = term.replace("+", "plus").replace("×", "times")
    term = term.replace("/", "-").replace("'", "").replace('"', "")

    # Remove dots (a.m. -> am), but keep hyphens
    slug = term.lower().strip()
    slug = slug.replace(".", "")

    # Replace whitespace and non-alphanumeric (except hyphen) with hyphen
    slug = re.sub(r"[^a-z0-9-]", "-", slug)
    # Collapse multiple hyphens
    slug = re.sub(r"-+", "-", slug)
    # Strip leading/trailing hyphens
    slug = slug.strip("-")

    return slug


def parse_key_vocabulary(vocab_str: str) -> list[str]:
    """Split a comma-separated key_vocabulary string into individual terms.

    Handles edge cases:
        - Empty strings
        - Extra whitespace
        - Terms with internal commas in parentheses (rare)
    """
    if not vocab_str or not vocab_str.strip():
        return []

    terms = []
    for part in vocab_str.split(","):
        term = part.strip()
        if term:
            terms.append(term)
    return terms


def detect_year_or_ks(filename: str, metadata: dict) -> str:
    """Determine the year/KS label from filename and metadata.

    Returns strings like 'Y1', 'Y2', 'KS1', 'KS2', 'KS3', 'KS4', 'EYFS'.
    """
    years = metadata.get("years_covered", [])
    ks = metadata.get("key_stage", "")

    # If single year, use Y{n}
    if len(years) == 1:
        return f"Y{years[0]}"

    # If multiple years within a KS, use KS label
    if ks:
        return ks.upper()

    # Fall back to filename parsing
    fn = filename.upper()
    if "EYFS" in fn:
        return "EYFS"
    for y in range(1, 12):
        if f"_Y{y}_" in fn or fn.endswith(f"_Y{y}"):
            return f"Y{y}"
    for k in ["KS1", "KS2", "KS3", "KS4", "KS3-4", "KS1-2"]:
        if k in fn:
            return k

    return ks.upper() if ks else "UNKNOWN"


def make_output_filename(subject: str, year_ks: str) -> str:
    """Generate output filename like 'mathematics_y3.json' or 'science_ks2.json'."""
    subj = subject.lower().replace(" ", "_").replace("&", "and")
    yk = year_ks.lower().replace("-", "")
    return f"{subj}_{yk}.json"


def collect_extractions() -> list[tuple[Path, str]]:
    """Gather all extraction JSON file paths with their stage label (primary/secondary/eyfs)."""
    files = []

    # Primary extractions
    primary_dir = EXTRACTIONS_DIR / "primary"
    if primary_dir.exists():
        for p in sorted(primary_dir.glob("*_extracted.json")):
            files.append((p, "primary"))

    # Secondary extractions
    secondary_dir = EXTRACTIONS_DIR / "secondary"
    if secondary_dir.exists():
        for p in sorted(secondary_dir.glob("*_extracted.json")):
            files.append((p, "secondary"))

    # EYFS extractions
    if EYFS_EXTRACTIONS_DIR.exists():
        for p in sorted(EYFS_EXTRACTIONS_DIR.glob("*.json")):
            files.append((p, "eyfs"))

    return files


def extract_all(dry_run: bool = False, stats_only: bool = False) -> dict:
    """Main extraction pipeline.

    Returns stats dict with counts.
    """
    extraction_files = collect_extractions()
    if not extraction_files:
        print("ERROR: No extraction files found.")
        sys.exit(1)

    print(f"Found {len(extraction_files)} extraction files.\n")

    # Global registry: term_key -> term_id (for deduplication)
    # term_key = (subject_prefix, slug) — unique within a subject
    global_registry: dict[tuple[str, str], str] = {}

    # Track all concept links per term_id
    all_concept_links: dict[str, list[dict]] = defaultdict(list)

    # Track which file "owns" each term (first occurrence)
    term_owner: dict[str, str] = {}  # term_id -> output_filename

    # Per-file term collections
    file_terms: dict[str, list[dict]] = defaultdict(list)  # output_filename -> [term_stubs]
    file_metadata: dict[str, dict] = {}  # output_filename -> metadata

    # Statistics
    stats = {
        "extraction_files": len(extraction_files),
        "concepts_with_vocab": 0,
        "concepts_without_vocab": 0,
        "raw_term_instances": 0,
        "unique_terms": 0,
        "output_files": 0,
        "terms_per_subject": defaultdict(int),
    }

    for fpath, stage in extraction_files:
        with open(fpath) as f:
            data = json.load(f)

        metadata = data.get("metadata", {})
        subject = metadata.get("subject", "Unknown")
        prefix = SUBJECT_PREFIXES.get(subject, "XX")
        year_ks = detect_year_or_ks(fpath.stem, metadata)
        out_name = make_output_filename(subject, year_ks)

        file_metadata[out_name] = {
            "subject": subject,
            "year": year_ks,
            "source_file": fpath.name,
        }

        # Iterate concepts (may be nested under domains)
        concepts = []
        for domain in data.get("domains", []):
            concepts.extend(domain.get("concepts", []))
        # Also check top-level concepts (EYFS format)
        concepts.extend(data.get("concepts", []))

        for concept in concepts:
            concept_id = concept.get("concept_id", "")
            vocab_str = concept.get("key_vocabulary", "")

            if not vocab_str or not vocab_str.strip():
                stats["concepts_without_vocab"] += 1
                continue

            stats["concepts_with_vocab"] += 1
            terms = parse_key_vocabulary(vocab_str)

            for term_text in terms:
                stats["raw_term_instances"] += 1
                slug = slugify(term_text)
                if not slug:
                    continue

                term_key = (prefix, slug)
                if term_key not in global_registry:
                    term_id = f"VOC-{prefix}-{slug}"
                    global_registry[term_key] = term_id
                    term_owner[term_id] = out_name
                    stats["terms_per_subject"][prefix] += 1

                    # Create stub entry
                    file_terms[out_name].append({
                        "term_id": term_id,
                        "term": term_text.lower().strip(),
                        "definition": "",
                        "subject": subject,
                        "word_class": "",
                        "tier": 3 if prefix not in ("PE", "AD", "MU") else 2,
                        "etymology": "",
                        "example_usage": "",
                        "common_errors": "",
                        "related_everyday_word": "",
                    })

                term_id = global_registry[term_key]

                # Determine if this is the first concept to use this term
                existing_concept_ids = {
                    cl["concept_id"] for cl in all_concept_links[term_id]
                }
                if concept_id not in existing_concept_ids:
                    is_first = len(all_concept_links[term_id]) == 0
                    all_concept_links[term_id].append({
                        "concept_id": concept_id,
                        "introduced": is_first,
                        "importance": "core",
                    })

    stats["unique_terms"] = len(global_registry)

    if stats_only:
        _print_stats(stats)
        return stats

    if dry_run:
        _print_stats(stats)
        print("\n[DRY RUN] No files written.")
        return stats

    # Write output files
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    written_files = 0
    for out_name, terms in sorted(file_terms.items()):
        meta = file_metadata[out_name]

        # Attach concept_links to each term
        for term_stub in terms:
            term_stub["concept_links"] = all_concept_links.get(term_stub["term_id"], [])

        output = {
            "metadata": {
                "subject": meta["subject"],
                "year": meta["year"],
                "source_file": meta["source_file"],
                "term_count": len(terms),
            },
            "terms": sorted(terms, key=lambda t: t["term"]),
        }

        out_path = OUTPUT_DIR / out_name
        with open(out_path, "w") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        written_files += 1
        print(f"  {out_name}: {len(terms)} terms")

    stats["output_files"] = written_files

    print()
    _print_stats(stats)

    # Write empty relationship skeleton files
    rel_dir = Path(__file__).resolve().parents[1] / "data" / "relationships"
    rel_dir.mkdir(parents=True, exist_ok=True)

    for rel_file, desc in [
        ("refinements.json", "REFINES chains — e.g. 'integer' REFINES 'number'"),
        ("polysemy.json", "SAME_SPELLING_AS groups — e.g. VOC-SC-cell ↔ VOC-CO-cell"),
        ("semantic.json", "RELATED_TO links — synonyms, antonyms, hypernyms, meronyms"),
    ]:
        rel_path = rel_dir / rel_file
        if not rel_path.exists():
            skeleton = {
                "_comment": desc,
                "relationships": [],
            }
            with open(rel_path, "w") as f:
                json.dump(skeleton, f, indent=2)
            print(f"  Created skeleton: relationships/{rel_file}")

    return stats


def _print_stats(stats: dict):
    print("=" * 60)
    print("EXTRACTION SUMMARY")
    print("=" * 60)
    print(f"  Extraction files scanned:   {stats['extraction_files']}")
    print(f"  Concepts with vocabulary:   {stats['concepts_with_vocab']}")
    print(f"  Concepts without vocabulary:{stats['concepts_without_vocab']}")
    print(f"  Raw term instances:         {stats['raw_term_instances']}")
    print(f"  Unique terms (deduplicated):{stats['unique_terms']}")
    print(f"  Output files written:       {stats.get('output_files', 'N/A')}")
    print()
    print("  Terms by subject prefix:")
    for prefix, count in sorted(stats["terms_per_subject"].items(), key=lambda x: -x[1]):
        print(f"    {prefix}: {count}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract vocabulary terms from curriculum extraction JSONs"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Parse and count but don't write files"
    )
    parser.add_argument(
        "--stats", action="store_true",
        help="Print statistics only"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("Vocabulary Term Extractor")
    print("=" * 60)

    extract_all(dry_run=args.dry_run, stats_only=args.stats)

    print("\nDone.")


if __name__ == "__main__":
    main()

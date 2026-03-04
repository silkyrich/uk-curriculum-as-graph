#!/usr/bin/env python3
"""
Compile teacher planner metadata into a JSON manifest for the static site.

Walks generated/teacher-planners/, parses the structured header of each .md
file, and writes site/src/data/planners_manifest.json.

Usage:
    python3 scripts/compile_planners_manifest.py
    python3 scripts/compile_planners_manifest.py --output site/src/data
"""

import argparse
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PLANNERS_DIR = PROJECT_ROOT / "generated" / "teacher-planners"


def parse_planner_header(md_path: Path) -> dict | None:
    """Parse the structured header from a planner markdown file."""
    try:
        text = md_path.read_text(encoding="utf-8")
    except Exception:
        return None

    lines = text.split("\n")
    if len(lines) < 6:
        return None

    # Line 1: # Subject | Teacher Planner: Title
    title_match = re.search(r"Teacher Planner:\s*(.+)", lines[0])
    title = title_match.group(1).strip() if title_match else md_path.stem.replace("_", " ").title()

    # Line 2: *[STUDY-ID]*
    id_match = re.search(r"\*\[([^\]]+)\]\*", lines[1])
    study_id = id_match.group(1) if id_match else ""

    # Line 4 (index 3): **Subject:** X | **Key Stage:** Y | **Year group:** Z
    subject = ""
    key_stage = ""
    year_groups = []

    for line in lines[2:8]:
        subj_match = re.search(r"\*\*Subject:\*\*\s*([^|*]+)", line)
        if subj_match:
            subject = subj_match.group(1).strip()
        ks_match = re.search(r"\*\*Key Stage:\*\*\s*([^|*]+)", line)
        if ks_match:
            key_stage = ks_match.group(1).strip()
        yg_match = re.search(r"\*\*Year group:\*\*\s*([^|*]+)", line)
        if yg_match:
            year_groups = [y.strip() for y in yg_match.group(1).split(",")]

    # Line 6 (index 5): **Estimated duration:** N lessons | **Study type:** X | **Status:** Y
    duration = ""
    study_type = ""
    status = ""

    for line in lines[4:8]:
        dur_match = re.search(r"\*\*Estimated duration:\*\*\s*([^|*]+)", line)
        if dur_match:
            duration = dur_match.group(1).strip()
        st_match = re.search(r"\*\*Study type:\*\*\s*([^|*]+)", line)
        if st_match:
            study_type = st_match.group(1).strip()
        stat_match = re.search(r"\*\*Status:\*\*\s*([^|*\n]+)", line)
        if stat_match:
            status = stat_match.group(1).strip()

    # Line 8 (index 7): **Planner coverage:** 9/11 expected capabilities surfaced
    coverage = ""
    for line in lines[6:10]:
        cov_match = re.search(r"\*\*Planner coverage:\*\*\s*(\d+/\d+)", line)
        if cov_match:
            coverage = cov_match.group(1)
            break

    folder = md_path.parent.name
    slug = md_path.stem

    return {
        "study_id": study_id,
        "title": title,
        "subject": subject,
        "key_stage": key_stage,
        "year_groups": year_groups,
        "duration": duration,
        "study_type": study_type,
        "status": status,
        "coverage": coverage,
        "folder": folder,
        "slug": slug,
    }


def main():
    parser = argparse.ArgumentParser(description="Compile planner manifest for static site")
    parser.add_argument(
        "--output",
        type=str,
        default=str(PROJECT_ROOT / "site" / "src" / "data"),
        help="Output directory for planners_manifest.json",
    )
    parser.add_argument(
        "--planners-dir",
        type=str,
        default=str(PLANNERS_DIR),
        help="Directory containing generated teacher planners",
    )
    args = parser.parse_args()

    planners_dir = Path(args.planners_dir)
    out_dir = Path(args.output)

    if not planners_dir.exists():
        print(f"Planners directory not found: {planners_dir}")
        print("Run scripts/generate_all_planners.py --all --format md first.")
        return

    manifest = []
    md_files = sorted(planners_dir.rglob("*.md"))

    for md_path in md_files:
        entry = parse_planner_header(md_path)
        if entry:
            manifest.append(entry)

    # Sort by subject, key_stage, title
    manifest.sort(key=lambda e: (e["subject"], e["key_stage"], e["title"]))

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "planners_manifest.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(manifest)} planner entries to {out_path}")

    # Summary by subject
    subjects = {}
    for e in manifest:
        subjects[e["subject"]] = subjects.get(e["subject"], 0) + 1
    for subj, count in sorted(subjects.items()):
        print(f"  {subj}: {count}")


if __name__ == "__main__":
    main()

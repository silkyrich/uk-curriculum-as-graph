#!/usr/bin/env python3
"""
Generate teacher planners for all study nodes in the knowledge graph.

Usage:
    # Generate everything (md + pptx + docx)
    python3 scripts/generate_all_planners.py --all

    # Markdown only
    python3 scripts/generate_all_planners.py --all --format md

    # Filter by subject
    python3 scripts/generate_all_planners.py --subject history

    # Filter by key stage
    python3 scripts/generate_all_planners.py --subject science --ks KS2

    # Single study by ID
    python3 scripts/generate_all_planners.py --id HS-KS2-002

    # Dry run
    python3 scripts/generate_all_planners.py --all --dry-run
"""

import argparse
import sys
import time
from pathlib import Path

# Ensure we can import sibling modules
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT / "core" / "scripts"))

from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from planner_queries import (
    STUDY_NODES, query_all_study_ids, fetch_study_context,
    slugify, output_folder,
)
from render_markdown import render_markdown

OUTPUT_DIR = PROJECT_ROOT / "generated" / "teacher-planners"


def parse_args():
    parser = argparse.ArgumentParser(
        description='Generate teacher planners from the knowledge graph.'
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--all', action='store_true',
                       help='Generate planners for all study nodes')
    group.add_argument('--subject', type=str,
                       help='Filter by subject (e.g. history, science, english)')
    group.add_argument('--id', type=str,
                       help='Generate for a single study ID (e.g. HS-KS2-002)')

    parser.add_argument('--ks', type=str,
                        help='Filter by key stage (e.g. KS2) — combine with --subject')
    parser.add_argument('--format', type=str, default='md,pptx,docx',
                        help='Comma-separated formats: md,pptx,docx (default: all)')
    parser.add_argument('--dry-run', action='store_true',
                        help='List what would be generated without creating files')
    parser.add_argument('--output', type=str, default=None,
                        help='Override output directory')
    return parser.parse_args()


def resolve_study_id(study_id: str) -> tuple[str, str]:
    """Given a study ID, determine its label and id_field."""
    # Prefix-based detection
    prefix_map = {
        'HS-':    'HistoryStudy',
        'GS-GE-': 'GeoStudy',
        'SE-':    'ScienceEnquiry',
        'EU-':    'EnglishUnit',
        'TS-AD-': 'ArtTopicSuggestion',
        'TS-MU-': 'MusicTopicSuggestion',
        'TS-DT-': 'DTTopicSuggestion',
        'TS-CO-': 'ComputingTopicSuggestion',
        'TS-RS-': 'TopicSuggestion',
        'TS-CI-': 'TopicSuggestion',
    }
    for prefix, label in prefix_map.items():
        if study_id.startswith(prefix):
            return label, STUDY_NODES[label]['id_field']

    # Fallback: try all labels
    return None, None


def subject_matches(subject: str, filter_subject: str) -> bool:
    """Check if a subject matches the filter (case-insensitive, partial match)."""
    fs = filter_subject.lower()
    s = subject.lower()
    # Direct match
    if fs == s:
        return True
    # Partial match
    if fs in s or s.startswith(fs):
        return True
    # Common abbreviations
    abbrevs = {
        'dt': 'design and technology',
        'art': 'art and design',
        'rs': 'religious studies',
        'computing': 'computing',
        'comp': 'computing',
        'geo': 'geography',
        'hist': 'history',
        'sci': 'science',
        'eng': 'english',
        'mus': 'music',
    }
    return abbrevs.get(fs, '') == s


def get_renderers(formats: str) -> dict:
    """Load requested renderers. Returns {ext: render_fn}."""
    requested = [f.strip().lower() for f in formats.split(',')]
    renderers = {}

    if 'md' in requested:
        renderers['md'] = render_markdown

    if 'pptx' in requested:
        try:
            from render_pptx import render_pptx
            renderers['pptx'] = render_pptx
        except ImportError:
            print("  Warning: render_pptx.py not found, skipping PPTX generation")

    if 'docx' in requested:
        try:
            from render_docx import render_docx
            renderers['docx'] = render_docx
        except ImportError:
            print("  Warning: render_docx.py not found, skipping DOCX generation")

    return renderers


def generate_planner(session, label: str, study_id: str, renderers: dict,
                     output_dir: Path, dry_run: bool = False) -> tuple[bool, str]:
    """Generate planner files for a single study. Returns (success, message)."""
    ctx = fetch_study_context(session, label, study_id)
    if not ctx:
        return False, f"Study not found: {label}:{study_id}"

    folder_name = output_folder(ctx.subject, ctx.key_stage)
    file_stem = slugify(ctx.study.get('name', study_id))
    folder = output_dir / folder_name
    formats_generated = []

    if dry_run:
        for ext in renderers:
            formats_generated.append(ext)
        return True, f"{folder_name}/{file_stem} ({'+'.join(formats_generated)})"

    folder.mkdir(parents=True, exist_ok=True)

    for ext, render_fn in renderers.items():
        filepath = folder / f"{file_stem}.{ext}"
        try:
            output = render_fn(ctx)
            if ext == 'md':
                filepath.write_text(output, encoding='utf-8')
            else:
                # PPTX and DOCX renderers return bytes or save directly
                if isinstance(output, bytes):
                    filepath.write_bytes(output)
                elif isinstance(output, str):
                    filepath.write_text(output, encoding='utf-8')
                else:
                    # Assume it's a Presentation or Document object with .save()
                    output.save(str(filepath))
            formats_generated.append(ext)
        except Exception as e:
            formats_generated.append(f"{ext}:ERR")
            print(f"    Error generating {ext} for {study_id}: {e}")

    return True, f"{folder_name}/{file_stem} ({'+'.join(formats_generated)})"


def main():
    args = parse_args()
    renderers = get_renderers(args.format)

    if not renderers:
        print("Error: No valid formats specified.")
        sys.exit(1)

    out_dir = Path(args.output) if args.output else OUTPUT_DIR

    print(f"Connecting to Neo4j: {NEO4J_URI}")
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    try:
        with driver.session() as session:
            # Build list of studies to generate
            if args.id:
                label, id_field = resolve_study_id(args.id)
                if not label:
                    # Try to find it by querying all
                    all_studies = query_all_study_ids(session)
                    match = [s for s in all_studies if s['study_id'] == args.id]
                    if match:
                        label = match[0]['label']
                    else:
                        print(f"Error: Cannot resolve study ID: {args.id}")
                        sys.exit(1)
                studies = [{'study_id': args.id, 'label': label, 'name': args.id,
                           'key_stage': '', 'subject': ''}]
            else:
                all_studies = query_all_study_ids(session)
                studies = all_studies

                # Apply filters
                if args.subject:
                    studies = [s for s in studies
                              if subject_matches(s.get('subject', ''), args.subject)]

                if args.ks:
                    ks = args.ks.upper()
                    studies = [s for s in studies if s.get('key_stage', '').upper() == ks]

            if not studies:
                print("No studies matched the given filters.")
                sys.exit(0)

            total = len(studies)
            fmt_list = ','.join(renderers.keys())
            action = "Would generate" if args.dry_run else "Generating"
            print(f"\n{action} teacher planners for {total} studies ({fmt_list})...")
            if args.dry_run:
                print(f"Output directory: {out_dir}\n")

            success_count = 0
            error_count = 0
            start_time = time.time()

            for i, study_info in enumerate(studies, 1):
                sid = study_info['study_id']
                label = study_info['label']
                name = study_info.get('name', sid)

                ok, msg = generate_planner(
                    session, label, sid, renderers, out_dir, dry_run=args.dry_run
                )

                status = "+" if ok else "X"
                print(f"[{i:3d}/{total}] {msg} {status}")

                if ok:
                    success_count += 1
                else:
                    error_count += 1

            elapsed = time.time() - start_time
            file_count = success_count * len(renderers)

            print(f"\nDone: {success_count} studies -> {file_count} files "
                  f"in {out_dir.relative_to(PROJECT_ROOT)}/")
            if error_count:
                print(f"Errors: {error_count}")
            print(f"Time: {elapsed:.1f}s")

    finally:
        driver.close()


if __name__ == '__main__':
    main()

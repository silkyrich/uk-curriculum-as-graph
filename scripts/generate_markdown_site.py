#!/usr/bin/env python3
"""
Generate a complete hierarchical markdown export of the curriculum graph.

The website (compile_site_data.py) compiles eight graph views into JSON.
The markdown build previously only emitted per-study teacher planners, so it
was missing every other view the site exposes. This script closes that gap:
it runs the *same* graph queries and renders all of them as markdown into a
nicely nested folder tree.

Output layout (default: generated/markdown-site/):

    README.md                                  site index + global stats
    subjects/<subject>/README.md               subject overview
    subjects/<subject>/<year>/<domain>.md       full domain page
    thinking-lenses/README.md + <lens>.md
    learner-profiles/README.md + <year>.md
    delivery-modes/README.md
    prerequisites/README.md
    planners/README.md
    planners/<subject>/<key-stage>/<study>.md   teacher planners

Usage:
    python3 scripts/generate_markdown_site.py
    python3 scripts/generate_markdown_site.py --output generated/markdown-site
    python3 scripts/generate_markdown_site.py --no-planners
"""

import argparse
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(PROJECT_ROOT / "core" / "scripts"))

from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

import compile_site_data as csd
import render_site_markdown as md
from planner_queries import (
    query_all_study_ids, fetch_study_context,
    slugify as planner_slugify, subject_slug,
)
from render_markdown import render_markdown

DEFAULT_OUTPUT = PROJECT_ROOT / "generated" / "markdown-site"


def write(path: Path, content: str):
    """Write a markdown file, creating parent folders as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not content.endswith('\n'):
        content += '\n'
    path.write_text(content, encoding='utf-8')


def generate_graph_views(session, out: Path) -> dict:
    """Render the seven non-planner graph views. Returns the data needed
    for the root index."""
    print("  Compiling overview...")
    overview = csd.query_overview(session)

    print("  Compiling subjects...")
    subjects = csd.query_subjects(session)
    for subject in subjects:
        sslug = subject.get('slug') or md.slug(subject.get('name', ''))
        write(out / 'subjects' / sslug / 'README.md',
              md.render_subject_index(subject))

    print("  Compiling domains...")
    domain_ids = csd.query_all_domains(session)
    domain_count = 0
    for i, did in enumerate(domain_ids, 1):
        domain = csd.query_domain_detail(session, did)
        if not domain:
            continue
        subj_name = domain.get('subject')
        sslug = md.slug(subj_name) if subj_name else '_orphans'
        yslug = domain.get('year_id') or '_no-year'
        write(out / 'subjects' / sslug / yslug / f"{did}.md",
              md.render_domain(domain))
        domain_count += 1
        if i % 50 == 0:
            print(f"    {i}/{len(domain_ids)} domains")
    print(f"    {domain_count} domain pages written")

    print("  Compiling thinking lenses...")
    lenses = csd.query_thinking_lenses(session)
    write(out / 'thinking-lenses' / 'README.md', md.render_lens_index(lenses))
    for tl in lenses:
        write(out / 'thinking-lenses' / f"{md.slug(tl.get('name', ''))}.md",
              md.render_lens(tl))

    print("  Compiling learner profiles...")
    profiles = csd.query_learner_profiles(session)
    write(out / 'learner-profiles' / 'README.md',
          md.render_profile_index(profiles))
    for p in profiles:
        write(out / 'learner-profiles' / f"{md.slug(p.get('year_id', ''))}.md",
              md.render_profile(p))

    print("  Compiling delivery modes...")
    delivery = csd.query_delivery_modes(session)
    write(out / 'delivery-modes' / 'README.md', md.render_delivery(delivery))

    print("  Compiling prerequisites...")
    prereq_graph = csd.query_prerequisite_graph(session)
    write(out / 'prerequisites' / 'README.md',
          md.render_prerequisites(prereq_graph))

    return {'overview': overview, 'subjects': subjects, 'lenses': lenses,
            'profiles': profiles}


def generate_planners(session, out: Path) -> list[dict]:
    """Render every study planner into planners/<subject>/<ks>/. Returns a
    manifest list for the planner index."""
    studies = query_all_study_ids(session)
    print(f"  Generating {len(studies)} teacher planners...")
    manifest = []
    planners_root = out / 'planners'

    for i, study in enumerate(studies, 1):
        sid = study['study_id']
        label = study['label']
        ctx = fetch_study_context(session, label, sid)
        if not ctx:
            print(f"    [skip] {label}:{sid} — no context")
            continue
        sslug = subject_slug(ctx.subject or 'other')
        ks = (ctx.key_stage or 'general').lower()
        stem = planner_slugify(ctx.study.get('name', sid))
        rel_path = f"{sslug}/{ks}/{stem}.md"
        write(planners_root / rel_path, render_markdown(ctx))
        manifest.append({
            'study_id': sid,
            'title': ctx.study.get('name', sid),
            'subject': ctx.subject or 'Other',
            'key_stage': ctx.key_stage or '',
            'rel_path': rel_path,
        })
        if i % 50 == 0:
            print(f"    {i}/{len(studies)} planners")

    write(planners_root / 'README.md', md.render_planner_index(manifest))
    print(f"    {len(manifest)} planners written")
    return manifest


def main():
    parser = argparse.ArgumentParser(
        description='Generate a hierarchical markdown export of the graph.')
    parser.add_argument('--output', type=str, default=str(DEFAULT_OUTPUT),
                        help='Output directory (default: generated/markdown-site)')
    parser.add_argument('--no-planners', action='store_true',
                        help='Skip teacher planner generation (graph views only)')
    args = parser.parse_args()

    out = Path(args.output)
    print(f"Connecting to Neo4j: {NEO4J_URI}")
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    start = time.time()

    try:
        with driver.session() as session:
            views = generate_graph_views(session, out)

            planners = []
            if not args.no_planners:
                planners = generate_planners(session, out)

            # Root index — written last so it can count planners
            write(out / 'README.md', md.render_site_index(
                views['overview'], views['subjects'], views['lenses'],
                views['profiles'], len(planners)))
    finally:
        driver.close()

    elapsed = time.time() - start
    file_count = sum(1 for _ in out.rglob('*.md'))
    print(f"\nDone: {file_count} markdown files written to {out}")
    print(f"Time: {elapsed:.1f}s")


if __name__ == '__main__':
    main()

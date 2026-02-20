#!/usr/bin/env python3
"""
Apply all visualization formatting to the knowledge graph.

This is the entry point for the visualization layer. Runs in order:
  1. add_name_properties   — ensures every node has a 'name' property for Neo4j Browser
  2. add_display_properties — applies color, icon, category, size to all nodes
  3. upload_bloom_perspective — writes the Bloom perspective into the database

Usage:
  python3 layers/visualization/scripts/apply_formatting.py
  python3 layers/visualization/scripts/apply_formatting.py --skip-perspective
"""
import sys
import subprocess
import argparse
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPTS_DIR.parent.parent.parent


def run_script(script_path: Path, args: list = None) -> bool:
    cmd = [sys.executable, str(script_path)] + (args or [])
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description='Apply all visualization formatting')
    parser.add_argument('--skip-perspective', action='store_true',
                        help='Skip uploading Bloom perspective')
    parsed = parser.parse_args()

    print('=' * 70)
    print('VISUALIZATION LAYER — APPLY FORMATTING')
    print('=' * 70)

    steps = [
        ('Name properties',    SCRIPTS_DIR / 'add_name_properties.py',    []),
        ('Display properties', SCRIPTS_DIR / 'add_display_properties.py', []),
    ]
    if not parsed.skip_perspective:
        steps.append(('Bloom perspective', SCRIPTS_DIR / 'upload_bloom_perspective.py', []))

    failed = []
    for label, script, args in steps:
        print(f'\n{"─" * 70}')
        print(f'Step: {label}')
        print('─' * 70)
        if not run_script(script, args):
            print(f'✗ {label} FAILED')
            failed.append(label)

    print('\n' + '=' * 70)
    if failed:
        print(f'✗ {len(failed)} step(s) failed: {", ".join(failed)}')
        sys.exit(1)
    else:
        print('✅ Visualization formatting applied successfully!')
        print('   Open Bloom and select "UK Curriculum Knowledge Graph" perspective.')
    print('=' * 70)


if __name__ == '__main__':
    main()

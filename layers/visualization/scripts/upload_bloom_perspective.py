#!/usr/bin/env python3
"""
Write Bloom perspectives directly into the Neo4j database.

Bloom reads perspectives from _Bloom_Perspective_ nodes, so this script
creates/updates those nodes from JSON files — no manual import needed.

Usage:
  python3 layers/visualization/scripts/upload_bloom_perspective.py           # upload all perspectives
  python3 layers/visualization/scripts/upload_bloom_perspective.py --perspective path/to/file.json
"""
import json
import time
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "core" / "scripts"))
from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

LAYER_ROOT = Path(__file__).parent.parent
PERSPECTIVES_DIR = LAYER_ROOT / 'data' / 'perspectives'


def upload_perspective(driver, perspective_path: Path):
    with open(perspective_path) as f:
        perspective = json.load(f)

    perspective_json = json.dumps(perspective)
    ts = int(time.time() * 1000)
    name = perspective['name']

    with driver.session() as s:
        existing = s.run(
            'MATCH (p:`_Bloom_Perspective_` {name: $name}) RETURN p.name AS name',
            name=name
        ).single()

        if existing:
            s.run('''
                MATCH (p:`_Bloom_Perspective_` {name: $name})
                SET p.perspective = $perspective,
                    p.version     = $version,
                    p.updatedAt   = $ts
            ''', name=name, perspective=perspective_json,
                 version=perspective.get('version', '1.4.0'), ts=ts)
            action = 'Updated'
        else:
            s.run('''
                CREATE (p:`_Bloom_Perspective_`)
                SET p.name        = $name,
                    p.version     = $version,
                    p.perspective = $perspective,
                    p.hide        = false,
                    p.createdAt   = $ts,
                    p.updatedAt   = $ts
            ''', name=name, perspective=perspective_json,
                 version=perspective.get('version', '1.4.0'), ts=ts)
            action = 'Created'

        print(f'  {action}: "{name}"')


def main():
    parser = argparse.ArgumentParser(description='Upload Bloom perspectives to Neo4j')
    parser.add_argument('--perspective', default=None,
                        help='Path to a single perspective JSON file (default: upload all)')
    args = parser.parse_args()

    if args.perspective:
        paths = [Path(args.perspective)]
    else:
        paths = sorted(PERSPECTIVES_DIR.glob('*.json'))

    missing = [p for p in paths if not p.exists()]
    if missing:
        for p in missing:
            print(f'✗ Not found: {p}')
        raise SystemExit(1)

    print('=' * 60)
    print('UPLOADING BLOOM PERSPECTIVES')
    print('=' * 60)
    print(f'  URI: {NEO4J_URI}')
    print(f'  Perspectives: {len(paths)}\n')

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    try:
        for path in paths:
            upload_perspective(driver, path)

        with driver.session() as s:
            result = s.run(
                'MATCH (p:`_Bloom_Perspective_`) RETURN count(p) AS c, collect(p.name) AS names'
            ).single()
            print(f'\nTotal perspectives in database: {result["c"]}')
            for n in sorted(result['names']):
                print(f'  • {n}')

        print('\n✓ Done — refresh Bloom to see the perspectives')
    finally:
        driver.close()


if __name__ == '__main__':
    main()

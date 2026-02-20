#!/usr/bin/env python3
"""
Write Bloom perspective directly into the Neo4j database.

Bloom reads perspectives from _Bloom_Perspective_ nodes, so this script
creates/updates that node from the JSON file — no manual import needed.

Usage:
  python3 layers/visualization/scripts/upload_bloom_perspective.py
  python3 layers/visualization/scripts/upload_bloom_perspective.py --perspective layers/visualization/data/perspectives/main_perspective.json
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
DEFAULT_PERSPECTIVE = LAYER_ROOT / 'data' / 'perspectives' / 'main_perspective.json'


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
                 version=perspective.get('version', '1.4'), ts=ts)
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
                 version=perspective.get('version', '1.4'), ts=ts)
            action = 'Created'

        result = s.run(
            'MATCH (p:`_Bloom_Perspective_`) RETURN count(p) AS c, collect(p.name) AS names'
        ).single()

        print(f'  {action}: "{name}"')
        print(f'  Total perspectives in database: {result["c"]}')
        for n in result['names']:
            print(f'    • {n}')


def main():
    parser = argparse.ArgumentParser(description='Upload Bloom perspective to Neo4j')
    parser.add_argument('--perspective', default=str(DEFAULT_PERSPECTIVE),
                        help='Path to perspective JSON file')
    args = parser.parse_args()

    perspective_path = Path(args.perspective)
    if not perspective_path.exists():
        print(f'✗ Perspective file not found: {perspective_path}')
        raise SystemExit(1)

    print('='*60)
    print('UPLOADING BLOOM PERSPECTIVE')
    print('='*60)
    print(f'  File: {perspective_path}')
    print(f'  URI:  {NEO4J_URI}\n')

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    try:
        upload_perspective(driver, perspective_path)
        print('\n✓ Done — refresh Bloom to see the perspective')
    finally:
        driver.close()


if __name__ == '__main__':
    main()

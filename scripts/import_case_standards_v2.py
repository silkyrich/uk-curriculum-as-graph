#!/usr/bin/env python3
"""
Import CASE standards with PROPER structure parsing

Graph Model v3.5 (restructured) — CASE Standards layer

Creates properly-structured CASE frameworks that expose pedagogical models:
- NGSS: 3-dimensional learning (SEPs, DCIs, CCCs → Performance Expectations)
- Common Core Math: Practices + Content (SMPs → Standards by grade)

This replaces the generic blob import with intelligent structure parsing.
"""

import json
import time
import argparse
from pathlib import Path
from collections import defaultdict

import requests
from neo4j import GraphDatabase

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Updated to use shared config
# Updated to use shared config
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

PROJECT_ROOT = Path(__file__).parent.parent
CASE_DIR = PROJECT_ROOT / "data" / "extractions" / "case"
PACKAGES_DIR = CASE_DIR / "packages"
SOURCES_FILE = CASE_DIR / "case_sources.json"

REQUEST_DELAY_SECONDS = 1.0
BATCH_SIZE = 200


# ---------------------------------------------------------------------------
# NGSS Structure Parser
# ---------------------------------------------------------------------------

class NGSSParser:
    """Parse NGSS 3-dimensional learning structure from CASE package."""

    def __init__(self, package_data):
        self.package = package_data
        self.items_by_id = {item['identifier']: item for item in package_data['CFItems']}
        self.children_map = self._build_children_map()

    def _build_children_map(self):
        """Build parent → [children] map from associations."""
        children = defaultdict(list)
        for assoc in self.package['CFAssociations']:
            if assoc.get('associationType') == 'isChildOf':
                parent_id = assoc.get('destinationNodeURI', {}).get('identifier')
                child_id = assoc.get('originNodeURI', {}).get('identifier')
                if parent_id and child_id:
                    children[parent_id].append(child_id)
        return children

    def find_item_by_statement(self, statement_text):
        """Find CFItem by exact fullStatement match."""
        for item in self.package['CFItems']:
            if item.get('fullStatement', '').strip() == statement_text:
                return item
        return None

    def get_dimension_structure(self):
        """Parse the 3 dimensions and their children."""
        dimensions = {}

        # Find the 3 dimension parent nodes
        dimension_names = [
            "Science and Engineering Practices",
            "Disciplinary Core Ideas",
            "Crosscutting Concepts"
        ]

        for dim_name in dimension_names:
            dim_item = self.find_item_by_statement(dim_name)
            if dim_item:
                dim_id = dim_item['identifier']
                child_ids = self.children_map.get(dim_id, [])
                child_items = [self.items_by_id[cid] for cid in child_ids if cid in self.items_by_id]

                dimensions[dim_name] = {
                    'item': dim_item,
                    'children': child_items
                }

        return dimensions

    def get_performance_expectations(self):
        """Extract all Performance Expectations."""
        pes = []
        for item in self.package['CFItems']:
            if item.get('CFItemType') == 'Performance Expectation':
                pes.append(item)
        return pes

    def get_grade_bands(self):
        """Extract grade band structure."""
        grade_bands = set()
        for item in self.package['CFItems']:
            edu_levels = item.get('educationLevel', [])
            for level in edu_levels:
                # Map to grade bands
                if level in ['KG', '1', '2']:
                    grade_bands.add('K-2')
                elif level in ['3', '4', '5']:
                    grade_bands.add('3-5')
                elif level in ['6', '7', '8']:
                    grade_bands.add('6-8')
                elif level in ['9', '10', '11', '12']:
                    grade_bands.add('9-12')
        return sorted(grade_bands)


# ---------------------------------------------------------------------------
# Common Core Math Parser
# ---------------------------------------------------------------------------

class CommonCoreMathParser:
    """Parse Common Core Math structure from CASE package."""

    def __init__(self, package_data):
        self.package = package_data
        self.items_by_id = {item['identifier']: item for item in package_data['CFItems']}

    def get_math_practices(self):
        """Extract the 8 Standards for Mathematical Practice."""
        practices = []
        for item in self.package['CFItems']:
            stmt = item.get('fullStatement', '')
            code = item.get('humanCodingScheme', '')
            # SMPs have codes like "CCSS.Math.Practice.MP1"
            if 'MP' in code and 'Practice' in code:
                practices.append(item)
        return sorted(practices, key=lambda x: x.get('humanCodingScheme', ''))

    def get_grade_levels(self):
        """Extract grade levels (K, 1, 2, ..., 8, HS)."""
        grades = set()
        for item in self.package['CFItems']:
            code = item.get('humanCodingScheme', '')
            if code.startswith('CCSS.Math.Content.'):
                # Extract grade: CCSS.Math.Content.K.CC.1 → K
                parts = code.split('.')
                if len(parts) >= 4:
                    grade = parts[3]
                    grades.add(grade)
        return sorted(grades)


# ---------------------------------------------------------------------------
# Neo4j Importer (Restructured)
# ---------------------------------------------------------------------------

class CaseStandardsImporter:
    """Import CASE with proper structure parsing."""

    def __init__(self, driver):
        self.driver = driver
        self.stats = defaultdict(int)

    def import_ngss(self, package_data, source_def):
        """Import NGSS with 3D learning model structure."""
        parser = NGSSParser(package_data)

        with self.driver.session() as session:
            # Create Framework node
            framework_id = source_def['framework_id']
            session.run("""
                MERGE (f:Framework:CASE {framework_id: $framework_id})
                SET f.title = $title,
                    f.jurisdiction_id = $jurisdiction_id,
                    f.model_type = 'three_dimensional',
                    f.subject = $subject,
                    f.licence = $licence
            """, framework_id=framework_id,
                 title=source_def['title'],
                 jurisdiction_id=source_def['jurisdiction']['jurisdiction_id'],
                 subject=source_def['subject'],
                 licence=source_def['licence'])
            self.stats['frameworks'] += 1

            # Parse and create 3 Dimensions
            dimensions = parser.get_dimension_structure()

            for dim_name, dim_data in dimensions.items():
                dimension_type = {
                    "Science and Engineering Practices": "practice",
                    "Disciplinary Core Ideas": "core_idea",
                    "Crosscutting Concepts": "crosscutting"
                }.get(dim_name)

                dimension_id = f"ngss-{dimension_type}"

                session.run("""
                    MERGE (d:Dimension:CASE {dimension_id: $dimension_id})
                    SET d.dimension_name = $dimension_name,
                        d.dimension_type = $dimension_type,
                        d.framework_id = $framework_id
                    WITH d
                    MATCH (f:Framework {framework_id: $framework_id})
                    MERGE (f)-[:HAS_DIMENSION]->(d)
                """, dimension_id=dimension_id,
                     dimension_name=dim_name,
                     dimension_type=dimension_type,
                     framework_id=framework_id)
                self.stats['dimensions'] += 1

                # Create children of this dimension
                if dimension_type == 'practice':
                    self._create_practices(session, dim_data['children'], dimension_id)
                elif dimension_type == 'core_idea':
                    self._create_core_ideas(session, dim_data['children'], dimension_id)
                elif dimension_type == 'crosscutting':
                    self._create_crosscutting_concepts(session, dim_data['children'], dimension_id)

            # Create GradeBands
            grade_bands = parser.get_grade_bands()
            for gb_code in grade_bands:
                session.run("""
                    MERGE (gb:GradeBand:CASE {grade_band_id: $grade_band_id})
                    SET gb.grade_band_code = $grade_band_code,
                        gb.framework_id = $framework_id
                    WITH gb
                    MATCH (f:Framework {framework_id: $framework_id})
                    MERGE (f)-[:HAS_GRADE_BAND]->(gb)
                """, grade_band_id=f"ngss-{gb_code.lower()}",
                     grade_band_code=gb_code,
                     framework_id=framework_id)
                self.stats['grade_bands'] += 1

            # Create Performance Expectations
            pes = parser.get_performance_expectations()
            for pe_item in pes:
                code = pe_item.get('humanCodingScheme', '')
                if not code:
                    continue

                # Determine grade band from education level
                edu_levels = pe_item.get('educationLevel', [])
                grade_band_id = self._map_to_grade_band(edu_levels, 'ngss')

                session.run("""
                    MERGE (pe:PerformanceExpectation:CASE {pe_id: $pe_id})
                    SET pe.code = $code,
                        pe.statement = $statement,
                        pe.grade_band_id = $grade_band_id,
                        pe.framework_id = $framework_id
                    WITH pe
                    MATCH (gb:GradeBand {grade_band_id: $grade_band_id})
                    MERGE (gb)-[:HAS_PE]->(pe)
                """, pe_id=code,
                     code=code,
                     statement=pe_item.get('fullStatement', ''),
                     grade_band_id=grade_band_id,
                     framework_id=framework_id)
                self.stats['performance_expectations'] += 1

            print(f"  Created NGSS structure: {self.stats['dimensions']} dimensions, "
                  f"{self.stats['practices']} practices, {self.stats['core_ideas']} core ideas, "
                  f"{self.stats['performance_expectations']} PEs")

    def _create_practices(self, session, practice_items, dimension_id):
        """Create Practice nodes from SEP children."""
        # Filter to actual practices (8 main ones)
        practice_names = [
            "Asking Questions and Defining Problems",
            "Developing and Using Models",
            "Planning and Carrying Out Investigations",
            "Analyzing and Interpreting Data",
            "Using Mathematics and Computational Thinking",
            "Constructing Explanations and Designing Solutions",
            "Engaging in Argument from Evidence",
            "Obtaining, Evaluating, and Communicating Information"
        ]

        practice_num = 1
        for item in practice_items:
            stmt = item.get('fullStatement', '').strip()
            if stmt in practice_names:
                practice_id = f"ngss-sep-{practice_num}"
                session.run("""
                    MERGE (p:Practice:CASE {practice_id: $practice_id})
                    SET p.practice_name = $practice_name,
                        p.practice_number = $practice_number,
                        p.dimension_id = $dimension_id,
                        p.description = $description
                    WITH p
                    MATCH (d:Dimension {dimension_id: $dimension_id})
                    MERGE (d)-[:HAS_PRACTICE]->(p)
                """, practice_id=practice_id,
                     practice_name=stmt,
                     practice_number=practice_num,
                     dimension_id=dimension_id,
                     description=item.get('notes', ''))
                self.stats['practices'] += 1
                practice_num += 1

    def _create_core_ideas(self, session, dci_items, dimension_id):
        """Create CoreIdea nodes from DCI children."""
        for item in dci_items:
            code = item.get('humanCodingScheme', '')
            if not code:
                continue

            core_idea_id = f"ngss-{code.lower()}"
            session.run("""
                MERGE (ci:CoreIdea:CASE {core_idea_id: $core_idea_id})
                SET ci.code = $code,
                    ci.title = $title,
                    ci.dimension_id = $dimension_id
                WITH ci
                MATCH (d:Dimension {dimension_id: $dimension_id})
                MERGE (d)-[:HAS_CORE_IDEA]->(ci)
            """, core_idea_id=core_idea_id,
                 code=code,
                 title=item.get('fullStatement', ''),
                 dimension_id=dimension_id)
            self.stats['core_ideas'] += 1

    def _create_crosscutting_concepts(self, session, ccc_items, dimension_id):
        """Create CrosscuttingConcept nodes."""
        ccc_num = 1
        for item in ccc_items:
            stmt = item.get('fullStatement', '').strip()
            if stmt and len(stmt) < 100:  # Filter to main concepts (short titles)
                concept_id = f"ngss-ccc-{ccc_num}"
                session.run("""
                    MERGE (c:CrosscuttingConcept:CASE {concept_id: $concept_id})
                    SET c.concept_name = $concept_name,
                        c.concept_number = $concept_number,
                        c.dimension_id = $dimension_id
                    WITH c
                    MATCH (d:Dimension {dimension_id: $dimension_id})
                    MERGE (d)-[:HAS_CONCEPT]->(c)
                """, concept_id=concept_id,
                     concept_name=stmt,
                     concept_number=ccc_num,
                     dimension_id=dimension_id)
                self.stats['crosscutting_concepts'] += 1
                ccc_num += 1

    def _map_to_grade_band(self, edu_levels, framework_prefix):
        """Map education levels to grade band ID."""
        if not edu_levels:
            return f"{framework_prefix}-k-2"  # Default

        level = edu_levels[0]
        if level in ['KG', '1', '2']:
            return f"{framework_prefix}-k-2"
        elif level in ['3', '4', '5']:
            return f"{framework_prefix}-3-5"
        elif level in ['6', '7', '8']:
            return f"{framework_prefix}-6-8"
        else:
            return f"{framework_prefix}-9-12"

    def import_common_core_math(self, package_data, source_def):
        """Import Common Core Math with Practice + Content structure."""
        parser = CommonCoreMathParser(package_data)

        with self.driver.session() as session:
            framework_id = source_def['framework_id']
            session.run("""
                MERGE (f:Framework:CASE {framework_id: $framework_id})
                SET f.title = $title,
                    f.jurisdiction_id = $jurisdiction_id,
                    f.model_type = 'practice_plus_content',
                    f.subject = $subject,
                    f.licence = $licence
            """, framework_id=framework_id,
                 title=source_def['title'],
                 jurisdiction_id=source_def['jurisdiction']['jurisdiction_id'],
                 subject=source_def['subject'],
                 licence=source_def['licence'])
            self.stats['frameworks'] += 1

            # Create Math Practices (SMPs)
            practices = parser.get_math_practices()
            for i, practice_item in enumerate(practices[:8], 1):  # 8 SMPs
                practice_id = f"ccss-smp-{i}"
                session.run("""
                    MERGE (mp:MathPractice:CASE {practice_id: $practice_id})
                    SET mp.practice_number = $practice_number,
                        mp.practice_name = $practice_name,
                        mp.description = $description,
                        mp.framework_id = $framework_id
                    WITH mp
                    MATCH (f:Framework {framework_id: $framework_id})
                    MERGE (f)-[:HAS_PRACTICE]->(mp)
                """, practice_id=practice_id,
                     practice_number=i,
                     practice_name=practice_item.get('fullStatement', ''),
                     description=practice_item.get('notes', ''),
                     framework_id=framework_id)
                self.stats['math_practices'] += 1

            print(f"  Created Common Core Math structure: {self.stats['math_practices']} practices")

    def import_package(self, package_data, source_def):
        """Route to appropriate parser based on framework."""
        framework_id = source_def['framework_id']

        if '_fetch_status' in package_data:
            print(f"  [SKIP] {framework_id} — fetch failed previously")
            return

        print(f"\n--- Importing: {source_def['title']} ---")

        if 'ngss' in framework_id.lower():
            self.import_ngss(package_data, source_def)
        elif 'ccss-math' in framework_id.lower():
            self.import_common_core_math(package_data, source_def)
        else:
            print(f"  [SKIP] {framework_id} — no parser implemented yet")

    def import_all(self, subject_filter=None):
        """Import all cached packages."""
        if not SOURCES_FILE.exists():
            raise FileNotFoundError(f"Sources not found: {SOURCES_FILE}")

        with open(SOURCES_FILE) as f:
            config = json.load(f)

        sources = config['sources']
        if subject_filter:
            sources = [s for s in sources if subject_filter.lower() in s.get('subject', '').lower()]

        for source_def in sources:
            framework_id = source_def['framework_id']
            cache_path = PACKAGES_DIR / f"{framework_id}.json"

            if not cache_path.exists():
                print(f"\n[SKIP] {framework_id} — not fetched yet")
                continue

            with open(cache_path) as f:
                package_data = json.load(f)

            self.import_package(package_data, source_def)

        return self.stats


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_import(args):
    """Import cached packages with proper structure."""
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    try:
        importer = CaseStandardsImporter(driver)
        stats = importer.import_all(subject_filter=args.subject)

        print("\n" + "=" * 60)
        print("CASE IMPORT COMPLETE (STRUCTURED)")
        print("=" * 60)
        for key, val in sorted(stats.items()):
            print(f"  {key:<30} {val:>6}")
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"\n[ERROR] Import failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        driver.close()


def main():
    parser = argparse.ArgumentParser(
        description="Import CASE standards with proper structure parsing (v3.5 restructured)"
    )
    parser.add_argument(
        "--import",
        dest="do_import",
        action="store_true",
        help="Import cached packages into Neo4j with intelligent parsing"
    )
    parser.add_argument(
        "--subject",
        help="Filter by subject (e.g., science, mathematics)"
    )
    args = parser.parse_args()

    if args.do_import:
        exit(cmd_import(args))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

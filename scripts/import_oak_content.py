#!/usr/bin/env python3
"""
Import Oak National Academy content into Neo4j
Graph Model v3.4 — :Content layer

Creates a linked content layer mapped onto the existing curriculum graph:

  OakUnit  -[:HAS_LESSON]->  OakLesson
  OakUnit  -[:COVERS]->      Domain         (curriculum alignment)
  OakLesson -[:TEACHES]->    Concept        (curriculum alignment)

Workflow
--------
1. Obtain an Oak API key from https://open-api.thenational.academy/
   Set it as an environment variable:  export OAK_API_KEY=<your-key>

2. Run the discovery step to build a catalogue of all Oak units/lessons:
   python3 scripts/import_oak_content.py --discover

   This writes:  data/extractions/oak/catalogue/oak_catalogue.json

3. Review and create mapping files per subject in:
   data/extractions/oak/mappings/

   See data/extractions/oak/README.md for the mapping file format.

4. Run the full import to create :Content nodes and cross-layer links:
   python3 scripts/import_oak_content.py --import

   Or import a single subject:
   python3 scripts/import_oak_content.py --import --subject mathematics

5. Run schema validation to check the Content layer:
   python3 scripts/validate_schema.py

Graph model v3.4 — Oak National Academy content layer.
"""

import os
import json
import time
import argparse
from pathlib import Path

import requests
from neo4j import GraphDatabase

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

NEO4J_URI = "neo4j://127.0.0.1:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password123"

OAK_API_BASE = "https://open-api.thenational.academy"
OAK_API_KEY = os.environ.get("OAK_API_KEY", "")

PROJECT_ROOT = Path(__file__).parent.parent
OAK_DIR = PROJECT_ROOT / "data" / "extractions" / "oak"
CATALOGUE_DIR = OAK_DIR / "catalogue"
MAPPINGS_DIR = OAK_DIR / "mappings"

# Oak uses short subject slugs; map these to our subject_name values
OAK_SUBJECT_TO_CURRICULUM = {
    "maths": "Mathematics",
    "english": "English",
    "science": "Science",
    "history": "History",
    "geography": "Geography",
    "art-and-design": "Art and Design",
    "computing": "Computing",
    "design-and-technology": "Design and Technology",
    "music": "Music",
    "physical-education": "Physical Education",
    "rshe-pshe": "PSHE and RSE",
    "religious-education": "Religious Education",
}

# Oak key stage slugs to our canonical labels
OAK_KEY_STAGE_MAP = {
    "ks1": "KS1",
    "ks2": "KS2",
    "ks3": "KS3",
    "ks4": "KS4",
}

# Polite rate limiting for the Oak API
REQUEST_DELAY_SECONDS = 0.5


# ---------------------------------------------------------------------------
# Oak API client
# ---------------------------------------------------------------------------

class OakAPIClient:
    def __init__(self, api_key: str):
        if not api_key:
            raise EnvironmentError(
                "OAK_API_KEY environment variable is not set.\n"
                "Request an API key at https://open-api.thenational.academy/ "
                "and run:  export OAK_API_KEY=<your-key>"
            )
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        })

    def _get(self, path: str, params: dict = None) -> dict:
        url = f"{OAK_API_BASE}{path}"
        time.sleep(REQUEST_DELAY_SECONDS)
        response = self.session.get(url, params=params or {})
        response.raise_for_status()
        return response.json()

    def get_subjects(self, key_stage: str = None) -> list:
        """Return list of subjects, optionally filtered by key stage slug."""
        path = f"/key-stages/{key_stage}/subjects" if key_stage else "/subjects"
        data = self._get(path)
        return data if isinstance(data, list) else data.get("subjects", [])

    def get_units(self, key_stage: str, subject: str) -> list:
        """Return all units for a given key stage and subject slug."""
        data = self._get(f"/key-stages/{key_stage}/subjects/{subject}/units")
        return data if isinstance(data, list) else data.get("units", [])

    def get_lessons(self, unit_slug: str) -> list:
        """Return all lessons within a unit."""
        data = self._get(f"/units/{unit_slug}/lessons")
        return data if isinstance(data, list) else data.get("lessons", [])

    def get_lesson_summary(self, lesson_slug: str) -> dict:
        """Return detailed summary for a single lesson (includes misconceptions)."""
        return self._get(f"/lessons/{lesson_slug}/summary")


# ---------------------------------------------------------------------------
# Discovery: build catalogue from Oak API
# ---------------------------------------------------------------------------

def discover_catalogue(client: OakAPIClient) -> dict:
    """
    Fetch the full Oak unit/lesson hierarchy and write to
    data/extractions/oak/catalogue/oak_catalogue.json.

    This is a read-only operation — nothing is written to Neo4j.
    """
    print("\n" + "=" * 60)
    print("DISCOVERING OAK NATIONAL ACADEMY CONTENT CATALOGUE")
    print("=" * 60)

    CATALOGUE_DIR.mkdir(parents=True, exist_ok=True)

    catalogue = {}
    key_stages = ["ks1", "ks2", "ks3"]

    for ks_slug in key_stages:
        ks_label = OAK_KEY_STAGE_MAP[ks_slug]
        print(f"\n  Key Stage: {ks_label}")

        try:
            subjects = client.get_subjects(ks_slug)
        except Exception as e:
            print(f"    ! Failed to fetch subjects for {ks_slug}: {e}")
            continue

        for subject_obj in subjects:
            subject_slug = subject_obj.get("slug") or subject_obj.get("subject_slug", "")
            subject_title = subject_obj.get("title") or subject_obj.get("subject", subject_slug)

            print(f"    Subject: {subject_slug}")

            try:
                units = client.get_units(ks_slug, subject_slug)
            except Exception as e:
                print(f"      ! Failed to fetch units: {e}")
                continue

            for unit_obj in units:
                unit_slug = unit_obj.get("slug") or unit_obj.get("unit_slug", "")
                if not unit_slug:
                    continue

                unit_record = {
                    "oak_unit_slug": unit_slug,
                    "oak_unit_title": unit_obj.get("title") or unit_obj.get("unit_title", ""),
                    "key_stage": ks_label,
                    "key_stage_slug": ks_slug,
                    "subject": subject_title,
                    "subject_slug": subject_slug,
                    "year_group": unit_obj.get("year_group") or unit_obj.get("year", ""),
                    "programme_slug": unit_obj.get("programme_slug") or unit_obj.get("unit_programme_slug", ""),
                    "lesson_count": unit_obj.get("lesson_count", 0),
                    "lessons": [],
                }

                try:
                    lessons = client.get_lessons(unit_slug)
                except Exception as e:
                    print(f"      ! Failed to fetch lessons for unit {unit_slug}: {e}")
                    lessons = []

                for lesson_obj in lessons:
                    lesson_slug = lesson_obj.get("slug") or lesson_obj.get("lesson_slug", "")
                    if not lesson_slug:
                        continue

                    lesson_record = {
                        "oak_lesson_slug": lesson_slug,
                        "oak_lesson_title": lesson_obj.get("title") or lesson_obj.get("lesson_title", ""),
                        "oak_unit_slug": unit_slug,
                        "key_stage": ks_label,
                        "subject": subject_title,
                        "year_group": unit_record["year_group"],
                        "has_video": lesson_obj.get("has_video", False),
                        "quiz_question_count": lesson_obj.get("quiz_question_count", 0),
                    }
                    unit_record["lessons"].append(lesson_record)

                catalogue[unit_slug] = unit_record
                print(f"      Unit: {unit_slug} ({len(unit_record['lessons'])} lessons)")

    # Write catalogue
    catalogue_path = CATALOGUE_DIR / "oak_catalogue.json"
    with open(catalogue_path, "w") as f:
        json.dump(
            {
                "metadata": {
                    "source": "Oak National Academy API",
                    "api_base": OAK_API_BASE,
                    "fetched_key_stages": key_stages,
                    "unit_count": len(catalogue),
                },
                "units": catalogue,
            },
            f,
            indent=2,
        )

    print(f"\n  Catalogue written: {catalogue_path}")
    print(f"  Total units: {len(catalogue)}")
    return catalogue


# ---------------------------------------------------------------------------
# Import: read mapping files + create Content nodes in Neo4j
# ---------------------------------------------------------------------------

class OakContentImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            "oak_units": 0,
            "oak_lessons": 0,
            "has_lesson": 0,
            "covers_domain": 0,
            "teaches_concept": 0,
        }

    def close(self):
        self.driver.close()

    def _create_oak_unit(self, session, unit: dict):
        """MERGE an OakUnit node and its lesson children."""
        query = """
        MERGE (u:OakUnit {oak_unit_slug: $oak_unit_slug})
        SET u:Content,
            u.oak_unit_title = $oak_unit_title,
            u.key_stage = $key_stage,
            u.subject = $subject,
            u.year_group = $year_group,
            u.programme_slug = $programme_slug,
            u.lesson_count = $lesson_count,
            u.source_url = $source_url,
            u.licence = 'OGL v3.0'
        RETURN u
        """
        result = session.run(
            query,
            oak_unit_slug=unit["oak_unit_slug"],
            oak_unit_title=unit["oak_unit_title"],
            key_stage=unit.get("key_stage", ""),
            subject=unit.get("subject", ""),
            year_group=unit.get("year_group", ""),
            programme_slug=unit.get("programme_slug", ""),
            lesson_count=unit.get("lesson_count", 0),
            source_url=f"https://www.thenational.academy/teachers/programmes/{unit.get('programme_slug', '')}/units/{unit['oak_unit_slug']}",
        )
        if result.single():
            self.stats["oak_units"] += 1

    def _create_oak_lesson(self, session, lesson: dict):
        """MERGE an OakLesson node and link it to its parent OakUnit."""
        query = """
        MERGE (l:OakLesson {oak_lesson_slug: $oak_lesson_slug})
        SET l:Content,
            l.oak_lesson_title = $oak_lesson_title,
            l.oak_unit_slug = $oak_unit_slug,
            l.key_stage = $key_stage,
            l.subject = $subject,
            l.year_group = $year_group,
            l.has_video = $has_video,
            l.quiz_question_count = $quiz_question_count,
            l.source_url = $source_url,
            l.licence = 'OGL v3.0'
        RETURN l
        """
        result = session.run(
            query,
            oak_lesson_slug=lesson["oak_lesson_slug"],
            oak_lesson_title=lesson["oak_lesson_title"],
            oak_unit_slug=lesson["oak_unit_slug"],
            key_stage=lesson.get("key_stage", ""),
            subject=lesson.get("subject", ""),
            year_group=lesson.get("year_group", ""),
            has_video=lesson.get("has_video", False),
            quiz_question_count=lesson.get("quiz_question_count", 0),
            source_url=f"https://www.thenational.academy/teachers/programmes/{lesson.get('programme_slug', '')}/units/{lesson['oak_unit_slug']}/lessons/{lesson['oak_lesson_slug']}",
        )
        if result.single():
            self.stats["oak_lessons"] += 1

        # Link OakUnit -> OakLesson
        session.run(
            """
            MATCH (u:OakUnit {oak_unit_slug: $unit_slug})
            MATCH (l:OakLesson {oak_lesson_slug: $lesson_slug})
            MERGE (u)-[:HAS_LESSON]->(l)
            """,
            unit_slug=lesson["oak_unit_slug"],
            lesson_slug=lesson["oak_lesson_slug"],
        )
        self.stats["has_lesson"] += 1

    def _create_covers_domain(self, session, oak_unit_slug: str, domain_id: str):
        """Create OakUnit -[:COVERS]-> Domain mapping."""
        result = session.run(
            """
            MATCH (u:OakUnit {oak_unit_slug: $unit_slug})
            MATCH (d:Domain {domain_id: $domain_id})
            MERGE (u)-[:COVERS]->(d)
            RETURN d
            """,
            unit_slug=oak_unit_slug,
            domain_id=domain_id,
        )
        if result.single():
            self.stats["covers_domain"] += 1
        else:
            print(f"    ! COVERS: Domain '{domain_id}' not found (unit: {oak_unit_slug})")

    def _create_teaches_concept(self, session, oak_lesson_slug: str, concept_id: str):
        """Create OakLesson -[:TEACHES]-> Concept mapping."""
        result = session.run(
            """
            MATCH (l:OakLesson {oak_lesson_slug: $lesson_slug})
            MATCH (c:Concept {concept_id: $concept_id})
            MERGE (l)-[:TEACHES]->(c)
            RETURN c
            """,
            lesson_slug=oak_lesson_slug,
            concept_id=concept_id,
        )
        if result.single():
            self.stats["teaches_concept"] += 1
        else:
            print(f"    ! TEACHES: Concept '{concept_id}' not found (lesson: {oak_lesson_slug})")

    def import_mapping_file(self, session, mapping: dict):
        """Import one mapping file (one subject/key-stage pair)."""
        subject = mapping.get("metadata", {}).get("subject", "?")
        key_stage = mapping.get("metadata", {}).get("key_stage", "?")
        print(f"\n  Importing Oak content: {subject} {key_stage}")

        for unit in mapping.get("units", []):
            self._create_oak_unit(session, unit)

            for lesson in unit.get("lessons", []):
                self._create_oak_lesson(session, lesson)

            for domain_id in unit.get("covers_domain_ids", []):
                self._create_covers_domain(session, unit["oak_unit_slug"], domain_id)

        for lesson_map in mapping.get("lesson_concept_mappings", []):
            for concept_id in lesson_map.get("teaches_concept_ids", []):
                self._create_teaches_concept(
                    session,
                    lesson_map["oak_lesson_slug"],
                    concept_id,
                )

        print(f"    + {len(mapping.get('units', []))} units imported")

    def import_all(self, subject_filter: str = None):
        print("\n" + "=" * 60)
        print("IMPORTING OAK NATIONAL ACADEMY CONTENT")
        print("=" * 60)

        if not MAPPINGS_DIR.exists():
            print(f"! Mappings directory not found: {MAPPINGS_DIR}")
            print("  Run --discover first, then create mapping files.")
            return

        mapping_files = sorted(MAPPINGS_DIR.glob("*.json"))
        if not mapping_files:
            print(f"! No mapping files found in {MAPPINGS_DIR}")
            print("  See data/extractions/oak/README.md for the mapping file format.")
            return

        with self.driver.session() as session:
            for mapping_file in mapping_files:
                if subject_filter and subject_filter not in mapping_file.name:
                    continue
                try:
                    with open(mapping_file) as f:
                        mapping = json.load(f)
                    self.import_mapping_file(session, mapping)
                except Exception as e:
                    print(f"  ! Error importing {mapping_file.name}: {e}")
                    import traceback
                    traceback.print_exc()

        print("\n" + "=" * 60)
        print("OAK IMPORT SUMMARY")
        print("=" * 60)
        for key, value in self.stats.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        print("=" * 60)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Import Oak National Academy content into the curriculum graph"
    )
    parser.add_argument(
        "--discover",
        action="store_true",
        help="Fetch Oak catalogue from API and write to data/extractions/oak/catalogue/",
    )
    parser.add_argument(
        "--import",
        dest="do_import",
        action="store_true",
        help="Import mapping files into Neo4j",
    )
    parser.add_argument(
        "--subject",
        default=None,
        help="Filter import to a single subject (matches against mapping filename)",
    )
    args = parser.parse_args()

    if not args.discover and not args.do_import:
        parser.print_help()
        return

    print("UK Curriculum Knowledge Graph — Oak National Academy Importer")

    if args.discover:
        try:
            client = OakAPIClient(OAK_API_KEY)
        except EnvironmentError as e:
            print(f"\n{e}")
            return
        discover_catalogue(client)

    if args.do_import:
        importer = OakContentImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
        try:
            importer.import_all(subject_filter=args.subject)
        except Exception as e:
            print(f"\nImport failed: {e}")
            import traceback
            traceback.print_exc()
        finally:
            importer.close()

    print("\nDone!")


if __name__ == "__main__":
    main()

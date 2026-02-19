#!/usr/bin/env python3
"""
Import CASE (IMS Global Competencies and Academic Standards Exchange) standards
into Neo4j as a :CASE namespace layer.

Graph Model v3.5 — CASE Standards layer

Creates a browseable, comparable layer of international and US state academic standards:

  Jurisdiction  -[:PUBLISHES]->     CFDocument
  CFDocument    -[:CONTAINS_ITEM]-> CFItem
  CFItem        -[:CHILD_OF]->      CFItem      (hierarchy from isChildOf associations)
  CFItem        -[:PRECEDES]->      CFItem      (learning progression from precedes)
  CFItem        -[:ALIGNS_TO]->     Concept     (cross-layer: CASE ↔ UK curriculum)
  CFItem        -[:ALIGNS_TO]->     Objective   (cross-layer: CASE ↔ UK curriculum)

Workflow
--------
1. Fetch CASE packages from the IMS CASE Network (no auth required):
   python3 scripts/import_case_standards.py --fetch

   Downloads CFPackage JSON for each source defined in:
     data/extractions/case/case_sources.json
   Caches packages to:
     data/extractions/case/packages/{framework_id}.json

2. Review fetched packages and populate cf_item_ids in mapping files:
     data/extractions/case/mappings/

3. Import all frameworks into Neo4j:
   python3 scripts/import_case_standards.py --import

   Or filter by subject:
   python3 scripts/import_case_standards.py --import --subject science

4. Run schema validation:
   python3 scripts/validate_schema.py

Graph model v3.5 — CASE Standards layer.
"""

import json
import time
import argparse
from pathlib import Path
from collections import deque

import requests
from neo4j import GraphDatabase

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

NEO4J_URI = "neo4j://127.0.0.1:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password123"

PROJECT_ROOT = Path(__file__).parent.parent
CASE_DIR = PROJECT_ROOT / "data" / "extractions" / "case"
PACKAGES_DIR = CASE_DIR / "packages"
MAPPINGS_DIR = CASE_DIR / "mappings"
SOURCES_FILE = CASE_DIR / "case_sources.json"

# Polite rate limiting for CASE Network API
REQUEST_DELAY_SECONDS = 1.0

# Maximum items to process in a single Cypher batch
BATCH_SIZE = 200


# ---------------------------------------------------------------------------
# CASE API client
# ---------------------------------------------------------------------------

class CaseFetcher:
    """Fetches CASE packages from a CASE-compliant endpoint."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "uk-curriculum-as-graph/3.5 (research; github.com/curriculum-graph)",
        })

    def list_documents(self) -> list:
        """GET /CFDocuments — list all available CFDocuments."""
        url = f"{self.base_url}/CFDocuments"
        print(f"  Listing documents: {url}")
        resp = self.session.get(url, timeout=30)
        resp.raise_for_status()
        time.sleep(REQUEST_DELAY_SECONDS)
        data = resp.json()
        # CASE v1p0 wraps in CFDocuments key
        return data.get("CFDocuments", data if isinstance(data, list) else [])

    def fetch_package(self, pkg_id: str) -> dict:
        """GET /CFPackages/{id} — fetch full package including all items and associations."""
        url = f"{self.base_url}/CFPackages/{pkg_id}"
        print(f"  Fetching package: {url}")
        resp = self.session.get(url, timeout=120)
        resp.raise_for_status()
        time.sleep(REQUEST_DELAY_SECONDS)
        return resp.json()

    def find_package_id(self, search_title: str) -> str | None:
        """Search the CFDocuments list for a document matching search_title."""
        documents = self.list_documents()
        search_lower = search_title.lower()
        for doc in documents:
            title = doc.get("title", "")
            if search_lower in title.lower():
                return doc.get("identifier") or doc.get("id")
        return None

    def fetch_and_cache(self, source_def: dict) -> Path:
        """
        Download a CASE package and write it to the packages directory.
        Returns the path to the cached file.
        """
        framework_id = source_def["framework_id"]
        cache_path = PACKAGES_DIR / f"{framework_id}.json"

        if cache_path.exists():
            print(f"  [cache hit] {cache_path.name} — skipping download")
            return cache_path

        # Use framework-specific base URL if provided (e.g. Texas TEA)
        base_url = source_def.get("case_base_url", self.base_url)
        fetcher = CaseFetcher(base_url) if base_url != self.base_url else self

        search_title = source_def.get("search_title", source_def["title"])
        print(f"  Searching for: '{search_title}'")
        pkg_id = fetcher.find_package_id(search_title)

        if not pkg_id:
            print(f"  [WARNING] Could not find package for '{search_title}' at {base_url}")
            # Write an empty stub so we can track the failure
            stub = {
                "_fetch_status": "not_found",
                "_framework_id": framework_id,
                "_search_title": search_title,
                "_base_url": base_url,
            }
            cache_path.write_text(json.dumps(stub, indent=2))
            return cache_path

        print(f"  Found package id: {pkg_id}")
        package = fetcher.fetch_package(pkg_id)
        cache_path.write_text(json.dumps(package, indent=2))
        print(f"  Cached to: {cache_path}")
        return cache_path


# ---------------------------------------------------------------------------
# Neo4j importer
# ---------------------------------------------------------------------------

class CaseStandardsImporter:
    """Imports CASE packages into Neo4j."""

    def __init__(self, driver):
        self.driver = driver
        self.stats = {
            "jurisdictions": 0,
            "cf_documents": 0,
            "cf_items": 0,
            "child_of": 0,
            "precedes": 0,
            "aligns_to": 0,
        }

    def create_jurisdiction(self, session, jur_def: dict):
        """MERGE a Jurisdiction node from a jurisdiction definition dict."""
        session.run("""
            MERGE (j:CASE:Jurisdiction {jurisdiction_id: $jurisdiction_id})
            SET j.name               = $name,
                j.jurisdiction_type  = $jurisdiction_type,
                j.country            = $country,
                j.ngss_adopted       = $ngss_adopted,
                j.notes              = $notes
        """, **{k: jur_def.get(k) for k in (
            "jurisdiction_id", "name", "jurisdiction_type",
            "country", "ngss_adopted", "notes",
        )})
        self.stats["jurisdictions"] += 1

    def create_cf_document(self, session, cf_doc: dict, jur_id: str, source_def: dict):
        """MERGE a CFDocument node and link it to its Jurisdiction."""
        doc_id = cf_doc.get("identifier") or cf_doc.get("id", "")
        if not doc_id:
            print("    [WARNING] CFDocument has no identifier — skipping")
            return

        session.run("""
            MERGE (d:CASE:CFDocument {cf_doc_id: $cf_doc_id})
            SET d.title           = $title,
                d.creator         = $creator,
                d.subject         = $subject,
                d.adoption_status = $adoption_status,
                d.version         = $version,
                d.language        = $language,
                d.case_uri        = $case_uri,
                d.source_url      = $source_url,
                d.licence         = $licence
        """,
            cf_doc_id=doc_id,
            title=cf_doc.get("title", ""),
            creator=cf_doc.get("creator", ""),
            subject=source_def.get("subject", cf_doc.get("subject", "")),
            adoption_status=cf_doc.get("adoptionStatus", "unknown"),
            version=cf_doc.get("version", ""),
            language=cf_doc.get("language", "en"),
            case_uri=cf_doc.get("uri", ""),
            source_url=source_def.get("case_base_url", ""),
            licence=source_def.get("licence", ""),
        )

        # Link Jurisdiction -[:PUBLISHES]-> CFDocument
        session.run("""
            MATCH (j:Jurisdiction {jurisdiction_id: $jur_id})
            MATCH (d:CFDocument {cf_doc_id: $doc_id})
            MERGE (j)-[:PUBLISHES]->(d)
        """, jur_id=jur_id, doc_id=doc_id)

        self.stats["cf_documents"] += 1
        return doc_id

    def create_cf_items(self, session, cf_items: list, doc_id: str):
        """
        Bulk-MERGE all CFItem nodes and create CONTAINS_ITEM links from CFDocument.
        CFItems are stored flat; hierarchy is built separately from associations.
        """
        if not cf_items:
            return

        # Process in batches for performance
        for i in range(0, len(cf_items), BATCH_SIZE):
            batch = cf_items[i:i + BATCH_SIZE]
            rows = []
            for item in batch:
                item_id = item.get("identifier") or item.get("id", "")
                if not item_id:
                    continue
                rows.append({
                    "cf_item_id": item_id,
                    "full_statement": item.get("fullStatement", ""),
                    "abbreviated_statement": item.get("abbreviatedStatement", ""),
                    "human_coding_scheme": item.get("humanCodingScheme", ""),
                    "education_level": item.get("educationLevel", []),
                    "concept_keywords": item.get("conceptKeywords", [])
                        if isinstance(item.get("conceptKeywords"), list)
                        else (item.get("conceptKeywords", "").split(",")
                              if item.get("conceptKeywords") else []),
                    "item_type": item.get("CFItemType", item.get("type", "Standard")),
                    "cf_doc_id": doc_id,
                    "depth": 0,  # computed later by build_hierarchy
                    "case_uri": item.get("uri", ""),
                })

            session.run("""
                UNWIND $rows AS row
                MERGE (i:CASE:CFItem {cf_item_id: row.cf_item_id})
                SET i.full_statement       = row.full_statement,
                    i.abbreviated_statement = row.abbreviated_statement,
                    i.human_coding_scheme  = row.human_coding_scheme,
                    i.education_level      = row.education_level,
                    i.concept_keywords     = row.concept_keywords,
                    i.item_type            = row.item_type,
                    i.cf_doc_id            = row.cf_doc_id,
                    i.depth                = row.depth,
                    i.case_uri             = row.case_uri
                WITH i, row
                MATCH (d:CFDocument {cf_doc_id: row.cf_doc_id})
                MERGE (d)-[:CONTAINS_ITEM]->(i)
            """, rows=rows)

            self.stats["cf_items"] += len(rows)

    def build_hierarchy(self, session, associations: list, doc_id: str):
        """
        Create CHILD_OF relationships from isChildOf associations,
        then compute depth via BFS from root items.
        """
        child_of_rows = []
        for assoc in associations:
            assoc_type = assoc.get("associationType", "")
            if assoc_type != "isChildOf":
                continue
            origin_id = (assoc.get("originNodeURI") or {}).get("identifier", "")
            dest_id = (assoc.get("destinationNodeURI") or {}).get("identifier", "")
            if origin_id and dest_id:
                child_of_rows.append({"child_id": origin_id, "parent_id": dest_id})

        if child_of_rows:
            for i in range(0, len(child_of_rows), BATCH_SIZE):
                batch = child_of_rows[i:i + BATCH_SIZE]
                session.run("""
                    UNWIND $rows AS row
                    MATCH (child:CFItem {cf_item_id: row.child_id})
                    MATCH (parent:CFItem {cf_item_id: row.parent_id})
                    MERGE (child)-[:CHILD_OF]->(parent)
                """, rows=batch)
            self.stats["child_of"] += len(child_of_rows)

        # Compute depth via BFS: root items are those with no CHILD_OF outgoing edge
        # within this document, depth=1; each subsequent level increments.
        print(f"    Computing item depths for document {doc_id}...")
        session.run("""
            MATCH (d:CFDocument {cf_doc_id: $doc_id})-[:CONTAINS_ITEM]->(root:CFItem)
            WHERE NOT (root)-[:CHILD_OF]->(:CFItem)
            SET root.depth = 1
        """, doc_id=doc_id)

        # BFS via repeated Cypher passes (simpler than client-side BFS for graph data)
        max_depth = 10
        for depth in range(1, max_depth):
            result = session.run("""
                MATCH (parent:CFItem)<-[:CHILD_OF]-(child:CFItem)
                WHERE parent.depth = $depth AND child.depth = 0
                SET child.depth = $next_depth
                RETURN count(child) AS updated
            """, depth=depth, next_depth=depth + 1)
            updated = result.single()["updated"]
            if updated == 0:
                break

    def build_precedes(self, session, associations: list, doc_id: str):
        """Create PRECEDES relationships from precedes associations."""
        precedes_rows = []
        for assoc in associations:
            assoc_type = assoc.get("associationType", "")
            if assoc_type != "precedes":
                continue
            origin_id = (assoc.get("originNodeURI") or {}).get("identifier", "")
            dest_id = (assoc.get("destinationNodeURI") or {}).get("identifier", "")
            if origin_id and dest_id:
                precedes_rows.append({"from_id": origin_id, "to_id": dest_id})

        if not precedes_rows:
            return

        for i in range(0, len(precedes_rows), BATCH_SIZE):
            batch = precedes_rows[i:i + BATCH_SIZE]
            session.run("""
                UNWIND $rows AS row
                MATCH (a:CFItem {cf_item_id: row.from_id})
                MATCH (b:CFItem {cf_item_id: row.to_id})
                MERGE (a)-[:PRECEDES]->(b)
            """, rows=batch)
        self.stats["precedes"] += len(precedes_rows)

    def load_alignments(self, session, mapping_file: Path):
        """
        Load cross-layer ALIGNS_TO relationships from a mapping JSON file.
        CFItem -[:ALIGNS_TO]-> Concept or Objective.
        """
        if not mapping_file.exists():
            return

        with open(mapping_file) as f:
            mapping = json.load(f)

        alignments = mapping.get("alignments", [])
        for align in alignments:
            cf_item_id = align.get("cf_item_id", "")
            if not cf_item_id or "PLACEHOLDER" in cf_item_id:
                continue  # skip stubs

            confidence = align.get("confidence", "inferred")
            notes = align.get("notes", "")

            for concept_id in align.get("aligns_to_concept_ids", []):
                session.run("""
                    MATCH (i:CFItem {cf_item_id: $cf_item_id})
                    MATCH (c:Concept {concept_id: $concept_id})
                    MERGE (i)-[r:ALIGNS_TO]->(c)
                    SET r.confidence = $confidence, r.notes = $notes
                """, cf_item_id=cf_item_id, concept_id=concept_id,
                     confidence=confidence, notes=notes)
                self.stats["aligns_to"] += 1

            for obj_id in align.get("aligns_to_objective_ids", []):
                session.run("""
                    MATCH (i:CFItem {cf_item_id: $cf_item_id})
                    MATCH (o:Objective {objective_id: $obj_id})
                    MERGE (i)-[r:ALIGNS_TO]->(o)
                    SET r.confidence = $confidence, r.notes = $notes
                """, cf_item_id=cf_item_id, obj_id=obj_id,
                     confidence=confidence, notes=notes)
                self.stats["aligns_to"] += 1

    def import_package(self, session, package_data: dict, source_def: dict):
        """Import a single CASE package: document, items, hierarchy, progressions."""
        # Check for fetch stubs (failed downloads)
        if "_fetch_status" in package_data:
            status = package_data["_fetch_status"]
            print(f"  [SKIP] Package stub with status '{status}' — was not fetched")
            return

        jur_def = source_def["jurisdiction"]
        jur_id = jur_def["jurisdiction_id"]

        print(f"  Creating Jurisdiction: {jur_def['name']} ({jur_id})")
        self.create_jurisdiction(session, jur_def)

        # CFDocument is at the top level
        cf_doc = package_data.get("CFDocument", {})
        print(f"  Creating CFDocument: {cf_doc.get('title', '(untitled)')}")
        doc_id = self.create_cf_document(session, cf_doc, jur_id, source_def)
        if not doc_id:
            return

        # CFItems are in CFItems array (flat)
        cf_items = package_data.get("CFItems", [])
        print(f"  Creating {len(cf_items)} CFItems...")
        self.create_cf_items(session, cf_items, doc_id)

        # Associations define hierarchy and progressions
        associations = package_data.get("CFAssociations", [])
        print(f"  Processing {len(associations)} associations...")
        self.build_hierarchy(session, associations, doc_id)
        self.build_precedes(session, associations, doc_id)

    def import_all(self, subject_filter: str = None):
        """Import all cached CASE packages, optionally filtered by subject."""
        if not SOURCES_FILE.exists():
            raise FileNotFoundError(f"Sources config not found: {SOURCES_FILE}")

        with open(SOURCES_FILE) as f:
            config = json.load(f)

        sources = config["sources"]
        if subject_filter:
            filter_lower = subject_filter.lower()
            sources = [s for s in sources
                       if filter_lower in s.get("subject", "").lower()]
            print(f"Subject filter '{subject_filter}' matched {len(sources)} source(s)")

        with self.driver.session() as session:
            for source_def in sources:
                framework_id = source_def["framework_id"]
                cache_path = PACKAGES_DIR / f"{framework_id}.json"

                if not cache_path.exists():
                    print(f"\n[SKIP] {framework_id} — not yet fetched (run --fetch first)")
                    continue

                print(f"\n--- Importing: {source_def['title']} ---")
                with open(cache_path) as f:
                    package_data = json.load(f)

                self.import_package(session, package_data, source_def)

                # Load alignment mappings if available
                mapping_file = MAPPINGS_DIR / f"{framework_id}_to_uk_science.json"
                if mapping_file.exists():
                    print(f"  Loading alignments from {mapping_file.name}...")
                    self.load_alignments(session, mapping_file)

        return self.stats


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_fetch(args):
    """Fetch CASE packages from the IMS CASE Network."""
    if not SOURCES_FILE.exists():
        print(f"ERROR: Sources file not found: {SOURCES_FILE}")
        return 1

    with open(SOURCES_FILE) as f:
        config = json.load(f)

    base_url = config["case_network_base"]
    sources = config["sources"]

    if args.subject:
        filter_lower = args.subject.lower()
        sources = [s for s in sources
                   if filter_lower in s.get("subject", "").lower()]
        print(f"Subject filter '{args.subject}' matched {len(sources)} source(s)")

    fetcher = CaseFetcher(base_url)
    PACKAGES_DIR.mkdir(parents=True, exist_ok=True)

    success = 0
    failed = 0
    for source_def in sources:
        print(f"\n--- Fetching: {source_def['title']} ---")
        try:
            cache_path = fetcher.fetch_and_cache(source_def)
            # Quick peek at what we got
            with open(cache_path) as f:
                data = json.load(f)
            if "_fetch_status" in data:
                print(f"  [WARN] Fetch failed: {data['_fetch_status']}")
                failed += 1
            else:
                n_items = len(data.get("CFItems", []))
                n_assoc = len(data.get("CFAssociations", []))
                print(f"  OK — {n_items} items, {n_assoc} associations")
                success += 1
        except Exception as e:
            print(f"  [ERROR] {e}")
            failed += 1

    print(f"\nFetch complete: {success} succeeded, {failed} failed")
    return 0 if failed == 0 else 1


def cmd_import(args):
    """Import cached CASE packages into Neo4j."""
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    try:
        importer = CaseStandardsImporter(driver)
        stats = importer.import_all(subject_filter=args.subject)

        print("\n" + "=" * 60)
        print("CASE IMPORT COMPLETE")
        print("=" * 60)
        for key, val in stats.items():
            print(f"  {key:<20} {val:>6}")
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"\n[ERROR] Import failed: {e}")
        raise
    finally:
        driver.close()


def main():
    parser = argparse.ArgumentParser(
        description="Import CASE standards into Neo4j (graph model v3.5)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--fetch",
        action="store_true",
        help="Fetch CASE packages from the IMS CASE Network and cache locally",
    )
    mode.add_argument(
        "--import",
        dest="do_import",
        action="store_true",
        help="Import cached packages into Neo4j",
    )
    parser.add_argument(
        "--subject",
        metavar="SUBJECT",
        help="Filter by subject (e.g. science, mathematics)",
    )
    args = parser.parse_args()

    if args.fetch:
        exit(cmd_fetch(args))
    elif args.do_import:
        exit(cmd_import(args))


if __name__ == "__main__":
    main()

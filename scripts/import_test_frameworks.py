#!/usr/bin/env python3
"""
Import KS2 Test Framework data into Neo4j

Adds a TestFramework layer to the curriculum graph:
  TestFramework -[HAS_PAPER]-> TestPaper
  TestPaper -[INCLUDES_CONTENT]-> ContentDomainCode
  ContentDomainCode -[ASSESSES]-> Programme
  TestFramework -[SOURCED_FROM]-> SourceDocument

Graph model v3.1 — test framework extension.
"""

from neo4j import GraphDatabase
import json
import os
from pathlib import Path

NEO4J_URI = "neo4j://127.0.0.1:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password123"

PROJECT_ROOT = Path(__file__).parent.parent
TEST_FRAMEWORK_DIR = PROJECT_ROOT / "data" / "extractions" / "test-frameworks"


class TestFrameworkImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            "frameworks": 0,
            "papers": 0,
            "content_domain_codes": 0,
            "source_documents": 0,
            "assesses_programme": 0,
            "assesses_domain": 0,
        }

    def close(self):
        self.driver.close()

    # -------------------------------------------------------------------------
    # Constraints and indexes
    # -------------------------------------------------------------------------

    def create_constraints(self, session):
        constraints = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (tf:TestFramework) REQUIRE tf.framework_id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (tp:TestPaper) REQUIRE tp.paper_id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (cdc:ContentDomainCode) REQUIRE cdc.code_id IS UNIQUE",
        ]
        for c in constraints:
            try:
                session.run(c)
            except Exception as e:
                print(f"  ! Constraint warning: {e}")

    # -------------------------------------------------------------------------
    # TestFramework node
    # -------------------------------------------------------------------------

    def create_framework(self, session, meta):
        query = """
        MERGE (tf:TestFramework {framework_id: $framework_id})
        SET tf:Assessment,
            tf.name = $name,
            tf.subject = $subject,
            tf.key_stage = $key_stage,
            tf.year_published = $year_published,
            tf.sta_reference = $sta_reference,
            tf.isbn = $isbn,
            tf.total_marks = $total_marks,
            tf.total_time_minutes = $total_time_minutes,
            tf.source_url = $source_url,
            tf.publication_page = $publication_page,
            tf.local_file = $local_file
        RETURN tf
        """
        result = session.run(query, **{k: meta.get(k, "") for k in [
            "framework_id", "name", "subject", "key_stage",
            "year_published", "sta_reference", "isbn",
            "total_marks", "total_time_minutes",
            "source_url", "publication_page", "local_file",
        ]})
        if result.single():
            self.stats["frameworks"] += 1

        # Link to Curriculum
        session.run("""
            MATCH (c:Curriculum {curriculum_id: 'uk-national-curriculum'})
            MATCH (tf:TestFramework {framework_id: $framework_id})
            MERGE (c)-[:HAS_TEST_FRAMEWORK]->(tf)
        """, framework_id=meta["framework_id"])

        # Create and link SourceDocument
        self._create_source_doc(session, meta)

    def _create_source_doc(self, session, meta):
        doc_id = f"DOC-TF-{meta['framework_id']}"
        session.run("""
            MATCH (c:Curriculum {curriculum_id: 'uk-national-curriculum'})
            MERGE (sd:SourceDocument {document_id: $document_id})
            SET sd:Assessment,
                sd.title = $title,
                sd.subject = $subject,
                sd.key_stages = $key_stages,
                sd.url = $url,
                sd.publication_page = $publication_page,
                sd.dfe_reference = $dfe_reference,
                sd.document_type = 'test_framework',
                sd.local_file = $local_file
            MERGE (c)-[:HAS_DOCUMENT]->(sd)
        """,
            document_id=doc_id,
            title=meta["name"],
            subject=meta["subject"],
            key_stages=[meta["key_stage"]],
            url=meta.get("source_url", ""),
            publication_page=meta.get("publication_page", ""),
            dfe_reference=meta.get("sta_reference", ""),
            local_file=meta.get("local_file", ""),
        )
        # Link framework -> source doc
        session.run("""
            MATCH (tf:TestFramework {framework_id: $framework_id})
            MATCH (sd:SourceDocument {document_id: $doc_id})
            MERGE (tf)-[:SOURCED_FROM]->(sd)
        """, framework_id=meta["framework_id"], doc_id=doc_id)
        self.stats["source_documents"] += 1

    # -------------------------------------------------------------------------
    # TestPaper nodes
    # -------------------------------------------------------------------------

    def create_papers(self, session, framework_id, papers):
        query = """
        MATCH (tf:TestFramework {framework_id: $framework_id})
        MERGE (tp:TestPaper {paper_id: $paper_id})
        SET tp:Assessment,
            tp.name = $name,
            tp.paper_number = $paper_number,
            tp.component_type = $component_type,
            tp.marks = $marks,
            tp.time_minutes = $time_minutes,
            tp.description = $description,
            tp.framework_id = $framework_id
        MERGE (tf)-[:HAS_PAPER]->(tp)
        RETURN tp
        """
        for paper in papers:
            result = session.run(
                query,
                framework_id=framework_id,
                paper_id=paper["paper_id"],
                name=paper["name"],
                paper_number=paper.get("paper_number", 1),
                component_type=paper.get("component_type", ""),
                marks=paper.get("marks", 0),
                time_minutes=paper.get("time_minutes", 0),
                description=paper.get("description", ""),
            )
            if result.single():
                self.stats["papers"] += 1

    # -------------------------------------------------------------------------
    # ContentDomainCode nodes
    # -------------------------------------------------------------------------

    def create_content_domain_codes(self, session, framework_id, codes):
        for code_data in codes:
            code_id = code_data["code_id"]
            code = code_data["code"]

            # Create/merge the ContentDomainCode node
            session.run("""
                MERGE (cdc:ContentDomainCode {code_id: $code_id})
                SET cdc:Assessment,
                    cdc.code = $code,
                    cdc.framework_id = $framework_id,
                    cdc.year = $year,
                    cdc.strand_code = $strand_code,
                    cdc.strand_name = $strand_name,
                    cdc.substrand = $substrand,
                    cdc.substrand_name = $substrand_name,
                    cdc.description = $description
                RETURN cdc
            """,
                code_id=code_id,
                code=code,
                framework_id=framework_id,
                year=code_data.get("year"),
                strand_code=code_data.get("strand_code", ""),
                strand_name=code_data.get("strand_name", ""),
                substrand=code_data.get("substrand", ""),
                substrand_name=code_data.get("substrand_name", ""),
                description=code_data.get("description", ""),
            )
            self.stats["content_domain_codes"] += 1

            # Link code -> TestPaper(s)
            for paper_id in code_data.get("papers", []):
                session.run("""
                    MATCH (tp:TestPaper {paper_id: $paper_id})
                    MATCH (cdc:ContentDomainCode {code_id: $code_id})
                    MERGE (tp)-[:INCLUDES_CONTENT]->(cdc)
                """, paper_id=paper_id, code_id=code_id)

            # Link code -> Programme (ASSESSES)
            programme_id = code_data.get("programme_id")
            if programme_id:
                result = session.run("""
                    MATCH (p:Programme {programme_id: $programme_id})
                    MATCH (cdc:ContentDomainCode {code_id: $code_id})
                    MERGE (cdc)-[:ASSESSES]->(p)
                    RETURN p
                """, programme_id=programme_id, code_id=code_id)
                if result.single():
                    self.stats["assesses_programme"] += 1
                else:
                    print(f"    ! Programme not found: {programme_id} (for code {code})")

            # Link code -> Concept (ASSESSES_CONCEPT) via matched concept_ids
            for concept_id in code_data.get("concept_ids", []):
                result = session.run("""
                    MATCH (c:Concept {concept_id: $concept_id})
                    MATCH (cdc:ContentDomainCode {code_id: $code_id})
                    MERGE (cdc)-[:ASSESSES_CONCEPT]->(c)
                    RETURN c
                """, concept_id=concept_id, code_id=code_id)
                if result.single():
                    self.stats.setdefault("assesses_concept", 0)
                    self.stats["assesses_concept"] += 1

            # Link code -> Domain (ASSESSES_DOMAIN) by strand_name matching
            strand_name = code_data.get("strand_name", "")
            if strand_name and programme_id:
                result = session.run("""
                    MATCH (p:Programme {programme_id: $programme_id})-[:HAS_DOMAIN]->(d:Domain)
                    WHERE toLower(d.domain_name) CONTAINS toLower($strand_name)
                       OR toLower($strand_name) CONTAINS toLower(d.domain_name)
                    MATCH (cdc:ContentDomainCode {code_id: $code_id})
                    MERGE (cdc)-[:ASSESSES_DOMAIN]->(d)
                    RETURN d
                """, programme_id=programme_id, strand_name=strand_name, code_id=code_id)
                records = list(result)
                self.stats["assesses_domain"] += len(records)

    # -------------------------------------------------------------------------
    # Import a single framework file
    # -------------------------------------------------------------------------

    def import_framework(self, session, data):
        meta = data["framework_metadata"]
        framework_id = meta["framework_id"]

        print(f"\n  Importing: {meta['name']}")
        self.create_framework(session, meta)
        print(f"    + Framework node: {framework_id}")

        papers = data.get("test_papers", [])
        self.create_papers(session, framework_id, papers)
        print(f"    + {len(papers)} test papers")

        codes = data.get("content_domain_codes", [])
        self.create_content_domain_codes(session, framework_id, codes)
        print(f"    + {len(codes)} content domain codes")

    # -------------------------------------------------------------------------
    # Main entry
    # -------------------------------------------------------------------------

    def import_all(self):
        print("\n" + "=" * 60)
        print("IMPORTING KS2 TEST FRAMEWORK DATA")
        print("=" * 60)

        if not TEST_FRAMEWORK_DIR.exists():
            print(f"! Test framework extractions directory not found: {TEST_FRAMEWORK_DIR}")
            return

        with self.driver.session() as session:
            self.create_constraints(session)

            for json_file in sorted(TEST_FRAMEWORK_DIR.glob("*.json")):
                try:
                    with open(json_file) as f:
                        data = json.load(f)
                    self.import_framework(session, data)
                except Exception as e:
                    print(f"  ! Error importing {json_file.name}: {e}")
                    import traceback
                    traceback.print_exc()

        print("\n" + "=" * 60)
        print("IMPORT SUMMARY")
        print("=" * 60)
        for key, value in self.stats.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        print("=" * 60)


def main():
    print("UK Curriculum Knowledge Graph — Test Framework Importer")
    importer = TestFrameworkImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    try:
        importer.import_all()
    except Exception as e:
        print(f"\nImport failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        importer.close()
    print("\nImport complete!")


if __name__ == "__main__":
    main()

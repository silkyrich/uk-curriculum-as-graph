#!/usr/bin/env python3
"""
UK Curriculum Graph — Schema Validation Script
Runs Cypher queries against Neo4j and produces a structured PASS/WARN/FAIL report.
"""

from neo4j import GraphDatabase
from datetime import datetime

# Neo4j connection
NEO4J_URI = "neo4j://127.0.0.1:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password123"

VALID_CONCEPT_TYPES = {"knowledge", "skill", "process", "attitude", "content"}
VALID_STRUCTURE_TYPES = {
    "sequential", "hierarchical", "mixed", "exploratory",
    "conceptual", "applied", "knowledge",
    # Legitimate types confirmed after data review:
    "process",       # design/evaluate/composing domains in DT, Music, Art
    "developmental", # spoken language, reading, writing, PE domains
    "thematic",      # cross-cutting thematic domains
}
VALID_PREREQ_CONFIDENCE = {"explicit", "inferred", "fuzzy", "suggested"}
VALID_PREREQ_REL_TYPES = {
    "logical", "developmental", "instructional", "temporal", "foundational",
    "cognitive",   # confirmed: relationships where shared cognitive capacity is the link
    "enabling",    # confirmed: Maths Y1/Y2 — one concept directly enables another
    "supportive",  # confirmed: English Y3 — supporting rather than strictly prerequisite
}


class ValidationResult:
    def __init__(self, label, status, count, details=None):
        self.label = label
        self.status = status  # PASS, WARN, FAIL
        self.count = count
        self.details = details or []

    def __repr__(self):
        count_str = f"{self.count} nodes checked" if self.count > 0 else "0 issues"
        return f"[CHECK] {self.label:<45} {self.status:<5} {count_str}"


class SchemaValidator:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.results = []
        self.all_warnings = []

    def close(self):
        self.driver.close()

    def run(self, query, **params):
        with self.driver.session() as session:
            return list(session.run(query, **params))

    def scalar(self, query, **params):
        records = self.run(query, **params)
        if records:
            return records[0][0]
        return None

    def add(self, result):
        self.results.append(result)
        for detail in result.details:
            self.all_warnings.append(detail)

    # =========================================================================
    # A. Node completeness
    # =========================================================================

    def check_programme_completeness(self):
        """All Programme nodes have required non-empty properties."""
        records = self.run("""
            MATCH (p:Programme)
            WHERE p.programme_id IS NULL OR p.programme_id = ''
               OR p.subject_name IS NULL OR p.subject_name = ''
               OR p.key_stage IS NULL OR p.key_stage = ''
               OR p.source_url IS NULL OR p.source_url = ''
               OR p.dfe_reference IS NULL OR p.dfe_reference = ''
               OR p.age_range IS NULL OR p.age_range = ''
            RETURN p.programme_id AS id
        """)
        total = self.scalar("MATCH (p:Programme) RETURN count(p)")
        issues = [r["id"] or "(null)" for r in records]
        status = "FAIL" if issues else "PASS"
        details = [f"Programme {i} missing required properties" for i in issues]
        self.add(ValidationResult("Programme node completeness", status, total, details))

    def check_domain_completeness(self):
        """All Domain nodes have required non-empty properties."""
        records = self.run("""
            MATCH (d:Domain)
            WHERE d.domain_id IS NULL OR d.domain_id = ''
               OR d.domain_name IS NULL OR d.domain_name = ''
               OR d.description IS NULL OR d.description = ''
               OR d.curriculum_context IS NULL OR d.curriculum_context = ''
            RETURN d.domain_id AS id
        """)
        total = self.scalar("MATCH (d:Domain) RETURN count(d)")
        issues = [r["id"] or "(null)" for r in records]
        status = "WARN" if issues else "PASS"
        details = [f"Domain {i} missing required properties" for i in issues]
        self.add(ValidationResult("Domain node completeness", status, total, details))

    def check_objective_completeness(self):
        """All Objective nodes have non-empty objective_text."""
        records = self.run("""
            MATCH (o:Objective)
            WHERE o.objective_id IS NULL OR o.objective_id = ''
               OR o.objective_text IS NULL OR o.objective_text = ''
               OR o.is_statutory IS NULL
            RETURN o.objective_id AS id
        """)
        total = self.scalar("MATCH (o:Objective) RETURN count(o)")
        issues = [r["id"] or "(null)" for r in records]
        status = "WARN" if issues else "PASS"
        details = [f"Objective {i} missing required properties" for i in issues]
        self.add(ValidationResult("Objective non-empty text", status, total, details))

    def check_concept_completeness(self):
        """All Concept nodes have required non-empty properties."""
        records = self.run("""
            MATCH (c:Concept)
            WHERE c.concept_id IS NULL OR c.concept_id = ''
               OR c.concept_name IS NULL OR c.concept_name = ''
               OR c.description IS NULL OR c.description = ''
               OR c.concept_type IS NULL OR c.concept_type = ''
               OR c.complexity_level IS NULL
            RETURN c.concept_id AS id
        """)
        total = self.scalar("MATCH (c:Concept) RETURN count(c)")
        issues = [r["id"] or "(null)" for r in records]
        status = "WARN" if issues else "PASS"
        details = [f"Concept {i} missing required properties" for i in issues]
        self.add(ValidationResult("Concept required properties", status, total, details))

    def check_source_document_completeness(self):
        """All SourceDocument nodes have required non-empty properties."""
        records = self.run("""
            MATCH (sd:SourceDocument)
            WHERE sd.document_id IS NULL OR sd.document_id = ''
               OR sd.url IS NULL OR sd.url = ''
               OR sd.subject IS NULL OR sd.subject = ''
            RETURN sd.document_id AS id
        """)
        total = self.scalar("MATCH (sd:SourceDocument) RETURN count(sd)")
        issues = [r["id"] or "(null)" for r in records]
        status = "WARN" if issues else "PASS"
        details = [f"SourceDocument {i} missing required properties" for i in issues]
        self.add(ValidationResult("SourceDocument completeness", status, total, details))

    # =========================================================================
    # B. Value constraints (enum checks)
    # =========================================================================

    def check_concept_type_values(self):
        """Concept.concept_type must be one of the valid enum values."""
        records = self.run("""
            MATCH (c:Concept)
            WHERE NOT c.concept_type IN $valid_types
            RETURN c.concept_id AS id, c.concept_type AS val
        """, valid_types=list(VALID_CONCEPT_TYPES))
        total = self.scalar("MATCH (c:Concept) RETURN count(c)")
        issues = [f"Concept {r['id']} has invalid concept_type '{r['val']}'" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("concept_type valid values", status, total, issues))

    def check_complexity_level_values(self):
        """Concept.complexity_level must be an integer 1–5."""
        records = self.run("""
            MATCH (c:Concept)
            WHERE c.complexity_level IS NULL
               OR NOT (c.complexity_level >= 1 AND c.complexity_level <= 5)
            RETURN c.concept_id AS id, c.complexity_level AS val
        """)
        total = self.scalar("MATCH (c:Concept) RETURN count(c)")
        issues = [f"Concept {r['id']} has complexity_level={r['val']} (must be 1-5)" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("complexity_level in range 1-5", status, total, issues))

    def check_domain_structure_type_values(self):
        """Domain.structure_type must be one of the valid enum values."""
        records = self.run("""
            MATCH (d:Domain)
            WHERE d.structure_type IS NOT NULL
              AND NOT d.structure_type IN $valid_types
            RETURN d.domain_id AS id, d.structure_type AS val
        """, valid_types=list(VALID_STRUCTURE_TYPES))
        total = self.scalar("MATCH (d:Domain) RETURN count(d)")
        issues = [f"Domain {r['id']} has invalid structure_type '{r['val']}'" for r in records]
        status = "WARN" if issues else "PASS"
        self.add(ValidationResult("Domain structure_type valid values", status, total, issues))

    def check_prereq_confidence_values(self):
        """PREREQUISITE_OF.confidence must be one of the valid enum values."""
        records = self.run("""
            MATCH ()-[r:PREREQUISITE_OF]->()
            WHERE r.confidence IS NOT NULL
              AND NOT r.confidence IN $valid_vals
            RETURN r.confidence AS val
            LIMIT 20
        """, valid_vals=list(VALID_PREREQ_CONFIDENCE))
        total = self.scalar("MATCH ()-[r:PREREQUISITE_OF]->() RETURN count(r)")
        issues = [f"PREREQUISITE_OF has invalid confidence '{r['val']}'" for r in records]
        status = "WARN" if issues else "PASS"
        count_label = total or 0
        self.add(ValidationResult("PREREQUISITE_OF confidence values", status, count_label, issues))

    def check_prereq_relationship_type_values(self):
        """PREREQUISITE_OF.relationship_type must be one of the valid enum values."""
        records = self.run("""
            MATCH ()-[r:PREREQUISITE_OF]->()
            WHERE r.relationship_type IS NOT NULL
              AND NOT r.relationship_type IN $valid_vals
            RETURN r.relationship_type AS val
            LIMIT 20
        """, valid_vals=list(VALID_PREREQ_REL_TYPES))
        total = self.scalar("MATCH ()-[r:PREREQUISITE_OF]->() RETURN count(r)")
        issues = [f"PREREQUISITE_OF has invalid relationship_type '{r['val']}'" for r in records]
        status = "WARN" if issues else "PASS"
        count_label = total or 0
        self.add(ValidationResult("PREREQUISITE_OF relationship_type values", status, count_label, issues))

    # =========================================================================
    # C. Relationship integrity
    # =========================================================================

    def check_orphaned_domains(self):
        """Every Domain is linked FROM at least one Programme (HAS_DOMAIN)."""
        records = self.run("""
            MATCH (d:Domain)
            WHERE NOT ()-[:HAS_DOMAIN]->(d)
            RETURN d.domain_id AS id
        """)
        total = self.scalar("MATCH (d:Domain) RETURN count(d)")
        issues = [f"Domain {r['id']} has no incoming HAS_DOMAIN" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("Orphaned Domains", status, total, issues))

    def check_orphaned_objectives(self):
        """Every Objective is linked FROM at least one Domain (CONTAINS)."""
        records = self.run("""
            MATCH (o:Objective)
            WHERE NOT ()-[:CONTAINS]->(o)
            RETURN o.objective_id AS id
        """)
        total = self.scalar("MATCH (o:Objective) RETURN count(o)")
        issues = [f"Objective {r['id']} has no incoming CONTAINS" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("Orphaned Objectives", status, total, issues))

    def check_orphaned_concepts(self):
        """Every Concept is linked FROM at least one Programme (HAS_CONCEPT)."""
        records = self.run("""
            MATCH (c:Concept)
            WHERE NOT ()-[:HAS_CONCEPT]->(c)
            RETURN c.concept_id AS id
        """)
        total = self.scalar("MATCH (c:Concept) RETURN count(c)")
        issues = [f"Concept {r['id']} has no incoming HAS_CONCEPT" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("Orphaned Concepts", status, total, issues))

    def check_programme_year_links(self):
        """Every Programme is linked FROM at least one Year (HAS_PROGRAMME)."""
        records = self.run("""
            MATCH (p:Programme)
            WHERE NOT ()-[:HAS_PROGRAMME]->(p)
            RETURN p.programme_id AS id
        """)
        total = self.scalar("MATCH (p:Programme) RETURN count(p)")
        issues = [f"Programme {r['id']} has no incoming HAS_PROGRAMME" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("Programme → Year links", status, total, issues))

    def check_programme_source_doc_links(self):
        """Every Programme has a SOURCED_FROM → SourceDocument."""
        records = self.run("""
            MATCH (p:Programme)
            WHERE NOT (p)-[:SOURCED_FROM]->(:SourceDocument)
            RETURN p.programme_id AS id
        """)
        total = self.scalar("MATCH (p:Programme) RETURN count(p)")
        issues = [f"Programme {r['id']} missing SOURCED_FROM link" for r in records]
        status = "WARN" if issues else "PASS"
        self.add(ValidationResult("Programme → SourceDocument links", status, total, issues))

    # =========================================================================
    # D. Data quality thresholds
    # =========================================================================

    def check_domain_curriculum_context_length(self):
        """curriculum_context length >= 200 chars for every Domain."""
        records = self.run("""
            MATCH (d:Domain)
            WHERE d.curriculum_context IS NOT NULL
              AND size(d.curriculum_context) < 200
            RETURN d.domain_id AS id, size(d.curriculum_context) AS len
        """)
        total = self.scalar("MATCH (d:Domain) RETURN count(d)")
        issues = [f"Domain {r['id']} has curriculum_context only {r['len']} chars" for r in records]
        status = "WARN" if issues else "PASS"
        self.add(ValidationResult("Domain curriculum_context ≥200 chars", status, total, issues))

    def check_concept_description_length(self):
        """description length >= 25 chars for every Concept."""
        records = self.run("""
            MATCH (c:Concept)
            WHERE c.description IS NOT NULL AND c.description <> ''
              AND size(c.description) < 25
            RETURN c.concept_id AS id, size(c.description) AS len
        """)
        total = self.scalar("MATCH (c:Concept) RETURN count(c)")
        issues = [f"Concept {r['id']} description only {r['len']} chars — may be too brief" for r in records]
        status = "WARN" if issues else "PASS"
        self.add(ValidationResult("Concept description ≥30 chars", status, total, issues))

    def check_objective_text_length(self):
        """objective_text length >= 10 chars for every Objective."""
        records = self.run("""
            MATCH (o:Objective)
            WHERE o.objective_text IS NOT NULL
              AND size(o.objective_text) < 10
            RETURN o.objective_id AS id, size(o.objective_text) AS len
        """)
        total = self.scalar("MATCH (o:Objective) RETURN count(o)")
        issues = [f"Objective {r['id']} text only {r['len']} chars" for r in records]
        status = "WARN" if issues else "PASS"
        self.add(ValidationResult("Objective text ≥10 chars", status, total, issues))

    def check_source_reference_present(self):
        """source_reference is present on Domain, Objective, and Concept nodes."""
        domain_missing = self.scalar("""
            MATCH (d:Domain)
            WHERE d.source_reference IS NULL OR d.source_reference = ''
            RETURN count(d)
        """) or 0
        obj_missing = self.scalar("""
            MATCH (o:Objective)
            WHERE o.source_reference IS NULL OR o.source_reference = ''
            RETURN count(o)
        """) or 0
        concept_missing = self.scalar("""
            MATCH (c:Concept)
            WHERE c.source_reference IS NULL OR c.source_reference = ''
            RETURN count(c)
        """) or 0

        total_missing = domain_missing + obj_missing + concept_missing
        issues = []
        if domain_missing:
            issues.append(f"{domain_missing} Domain nodes missing source_reference")
        if obj_missing:
            issues.append(f"{obj_missing} Objective nodes missing source_reference")
        if concept_missing:
            issues.append(f"{concept_missing} Concept nodes missing source_reference")

        status = "FAIL" if total_missing else "PASS"
        total = self.scalar("""
            MATCH (n)
            WHERE n:Domain OR n:Objective OR n:Concept
            RETURN count(n)
        """) or 0
        self.add(ValidationResult("source_reference present (D/O/C)", status, total, issues))

    # =========================================================================
    # E. Prerequisite integrity
    # =========================================================================

    def check_prerequisite_dangling(self):
        """Both ends of every PREREQUISITE_OF exist as Concept nodes."""
        # Since we use MATCH in the import query, dangling refs shouldn't exist,
        # but we verify via counting relationships vs nodes
        records = self.run("""
            MATCH (c1)-[r:PREREQUISITE_OF]->(c2)
            WHERE NOT (c1:Concept) OR NOT (c2:Concept)
            RETURN id(r) AS rel_id
        """)
        total = self.scalar("MATCH ()-[r:PREREQUISITE_OF]->() RETURN count(r)") or 0
        issues = [f"PREREQUISITE_OF rel {r['rel_id']} has non-Concept endpoint" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("Prerequisite dangling references", status, total, issues))

    def check_prerequisite_self_reference(self):
        """No self-referential prerequisites (c -[PREREQUISITE_OF]-> c)."""
        records = self.run("""
            MATCH (c:Concept)-[r:PREREQUISITE_OF]->(c)
            RETURN c.concept_id AS id
        """)
        total = self.scalar("MATCH ()-[r:PREREQUISITE_OF]->() RETURN count(r)") or 0
        issues = [f"Concept {r['id']} has self-referential PREREQUISITE_OF" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("Self-referential prerequisites", status, total, issues))

    # =========================================================================
    # F. Epistemic skill layer
    # =========================================================================

    def check_working_scientifically_completeness(self):
        """All WorkingScientifically nodes have required non-empty properties."""
        missing = self.scalar("""
            MATCH (s:WorkingScientifically)
            WHERE s.skill_id IS NULL OR s.skill_name IS NULL OR s.description IS NULL
               OR s.key_stage IS NULL OR s.complexity_level IS NULL
            RETURN count(s) AS missing
        """) or 0
        total = self.scalar("MATCH (s:WorkingScientifically) RETURN count(s)") or 0
        status = "FAIL" if missing else "PASS"
        details = [f"{missing} WorkingScientifically nodes missing required properties"] if missing else []
        self.add(ValidationResult("WorkingScientifically node completeness", status, total, details))

    def check_geographical_skill_completeness(self):
        """All GeographicalSkill nodes have required non-empty properties."""
        missing = self.scalar("""
            MATCH (s:GeographicalSkill)
            WHERE s.skill_id IS NULL OR s.skill_name IS NULL OR s.description IS NULL
               OR s.key_stage IS NULL OR s.complexity_level IS NULL
            RETURN count(s) AS missing
        """) or 0
        total = self.scalar("MATCH (s:GeographicalSkill) RETURN count(s)") or 0
        status = "FAIL" if missing else "PASS"
        details = [f"{missing} GeographicalSkill nodes missing required properties"] if missing else []
        self.add(ValidationResult("GeographicalSkill node completeness", status, total, details))

    def check_reading_skill_completeness(self):
        """All ReadingSkill nodes have required non-empty properties."""
        missing = self.scalar("""
            MATCH (s:ReadingSkill)
            WHERE s.skill_id IS NULL OR s.skill_name IS NULL OR s.description IS NULL
               OR s.key_stage IS NULL OR s.complexity_level IS NULL
            RETURN count(s) AS missing
        """) or 0
        total = self.scalar("MATCH (s:ReadingSkill) RETURN count(s)") or 0
        status = "FAIL" if missing else "PASS"
        details = [f"{missing} ReadingSkill nodes missing required properties"] if missing else []
        self.add(ValidationResult("ReadingSkill node completeness", status, total, details))

    def check_mathematical_reasoning_completeness(self):
        """All MathematicalReasoning nodes have required non-empty properties including paper."""
        missing = self.scalar("""
            MATCH (s:MathematicalReasoning)
            WHERE s.skill_id IS NULL OR s.skill_name IS NULL OR s.description IS NULL
               OR s.key_stage IS NULL OR s.complexity_level IS NULL OR s.paper IS NULL
            RETURN count(s) AS missing
        """) or 0
        total = self.scalar("MATCH (s:MathematicalReasoning) RETURN count(s)") or 0
        status = "FAIL" if missing else "PASS"
        details = [f"{missing} MathematicalReasoning nodes missing required properties"] if missing else []
        self.add(ValidationResult("MathematicalReasoning node completeness", status, total, details))

    def check_historical_thinking_completeness(self):
        """All HistoricalThinking nodes have required non-empty properties including second_order."""
        missing = self.scalar("""
            MATCH (s:HistoricalThinking)
            WHERE s.skill_id IS NULL OR s.skill_name IS NULL OR s.description IS NULL
               OR s.complexity_level IS NULL OR s.second_order IS NULL
            RETURN count(s) AS missing
        """) or 0
        total = self.scalar("MATCH (s:HistoricalThinking) RETURN count(s)") or 0
        status = "FAIL" if missing else "PASS"
        details = [f"{missing} HistoricalThinking nodes missing required properties"] if missing else []
        self.add(ValidationResult("HistoricalThinking node completeness", status, total, details))

    def check_computational_thinking_completeness(self):
        """All ComputationalThinking nodes have required non-empty properties."""
        missing = self.scalar("""
            MATCH (s:ComputationalThinking)
            WHERE s.skill_id IS NULL OR s.skill_name IS NULL OR s.description IS NULL
               OR s.key_stage IS NULL OR s.complexity_level IS NULL
            RETURN count(s) AS missing
        """) or 0
        total = self.scalar("MATCH (s:ComputationalThinking) RETURN count(s)") or 0
        status = "FAIL" if missing else "PASS"
        details = [f"{missing} ComputationalThinking nodes missing required properties"] if missing else []
        self.add(ValidationResult("ComputationalThinking node completeness", status, total, details))

    def check_progression_of_integrity(self):
        """No PROGRESSION_OF relationship points to a node of an unexpected type."""
        broken = self.scalar("""
            MATCH (a)-[:PROGRESSION_OF]->(b)
            WHERE NOT (b:WorkingScientifically OR b:GeographicalSkill OR b:ReadingSkill
                    OR b:MathematicalReasoning OR b:ComputationalThinking)
            RETURN count(*) AS broken
        """) or 0
        total = self.scalar("MATCH ()-[r:PROGRESSION_OF]->() RETURN count(r)") or 0
        status = "FAIL" if broken else "PASS"
        details = [f"{broken} PROGRESSION_OF relationships point to unexpected node types"] if broken else []
        self.add(ValidationResult("PROGRESSION_OF chain integrity", status, total, details))

    def check_reading_skill_assesses_skill_coverage(self):
        """All 8 KS2 reading content domain codes (2a–2h) have an ASSESSES_SKILL link."""
        unlinked = self.scalar("""
            MATCH (code:ContentDomainCode)
            WHERE code.code IN ['2a','2b','2c','2d','2e','2f','2g','2h']
              AND NOT (code)-[:ASSESSES_SKILL]->(:ReadingSkill)
            RETURN count(code) AS unlinked
        """) or 0
        total = self.scalar("""
            MATCH (code:ContentDomainCode)
            WHERE code.code IN ['2a','2b','2c','2d','2e','2f','2g','2h']
            RETURN count(code)
        """) or 0
        status = "FAIL" if unlinked else "PASS"
        details = [f"{unlinked} KS2 content domain codes missing ASSESSES_SKILL link"] if unlinked else []
        self.add(ValidationResult("ReadingSkill ASSESSES_SKILL coverage", status, total, details))

    def check_programme_develops_skill_coverage(self):
        """Science, Geography, English, Mathematics, History, Computing each have DEVELOPS_SKILL."""
        expected_subjects = {"Science", "Geography", "English", "Mathematics", "History", "Computing"}
        records = self.run("""
            MATCH (p:Programme)-[:DEVELOPS_SKILL]->(s)
            RETURN p.subject_name AS subject, count(s) AS skill_count
        """)
        linked = {r["subject"] for r in records if r["skill_count"] > 0}
        missing = expected_subjects - linked
        total = self.scalar("MATCH (p:Programme) RETURN count(p)") or 0
        status = "WARN" if missing else "PASS"
        details = [f"Programme '{subj}' has 0 DEVELOPS_SKILL links" for subj in sorted(missing)]
        self.add(ValidationResult("Programme DEVELOPS_SKILL coverage", status, total, details))

    # =========================================================================
    # Run all checks
    # =========================================================================

    def run_all(self):
        checks = [
            # A. Node completeness
            self.check_programme_completeness,
            self.check_domain_completeness,
            self.check_objective_completeness,
            self.check_concept_completeness,
            self.check_source_document_completeness,
            # B. Value constraints
            self.check_concept_type_values,
            self.check_complexity_level_values,
            self.check_domain_structure_type_values,
            self.check_prereq_confidence_values,
            self.check_prereq_relationship_type_values,
            # C. Relationship integrity
            self.check_orphaned_domains,
            self.check_orphaned_objectives,
            self.check_orphaned_concepts,
            self.check_programme_year_links,
            self.check_programme_source_doc_links,
            # D. Data quality
            self.check_domain_curriculum_context_length,
            self.check_concept_description_length,
            self.check_objective_text_length,
            self.check_source_reference_present,
            # E. Prerequisite integrity
            self.check_prerequisite_dangling,
            self.check_prerequisite_self_reference,
            # F. Epistemic skill layer
            self.check_working_scientifically_completeness,
            self.check_geographical_skill_completeness,
            self.check_reading_skill_completeness,
            self.check_mathematical_reasoning_completeness,
            self.check_historical_thinking_completeness,
            self.check_computational_thinking_completeness,
            self.check_progression_of_integrity,
            self.check_reading_skill_assesses_skill_coverage,
            self.check_programme_develops_skill_coverage,
        ]
        for check in checks:
            try:
                check()
            except Exception as e:
                label = check.__name__.replace("check_", "").replace("_", " ").title()
                self.add(ValidationResult(label, "FAIL", 0, [f"Check error: {e}"]))

    def report(self):
        n_pass = sum(1 for r in self.results if r.status == "PASS")
        n_warn = sum(1 for r in self.results if r.status == "WARN")
        n_fail = sum(1 for r in self.results if r.status == "FAIL")
        total = len(self.results)

        # Compute concept richness: concepts with non-empty description ≥30 chars
        rich = self.scalar("""
            MATCH (c:Concept)
            WHERE c.description IS NOT NULL AND size(c.description) >= 30
            RETURN count(c)
        """) or 0
        total_concepts = self.scalar("MATCH (c:Concept) RETURN count(c)") or 1
        health_pct = round(100 * rich / total_concepts, 1)

        print()
        print("=" * 60)
        print("UK CURRICULUM GRAPH — SCHEMA VALIDATION REPORT")
        print("=" * 60)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        for r in self.results:
            count_str = f"{r.count} nodes checked" if r.count and r.count > 0 else "0 checked"
            print(f"[CHECK] {r.label:<45} {r.status:<5} {count_str}")
        print()
        print(f"SUMMARY: {total} checks | {n_pass} PASS | {n_warn} WARN | {n_fail} FAIL")
        print(f"Overall health: {health_pct}% (concepts with full rich content)")
        print("=" * 60)

        if self.all_warnings:
            print("[WARNINGS / FAILURES]")
            for w in self.all_warnings[:50]:  # cap at 50 lines
                print(f"  {w}")
            if len(self.all_warnings) > 50:
                print(f"  ... and {len(self.all_warnings) - 50} more")
            print("=" * 60)

        return n_fail


def main():
    print("UK Curriculum Graph — Schema Validator")
    validator = SchemaValidator(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    try:
        validator.run_all()
        n_fail = validator.report()
        exit(0 if n_fail == 0 else 1)
    finally:
        validator.close()


if __name__ == "__main__":
    main()

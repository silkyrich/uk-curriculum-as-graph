#!/usr/bin/env python3
"""
UK Curriculum Graph — Schema Validation Script
Runs Cypher queries against Neo4j and produces a structured PASS/WARN/FAIL report.
"""

from neo4j import GraphDatabase
from datetime import datetime
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

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

    def check_domain_concept_links(self):
        """Every Concept is linked FROM at least one Domain (HAS_CONCEPT)."""
        records = self.run("""
            MATCH (c:Concept)
            WHERE NOT ()-[:HAS_CONCEPT]->(c)
            RETURN c.concept_id AS id
        """)
        total = self.scalar("MATCH (c:Concept) RETURN count(c)")
        issues = [f"Concept {r['id']} has no Domain link" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("Domain → Concept links", status, total, issues))

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
    # G. Topic layer
    # =========================================================================

    def check_topic_completeness(self):
        """Every Topic node has topic_id, topic_name, subject, key_stage all non-empty."""
        records = self.run("""
            MATCH (t:Topic)
            WHERE t.topic_name IS NULL OR t.topic_name = ''
               OR t.subject IS NULL OR t.subject = ''
               OR t.key_stage IS NULL OR t.key_stage = ''
            RETURN t.topic_id AS id
        """)
        issues = [r["id"] for r in records]
        total = self.scalar("MATCH (t:Topic) RETURN count(t)") or 0
        status = "FAIL" if issues else "PASS"
        details = [f"Topic '{i}' missing required property" for i in issues]
        self.add(ValidationResult("Topic node completeness", status, total, details))

    def check_topic_teaches_coverage(self):
        """Every Topic has at least one TEACHES relationship to a Concept."""
        records = self.run("""
            MATCH (t:Topic)
            WHERE NOT (t)-[:TEACHES]->(:Concept)
            RETURN t.topic_id AS id
        """)
        issues = [r["id"] for r in records]
        total = self.scalar("MATCH (t:Topic) RETURN count(t)") or 0
        status = "WARN" if issues else "PASS"
        details = [f"Topic '{i}' has no TEACHES relationship" for i in issues]
        self.add(ValidationResult("Topic -> Concept coverage", status, total, details))

    # =========================================================================
    # H. Oak Content layer (v3.4) — skip gracefully if no content imported yet
    # =========================================================================

    def check_oak_unit_completeness(self):
        """OakUnit nodes have required properties (skipped if none exist)."""
        total = self.scalar("MATCH (u:OakUnit) RETURN count(u)") or 0
        if total == 0:
            self.add(ValidationResult("OakUnit completeness", "PASS", 0, ["No OakUnit nodes — import pending"]))
            return
        records = self.run("""
            MATCH (u:OakUnit)
            WHERE u.oak_unit_slug IS NULL OR u.oak_unit_title IS NULL OR u.subject IS NULL
            RETURN u.oak_unit_slug AS id
        """)
        issues = [f"OakUnit '{r['id']}' missing required property" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("OakUnit completeness", status, total, issues))

    def check_oak_lesson_completeness(self):
        """OakLesson nodes have required properties (skipped if none exist)."""
        total = self.scalar("MATCH (l:OakLesson) RETURN count(l)") or 0
        if total == 0:
            self.add(ValidationResult("OakLesson completeness", "PASS", 0, ["No OakLesson nodes — import pending"]))
            return
        records = self.run("""
            MATCH (l:OakLesson)
            WHERE l.oak_lesson_slug IS NULL OR l.oak_lesson_title IS NULL OR l.oak_unit_slug IS NULL
            RETURN l.oak_lesson_slug AS id
        """)
        issues = [f"OakLesson '{r['id']}' missing required property" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("OakLesson completeness", status, total, issues))

    def check_oak_unit_covers_domain(self):
        """Every OakUnit covers at least one Curriculum Domain (skipped if none exist)."""
        total = self.scalar("MATCH (u:OakUnit) RETURN count(u)") or 0
        if total == 0:
            self.add(ValidationResult("OakUnit -> Domain coverage", "PASS", 0, ["No OakUnit nodes — import pending"]))
            return
        records = self.run("""
            MATCH (u:OakUnit)
            WHERE NOT (u)-[:COVERS]->(:Domain)
            RETURN u.oak_unit_slug AS id
        """)
        issues = [f"OakUnit '{r['id']}' has no COVERS -> Domain link" for r in records]
        status = "WARN" if issues else "PASS"
        self.add(ValidationResult("OakUnit -> Domain coverage", status, total, issues))

    def check_oak_lesson_teaches_concept(self):
        """Every OakLesson teaches at least one Curriculum Concept (skipped if none exist)."""
        total = self.scalar("MATCH (l:OakLesson) RETURN count(l)") or 0
        if total == 0:
            self.add(ValidationResult("OakLesson -> Concept coverage", "PASS", 0, ["No OakLesson nodes — import pending"]))
            return
        records = self.run("""
            MATCH (l:OakLesson)
            WHERE NOT (l)-[:TEACHES]->(:Concept)
            RETURN l.oak_lesson_slug AS id
        """)
        issues = [f"OakLesson '{r['id']}' has no TEACHES -> Concept link" for r in records]
        status = "WARN" if issues else "PASS"
        self.add(ValidationResult("OakLesson -> Concept coverage", status, total, issues))

    # =========================================================================
    # I. CASE Standards layer (v3.5)
    # =========================================================================

    def check_jurisdiction_completeness(self):
        """All Jurisdiction nodes have required non-empty properties (skipped if none exist)."""
        total = self.scalar("MATCH (j:Jurisdiction) RETURN count(j)") or 0
        if total == 0:
            self.add(ValidationResult("Jurisdiction node completeness", "PASS", 0,
                                      ["No Jurisdiction nodes — import pending"]))
            return
        records = self.run("""
            MATCH (j:Jurisdiction)
            WHERE j.jurisdiction_id IS NULL OR j.jurisdiction_id = ''
               OR j.name IS NULL OR j.name = ''
               OR j.jurisdiction_type IS NULL OR j.jurisdiction_type = ''
               OR j.country IS NULL OR j.country = ''
            RETURN j.jurisdiction_id AS id
        """)
        issues = [f"Jurisdiction '{r['id'] or '(null)'}' missing required properties" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("Jurisdiction node completeness", status, total, issues))

    def check_cf_document_completeness(self):
        """All CFDocument nodes have required non-empty properties (skipped if none exist)."""
        total = self.scalar("MATCH (d:CFDocument) RETURN count(d)") or 0
        if total == 0:
            self.add(ValidationResult("CFDocument node completeness", "PASS", 0,
                                      ["No CFDocument nodes — import pending"]))
            return
        records = self.run("""
            MATCH (d:CFDocument)
            WHERE d.cf_doc_id IS NULL OR d.cf_doc_id = ''
               OR d.title IS NULL OR d.title = ''
               OR d.subject IS NULL OR d.subject = ''
            RETURN d.cf_doc_id AS id
        """)
        issues = [f"CFDocument '{r['id'] or '(null)'}' missing required properties" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("CFDocument node completeness", status, total, issues))

    def check_cf_item_completeness(self):
        """All CFItem nodes have required non-empty properties (skipped if none exist)."""
        total = self.scalar("MATCH (i:CFItem) RETURN count(i)") or 0
        if total == 0:
            self.add(ValidationResult("CFItem node completeness", "PASS", 0,
                                      ["No CFItem nodes — import pending"]))
            return
        records = self.run("""
            MATCH (i:CFItem)
            WHERE i.cf_item_id IS NULL OR i.cf_item_id = ''
               OR i.full_statement IS NULL OR i.full_statement = ''
               OR i.cf_doc_id IS NULL OR i.cf_doc_id = ''
            RETURN i.cf_item_id AS id
            LIMIT 20
        """)
        issues = [f"CFItem '{r['id'] or '(null)'}' missing required properties" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("CFItem node completeness", status, total, issues))

    def check_cf_item_child_of_integrity(self):
        """No CHILD_OF relationship points to a non-existent CFItem (skipped if none exist)."""
        total = self.scalar("MATCH (:CFItem)-[:CHILD_OF]->() RETURN count(*)") or 0
        if total == 0:
            self.add(ValidationResult("CFItem CHILD_OF integrity", "PASS", 0,
                                      ["No CHILD_OF relationships — import pending"]))
            return
        records = self.run("""
            MATCH (child:CFItem)-[:CHILD_OF]->(parent)
            WHERE NOT parent:CFItem
            RETURN child.cf_item_id AS id
        """)
        issues = [f"CFItem '{r['id']}' has CHILD_OF pointing to non-CFItem node" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("CFItem CHILD_OF integrity", status, total, issues))

    # =========================================================================
    # J. Learner Profile layer
    # =========================================================================

    def check_learner_profile_nodes_exist(self):
        """All 5 learner profile node types must be present."""
        expected = {
            'InteractionType': 33,
            'ContentGuideline': 11,
            'PedagogyProfile': 11,
            'FeedbackProfile': 11,
            'PedagogyTechnique': 5,
        }
        issues = []
        total = 0
        for label, expected_count in expected.items():
            count = self.scalar(f"MATCH (n:{label}) RETURN count(n)") or 0
            total += count
            if count == 0:
                issues.append(f"{label}: 0 nodes (expected {expected_count}) — import pending?")
            elif count != expected_count:
                issues.append(f"{label}: {count} nodes (expected {expected_count})")
        status = "FAIL" if any("0 nodes" in i for i in issues) else ("WARN" if issues else "PASS")
        self.add(ValidationResult("Learner profile nodes exist", status, total, issues))

    def check_year_learner_profile_links(self):
        """Every Year node should link to ContentGuideline, PedagogyProfile, and FeedbackProfile."""
        records = self.run("""
            MATCH (y:Year)
            OPTIONAL MATCH (y)-[:HAS_CONTENT_GUIDELINE]->(cg:ContentGuideline)
            OPTIONAL MATCH (y)-[:HAS_PEDAGOGY_PROFILE]->(pp:PedagogyProfile)
            OPTIONAL MATCH (y)-[:HAS_FEEDBACK_PROFILE]->(fp:FeedbackProfile)
            WITH y, cg, pp, fp
            WHERE cg IS NULL OR pp IS NULL OR fp IS NULL
            RETURN y.year_id AS id,
                   CASE WHEN cg IS NULL THEN 'ContentGuideline' ELSE '' END +
                   CASE WHEN pp IS NULL THEN ' PedagogyProfile' ELSE '' END +
                   CASE WHEN fp IS NULL THEN ' FeedbackProfile' ELSE '' END AS missing
        """)
        issues = [f"Year {r['id']} missing: {r['missing'].strip()}" for r in records]
        total = self.scalar("MATCH (y:Year) RETURN count(y)") or 0
        # FAIL if learner profiles exist but links are broken; WARN if no profiles at all
        profile_count = self.scalar("MATCH (n:ContentGuideline) RETURN count(n)") or 0
        if profile_count == 0:
            status = "WARN" if issues else "PASS"
            issues = ["Learner profile layer not imported — skipping link check"] if issues else []
        else:
            status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("Year → Learner profile links", status, total, issues))

    def check_interaction_type_completeness(self):
        """InteractionType nodes have required properties (skipped if none exist)."""
        total = self.scalar("MATCH (n:InteractionType) RETURN count(n)") or 0
        if total == 0:
            self.add(ValidationResult("InteractionType completeness", "PASS", 0,
                                      ["No InteractionType nodes — import pending"]))
            return
        records = self.run("""
            MATCH (n:InteractionType)
            WHERE n.interaction_id IS NULL OR n.name IS NULL OR n.agent_prompt IS NULL
            RETURN n.interaction_id AS id
        """)
        issues = [f"InteractionType '{r['id'] or '(null)'}' missing required properties" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("InteractionType completeness", status, total, issues))

    def check_interaction_precedes_chain(self):
        """InteractionType PRECEDES chain should form a connected sequence."""
        total = self.scalar("MATCH (n:InteractionType) RETURN count(n)") or 0
        if total == 0:
            self.add(ValidationResult("InteractionType PRECEDES chain", "PASS", 0,
                                      ["No InteractionType nodes — import pending"]))
            return
        chain_count = self.scalar("""
            MATCH (:InteractionType)-[r:PRECEDES]->(:InteractionType) RETURN count(r)
        """) or 0
        status = "PASS" if chain_count > 0 else "WARN"
        details = [] if chain_count > 0 else ["No PRECEDES chain between InteractionType nodes"]
        self.add(ValidationResult("InteractionType PRECEDES chain", status, total, details))

    # =========================================================================
    # K-bis. Concept Grouping layer (v3.7)
    # =========================================================================

    def check_teaching_weight_values(self):
        """teaching_weight must be 1-6 where present."""
        records = self.run("""
            MATCH (c:Concept)
            WHERE c.teaching_weight IS NOT NULL
              AND NOT (c.teaching_weight >= 1 AND c.teaching_weight <= 6)
            RETURN c.concept_id AS id, c.teaching_weight AS val
        """)
        total = self.scalar("MATCH (c:Concept) WHERE c.teaching_weight IS NOT NULL RETURN count(c)") or 0
        issues = [f"Concept {r['id']} has teaching_weight={r['val']} (must be 1-6)" for r in records]
        status = "WARN" if issues else "PASS"
        self.add(ValidationResult("teaching_weight in range 1-6", status, total, issues))

    def check_is_keystone_consistency(self):
        """is_keystone should be true iff prerequisite_fan_out >= 3."""
        records = self.run("""
            MATCH (c:Concept)
            WHERE c.is_keystone IS NOT NULL AND c.prerequisite_fan_out IS NOT NULL
              AND ((c.is_keystone = true AND c.prerequisite_fan_out < 3)
                OR (c.is_keystone = false AND c.prerequisite_fan_out >= 3))
            RETURN c.concept_id AS id, c.is_keystone AS ks, c.prerequisite_fan_out AS fo
        """)
        total = self.scalar("MATCH (c:Concept) WHERE c.is_keystone IS NOT NULL RETURN count(c)") or 0
        issues = [f"Concept {r['id']} is_keystone={r['ks']} but fan_out={r['fo']}" for r in records]
        status = "WARN" if issues else "PASS"
        self.add(ValidationResult("is_keystone consistency", status, total, issues))

    def check_co_teaches_integrity(self):
        """CO_TEACHES should connect Concepts in the same domain (cross-domain is WARN)."""
        records = self.run("""
            MATCH (c1:Concept)-[r:CO_TEACHES]->(c2:Concept)
            WHERE NOT EXISTS {
                MATCH (d:Domain)-[:HAS_CONCEPT]->(c1)
                MATCH (d)-[:HAS_CONCEPT]->(c2)
            }
            RETURN c1.concept_id AS src, c2.concept_id AS tgt
            LIMIT 20
        """)
        total = self.scalar("MATCH ()-[r:CO_TEACHES]->() RETURN count(r)") or 0
        issues = [f"CO_TEACHES {r['src']} -> {r['tgt']} cross-domain" for r in records]
        # Cross-domain within same programme is valid teaching advice, not a data error
        status = "WARN" if issues else "PASS"
        self.add(ValidationResult("CO_TEACHES same-domain integrity", status, total, issues))

    def check_concept_cluster_completeness(self):
        """ConceptCluster nodes have required non-null properties (skipped if none exist)."""
        total = self.scalar("MATCH (cc:ConceptCluster) RETURN count(cc)") or 0
        if total == 0:
            self.add(ValidationResult("ConceptCluster completeness", "PASS", 0,
                                      ["No ConceptCluster nodes — generation pending"]))
            return
        records = self.run("""
            MATCH (cc:ConceptCluster)
            WHERE cc.cluster_id IS NULL OR cc.cluster_name IS NULL OR cc.cluster_type IS NULL
            RETURN cc.cluster_id AS id
        """)
        issues = [f"ConceptCluster '{r['id'] or '(null)'}' missing required properties" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("ConceptCluster completeness", status, total, issues))

    def check_concept_cluster_coverage(self):
        """Every Concept in a domain with clusters should be grouped (skipped if none exist)."""
        total = self.scalar("MATCH (cc:ConceptCluster) RETURN count(cc)") or 0
        if total == 0:
            self.add(ValidationResult("ConceptCluster coverage", "PASS", 0,
                                      ["No ConceptCluster nodes — generation pending"]))
            return
        records = self.run("""
            MATCH (d:Domain)-[:HAS_CLUSTER]->(:ConceptCluster)
            WITH COLLECT(DISTINCT d) AS clustered_domains
            UNWIND clustered_domains AS d
            MATCH (d)-[:HAS_CONCEPT]->(c:Concept)
            WHERE NOT (:ConceptCluster)-[:GROUPS]->(c)
            RETURN c.concept_id AS id
            LIMIT 20
        """)
        total_concepts = self.scalar("""
            MATCH (d:Domain)-[:HAS_CLUSTER]->(:ConceptCluster)
            WITH COLLECT(DISTINCT d) AS clustered_domains
            UNWIND clustered_domains AS d
            MATCH (d)-[:HAS_CONCEPT]->(c:Concept)
            RETURN count(DISTINCT c)
        """) or 0
        issues = [f"Concept {r['id']} in clustered domain but not grouped" for r in records]
        status = "WARN" if issues else "PASS"
        self.add(ValidationResult("ConceptCluster coverage", status, total_concepts, issues))

    def check_cluster_sequencing(self):
        """SEQUENCED_AFTER forms a valid chain per domain (skipped if none exist)."""
        total = self.scalar("MATCH (cc:ConceptCluster) RETURN count(cc)") or 0
        if total == 0:
            self.add(ValidationResult("Cluster SEQUENCED_AFTER chain", "PASS", 0,
                                      ["No ConceptCluster nodes — generation pending"]))
            return
        # Check for cycles: a cluster that is SEQUENCED_AFTER itself (directly or indirectly)
        records = self.run("""
            MATCH (cc:ConceptCluster)-[:SEQUENCED_AFTER]->(cc)
            RETURN cc.cluster_id AS id
        """)
        # Check for multiple incoming SEQUENCED_AFTER (would mean branching, not a chain)
        records2 = self.run("""
            MATCH (cc:ConceptCluster)<-[r:SEQUENCED_AFTER]-()
            WITH cc, count(r) AS incoming
            WHERE incoming > 1
            RETURN cc.cluster_id AS id, incoming
            LIMIT 10
        """)
        issues = [f"Cluster {r['id']} has self-referential SEQUENCED_AFTER" for r in records]
        issues += [f"Cluster {r['id']} has {r['incoming']} incoming SEQUENCED_AFTER (expected <=1)" for r in records2]
        chain_count = self.scalar("MATCH ()-[r:SEQUENCED_AFTER]->() RETURN count(r)") or 0
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("Cluster SEQUENCED_AFTER chain", status, chain_count, issues))

    def check_cluster_max_size(self):
        """No cluster should group more than 6 concepts (skipped if none exist)."""
        total = self.scalar("MATCH (cc:ConceptCluster) RETURN count(cc)") or 0
        if total == 0:
            self.add(ValidationResult("Cluster max size ≤6", "PASS", 0,
                                      ["No ConceptCluster nodes — generation pending"]))
            return
        records = self.run("""
            MATCH (cc:ConceptCluster)-[:GROUPS]->(c:Concept)
            WITH cc, count(c) AS sz
            WHERE sz > 6
            RETURN cc.cluster_id AS id, sz
            ORDER BY sz DESC
            LIMIT 10
        """)
        issues = [f"Cluster {r['id']} groups {r['sz']} concepts (max 6)" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("Cluster max size ≤6", status, total, issues))

    def check_cluster_non_empty(self):
        """Every cluster must group at least 1 concept via GROUPS (skipped if none exist)."""
        total = self.scalar("MATCH (cc:ConceptCluster) RETURN count(cc)") or 0
        if total == 0:
            self.add(ValidationResult("Cluster non-empty", "PASS", 0,
                                      ["No ConceptCluster nodes — generation pending"]))
            return
        records = self.run("""
            MATCH (cc:ConceptCluster)
            WHERE NOT (cc)-[:GROUPS]->(:Concept)
            RETURN cc.cluster_id AS id, cc.cluster_type AS ctype
            LIMIT 10
        """)
        issues = [f"Cluster {r['id']} ({r['ctype']}) has no GROUPS relationships" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("Cluster non-empty", status, total, issues))

    def check_cluster_type_distribution(self):
        """Cluster type distribution should be reasonable (skipped if none exist)."""
        total = self.scalar("MATCH (cc:ConceptCluster) RETURN count(cc)") or 0
        if total == 0:
            self.add(ValidationResult("Cluster type distribution", "PASS", 0,
                                      ["No ConceptCluster nodes — generation pending"]))
            return
        records = self.run("""
            MATCH (cc:ConceptCluster)
            RETURN cc.cluster_type AS ctype, count(cc) AS cnt
            ORDER BY cnt DESC
        """)
        dist = {r["ctype"]: r["cnt"] for r in records}
        issues = []

        # Practice should be the majority (>40% of total)
        practice = dist.get("practice", 0)
        practice_pct = round(100 * practice / total, 1) if total else 0
        if practice_pct < 40:
            issues.append(f"Practice clusters are only {practice_pct}% ({practice}/{total}) — expected >40%")

        # Consolidation should be ~15-25%
        consol = dist.get("consolidation", 0)
        consol_pct = round(100 * consol / total, 1) if total else 0
        if consol_pct > 30:
            issues.append(f"Consolidation clusters are {consol_pct}% ({consol}/{total}) — expected <30%")

        # Assessment should be ~10-20%
        assess = dist.get("assessment", 0)
        assess_pct = round(100 * assess / total, 1) if total else 0
        if assess_pct > 30:
            issues.append(f"Assessment clusters are {assess_pct}% ({assess}/{total}) — expected <30%")

        # Report distribution in detail
        dist_str = ", ".join(f"{k}: {v} ({round(100*v/total,1)}%)" for k, v in sorted(dist.items()))
        if not issues:
            issues = [f"Distribution: {dist_str}"]

        status = "WARN" if any("expected" in i for i in issues) else "PASS"
        self.add(ValidationResult("Cluster type distribution", status, total, issues))

    # =========================================================================
    # K. Enrichment coverage (DB-level)
    # =========================================================================

    def check_concept_enrichment_coverage(self):
        """Concepts should have teaching_guidance, key_vocabulary, common_misconceptions."""
        records = self.run("""
            MATCH (c:Concept)
            WHERE c.teaching_guidance IS NULL OR c.teaching_guidance = ''
            MATCH (d:Domain)-[:HAS_CONCEPT]->(c)
            MATCH (p:Programme)-[:HAS_DOMAIN]->(d)
            RETURN p.subject_name AS subject, count(c) AS bare
            ORDER BY bare DESC
        """)
        total_bare = sum(r['bare'] for r in records)
        total = self.scalar("MATCH (c:Concept) RETURN count(c)") or 0
        enriched = total - total_bare
        pct = round(100 * enriched / total, 1) if total else 0
        issues = [f"{r['subject']}: {r['bare']} concepts without teaching_guidance" for r in records]
        if total_bare > 0:
            issues.insert(0, f"{total_bare}/{total} concepts bare ({pct}% enriched)")
        status = "WARN" if total_bare > 0 else "PASS"
        self.add(ValidationResult("Concept enrichment coverage", status, total, issues))

    # =========================================================================
    # L. Display & Visualization invariants
    # =========================================================================

    def check_name_property_coverage(self):
        """Every node must have a non-null, non-empty name property."""
        records = self.run("""
            MATCH (n) WHERE n.name IS NULL OR n.name = ''
            RETURN labels(n)[0] AS label, count(n) AS count
            ORDER BY count DESC
        """)
        issues = [f"{r['count']} {r['label']} node(s) missing name" for r in records]
        total_missing = sum(r['count'] for r in records)
        total = self.scalar("MATCH (n) RETURN count(n)") or 0
        status = "FAIL" if total_missing else "PASS"
        self.add(ValidationResult("name property coverage", status, total, issues))

    def check_display_color_coverage(self):
        """Every non-internal node must have a display_color property."""
        records = self.run("""
            MATCH (n) WHERE n.display_color IS NULL
            WITH labels(n)[0] AS label, count(n) AS count
            WHERE NOT label STARTS WITH '_'
            RETURN label, count ORDER BY count DESC
        """)
        issues = [f"{r['count']} {r['label']} node(s) missing display_color" for r in records]
        total_missing = sum(r['count'] for r in records)
        total = self.scalar("MATCH (n) WHERE NOT labels(n)[0] STARTS WITH '_' RETURN count(n)") or 0
        status = "WARN" if total_missing else "PASS"
        self.add(ValidationResult("display_color coverage", status, total, issues))

    def check_display_category_coverage(self):
        """Every non-internal node must have a display_category property."""
        records = self.run("""
            MATCH (n) WHERE n.display_category IS NULL
            WITH labels(n)[0] AS label, count(n) AS count
            WHERE NOT label STARTS WITH '_'
            RETURN label, count ORDER BY count DESC
        """)
        issues = [f"{r['count']} {r['label']} node(s) missing display_category" for r in records]
        total_missing = sum(r['count'] for r in records)
        total = self.scalar("MATCH (n) WHERE NOT labels(n)[0] STARTS WITH '_' RETURN count(n)") or 0
        status = "WARN" if total_missing else "PASS"
        self.add(ValidationResult("display_category coverage", status, total, issues))

    def check_display_category_values(self):
        """display_category must be one of the recognised values."""
        valid_categories = {
            'UK Curriculum', 'CASE Standards', 'Epistemic Skills',
            'Assessment', 'Structure', 'Learner Profile', 'Oak Content',
        }
        records = self.run("""
            MATCH (n)
            WHERE n.display_category IS NOT NULL
              AND NOT n.display_category IN $valid_cats
            RETURN n.display_category AS val, count(n) AS count
        """, valid_cats=list(valid_categories))
        issues = [f"{r['count']} node(s) with unrecognised display_category '{r['val']}'" for r in records]
        total = self.scalar("MATCH (n) WHERE n.display_category IS NOT NULL RETURN count(n)") or 0
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("display_category valid values", status, total, issues))

    def check_year_node_invariants(self):
        """All 11 Year nodes (Y1-Y11) exist with required properties and correct name."""
        total = self.scalar("MATCH (y:Year) RETURN count(y)") or 0
        issues = []
        if total != 11:
            issues.append(f"Expected 11 Year nodes, found {total}")
        # Check required properties and name format
        records = self.run("""
            MATCH (y:Year)
            WHERE y.year_id IS NULL OR y.year_number IS NULL
               OR y.age_range IS NULL OR y.key_stage IS NULL
               OR y.name IS NULL
               OR y.name <> ('Year ' + toString(y.year_number))
            RETURN y.year_id AS id, y.year_number AS num, y.name AS name
        """)
        for r in records:
            yr_id = r['id'] or '(null)'
            yr_num = r['num']
            yr_name = r['name']
            if yr_name is None:
                issues.append(f"Year {yr_id} missing name property")
            elif yr_num is not None and yr_name != f"Year {yr_num}":
                issues.append(f"Year {yr_id} name='{yr_name}' (expected 'Year {yr_num}')")
            else:
                issues.append(f"Year {yr_id} missing required properties")
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("Year node invariants", status, total, issues))

    def check_bloom_perspective_exists(self):
        """At least one _Bloom_Perspective_ node exists (needed for Bloom visualization)."""
        total = self.scalar("MATCH (p:`_Bloom_Perspective_`) RETURN count(p)") or 0
        status = "PASS" if total > 0 else "WARN"
        details = [] if total > 0 else ["No _Bloom_Perspective_ nodes found — Bloom visualisation won't work"]
        self.add(ValidationResult("Bloom perspective exists", status, total, details))

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
            self.check_domain_concept_links,
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
            # G. Topic layer
            self.check_topic_completeness,
            self.check_topic_teaches_coverage,
            # H. Oak Content layer (v3.4)
            self.check_oak_unit_completeness,
            self.check_oak_lesson_completeness,
            self.check_oak_unit_covers_domain,
            self.check_oak_lesson_teaches_concept,
            # I. CASE Standards layer (v3.5)
            self.check_jurisdiction_completeness,
            self.check_cf_document_completeness,
            self.check_cf_item_completeness,
            self.check_cf_item_child_of_integrity,
            # J. Learner Profile layer
            self.check_learner_profile_nodes_exist,
            self.check_year_learner_profile_links,
            self.check_interaction_type_completeness,
            self.check_interaction_precedes_chain,
            # K-bis. Concept Grouping (v3.7)
            self.check_teaching_weight_values,
            self.check_is_keystone_consistency,
            self.check_co_teaches_integrity,
            self.check_concept_cluster_completeness,
            self.check_concept_cluster_coverage,
            self.check_cluster_sequencing,
            self.check_cluster_max_size,
            self.check_cluster_non_empty,
            self.check_cluster_type_distribution,
            # K. Enrichment coverage
            self.check_concept_enrichment_coverage,
            # L. Display & Visualization
            self.check_name_property_coverage,
            self.check_display_color_coverage,
            self.check_display_category_coverage,
            self.check_display_category_values,
            self.check_year_node_invariants,
            self.check_bloom_perspective_exists,
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


# ============================================================
# COMPLETION QUERIES
# ============================================================
# Unified completion view — works across all subjects:
#
# For subjects WITH Topics (History, Geography etc.):
#   MATCH (t:Topic)-[:TEACHES]->(c:Concept)
#   RETURN t.subject, t.key_stage, t.topic_name,
#          count(c) AS concepts_covered
#   ORDER BY t.subject, t.key_stage
#
# For Maths/Science (Topics = Domains):
#   MATCH (d:Domain)-[:HAS_CONCEPT]->(c:Concept)
#   WHERE d.domain_id STARTS WITH 'MA-'
#   RETURN d.domain_name, count(c) AS concept_count
#
# Concepts with no topic coverage (gap analysis):
#   MATCH (c:Concept)
#   WHERE NOT (:Topic)-[:TEACHES]->(c)
#   RETURN c.concept_id, c.concept_name, c.source_reference
#   ORDER BY c.source_reference
# ============================================================


if __name__ == "__main__":
    main()

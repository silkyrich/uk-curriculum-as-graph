#!/usr/bin/env python3
"""
Validate Vocabulary layer in Neo4j.

Checks:
  1. VocabularyTerm node completeness (required properties)
  2. Tier value validity (1, 2, or 3)
  3. USES_TERM relationship integrity (both endpoints exist)
  4. USES_TERM importance values validity
  5. Coverage reporting (terms per subject, terms with definitions)
  6. REFINES relationship integrity
  7. Orphaned terms (no USES_TERM incoming)

Usage:
  python3 layers/vocabulary/scripts/validate_vocabulary.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / "core" / "scripts"))

from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

VALID_TIERS = {1, 2, 3}
VALID_IMPORTANCE = {"core", "supporting", "extension"}
VALID_WORD_CLASSES = {"noun", "verb", "adjective", "adverb", "phrase", ""}


class ValidationResult:
    def __init__(self, label, status, count, details=None):
        self.label = label
        self.status = status  # PASS, WARN, FAIL
        self.count = count
        self.details = details or []


class VocabularyValidator:
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
    # 1. Node completeness
    # =========================================================================

    def check_term_completeness(self):
        """All VocabularyTerm nodes have required non-empty properties."""
        total = self.scalar("MATCH (vt:VocabularyTerm) RETURN count(vt)") or 0
        if total == 0:
            self.add(ValidationResult("VocabularyTerm completeness", "PASS", 0,
                                      ["No VocabularyTerm nodes — import pending"]))
            return

        records = self.run("""
            MATCH (vt:VocabularyTerm)
            WHERE vt.term_id IS NULL OR vt.term_id = ''
               OR vt.term IS NULL OR vt.term = ''
               OR vt.subject IS NULL OR vt.subject = ''
               OR vt.tier IS NULL
            RETURN vt.term_id AS id
            LIMIT 20
        """)
        issues = [f"VocabularyTerm '{r['id'] or '(null)'}' missing required properties" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("VocabularyTerm completeness", status, total, issues))

    # =========================================================================
    # 2. Tier values
    # =========================================================================

    def check_tier_values(self):
        """VocabularyTerm.tier must be 1, 2, or 3."""
        total = self.scalar("MATCH (vt:VocabularyTerm) RETURN count(vt)") or 0
        if total == 0:
            self.add(ValidationResult("Tier valid values", "PASS", 0, []))
            return

        records = self.run("""
            MATCH (vt:VocabularyTerm)
            WHERE NOT vt.tier IN [1, 2, 3]
            RETURN vt.term_id AS id, vt.tier AS val
            LIMIT 20
        """)
        issues = [f"VocabularyTerm {r['id']} has invalid tier {r['val']}" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("Tier valid values", status, total, issues))

    # =========================================================================
    # 3. USES_TERM relationship integrity
    # =========================================================================

    def check_uses_term_integrity(self):
        """USES_TERM relationships connect Concept -> VocabularyTerm."""
        total = self.scalar("MATCH ()-[r:USES_TERM]->() RETURN count(r)") or 0
        if total == 0:
            self.add(ValidationResult("USES_TERM integrity", "PASS", 0,
                                      ["No USES_TERM relationships — import pending"]))
            return

        # Check source is Concept
        bad_source = self.scalar("""
            MATCH (a)-[r:USES_TERM]->(b)
            WHERE NOT a:Concept
            RETURN count(r)
        """) or 0

        # Check target is VocabularyTerm
        bad_target = self.scalar("""
            MATCH (a)-[r:USES_TERM]->(b)
            WHERE NOT b:VocabularyTerm
            RETURN count(r)
        """) or 0

        issues = []
        if bad_source > 0:
            issues.append(f"{bad_source} USES_TERM rels have non-Concept source")
        if bad_target > 0:
            issues.append(f"{bad_target} USES_TERM rels have non-VocabularyTerm target")

        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("USES_TERM integrity", status, total, issues))

    # =========================================================================
    # 4. USES_TERM importance values
    # =========================================================================

    def check_uses_term_importance_values(self):
        """USES_TERM.importance must be 'core', 'supporting', or 'extension'."""
        total = self.scalar("MATCH ()-[r:USES_TERM]->() RETURN count(r)") or 0
        if total == 0:
            self.add(ValidationResult("USES_TERM importance values", "PASS", 0, []))
            return

        records = self.run("""
            MATCH (c)-[r:USES_TERM]->(vt)
            WHERE r.importance IS NOT NULL
              AND NOT r.importance IN $valid_vals
            RETURN c.concept_id AS cid, vt.term_id AS tid, r.importance AS val
            LIMIT 20
        """, valid_vals=list(VALID_IMPORTANCE))
        issues = [f"{r['cid']}->{r['tid']} has invalid importance '{r['val']}'" for r in records]
        status = "WARN" if issues else "PASS"
        self.add(ValidationResult("USES_TERM importance values", status, total, issues))

    # =========================================================================
    # 5. Coverage reporting
    # =========================================================================

    def check_definition_coverage(self):
        """Report how many terms have definitions vs empty stubs."""
        total = self.scalar("MATCH (vt:VocabularyTerm) RETURN count(vt)") or 0
        if total == 0:
            self.add(ValidationResult("Definition coverage", "PASS", 0,
                                      ["No VocabularyTerm nodes — import pending"]))
            return

        defined = self.scalar("""
            MATCH (vt:VocabularyTerm)
            WHERE vt.definition IS NOT NULL AND vt.definition <> ''
            RETURN count(vt)
        """) or 0

        pct = round(100 * defined / total, 1) if total else 0
        issues = [f"{defined}/{total} terms have definitions ({pct}%)"]
        if pct < 50:
            issues.append("Less than 50% coverage — definition generation pending")
        status = "WARN" if pct < 10 else "PASS"
        self.add(ValidationResult("Definition coverage", status, total, issues))

    def check_subject_distribution(self):
        """Report term distribution by subject prefix."""
        total = self.scalar("MATCH (vt:VocabularyTerm) RETURN count(vt)") or 0
        if total == 0:
            self.add(ValidationResult("Subject distribution", "PASS", 0, []))
            return

        records = self.run("""
            MATCH (vt:VocabularyTerm)
            RETURN vt.subject AS subject, count(vt) AS count
            ORDER BY count DESC
        """)
        issues = [f"{r['subject']}: {r['count']} terms" for r in records]
        self.add(ValidationResult("Subject distribution", "PASS", total, issues))

    # =========================================================================
    # 6. REFINES integrity
    # =========================================================================

    def check_refines_integrity(self):
        """REFINES relationships connect VocabularyTerm -> VocabularyTerm."""
        total = self.scalar("MATCH ()-[r:REFINES]->() RETURN count(r)") or 0
        if total == 0:
            self.add(ValidationResult("REFINES integrity", "PASS", 0,
                                      ["No REFINES relationships — authoring pending"]))
            return

        bad = self.scalar("""
            MATCH (a)-[r:REFINES]->(b)
            WHERE NOT a:VocabularyTerm OR NOT b:VocabularyTerm
            RETURN count(r)
        """) or 0

        issues = []
        if bad > 0:
            issues.append(f"{bad} REFINES rels connect non-VocabularyTerm nodes")
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("REFINES integrity", status, total, issues))

    # =========================================================================
    # 7. Orphaned terms
    # =========================================================================

    def check_orphaned_terms(self):
        """Terms with no incoming USES_TERM (not linked to any concept)."""
        total = self.scalar("MATCH (vt:VocabularyTerm) RETURN count(vt)") or 0
        if total == 0:
            self.add(ValidationResult("Orphaned terms", "PASS", 0, []))
            return

        orphaned = self.scalar("""
            MATCH (vt:VocabularyTerm)
            WHERE NOT (:Concept)-[:USES_TERM]->(vt)
            RETURN count(vt)
        """) or 0

        issues = []
        if orphaned > 0:
            issues.append(f"{orphaned}/{total} VocabularyTerm nodes have no USES_TERM")
        status = "WARN" if orphaned > 0 else "PASS"
        self.add(ValidationResult("Orphaned terms", status, total, issues))

    # =========================================================================
    # Run all + report
    # =========================================================================

    def run_all(self):
        checks = [
            self.check_term_completeness,
            self.check_tier_values,
            self.check_uses_term_integrity,
            self.check_uses_term_importance_values,
            self.check_definition_coverage,
            self.check_subject_distribution,
            self.check_refines_integrity,
            self.check_orphaned_terms,
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

        print()
        print("=" * 60)
        print("VOCABULARY LAYER — VALIDATION REPORT")
        print("=" * 60)
        print()
        for i, r in enumerate(self.results, 1):
            count_str = f"{r.count} checked" if r.count and r.count > 0 else "0 checked"
            print(f"  {i}. [{r.status}] {r.label:<40} {count_str}")
        print()
        print(f"SUMMARY: {total} checks | {n_pass} PASS | {n_warn} WARN | {n_fail} FAIL")
        print("=" * 60)

        if self.all_warnings:
            print("[DETAILS]")
            for w in self.all_warnings[:50]:
                print(f"  {w}")
            if len(self.all_warnings) > 50:
                print(f"  ... and {len(self.all_warnings) - 50} more")
            print("=" * 60)

        return n_fail


def main():
    print("Vocabulary Layer — Validator")
    validator = VocabularyValidator(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    try:
        validator.run_all()
        n_fail = validator.report()
        exit(0 if n_fail == 0 else 1)
    finally:
        validator.close()


if __name__ == "__main__":
    main()

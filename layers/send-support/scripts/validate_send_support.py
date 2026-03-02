#!/usr/bin/env python3
"""
SEND Support Layer — Validation Script

Runs Cypher queries against Neo4j and produces a structured PASS/WARN/FAIL report
for the SEND Support layer (NeedArea, AccessRequirement, SupportStrategy nodes
and their relationships).

Usage:
  python3 layers/send-support/scripts/validate_send_support.py
"""

import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / "core" / "scripts"))

from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

VALID_TIERS = {"universal", "targeted", "specialist"}
VALID_CONSTRUCT_RISK = {"low", "conditional", "high"}
VALID_INTENSITY = {"low", "medium", "high"}
VALID_ACCESS_LEVELS = {"low", "medium", "high"}

# Diagnosis terms that must never appear as primary node labels or identifiers
DIAGNOSIS_TERMS = {
    "dyslexia", "adhd", "autism", "asd", "dyscalculia", "dyspraxia",
    "tourette", "ocd", "anxiety", "depression", "downs", "cerebral",
    "epilepsy", "asperger", "spld",
}


class ValidationResult:
    def __init__(self, label, status, count, details=None):
        self.label = label
        self.status = status  # PASS, WARN, FAIL
        self.count = count
        self.details = details or []


class SendSupportValidator:
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
    # 1. Schema completeness
    # =========================================================================

    def check_need_area_completeness(self):
        """All NeedArea nodes have required non-empty properties."""
        total = self.scalar("MATCH (na:NeedArea) RETURN count(na)") or 0
        if total == 0:
            self.add(ValidationResult("NeedArea completeness", "PASS", 0,
                                      ["No NeedArea nodes — import pending"]))
            return
        records = self.run("""
            MATCH (na:NeedArea)
            WHERE na.need_area_id IS NULL OR na.need_area_id = ''
               OR na.name IS NULL OR na.name = ''
               OR na.description IS NULL OR na.description = ''
               OR na.statutory_order IS NULL
            RETURN na.need_area_id AS id
        """)
        issues = [f"NeedArea '{r['id'] or '(null)'}' missing required properties" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("NeedArea completeness", status, total, issues))

    def check_access_requirement_completeness(self):
        """All AccessRequirement nodes have required non-empty properties."""
        total = self.scalar("MATCH (ar:AccessRequirement) RETURN count(ar)") or 0
        if total == 0:
            self.add(ValidationResult("AccessRequirement completeness", "PASS", 0,
                                      ["No AccessRequirement nodes — import pending"]))
            return
        records = self.run("""
            MATCH (ar:AccessRequirement)
            WHERE ar.access_req_id IS NULL OR ar.access_req_id = ''
               OR ar.name IS NULL OR ar.name = ''
               OR ar.category IS NULL OR ar.category = ''
               OR ar.description IS NULL OR ar.description = ''
               OR ar.intensity_default IS NULL OR ar.intensity_default = ''
            RETURN ar.access_req_id AS id
        """)
        issues = [f"AccessRequirement '{r['id'] or '(null)'}' missing required properties" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("AccessRequirement completeness", status, total, issues))

    def check_support_strategy_completeness(self):
        """All SupportStrategy nodes have required non-empty properties."""
        total = self.scalar("MATCH (ss:SupportStrategy) RETURN count(ss)") or 0
        if total == 0:
            self.add(ValidationResult("SupportStrategy completeness", "PASS", 0,
                                      ["No SupportStrategy nodes — import pending"]))
            return
        records = self.run("""
            MATCH (ss:SupportStrategy)
            WHERE ss.support_id IS NULL OR ss.support_id = ''
               OR ss.name IS NULL OR ss.name = ''
               OR ss.tier IS NULL OR ss.tier = ''
               OR ss.description IS NULL OR ss.description = ''
               OR ss.construct_risk IS NULL OR ss.construct_risk = ''
            RETURN ss.support_id AS id
        """)
        issues = [f"SupportStrategy '{r['id'] or '(null)'}' missing required properties" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("SupportStrategy completeness", status, total, issues))

    # =========================================================================
    # 2. Enum validity
    # =========================================================================

    def check_tier_values(self):
        """SupportStrategy.tier must be one of: universal, targeted, specialist."""
        total = self.scalar("MATCH (ss:SupportStrategy) RETURN count(ss)") or 0
        if total == 0:
            self.add(ValidationResult("SupportStrategy tier values", "PASS", 0,
                                      ["No SupportStrategy nodes — import pending"]))
            return
        records = self.run("""
            MATCH (ss:SupportStrategy)
            WHERE NOT ss.tier IN $valid_tiers
            RETURN ss.support_id AS id, ss.tier AS val
        """, valid_tiers=list(VALID_TIERS))
        issues = [f"SupportStrategy '{r['id']}' has invalid tier '{r['val']}'" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("SupportStrategy tier values", status, total, issues))

    def check_construct_risk_values(self):
        """SupportStrategy.construct_risk must be one of: low, conditional, high."""
        total = self.scalar("MATCH (ss:SupportStrategy) RETURN count(ss)") or 0
        if total == 0:
            self.add(ValidationResult("construct_risk values", "PASS", 0,
                                      ["No SupportStrategy nodes — import pending"]))
            return
        records = self.run("""
            MATCH (ss:SupportStrategy)
            WHERE NOT ss.construct_risk IN $valid_vals
            RETURN ss.support_id AS id, ss.construct_risk AS val
        """, valid_vals=list(VALID_CONSTRUCT_RISK))
        issues = [f"SupportStrategy '{r['id']}' has invalid construct_risk '{r['val']}'" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("construct_risk values", status, total, issues))

    def check_intensity_default_values(self):
        """AccessRequirement.intensity_default must be one of: low, medium, high."""
        total = self.scalar("MATCH (ar:AccessRequirement) RETURN count(ar)") or 0
        if total == 0:
            self.add(ValidationResult("intensity_default values", "PASS", 0,
                                      ["No AccessRequirement nodes — import pending"]))
            return
        records = self.run("""
            MATCH (ar:AccessRequirement)
            WHERE NOT ar.intensity_default IN $valid_vals
            RETURN ar.access_req_id AS id, ar.intensity_default AS val
        """, valid_vals=list(VALID_INTENSITY))
        issues = [f"AccessRequirement '{r['id']}' has invalid intensity_default '{r['val']}'" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("intensity_default values", status, total, issues))

    def check_has_access_requirement_level_values(self):
        """HAS_ACCESS_REQUIREMENT.level must be one of: low, medium, high."""
        total = self.scalar("MATCH ()-[r:HAS_ACCESS_REQUIREMENT]->() RETURN count(r)") or 0
        if total == 0:
            self.add(ValidationResult("HAS_ACCESS_REQUIREMENT level values", "PASS", 0,
                                      ["No HAS_ACCESS_REQUIREMENT relationships — import pending"]))
            return
        records = self.run("""
            MATCH (c:Concept)-[r:HAS_ACCESS_REQUIREMENT]->(ar:AccessRequirement)
            WHERE NOT r.level IN $valid_vals
            RETURN c.concept_id AS cid, ar.access_req_id AS arid, r.level AS val
            LIMIT 20
        """, valid_vals=list(VALID_ACCESS_LEVELS))
        issues = [f"HAS_ACCESS_REQUIREMENT {r['cid']} -> {r['arid']} has invalid level '{r['val']}'" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("HAS_ACCESS_REQUIREMENT level values", status, total, issues))

    # =========================================================================
    # 3. Relationship integrity
    # =========================================================================

    def check_strategy_mitigates_coverage(self):
        """Every non-specialist SupportStrategy must mitigate at least 1 AccessRequirement.
        Specialist strategies (e.g. SENCO review flag) may have zero MITIGATES — they are
        escalation mechanisms, not direct mitigations."""
        total = self.scalar("MATCH (ss:SupportStrategy) RETURN count(ss)") or 0
        if total == 0:
            self.add(ValidationResult("SupportStrategy MITIGATES coverage", "PASS", 0,
                                      ["No SupportStrategy nodes — import pending"]))
            return
        # Specialist strategies with no MITIGATES are WARN, non-specialist are FAIL
        records = self.run("""
            MATCH (ss:SupportStrategy)
            WHERE NOT (ss)-[:MITIGATES]->(:AccessRequirement)
            RETURN ss.support_id AS id, ss.tier AS tier
        """)
        issues = []
        has_fail = False
        for r in records:
            if r["tier"] == "specialist":
                issues.append(f"SupportStrategy '{r['id']}' (specialist) has no MITIGATES — OK for escalation strategies")
            else:
                issues.append(f"SupportStrategy '{r['id']}' ({r['tier']}) has no MITIGATES relationship")
                has_fail = True
        status = "FAIL" if has_fail else ("WARN" if issues else "PASS")
        self.add(ValidationResult("SupportStrategy MITIGATES coverage", status, total, issues))

    def check_access_requirement_tagged_as(self):
        """Every AccessRequirement should be TAGGED_AS at least 1 NeedArea."""
        total = self.scalar("MATCH (ar:AccessRequirement) RETURN count(ar)") or 0
        if total == 0:
            self.add(ValidationResult("AccessRequirement TAGGED_AS coverage", "PASS", 0,
                                      ["No AccessRequirement nodes — import pending"]))
            return
        records = self.run("""
            MATCH (ar:AccessRequirement)
            WHERE NOT (ar)-[:TAGGED_AS]->(:NeedArea)
            RETURN ar.access_req_id AS id
        """)
        issues = [f"AccessRequirement '{r['id']}' has no TAGGED_AS relationship" for r in records]
        status = "WARN" if issues else "PASS"
        self.add(ValidationResult("AccessRequirement TAGGED_AS coverage", status, total, issues))

    def check_concept_link_integrity(self):
        """Every HAS_ACCESS_REQUIREMENT target must exist as an AccessRequirement node."""
        total = self.scalar("MATCH ()-[r:HAS_ACCESS_REQUIREMENT]->() RETURN count(r)") or 0
        if total == 0:
            self.add(ValidationResult("HAS_ACCESS_REQUIREMENT integrity", "PASS", 0,
                                      ["No HAS_ACCESS_REQUIREMENT relationships — import pending"]))
            return
        # Check that every target is actually an AccessRequirement
        records = self.run("""
            MATCH (c:Concept)-[r:HAS_ACCESS_REQUIREMENT]->(ar)
            WHERE NOT ar:AccessRequirement
            RETURN c.concept_id AS cid
            LIMIT 20
        """)
        issues = [f"HAS_ACCESS_REQUIREMENT from {r['cid']} targets non-AccessRequirement node" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("HAS_ACCESS_REQUIREMENT integrity", status, total, issues))

    def check_concept_link_source_exists(self):
        """Every HAS_ACCESS_REQUIREMENT source must exist as a Concept node."""
        total = self.scalar("MATCH ()-[r:HAS_ACCESS_REQUIREMENT]->() RETURN count(r)") or 0
        if total == 0:
            self.add(ValidationResult("HAS_ACCESS_REQUIREMENT source integrity", "PASS", 0,
                                      ["No HAS_ACCESS_REQUIREMENT relationships — import pending"]))
            return
        records = self.run("""
            MATCH (n)-[r:HAS_ACCESS_REQUIREMENT]->(ar:AccessRequirement)
            WHERE NOT n:Concept
            RETURN labels(n)[0] AS label
            LIMIT 20
        """)
        issues = [f"HAS_ACCESS_REQUIREMENT from non-Concept node ({r['label']})" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("HAS_ACCESS_REQUIREMENT source integrity", status, total, issues))

    def check_can_apply_integrity(self):
        """CAN_APPLY relationships must connect VehicleTemplate -> SupportStrategy."""
        total = self.scalar("MATCH ()-[r:CAN_APPLY]->() RETURN count(r)") or 0
        if total == 0:
            self.add(ValidationResult("CAN_APPLY integrity", "PASS", 0,
                                      ["No CAN_APPLY relationships — import pending"]))
            return
        records = self.run("""
            MATCH (vt)-[r:CAN_APPLY]->(ss)
            WHERE NOT vt:VehicleTemplate OR NOT ss:SupportStrategy
            RETURN count(r) AS bad
        """)
        bad = records[0]["bad"] if records else 0
        issues = [f"{bad} CAN_APPLY relationships connect wrong node types"] if bad > 0 else []
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("CAN_APPLY integrity", status, total, issues))

    def check_enables_integrity(self):
        """ENABLES relationships must connect InteractionType -> SupportStrategy."""
        total = self.scalar("MATCH ()-[r:ENABLES]->() RETURN count(r)") or 0
        if total == 0:
            self.add(ValidationResult("ENABLES integrity", "PASS", 0,
                                      ["No ENABLES relationships — import pending"]))
            return
        records = self.run("""
            MATCH (it)-[r:ENABLES]->(ss)
            WHERE NOT it:InteractionType OR NOT ss:SupportStrategy
            RETURN count(r) AS bad
        """)
        bad = records[0]["bad"] if records else 0
        issues = [f"{bad} ENABLES relationships connect wrong node types"] if bad > 0 else []
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("ENABLES integrity", status, total, issues))

    def check_supported_by_integrity(self):
        """SUPPORTED_BY relationships must connect TeachingRequirement -> SupportStrategy."""
        total = self.scalar("MATCH ()-[r:SUPPORTED_BY]->() RETURN count(r)") or 0
        if total == 0:
            self.add(ValidationResult("SUPPORTED_BY integrity", "PASS", 0,
                                      ["No SUPPORTED_BY relationships — import pending"]))
            return
        records = self.run("""
            MATCH (tr)-[r:SUPPORTED_BY]->(ss)
            WHERE NOT tr:TeachingRequirement OR NOT ss:SupportStrategy
            RETURN count(r) AS bad
        """)
        bad = records[0]["bad"] if records else 0
        issues = [f"{bad} SUPPORTED_BY relationships connect wrong node types"] if bad > 0 else []
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("SUPPORTED_BY integrity", status, total, issues))

    # =========================================================================
    # 4. Safety rules
    # =========================================================================

    def check_no_diagnosis_labels(self):
        """No SEND Support node should contain diagnosis terms in its ID or name.
        Checks across all three SEND display categories."""
        send_categories = ['SEND Need Area', 'Access Requirement', 'Support Strategy']
        total = self.scalar("""
            MATCH (n) WHERE n.display_category IN $cats
            RETURN count(n)
        """, cats=send_categories) or 0
        if total == 0:
            self.add(ValidationResult("No diagnosis labels in SEND nodes", "PASS", 0,
                                      ["No SEND Support nodes — import pending"]))
            return

        issues = []
        records = self.run("""
            MATCH (n) WHERE n.display_category IN $cats
            RETURN coalesce(n.need_area_id, n.access_req_id, n.support_id) AS id,
                   n.name AS name,
                   labels(n)[0] AS label
        """, cats=send_categories)
        for r in records:
            node_id = (r["id"] or "").lower()
            node_name = (r["name"] or "").lower()
            for term in DIAGNOSIS_TERMS:
                if term in node_id:
                    issues.append(f"{r['label']} '{r['id']}' contains diagnosis term '{term}' in ID")
                if term in node_name:
                    issues.append(f"{r['label']} '{r['name']}' contains diagnosis term '{term}' in name")

        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("No diagnosis labels in SEND nodes", status, total, issues))

    def check_high_risk_not_default(self):
        """No SupportStrategy with construct_risk=high should be default=true on any CAN_APPLY."""
        total = self.scalar("""
            MATCH (ss:SupportStrategy {construct_risk: 'high'})
            RETURN count(ss)
        """) or 0
        if total == 0:
            self.add(ValidationResult("High construct_risk not default", "PASS", 0,
                                      ["No high construct_risk strategies"]))
            return

        records = self.run("""
            MATCH (vt:VehicleTemplate)-[r:CAN_APPLY {default: true}]->(ss:SupportStrategy {construct_risk: 'high'})
            RETURN vt.template_id AS vt_id, ss.support_id AS ss_id
        """)
        issues = [f"CAN_APPLY from {r['vt_id']} to high-risk strategy {r['ss_id']} is marked default=true" for r in records]
        status = "FAIL" if issues else "PASS"
        self.add(ValidationResult("High construct_risk not default", status, total, issues))

    # =========================================================================
    # 5. Coverage reporting
    # =========================================================================

    def check_concept_access_coverage_by_subject(self):
        """Report concepts with HAS_ACCESS_REQUIREMENT by subject prefix."""
        total = self.scalar("MATCH ()-[r:HAS_ACCESS_REQUIREMENT]->() RETURN count(r)") or 0
        if total == 0:
            self.add(ValidationResult("Concept access coverage by subject", "PASS", 0,
                                      ["No HAS_ACCESS_REQUIREMENT relationships — import pending"]))
            return

        records = self.run("""
            MATCH (c:Concept)-[r:HAS_ACCESS_REQUIREMENT]->(ar:AccessRequirement)
            WITH substring(c.concept_id, 0, 2) AS prefix, count(DISTINCT c) AS concepts, count(r) AS rels
            RETURN prefix, concepts, rels
            ORDER BY concepts DESC
        """)
        issues = [f"  {r['prefix']}: {r['concepts']} concepts, {r['rels']} links" for r in records]
        issues.insert(0, f"Total: {total} HAS_ACCESS_REQUIREMENT relationships")
        self.add(ValidationResult("Concept access coverage by subject", "PASS", total, issues))

    def check_concept_access_coverage_by_key_stage(self):
        """Report concepts with HAS_ACCESS_REQUIREMENT by key stage."""
        total = self.scalar("MATCH ()-[r:HAS_ACCESS_REQUIREMENT]->() RETURN count(r)") or 0
        if total == 0:
            self.add(ValidationResult("Concept access coverage by KS", "PASS", 0,
                                      ["No HAS_ACCESS_REQUIREMENT relationships — import pending"]))
            return

        records = self.run("""
            MATCH (c:Concept)-[r:HAS_ACCESS_REQUIREMENT]->(ar:AccessRequirement)
            MATCH (d:Domain)-[:CONTAINS]->(:Objective)-[:TEACHES]->(c)
            MATCH (p:Programme)-[:HAS_DOMAIN]->(d)
            WITH p.key_stage AS ks, count(DISTINCT c) AS concepts, count(r) AS rels
            RETURN ks, concepts, rels
            ORDER BY ks
        """)
        issues = [f"  {r['ks']}: {r['concepts']} concepts, {r['rels']} links" for r in records]
        self.add(ValidationResult("Concept access coverage by KS", "PASS", total, issues))

    def check_strategy_tier_distribution(self):
        """Count SupportStrategy nodes by tier."""
        total = self.scalar("MATCH (ss:SupportStrategy) RETURN count(ss)") or 0
        if total == 0:
            self.add(ValidationResult("SupportStrategy tier distribution", "PASS", 0,
                                      ["No SupportStrategy nodes — import pending"]))
            return

        records = self.run("""
            MATCH (ss:SupportStrategy)
            RETURN ss.tier AS tier, count(ss) AS cnt
            ORDER BY cnt DESC
        """)
        issues = [f"  {r['tier']}: {r['cnt']}" for r in records]
        self.add(ValidationResult("SupportStrategy tier distribution", "PASS", total, issues))

    def check_access_requirement_category_distribution(self):
        """Count AccessRequirement nodes by category."""
        total = self.scalar("MATCH (ar:AccessRequirement) RETURN count(ar)") or 0
        if total == 0:
            self.add(ValidationResult("AccessRequirement category distribution", "PASS", 0,
                                      ["No AccessRequirement nodes — import pending"]))
            return

        records = self.run("""
            MATCH (ar:AccessRequirement)
            RETURN ar.category AS category, count(ar) AS cnt
            ORDER BY cnt DESC
        """)
        issues = [f"  {r['category']}: {r['cnt']}" for r in records]
        self.add(ValidationResult("AccessRequirement category distribution", "PASS", total, issues))

    # =========================================================================
    # Run all checks
    # =========================================================================

    def run_all(self):
        checks = [
            # 1. Schema completeness
            self.check_need_area_completeness,
            self.check_access_requirement_completeness,
            self.check_support_strategy_completeness,
            # 2. Enum validity
            self.check_tier_values,
            self.check_construct_risk_values,
            self.check_intensity_default_values,
            self.check_has_access_requirement_level_values,
            # 3. Relationship integrity
            self.check_strategy_mitigates_coverage,
            self.check_access_requirement_tagged_as,
            self.check_concept_link_integrity,
            self.check_concept_link_source_exists,
            self.check_can_apply_integrity,
            self.check_enables_integrity,
            self.check_supported_by_integrity,
            # 4. Safety rules
            self.check_no_diagnosis_labels,
            self.check_high_risk_not_default,
            # 5. Coverage reporting
            self.check_concept_access_coverage_by_subject,
            self.check_concept_access_coverage_by_key_stage,
            self.check_strategy_tier_distribution,
            self.check_access_requirement_category_distribution,
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
        print("SEND SUPPORT LAYER — VALIDATION REPORT")
        print("=" * 60)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        check_num = 1
        for r in self.results:
            count_str = f"{r.count} checked" if r.count and r.count > 0 else "0 checked"
            print(f"  {check_num:2d}. [{r.status}] {r.label:<45} {count_str}")
            check_num += 1

        print()
        print(f"SUMMARY: {total} checks | {n_pass} PASS | {n_warn} WARN | {n_fail} FAIL")
        print("=" * 60)

        if self.all_warnings:
            print("\n[DETAILS]")
            for w in self.all_warnings[:50]:
                print(f"  {w}")
            if len(self.all_warnings) > 50:
                print(f"  ... and {len(self.all_warnings) - 50} more")
            print("=" * 60)

        return n_fail


def main():
    print("SEND Support Layer — Validator")
    print(f"Connecting to Neo4j at {NEO4J_URI}...")

    validator = SendSupportValidator(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    try:
        validator.run_all()
        n_fail = validator.report()
        sys.exit(0 if n_fail == 0 else 1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        validator.close()


if __name__ == "__main__":
    main()

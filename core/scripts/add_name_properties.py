#!/usr/bin/env python3
"""
Add standard 'name' property to all nodes for Neo4j Browser visualization.

Neo4j Browser looks for a 'name' property to display nodes. Our nodes use
type-specific properties (concept_name, domain_name, etc.), which makes
visualization confusing. This script adds a 'name' property to all nodes.
"""

from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

def add_name_properties(driver):
    """Add 'name' property to nodes that don't have it"""

    mappings = [
        # UK Curriculum nodes
        ("Concept", "concept_name"),
        ("Domain", "domain_name"),
        ("Objective", "objective_id"),  # No name field, use ID
        ("Topic", "topic_name"),

        # CASE nodes
        ("Practice", "practice_name"),
        ("CoreIdea", "title"),
        ("PerformanceExpectation", "code"),  # Use code as name (e.g. K-PS2-1)
        ("Dimension", "dimension_name"),
        ("Framework", "title"),
        ("CrosscuttingConcept", "concept_name"),
        ("GradeBand", "grade_band_code"),

        # Epistemic skills
        ("WorkingScientifically", "skill_name"),
        ("ReadingSkill", "skill_name"),
        ("MathematicalReasoning", "skill_name"),
        ("GeographicalSkill", "skill_name"),
        ("HistoricalThinking", "skill_name"),
        ("ComputationalThinking", "skill_name"),

        # Assessment
        ("ContentDomainCode", "test_domain_code"),
        ("TestPaper", "paper_code"),
        ("TestFramework", "framework_id"),

        # Already have 'name': Subject, Programme, Year, KeyStage
    ]

    with driver.session() as session:
        print("Adding 'name' properties to nodes...\n")

        for node_label, source_property in mappings:
            try:
                result = session.run(f"""
                    MATCH (n:{node_label})
                    WHERE n.name IS NULL AND n.{source_property} IS NOT NULL
                    SET n.name = n.{source_property}
                    RETURN count(n) as updated
                """)
                updated = result.single()['updated']
                if updated > 0:
                    print(f"  ✓ {node_label:30} → {updated:4} nodes updated (from {source_property})")
            except Exception as e:
                print(f"  ✗ {node_label:30} → Error: {e}")

        print("\n✅ Name properties added!")

        # Verify
        print("\n--- VERIFICATION ---")
        result = session.run("""
            MATCH (n)
            WHERE n.name IS NULL
            RETURN labels(n) as labels, count(n) as count
            ORDER BY count DESC
            LIMIT 10
        """)
        nodes_without_name = 0
        for record in result:
            nodes_without_name += record['count']
            print(f"  {record['labels']}: {record['count']} nodes without 'name'")

        if nodes_without_name == 0:
            print("  ✅ All nodes now have 'name' property!")
        else:
            print(f"  ⚠️  {nodes_without_name} nodes still missing 'name'")

def main():
    print("="*60)
    print("Add 'name' Properties for Neo4j Browser Visualization")
    print("="*60)
    print(f"\nConnecting to {NEO4J_URI}...")

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    try:
        add_name_properties(driver)
    finally:
        driver.close()

    print("\n" + "="*60)
    print("✅ Migration complete!")
    print("="*60)

if __name__ == "__main__":
    main()

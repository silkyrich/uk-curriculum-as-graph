#!/usr/bin/env python3
"""
Create Neo4j schema for UK Curriculum Knowledge Graph
Applies constraints and indexes from neo4j_schema.cypher
"""

from neo4j import GraphDatabase
import sys

# Neo4j connection details
NEO4J_URI = "neo4j://127.0.0.1:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password123"

def create_schema(driver):
    """Apply schema constraints and indexes to Neo4j database"""

    # Constraints
    constraints = [
        "CREATE CONSTRAINT curriculum_id_unique IF NOT EXISTS FOR (c:Curriculum) REQUIRE c.curriculum_id IS UNIQUE",
        "CREATE CONSTRAINT key_stage_id_unique IF NOT EXISTS FOR (ks:KeyStage) REQUIRE ks.key_stage_id IS UNIQUE",
        "CREATE CONSTRAINT year_id_unique IF NOT EXISTS FOR (y:Year) REQUIRE y.year_id IS UNIQUE",
        "CREATE CONSTRAINT subject_id_unique IF NOT EXISTS FOR (s:Subject) REQUIRE s.subject_id IS UNIQUE",
        "CREATE CONSTRAINT domain_id_unique IF NOT EXISTS FOR (d:Domain) REQUIRE d.domain_id IS UNIQUE",
        "CREATE CONSTRAINT objective_id_unique IF NOT EXISTS FOR (o:Objective) REQUIRE o.objective_id IS UNIQUE",
        "CREATE CONSTRAINT concept_id_unique IF NOT EXISTS FOR (c:Concept) REQUIRE c.concept_id IS UNIQUE",
    ]

    # Indexes
    indexes = [
        "CREATE INDEX concept_type_idx IF NOT EXISTS FOR (c:Concept) ON (c.concept_type)",
        "CREATE INDEX concept_complexity_idx IF NOT EXISTS FOR (c:Concept) ON (c.complexity_level)",
        "CREATE INDEX concept_cross_cutting_idx IF NOT EXISTS FOR (c:Concept) ON (c.is_cross_cutting)",
        "CREATE INDEX domain_cross_cutting_idx IF NOT EXISTS FOR (d:Domain) ON (d.is_cross_cutting)",
        "CREATE INDEX subject_name_idx IF NOT EXISTS FOR (s:Subject) ON (s.name)",
        "CREATE INDEX year_number_idx IF NOT EXISTS FOR (y:Year) ON (y.year_number)",
    ]

    print("Creating constraints...")
    with driver.session() as session:
        for constraint in constraints:
            try:
                session.run(constraint)
                print(f"✓ {constraint.split('CREATE CONSTRAINT ')[1].split(' IF')[0]}")
            except Exception as e:
                print(f"✗ Error creating constraint: {e}")

    print("\nCreating indexes...")
    with driver.session() as session:
        for index in indexes:
            try:
                session.run(index)
                print(f"✓ {index.split('CREATE INDEX ')[1].split(' IF')[0]}")
            except Exception as e:
                print(f"✗ Error creating index: {e}")

    print("\n✅ Schema creation complete!")

def verify_connection(driver):
    """Verify connection to Neo4j and print database info"""
    try:
        with driver.session() as session:
            result = session.run("CALL dbms.components() YIELD name, versions, edition RETURN name, versions[0] as version, edition")
            record = result.single()
            print(f"\n✅ Connected to Neo4j:")
            print(f"   Name: {record['name']}")
            print(f"   Version: {record['version']}")
            print(f"   Edition: {record['edition']}")
            return True
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        return False

def show_schema_info(driver):
    """Display current schema information"""
    print("\n" + "="*60)
    print("CURRENT SCHEMA INFORMATION")
    print("="*60)

    with driver.session() as session:
        # Show constraints
        print("\nConstraints:")
        result = session.run("SHOW CONSTRAINTS")
        for record in result:
            print(f"  • {record['name']}: {record['labelsOrTypes']} ({record['properties']})")

        # Show indexes
        print("\nIndexes:")
        result = session.run("SHOW INDEXES")
        for record in result:
            if record['type'] != 'LOOKUP':  # Skip internal lookup indexes
                print(f"  • {record['name']}: {record['labelsOrTypes']} ({record['properties']})")

        # Show node counts
        print("\nNode counts:")
        result = session.run("MATCH (n) RETURN labels(n) as labels, count(n) as count ORDER BY count DESC")
        total = 0
        for record in result:
            count = record['count']
            total += count
            print(f"  • {record['labels']}: {count}")
        print(f"  TOTAL: {total}")

        # Show relationship counts
        print("\nRelationship counts:")
        result = session.run("MATCH ()-[r]->() RETURN type(r) as type, count(r) as count ORDER BY count DESC")
        total = 0
        for record in result:
            count = record['count']
            total += count
            print(f"  • {record['type']}: {count}")
        print(f"  TOTAL: {total}")

def main():
    """Main execution"""
    print("="*60)
    print("UK Curriculum Knowledge Graph - Schema Creator")
    print("="*60)

    # Connect to Neo4j
    print(f"\nConnecting to Neo4j at {NEO4J_URI}...")
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    # Verify connection
    if not verify_connection(driver):
        print("\n❌ Cannot proceed without database connection.")
        sys.exit(1)

    # Create schema
    try:
        create_schema(driver)
    except Exception as e:
        print(f"\n❌ Schema creation failed: {e}")
        sys.exit(1)

    # Show schema information
    show_schema_info(driver)

    # Close connection
    driver.close()
    print("\n✅ Schema setup complete and verified!")

if __name__ == "__main__":
    main()

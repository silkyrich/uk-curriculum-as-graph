#!/usr/bin/env python3
"""
Create Neo4j schema for UK Curriculum Knowledge Graph
Applies constraints and indexes from neo4j_schema.cypher
"""

from neo4j import GraphDatabase
import sys
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

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
        # Epistemic skills node types (v3.2)
        "CREATE CONSTRAINT working_scientifically_skill_id_unique IF NOT EXISTS FOR (ws:WorkingScientifically) REQUIRE ws.skill_id IS UNIQUE",
        "CREATE CONSTRAINT geographical_skill_skill_id_unique IF NOT EXISTS FOR (gs:GeographicalSkill) REQUIRE gs.skill_id IS UNIQUE",
        "CREATE CONSTRAINT reading_skill_skill_id_unique IF NOT EXISTS FOR (rs:ReadingSkill) REQUIRE rs.skill_id IS UNIQUE",
        "CREATE CONSTRAINT mathematical_reasoning_skill_id_unique IF NOT EXISTS FOR (mr:MathematicalReasoning) REQUIRE mr.skill_id IS UNIQUE",
        "CREATE CONSTRAINT historical_thinking_skill_id_unique IF NOT EXISTS FOR (ht:HistoricalThinking) REQUIRE ht.skill_id IS UNIQUE",
        "CREATE CONSTRAINT computational_thinking_skill_id_unique IF NOT EXISTS FOR (ct:ComputationalThinking) REQUIRE ct.skill_id IS UNIQUE",
        # Topic nodes (v3.3)
        "CREATE CONSTRAINT topic_id_unique IF NOT EXISTS FOR (t:Topic) REQUIRE t.topic_id IS UNIQUE",
        # Oak National Academy content nodes (v3.4)
        "CREATE CONSTRAINT oak_unit_slug_unique IF NOT EXISTS FOR (u:OakUnit) REQUIRE u.oak_unit_slug IS UNIQUE",
        "CREATE CONSTRAINT oak_lesson_slug_unique IF NOT EXISTS FOR (l:OakLesson) REQUIRE l.oak_lesson_slug IS UNIQUE",
        # CASE Standards layer (v3.5 restructured)
        "CREATE CONSTRAINT case_framework_id_unique IF NOT EXISTS FOR (f:Framework) REQUIRE f.framework_id IS UNIQUE",
        "CREATE CONSTRAINT case_dimension_id_unique IF NOT EXISTS FOR (d:Dimension) REQUIRE d.dimension_id IS UNIQUE",
        "CREATE CONSTRAINT case_practice_id_unique IF NOT EXISTS FOR (p:Practice) REQUIRE p.practice_id IS UNIQUE",
        "CREATE CONSTRAINT case_core_idea_id_unique IF NOT EXISTS FOR (c:CoreIdea) REQUIRE c.core_idea_id IS UNIQUE",
        "CREATE CONSTRAINT case_pe_id_unique IF NOT EXISTS FOR (pe:PerformanceExpectation) REQUIRE pe.pe_id IS UNIQUE",
        "CREATE CONSTRAINT case_math_practice_id_unique IF NOT EXISTS FOR (mp:MathPractice) REQUIRE mp.practice_id IS UNIQUE",
        # Learner Profiles layer (v3.6)
        "CREATE CONSTRAINT interaction_type_id_unique IF NOT EXISTS FOR (i:InteractionType) REQUIRE i.interaction_id IS UNIQUE",
        "CREATE CONSTRAINT content_guideline_year_unique IF NOT EXISTS FOR (c:ContentGuideline) REQUIRE c.year_code IS UNIQUE",
        "CREATE CONSTRAINT pedagogy_profile_year_unique IF NOT EXISTS FOR (p:PedagogyProfile) REQUIRE p.year_code IS UNIQUE",
        "CREATE CONSTRAINT feedback_profile_year_unique IF NOT EXISTS FOR (f:FeedbackProfile) REQUIRE f.year_code IS UNIQUE",
        "CREATE CONSTRAINT pedagogy_technique_id_unique IF NOT EXISTS FOR (pt:PedagogyTechnique) REQUIRE pt.technique_id IS UNIQUE",
        # Concept Grouping layer (v3.7)
        "CREATE CONSTRAINT concept_cluster_id_unique IF NOT EXISTS FOR (cc:ConceptCluster) REQUIRE cc.cluster_id IS UNIQUE",
        # Content Vehicles layer (v3.8)
        "CREATE CONSTRAINT content_vehicle_id_unique IF NOT EXISTS FOR (cv:ContentVehicle) REQUIRE cv.vehicle_id IS UNIQUE",
        # DifficultyLevel layer (v3.9)
        "CREATE CONSTRAINT difficulty_level_id_unique IF NOT EXISTS FOR (dl:DifficultyLevel) REQUIRE dl.level_id IS UNIQUE",
        # Topic Suggestions layer (v4.0) — 9 typed labels + VehicleTemplate
        "CREATE CONSTRAINT vehicle_template_id_unique IF NOT EXISTS FOR (vt:VehicleTemplate) REQUIRE vt.template_id IS UNIQUE",
        "CREATE CONSTRAINT history_ts_id_unique IF NOT EXISTS FOR (ts:HistoryTopicSuggestion) REQUIRE ts.suggestion_id IS UNIQUE",
        "CREATE CONSTRAINT geography_ts_id_unique IF NOT EXISTS FOR (ts:GeographyTopicSuggestion) REQUIRE ts.suggestion_id IS UNIQUE",
        "CREATE CONSTRAINT science_ts_id_unique IF NOT EXISTS FOR (ts:ScienceTopicSuggestion) REQUIRE ts.suggestion_id IS UNIQUE",
        "CREATE CONSTRAINT english_ts_id_unique IF NOT EXISTS FOR (ts:EnglishTopicSuggestion) REQUIRE ts.suggestion_id IS UNIQUE",
        "CREATE CONSTRAINT maths_ts_id_unique IF NOT EXISTS FOR (ts:MathsTopicSuggestion) REQUIRE ts.suggestion_id IS UNIQUE",
        "CREATE CONSTRAINT art_ts_id_unique IF NOT EXISTS FOR (ts:ArtTopicSuggestion) REQUIRE ts.suggestion_id IS UNIQUE",
        "CREATE CONSTRAINT music_ts_id_unique IF NOT EXISTS FOR (ts:MusicTopicSuggestion) REQUIRE ts.suggestion_id IS UNIQUE",
        "CREATE CONSTRAINT dt_ts_id_unique IF NOT EXISTS FOR (ts:DTTopicSuggestion) REQUIRE ts.suggestion_id IS UNIQUE",
        "CREATE CONSTRAINT topic_suggestion_id_unique IF NOT EXISTS FOR (ts:TopicSuggestion) REQUIRE ts.suggestion_id IS UNIQUE",
    ]

    # Indexes
    indexes = [
        "CREATE INDEX concept_type_idx IF NOT EXISTS FOR (c:Concept) ON (c.concept_type)",
        # (complexity_level index removed — property deprecated in v3.9)
        "CREATE INDEX concept_cross_cutting_idx IF NOT EXISTS FOR (c:Concept) ON (c.is_cross_cutting)",
        "CREATE INDEX domain_cross_cutting_idx IF NOT EXISTS FOR (d:Domain) ON (d.is_cross_cutting)",
        "CREATE INDEX subject_name_idx IF NOT EXISTS FOR (s:Subject) ON (s.name)",
        "CREATE INDEX year_number_idx IF NOT EXISTS FOR (y:Year) ON (y.year_number)",
        # Epistemic skills indexes (v3.2)
        "CREATE INDEX working_scientifically_key_stage_idx IF NOT EXISTS FOR (ws:WorkingScientifically) ON (ws.key_stage)",
        "CREATE INDEX geographical_skill_key_stage_idx IF NOT EXISTS FOR (gs:GeographicalSkill) ON (gs.key_stage)",
        "CREATE INDEX reading_skill_test_code_idx IF NOT EXISTS FOR (rs:ReadingSkill) ON (rs.test_code)",
        "CREATE INDEX mathematical_reasoning_paper_idx IF NOT EXISTS FOR (mr:MathematicalReasoning) ON (mr.paper)",
        "CREATE INDEX computational_thinking_key_stage_idx IF NOT EXISTS FOR (ct:ComputationalThinking) ON (ct.key_stage)",
        # Oak content indexes (v3.4)
        "CREATE INDEX oak_unit_subject_idx IF NOT EXISTS FOR (u:OakUnit) ON (u.subject)",
        "CREATE INDEX oak_unit_key_stage_idx IF NOT EXISTS FOR (u:OakUnit) ON (u.key_stage)",
        "CREATE INDEX oak_lesson_subject_idx IF NOT EXISTS FOR (l:OakLesson) ON (l.subject)",
        # CASE Standards indexes (v3.5 restructured)
        "CREATE INDEX case_framework_model_type_idx IF NOT EXISTS FOR (f:Framework) ON (f.model_type)",
        "CREATE INDEX case_dimension_type_idx IF NOT EXISTS FOR (d:Dimension) ON (d.dimension_type)",
        "CREATE INDEX case_practice_number_idx IF NOT EXISTS FOR (p:Practice) ON (p.practice_number)",
        "CREATE INDEX case_pe_code_idx IF NOT EXISTS FOR (pe:PerformanceExpectation) ON (pe.code)",
        # Learner Profiles indexes (v3.6)
        "CREATE INDEX interaction_type_category_idx IF NOT EXISTS FOR (i:InteractionType) ON (i.category)",
        "CREATE INDEX interaction_type_input_method_idx IF NOT EXISTS FOR (i:InteractionType) ON (i.input_method)",
        "CREATE INDEX content_guideline_tts_required_idx IF NOT EXISTS FOR (c:ContentGuideline) ON (c.tts_required)",
        "CREATE INDEX pedagogy_profile_scaffolding_idx IF NOT EXISTS FOR (p:PedagogyProfile) ON (p.scaffolding_level)",
        "CREATE INDEX pedagogy_technique_min_year_idx IF NOT EXISTS FOR (pt:PedagogyTechnique) ON (pt.min_year_appropriate)",
        # Concept Grouping indexes (v3.7)
        "CREATE INDEX concept_cluster_type_idx IF NOT EXISTS FOR (cc:ConceptCluster) ON (cc.cluster_type)",
        "CREATE INDEX concept_is_keystone_idx IF NOT EXISTS FOR (c:Concept) ON (c.is_keystone)",
        "CREATE INDEX concept_teaching_weight_idx IF NOT EXISTS FOR (c:Concept) ON (c.teaching_weight)",
        # Content Vehicles indexes (v3.8)
        "CREATE INDEX content_vehicle_type_idx IF NOT EXISTS FOR (cv:ContentVehicle) ON (cv.vehicle_type)",
        "CREATE INDEX content_vehicle_subject_idx IF NOT EXISTS FOR (cv:ContentVehicle) ON (cv.subject)",
        "CREATE INDEX content_vehicle_ks_idx IF NOT EXISTS FOR (cv:ContentVehicle) ON (cv.key_stage)",
        # DifficultyLevel indexes (v3.9)
        "CREATE INDEX difficulty_level_number_idx IF NOT EXISTS FOR (dl:DifficultyLevel) ON (dl.level_number)",
        "CREATE INDEX difficulty_level_label_idx IF NOT EXISTS FOR (dl:DifficultyLevel) ON (dl.label)",
        # Topic Suggestions indexes (v4.0)
        "CREATE INDEX vehicle_template_type_idx IF NOT EXISTS FOR (vt:VehicleTemplate) ON (vt.template_type)",
        "CREATE INDEX history_ts_subject_idx IF NOT EXISTS FOR (ts:HistoryTopicSuggestion) ON (ts.subject)",
        "CREATE INDEX history_ts_ks_idx IF NOT EXISTS FOR (ts:HistoryTopicSuggestion) ON (ts.key_stage)",
        "CREATE INDEX geography_ts_subject_idx IF NOT EXISTS FOR (ts:GeographyTopicSuggestion) ON (ts.subject)",
        "CREATE INDEX geography_ts_ks_idx IF NOT EXISTS FOR (ts:GeographyTopicSuggestion) ON (ts.key_stage)",
        "CREATE INDEX science_ts_subject_idx IF NOT EXISTS FOR (ts:ScienceTopicSuggestion) ON (ts.subject)",
        "CREATE INDEX science_ts_ks_idx IF NOT EXISTS FOR (ts:ScienceTopicSuggestion) ON (ts.key_stage)",
        "CREATE INDEX english_ts_subject_idx IF NOT EXISTS FOR (ts:EnglishTopicSuggestion) ON (ts.subject)",
        "CREATE INDEX english_ts_ks_idx IF NOT EXISTS FOR (ts:EnglishTopicSuggestion) ON (ts.key_stage)",
        "CREATE INDEX maths_ts_ks_idx IF NOT EXISTS FOR (ts:MathsTopicSuggestion) ON (ts.key_stage)",
        "CREATE INDEX art_ts_ks_idx IF NOT EXISTS FOR (ts:ArtTopicSuggestion) ON (ts.key_stage)",
        "CREATE INDEX music_ts_ks_idx IF NOT EXISTS FOR (ts:MusicTopicSuggestion) ON (ts.key_stage)",
        "CREATE INDEX dt_ts_ks_idx IF NOT EXISTS FOR (ts:DTTopicSuggestion) ON (ts.key_stage)",
        "CREATE INDEX topic_suggestion_subject_idx IF NOT EXISTS FOR (ts:TopicSuggestion) ON (ts.subject)",
        "CREATE INDEX topic_suggestion_ks_idx IF NOT EXISTS FOR (ts:TopicSuggestion) ON (ts.key_stage)",
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

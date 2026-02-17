// UK Curriculum Knowledge Graph - Neo4j Schema
// Graph Model v3.0
// Created: 2026-02-12
// Updated: 2026-02-17 - Added Programme and SourceDocument nodes

// ============================================================================
// CONSTRAINTS & INDEXES
// ============================================================================

// Curriculum
CREATE CONSTRAINT curriculum_id_unique IF NOT EXISTS
FOR (c:Curriculum) REQUIRE c.curriculum_id IS UNIQUE;

// KeyStage
CREATE CONSTRAINT key_stage_id_unique IF NOT EXISTS
FOR (ks:KeyStage) REQUIRE ks.key_stage_id IS UNIQUE;

// Year
CREATE CONSTRAINT year_id_unique IF NOT EXISTS
FOR (y:Year) REQUIRE y.year_id IS UNIQUE;

// Subject
CREATE CONSTRAINT subject_id_unique IF NOT EXISTS
FOR (s:Subject) REQUIRE s.subject_id IS UNIQUE;

// Domain
CREATE CONSTRAINT domain_id_unique IF NOT EXISTS
FOR (d:Domain) REQUIRE d.domain_id IS UNIQUE;

// Objective
CREATE CONSTRAINT objective_id_unique IF NOT EXISTS
FOR (o:Objective) REQUIRE o.objective_id IS UNIQUE;

// Concept
CREATE CONSTRAINT concept_id_unique IF NOT EXISTS
FOR (c:Concept) REQUIRE c.concept_id IS UNIQUE;

// Programme (Subject × Year instantiation)
CREATE CONSTRAINT programme_id_unique IF NOT EXISTS
FOR (p:Programme) REQUIRE p.programme_id IS UNIQUE;

// SourceDocument (traceability to gov.uk URLs)
CREATE CONSTRAINT document_id_unique IF NOT EXISTS
FOR (sd:SourceDocument) REQUIRE sd.document_id IS UNIQUE;

// Indexes for common queries
CREATE INDEX concept_type_idx IF NOT EXISTS FOR (c:Concept) ON (c.concept_type);
CREATE INDEX concept_complexity_idx IF NOT EXISTS FOR (c:Concept) ON (c.complexity_level);
CREATE INDEX concept_cross_cutting_idx IF NOT EXISTS FOR (c:Concept) ON (c.is_cross_cutting);
CREATE INDEX domain_cross_cutting_idx IF NOT EXISTS FOR (d:Domain) ON (d.is_cross_cutting);
CREATE INDEX subject_name_idx IF NOT EXISTS FOR (s:Subject) ON (s.name);
CREATE INDEX year_number_idx IF NOT EXISTS FOR (y:Year) ON (y.year_number);
CREATE INDEX programme_subject_idx IF NOT EXISTS FOR (p:Programme) ON (p.subject_name);
CREATE INDEX programme_key_stage_idx IF NOT EXISTS FOR (p:Programme) ON (p.key_stage);
CREATE INDEX source_document_subject_idx IF NOT EXISTS FOR (sd:SourceDocument) ON (sd.subject);
CREATE INDEX source_document_url_idx IF NOT EXISTS FOR (sd:SourceDocument) ON (sd.url);

// ============================================================================
// NODE LABELS & PROPERTIES
// ============================================================================

// Curriculum Node
// Properties:
// - curriculum_id: string (UNIQUE)
// - name: string
// - country: string
// - version: string
// - source_url: string
// - last_updated: date

// KeyStage Node
// Properties:
// - key_stage_id: string (UNIQUE) e.g., "KS1", "KS2", "KS3"
// - name: string
// - years: list<int> e.g., [1,2] for KS1
// - age_range: string e.g., "5-7"
// - source_url: string

// Year Node
// Properties:
// - year_id: string (UNIQUE) e.g., "Y1", "Y2"
// - year_number: int (1-9)
// - age_range: string e.g., "5-6"
// - key_stage: string e.g., "KS1"

// Subject Node
// Properties:
// - subject_id: string (UNIQUE)
// - name: string
// - description: string
// - key_stages_covered: list<string>
// - is_core_subject: boolean (true for Mathematics, English, Science)
// - statutory: boolean
// - subject_type: string ("core" or "foundation")

// Programme Node  (Subject × Year instantiation — resolves the navigation context flaw)
// Properties:
// - programme_id: string (UNIQUE) e.g., "PROG-Mathematics-Y1", "PROG-Mathematics-KS1"
// - name: string
// - subject_name: string
// - years: list<int>
// - key_stage: string
// - age_range: string
// - is_core_subject: boolean
// - structure_rating: int
// - extraction_date: date
// - source_url: string
// - publication_url: string
// - dfe_reference: string
// - curriculum_name: string

// SourceDocument Node  (traceability to gov.uk PDFs)
// Properties:
// - document_id: string (UNIQUE) e.g., "DOC-Mathematics-KS1-2"
// - title: string
// - subject: string
// - key_stages: list<string>
// - url: string (direct PDF URL)
// - publication_page: string
// - dfe_reference: string
// - published: string
// - last_updated: string
// - pages: int
// - local_file: string

// Domain Node
// Properties:
// - domain_id: string (UNIQUE)
// - domain_name: string
// - description: string
// - is_cross_cutting: boolean
// - applies_to_domains: list<string> (if cross-cutting)
// - source_section: string
// - structure_type: string ("content", "skill", "process", "mixed")

// Objective Node
// Properties:
// - objective_id: string (UNIQUE)
// - objective_text: string (verbatim from curriculum)
// - is_statutory: boolean
// - source_page: int
// - source_section: string

// Concept Node (CORE OF THE GRAPH)
// Properties:
// - concept_id: string (UNIQUE)
// - concept_name: string
// - description: string
// - concept_type: string ("knowledge", "skill", "process", "attitude", "content")
// - complexity_level: int (1-5)
// - is_cross_cutting: boolean
// - assessment_type: string ("formative", "summative", "both")
// - source_objective_id: string
// - extraction_confidence: float (0.0-1.0)
// - extraction_notes: string

// ============================================================================
// RELATIONSHIP TYPES
// ============================================================================

// Hierarchical Relationships (v3.0 model with Programme node)
// (:Curriculum)-[:HAS_KEY_STAGE]->(:KeyStage)
// (:KeyStage)-[:HAS_YEAR]->(:Year)
// (:Year)-[:HAS_PROGRAMME]->(:Programme)
// (:Programme)-[:FOR_SUBJECT]->(:Subject)
// (:Programme)-[:HAS_DOMAIN]->(:Domain)
// (:Domain)-[:CONTAINS]->(:Objective)
// (:Objective)-[:TEACHES]->(:Concept)

// Source Traceability Relationships
// (:Curriculum)-[:HAS_DOCUMENT]->(:SourceDocument)
// (:Programme)-[:SOURCED_FROM]->(:SourceDocument)
// (:Concept)-[:SOURCED_FROM]->(:SourceDocument)

// Temporal Relationships
// (:Concept)-[:APPEARS_IN_YEAR]->(:Year)
// Properties:
// - is_introduced: boolean
// - is_reinforced: boolean
// - teaching_notes: string

// Prerequisite Relationships (ENHANCED)
// (:Concept)-[:PREREQUISITE_OF]->(:Concept)
// Properties:
// - confidence: string ("explicit", "inferred", "fuzzy")
// - relationship_type: string ("logical", "developmental", "instructional", "temporal")
// - strength: float (0.0-1.0)
// - rationale: string
// - years_gap: int (optional)
// - same_domain: boolean (optional)

// Cross-Domain Relationships
// (:Domain)-[:APPLIES_TO]->(:Domain)
// Properties:
// - application_type: string ("foundational", "supportive", "integrated")
// - description: string

// Concept Relationships
// (:Concept)-[:RELATED_TO]->(:Concept)
// Properties:
// - relationship_type: string ("supports", "contrasts", "exemplifies", "generalizes")
// - description: string

// ============================================================================
// SAMPLE QUERIES
// ============================================================================

// 1. Find all prerequisites for a specific concept (recursive)
// MATCH path = (prerequisite:Concept)-[:PREREQUISITE_OF*]->(target:Concept {concept_name: "multiplication"})
// RETURN path

// 2. Find all concepts of a specific type in a subject (via Programme)
// MATCH (s:Subject {name: "Mathematics"})<-[:FOR_SUBJECT]-(p:Programme)-[:HAS_DOMAIN]->(d:Domain)-[:CONTAINS]->(o:Objective)-[:TEACHES]->(c:Concept)
// WHERE c.concept_type = "skill"
// RETURN c.concept_name, c.complexity_level, p.key_stage

// 3. Find cross-cutting concepts
// MATCH (c:Concept {is_cross_cutting: true})
// RETURN c.concept_name, c.concept_type, c.description

// 4. Find concepts by complexity level
// MATCH (c:Concept)
// WHERE c.complexity_level >= 4
// RETURN c.concept_name, c.complexity_level, c.concept_type

// 5. Find learning progression for a concept across years
// MATCH (c:Concept {concept_name: "addition"})-[:APPEARS_IN_YEAR]->(y:Year)
// RETURN y.year_number, c.concept_name, c.complexity_level
// ORDER BY y.year_number

// 6. Find strongest prerequisite chains
// MATCH (c1:Concept)-[r:PREREQUISITE_OF]->(c2:Concept)
// WHERE r.strength >= 0.9
// RETURN c1.concept_name, c2.concept_name, r.strength, r.relationship_type

// 7. Find all concepts in a domain (with year context via Programme)
// MATCH (p:Programme)-[:HAS_DOMAIN]->(d:Domain {domain_name: "Number - addition and subtraction"})-[:CONTAINS]->(o:Objective)-[:TEACHES]->(c:Concept)
// RETURN c.concept_name, c.concept_type, c.complexity_level, p.years

// 8. Find domains that apply to other domains (cross-cutting)
// MATCH (d1:Domain {is_cross_cutting: true})-[r:APPLIES_TO]->(d2:Domain)
// RETURN d1.domain_name, d2.domain_name, r.application_type

// 9. Count concepts by type for a subject (via Programme)
// MATCH (s:Subject {name: "Mathematics"})<-[:FOR_SUBJECT]-(p:Programme)-[:HAS_DOMAIN]->(d:Domain)-[:CONTAINS]->(o:Objective)-[:TEACHES]->(c:Concept)
// RETURN c.concept_type, count(c) as count
// ORDER BY count DESC

// 11. Navigate from Year to Domain (now possible via Programme)
// MATCH (y:Year {year_number: 3})-[:HAS_PROGRAMME]->(p:Programme)-[:HAS_DOMAIN]->(d:Domain)
// RETURN y.year_id, p.programme_id, d.domain_name

// 12. Find source documents for a programme
// MATCH (p:Programme {programme_id: "PROG-Mathematics-Y1"})-[:SOURCED_FROM]->(sd:SourceDocument)
// RETURN sd.title, sd.url, sd.dfe_reference

// 10. Find concepts with fuzzy prerequisites (multiple valid pathways)
// MATCH (c1:Concept)-[r:PREREQUISITE_OF]->(c2:Concept)
// WHERE r.confidence = "fuzzy"
// RETURN c1.concept_name, c2.concept_name, r.rationale

// ============================================================================
// DATA VALIDATION QUERIES
// ============================================================================

// Check for orphaned concepts (no Programme connection via Domain)
// MATCH (c:Concept)
// WHERE NOT EXISTS {
//   MATCH (p:Programme)-[:HAS_DOMAIN]->(d:Domain)-[:CONTAINS]->(o:Objective)-[:TEACHES]->(c)
// }
// RETURN c.concept_id, c.concept_name

// Check for Programmes not linked to any Year
// MATCH (p:Programme)
// WHERE NOT EXISTS {
//   MATCH (y:Year)-[:HAS_PROGRAMME]->(p)
// }
// RETURN p.programme_id, p.name

// Check for Programmes not linked to a SourceDocument
// MATCH (p:Programme)
// WHERE NOT EXISTS {
//   MATCH (p)-[:SOURCED_FROM]->(:SourceDocument)
// }
// RETURN p.programme_id, p.subject_name

// Check for circular prerequisites (should be none in well-formed curriculum)
// MATCH path = (c:Concept)-[:PREREQUISITE_OF*]->(c)
// RETURN path

// Count nodes by type
// MATCH (n) RETURN labels(n) as type, count(n) as count

// Count relationships by type
// MATCH ()-[r]->() RETURN type(r) as relationship_type, count(r) as count

// ============================================================================
// CLEANUP QUERIES (USE WITH CAUTION)
// ============================================================================

// Delete all nodes and relationships (CAUTION: This deletes everything!)
// MATCH (n) DETACH DELETE n

// Delete specific subject and all related data (v3.0 - via Programme)
// MATCH (s:Subject {name: "Mathematics"})
// OPTIONAL MATCH (s)<-[:FOR_SUBJECT]-(p:Programme)
// OPTIONAL MATCH (p)-[:HAS_DOMAIN]->(d:Domain)
// OPTIONAL MATCH (d)-[:CONTAINS]->(o:Objective)
// OPTIONAL MATCH (o)-[:TEACHES]->(c:Concept)
// DETACH DELETE s, p, d, o, c

# UK Curriculum Knowledge Graph - Model v2.0

## Overview
Enhanced model based on extraction testing across 6 subjects (Mathematics, English, Science, History, Geography, Computing). This version handles both structured subjects (Maths, Computing) and "mushy" subjects (English, Science, History) that mix skills, knowledge, and cross-cutting domains.

## Node Types

### Curriculum
```cypher
(:Curriculum {
  curriculum_id: "uk-national-curriculum",
  name: "UK National Curriculum",
  country: "England",
  version: "2014",
  source_url: string,
  last_updated: date
})
```

### KeyStage
```cypher
(:KeyStage {
  key_stage_id: string,  // "KS1", "KS2", "KS3"
  name: string,
  years: [int],  // [1,2] for KS1, [3,4,5,6] for KS2, [7,8,9] for KS3
  age_range: string,  // "5-7", "7-11", "11-14"
  source_url: string
})
```

### Year
```cypher
(:Year {
  year_id: string,  // "Y1", "Y2", etc.
  year_number: int,  // 1-9
  age_range: string,  // "5-6", "6-7", etc.
  key_stage: string  // "KS1", "KS2", "KS3"
})
```

### Subject
```cypher
(:Subject {
  subject_id: string,
  name: string,
  key_stages: [string],
  source_url: string,
  dfe_reference: string,
  published_date: date,
  last_updated: date,
  subject_type: enum["core", "foundation"]  // Core: Maths, English, Science
})
```

### Domain
```cypher
(:Domain {
  domain_id: string,
  domain_name: string,
  description: string,
  is_cross_cutting: boolean,  // NEW: true for domains like "Working Scientifically", "Spoken Language"
  applies_to_domains: [string],  // NEW: if cross-cutting, which domains does it apply to?
  source_section: string,  // Page/section reference in source document
  structure_type: enum["content", "skill", "process", "mixed"]  // NEW: what type of domain is this?
})
```

### Objective
```cypher
(:Objective {
  objective_id: string,
  objective_text: string,  // Full text from curriculum document
  is_statutory: boolean,  // true for statutory requirements, false for non-statutory guidance
  source_page: int,
  source_section: string
})
```

### Concept (ENHANCED)
```cypher
(:Concept {
  concept_id: string,
  concept_name: string,
  description: string,

  // NEW FIELDS:
  concept_type: enum["knowledge", "skill", "process", "attitude", "content"],
  // - knowledge: discrete facts (e.g., "capital cities", "photosynthesis")
  // - skill: transferable abilities (e.g., "inference", "estimation")
  // - process: procedural knowledge (e.g., "planning experiments", "editing writing")
  // - attitude: dispositions (e.g., "curiosity", "resilience")
  // - content: specific curriculum content (e.g., "Great Fire of London", "Rivers")

  complexity_level: int,  // 1-5 scale for cognitive demand
  is_cross_cutting: boolean,  // true if concept applies across multiple domains
  assessment_type: enum["formative", "summative", "both"],

  // Traceability:
  source_objective_id: string,
  extraction_confidence: float,  // 0.0-1.0
  extraction_notes: string
})
```

## Relationship Types

### Hierarchical Relationships
```cypher
(:Curriculum)-[:HAS_KEY_STAGE]->(:KeyStage)
(:KeyStage)-[:HAS_YEAR]->(:Year)
(:Year)-[:TEACHES]->(:Subject)
(:Subject)-[:HAS_DOMAIN]->(:Domain)
(:Domain)-[:CONTAINS]->(:Objective)
(:Objective)-[:TEACHES]->(:Concept)
```

### Temporal Relationships
```cypher
(:Concept)-[:APPEARS_IN_YEAR {
  is_introduced: boolean,  // true if first appearance
  is_reinforced: boolean,  // true if building on prior year
  teaching_notes: string
}]->(:Year)
```

### Prerequisite Relationships (ENHANCED)
```cypher
(:Concept)-[:PREREQUISITE_OF {
  confidence: enum["explicit", "inferred", "fuzzy"],
  // - explicit: stated in curriculum ("building on Year 1 work...")
  // - inferred: logically necessary (addition before multiplication)
  // - fuzzy: pedagogically typical but not strictly necessary

  relationship_type: enum["logical", "developmental", "instructional", "temporal"],
  // - logical: must know A to understand B (Maths)
  // - developmental: cognitive maturity needed (English reading progression)
  // - instructional: teacher-guided sequence (History chronology)
  // - temporal: time-based only (do this before that)

  strength: float,  // 0.0-1.0, how strong is the dependency?
  rationale: string,  // Why is this a prerequisite?

  years_gap: int,  // How many years between prerequisite and dependent?
  same_domain: boolean  // Are both concepts in same domain?
}]->(:Concept)
```

### Cross-Domain Relationships (NEW)
```cypher
(:Domain)-[:APPLIES_TO {
  application_type: enum["foundational", "supportive", "integrated"],
  description: string
}]->(:Domain)

// Example: Science "Working Scientifically" APPLIES_TO all content domains
// Example: English "Spoken Language" APPLIES_TO Reading and Writing
```

### Concept Relationships (NEW)
```cypher
(:Concept)-[:RELATED_TO {
  relationship_type: enum["supports", "contrasts", "exemplifies", "generalizes"],
  description: string
}]->(:Concept)

// For concepts that aren't strictly prerequisites but are related
```

## Subject-Specific Considerations

### Mathematics (Structure: 9/10)
- **Domains**: Number, Algebra, Geometry, Measurement, Statistics
- **Concept Type**: Primarily "knowledge" and "skill"
- **Prerequisites**: Mostly "logical" and "explicit"
- **Extraction**: Most straightforward

### English (Structure: 4/10)
- **Domains**: Reading, Writing, Spoken Language (cross-cutting)
- **Concept Type**: Primarily "skill" and "process"
- **Prerequisites**: Mostly "developmental" and "fuzzy"
- **Challenge**: Heavy interdependencies, skills overlap across domains

### Science (Structure: 5/10)
- **Domains**: Working Scientifically (cross-cutting) + Content domains (Plants, Animals, Materials, etc.)
- **Concept Type**: Mixed "knowledge" (facts) and "process" (scientific method)
- **Prerequisites**: Mix of "logical" (within content) and "fuzzy" (across domains)
- **Challenge**: Dual nature of subject

### History (Structure: 5/10)
- **Domains**: Chronology, Knowledge, Enquiry, Interpretation
- **Concept Type**: Mix of "content" (specific events) and "skill" (historical thinking)
- **Prerequisites**: "temporal" (chronological) and "instructional" (teacher choice)
- **Challenge**: Balance between specific content and abstract skills

### Geography (Structure: 6/10)
- **Domains**: Locational Knowledge, Place Knowledge, Human/Physical Geography, Skills & Fieldwork
- **Concept Type**: Mix of "knowledge" (facts about places) and "skill" (map reading)
- **Prerequisites**: "instructional" with clear scale progression (local→national→global)
- **Challenge**: Content and skills deeply intertwined

### Computing (Structure: 8/10)
- **Domains**: Computer Science, Information Technology, Digital Literacy
- **Concept Type**: Mix of "knowledge" (algorithms) and "skill" (coding)
- **Prerequisites**: Mostly "logical" in CS domain, "instructional" in others
- **Extraction**: More structured than expected

## Extraction Guidelines

### 1. Domain Identification
- Use curriculum document section headings as primary guide
- Flag cross-cutting domains explicitly
- Note structure_type for each domain

### 2. Objective Extraction
- One objective per curriculum bullet point
- Preserve exact wording from document
- Mark statutory vs non-statutory
- Include page/section reference

### 3. Concept Decomposition
- Break compound objectives into atomic concepts
- Assign concept_type based on nature of learning
- Rate complexity_level (1=simple facts, 5=complex synthesis)
- Include extraction_confidence score

### 4. Prerequisite Identification
- Check for explicit prerequisites first (curriculum often references prior learning)
- Infer logical prerequisites where clear
- Mark as "fuzzy" when pedagogically typical but not strictly necessary
- Always include rationale

### 5. Cross-Cutting Handling
- Identify domains that apply to others
- Create APPLIES_TO relationships
- Mark constituent concepts as is_cross_cutting: true
- Link to specific content domains where applicable

## Validation Checklist

For each extracted subject:
- [ ] All domains identified with correct metadata
- [ ] All objectives extracted verbatim from document
- [ ] Concepts have appropriate concept_type
- [ ] Prerequisites include confidence and rationale
- [ ] Cross-cutting domains properly linked
- [ ] Source traceability maintained throughout
- [ ] Complexity levels assigned consistently
- [ ] Extraction confidence noted

## Model Revision History
- **v1.0** (2026-02-12): Initial hierarchical model
- **v2.0** (2026-02-12): Enhanced with concept_type, prerequisite metadata, cross-cutting domain support

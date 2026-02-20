# Assessment Layer

## Purpose

The **Standards and Testing Agency (STA) test frameworks** layer — how statutory KS2 assessments are structured and what curriculum content they assess.

## Graph Structure

```
TestFramework -[:HAS_PAPER]-> TestPaper
TestPaper -[:INCLUDES_CONTENT]-> ContentDomainCode
ContentDomainCode -[:ASSESSES]-> Programme
ContentDomainCode -[:ASSESSES_CONCEPT]-> Concept
ContentDomainCode -[:ASSESSES_DOMAIN]-> Domain
ContentDomainCode -[:ASSESSES_SKILL]-> ReadingSkill  (epistemic-skills layer)
TestFramework -[:SOURCED_FROM]-> SourceDocument
```

## Node Types

| Label | Example | Description |
|---|---|---|
| `TestFramework` | KS2 Mathematics 2023 | STA test framework document |
| `TestPaper` | Paper 1: Arithmetic | Individual test papers within a framework |
| `ContentDomainCode` | 3N1a | Coded assessment content descriptors |
| `SourceDocument` | STA Test Framework Doc | Source document metadata |

## Data Sources

All extractions from:
- `/data/extractions/test-frameworks/`
  - `ks2_mathematics_test_framework.json`
  - `ks2_english_reading_test_framework.json`
  - `ks2_english_gps_test_framework.json`

Source: [Standards & Testing Agency](https://www.gov.uk/government/organisations/standards-and-testing-agency)

## Usage

### Import all test frameworks

```bash
cd /Users/richardmorgan/Documents/GitHub/uk-curriculum-as-graph
python3 layers/assessment/scripts/import_test_frameworks.py
```

This will:
1. Create TestFramework nodes (one per subject)
2. Create TestPaper nodes (2-3 papers per framework)
3. Create ContentDomainCode nodes (200+ codes across all frameworks)
4. Link codes to curriculum Programmes, Domains, and Concepts
5. Link codes to ReadingSkill nodes (for English reading)
6. Create SourceDocument nodes

### Expected Output

```
Frameworks created              : 3
Test Papers created             : 7
Content Domain Codes created    : 245
ASSESSES Programme links        : 245
ASSESSES Concept links          : 892
ASSESSES Domain links           : 156
ASSESSES Skill links            : 45  (reading skills only)
```

## Integration Points

This layer **depends on**:
- **UK Curriculum**: Must be imported first (Programme, Domain, Concept nodes)
- **Epistemic Skills**: ReadingSkill nodes for ASSESSES_SKILL links

This layer **enables**:
- Assessment coverage queries ("Which concepts are NOT tested?")
- Curriculum-to-test alignment analysis
- Test paper difficulty profiling by content domain

## Content Domain Codes

Each `ContentDomainCode` represents a specific assessable skill or knowledge point. For example:

**Mathematics**:
- `3N1a`: "Order and compare numbers to 1000"
- `6F3a`: "Compare and order fractions, including fractions > 1"

**English Reading**:
- `2a`: "Give/explain the meaning of words in context"
- `2d`: "Make inferences from the text"

**English GPS (Grammar, Punctuation, Spelling)**:
- `G5.1`: "Use relative clauses"
- `P6.4`: "Use semi-colons, colons, dashes"

## Coding Scheme

Mathematics codes follow the pattern: `{Year}{Strand}{Substrand}`
- Year: 3-6 (KS2)
- Strand: N (Number), F (Fractions), R (Ratio), A (Algebra), M (Measurement), G (Geometry), S (Statistics)
- Substrand: 1, 2, 3... (ordered within strand)

English codes follow the pattern: `{Code}{Substrand}`
- Reading: 2a-2h (comprehension skills)
- GPS: G1.1, P1.1, S1.1 (Grammar, Punctuation, Spelling by year)

## Example Queries

### Find concepts NOT tested in KS2

```cypher
MATCH (c:Concept)<-[:HAS_CONCEPT]-(d:Domain)<-[:HAS_DOMAIN]-(p:Programme)
WHERE p.key_stage = 'KS2'
  AND NOT (:ContentDomainCode)-[:ASSESSES_CONCEPT]->(c)
RETURN p.subject_name, d.domain_name, c.concept_name
ORDER BY p.subject_name, d.domain_name
```

### Test paper coverage by domain

```cypher
MATCH (tp:TestPaper)-[:INCLUDES_CONTENT]->(cdc:ContentDomainCode)-[:ASSESSES_DOMAIN]->(d:Domain)
RETURN tp.name, d.domain_name, count(cdc) AS codes
ORDER BY tp.name, codes DESC
```

## Notes

- Test frameworks are updated annually by STA — data here reflects 2023 frameworks
- Not all curriculum content is assessed (e.g., KS1, KS3, KS4 have no test framework links)
- ContentDomainCode alignment to Concept nodes is manually curated
- Re-running the import is **idempotent** (uses MERGE patterns)

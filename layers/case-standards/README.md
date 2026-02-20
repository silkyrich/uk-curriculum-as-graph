# CASE Standards Layer

## Purpose

The **international/US academic standards** layer — provides browseable, comparable standards from the IMS Global CASE (Competencies and Academic Standards Exchange) network. Enables cross-jurisdictional comparison, especially for scientific literacy and pedagogical models.

## Graph Structure

```
Framework -[:HAS_DIMENSION]-> Dimension -[:HAS_PRACTICE]-> Practice
Framework -[:HAS_DIMENSION]-> Dimension -[:HAS_CORE_IDEA]-> CoreIdea
CoreIdea -[:HAS_PERFORMANCE_EXPECTATION]-> PerformanceExpectation
Practice -[:ALIGNS_TO]-> WorkingScientifically  (cross-layer to epistemic-skills)
PerformanceExpectation -[:ALIGNS_TO]-> Concept  (cross-layer to uk-curriculum)
```

## Node Types

| Label | Example | Description |
|---|---|---|
| `Framework` | NGSS Science 2013 | A complete academic standards framework |
| `Dimension` | Science and Engineering Practices | A pedagogical dimension (NGSS 3D model) |
| `Practice` | Asking Questions and Defining Problems | A specific practice/skill |
| `CoreIdea` | LS3: Heredity | A disciplinary core idea |
| `PerformanceExpectation` | 3-LS3-1 | A specific grade-level learning expectation |

## Framework Types

### NGSS (Next Generation Science Standards)

**3-Dimensional Learning Model**:
1. **Science and Engineering Practices (SEPs)**: How scientists work
2. **Disciplinary Core Ideas (DCIs)**: What to know
3. **Crosscutting Concepts (CCCs)**: Connecting ideas across disciplines

Performance Expectations (PEs) integrate all three dimensions into grade-level assessable standards.

### Common Core Mathematics

**Structure**:
1. **Standards for Mathematical Practice (SMPs)**: 8 practices (e.g., "Make sense of problems")
2. **Content Standards**: Organized by grade and domain (e.g., Number & Operations)

### Common Core ELA

**Structure**:
1. **Reading Standards**: Literature, Informational Text, Foundational Skills
2. **Writing Standards**: Text types, production, research
3. **Speaking & Listening**: Comprehension, presentation
4. **Language**: Conventions, vocabulary

## Data Sources

All data from `/data/extractions/case/`:
- **Packages** (cached CASE JSON): `/packages/ngss-science-2013.json`, etc.
- **Sources config**: `/case_sources.json` — framework metadata and fetch URLs
- **Mappings** (manual alignment): `/mappings/ngss_to_uk.json`, etc.

**Source**: [IMS Global CASE Network](https://casenetwork.imsglobal.org)

## Usage

### Fetch CASE packages from the CASE Network

```bash
cd /Users/richardmorgan/Documents/GitHub/uk-curriculum-as-graph
python3 layers/case-standards/scripts/import_case_standards_v2.py --fetch
```

This will:
1. Read `case_sources.json` for framework definitions
2. Query the CASE Network API for each framework
3. Download and cache full CFPackages to `/data/extractions/case/packages/`

### Import CASE standards into Neo4j

```bash
python3 layers/case-standards/scripts/import_case_standards_v2.py --import
```

Or import a single framework:

```bash
python3 layers/case-standards/scripts/import_case_standards_v2.py --import --framework ngss-science-2013
```

This will:
1. Create Framework nodes
2. Create Dimension nodes (NGSS: 3 dimensions; CC Math: 1 practice dimension + content)
3. Create Practice/CoreIdea/PerformanceExpectation nodes
4. Build hierarchical relationships (Framework → Dimension → Items)
5. Load cross-layer alignments from mapping files

### Expected Output

```
Frameworks Imported         : 3  (NGSS, CC Math, CC ELA)
Dimensions Created          : 8
Practices Created           : 16
Core Ideas Created          : 13
Performance Expectations    : 287
Cross-layer Alignments      : 45  (manual mappings only)
```

## Framework Properties

### Framework

| Property | Example | Description |
|---|---|---|
| `framework_id` | `ngss-science-2013` | Unique identifier |
| `title` | "Next Generation Science Standards" | Human-readable name |
| `creator` | "Achieve Inc." | Publishing organization |
| `subject` | "Science" | Subject area |
| `adoption_status` | "adopted" | Status (adopted, draft, etc.) |
| `version` | "2.0" | Framework version |
| `licence` | "CC-BY" | License type |
| `case_uri` | `https://...` | Canonical CASE URI |

### Practice (Science and Engineering Practices)

| Property | Example | Description |
|---|---|---|
| `practice_id` | `SEP-1` | Unique identifier |
| `practice_name` | "Asking Questions and Defining Problems" | Human-readable name |
| `description` | "Science begins with questions..." | Full text |
| `dimension_id` | `DIM-SEP` | Parent dimension ID |
| `framework_id` | `ngss-science-2013` | Parent framework ID |

### CoreIdea (Disciplinary Core Ideas)

| Property | Example | Description |
|---|---|---|
| `core_idea_id` | `LS3` | Unique identifier (e.g., LS3, PS1, ESS2) |
| `core_idea_name` | "Heredity: Inheritance and Variation of Traits" | Full name |
| `description` | "How are characteristics passed..." | Full text |
| `dimension_id` | `DIM-DCI` | Parent dimension ID |

### PerformanceExpectation

| Property | Example | Description |
|---|---|---|
| `pe_id` | `3-LS3-1` | Unique identifier (grade-strand-number) |
| `statement` | "Analyze and interpret data..." | Full assessment statement |
| `grade_level` | `3` | Grade level (3, 4, 5, etc.) |
| `dci_id` | `LS3` | Linked disciplinary core idea |
| `sep_ids` | `["SEP-4"]` | Linked science practices (array) |
| `ccc_ids` | `["CCC-1"]` | Linked crosscutting concepts (array) |

## Cross-Layer Alignments

The CASE layer can be **manually mapped** to UK curriculum nodes for comparison. Mapping files are in `/data/extractions/case/mappings/`.

### Example: NGSS Science Practices ↔ UK Working Scientifically

```json
{
  "metadata": {
    "framework_id": "ngss-science-2013",
    "aligns_to": "UK National Curriculum Science",
    "notes": "Science Practices ↔ Working Scientifically (KS3)"
  },
  "alignments": [
    {
      "practice_id": "SEP-1",
      "practice_name": "Asking Questions and Defining Problems",
      "aligns_to_skill_ids": ["WS-KS3-001"],
      "confidence": "strong",
      "notes": "Direct alignment to 'Asking scientific questions'"
    }
  ]
}
```

## Integration Points

This layer **depends on**:
- **UK Curriculum**: For cross-layer alignments (CASE → Concept, Objective)
- **Epistemic Skills**: For practice alignments (Practice → WorkingScientifically)

This layer **enables**:
- Cross-jurisdictional comparison (e.g., "How does NGSS climate change coverage compare to UK Science?")
- Pedagogical model comparison (e.g., "3D learning vs linear programmes of study")
- Controversial topics analysis (e.g., states that rejected NGSS over evolution/climate)

## Example Queries

### NGSS Performance Expectations for Grade 3

```cypher
MATCH (f:Framework {framework_id: 'ngss-science-2013'})
      -[:HAS_DIMENSION]->(:Dimension)
      -[:HAS_CORE_IDEA]->(ci:CoreIdea)
      -[:HAS_PERFORMANCE_EXPECTATION]->(pe:PerformanceExpectation {grade_level: '3'})
RETURN ci.core_idea_name, pe.pe_id, pe.statement
ORDER BY pe.pe_id
```

### NGSS practices aligned to UK skills

```cypher
MATCH (p:Practice)-[:ALIGNS_TO]->(ws:WorkingScientifically)
RETURN p.practice_name, ws.skill_name, ws.key_stage
ORDER BY p.practice_id
```

### Frameworks by subject

```cypher
MATCH (f:Framework)
RETURN f.subject, collect(f.title) AS frameworks
ORDER BY f.subject
```

### Compare NGSS DCI coverage to UK Science concepts

```cypher
MATCH (ci:CoreIdea)-[:HAS_PERFORMANCE_EXPECTATION]->(pe:PerformanceExpectation)
WHERE ci.core_idea_id STARTS WITH 'LS'  // Life Science DCIs only
WITH ci, count(pe) AS num_pes
MATCH (c:Concept)<-[:HAS_CONCEPT]-(d:Domain {subject: 'Science'})
WHERE toLower(c.concept_name) CONTAINS toLower(ci.core_idea_name)
RETURN ci.core_idea_name, num_pes, collect(c.concept_name) AS uk_concepts
```

## Jurisdictional Comparison

The CASE layer is designed to enable comparison of **how different US states and the UK approach the same content**. For example:

- **Wyoming** rejected NGSS over climate change → can compare their state standards to UK Science
- **Texas** uses TEKS (not NGSS) → can compare TEKS biology to UK Science KS3/KS4
- **California** adopted NGSS fully → can compare NGSS to UK as a reference point

Jurisdiction nodes (not yet implemented) would track adoption status and political context.

## Notes

- CASE packages are **fetched via the IMS Global CASE Network API** (no scraping)
- Alignments are **manually curated** (not automated matching)
- Only NGSS is currently implemented; Common Core Math/ELA are planned
- Re-running import is **idempotent** (uses MERGE patterns)
- Framework structures are **intelligently parsed** (not generic blob import)

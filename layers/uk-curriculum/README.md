# UK Curriculum Layer

## Purpose

The foundational layer of the knowledge graph — the statutory UK National Curriculum content organized as a programme-based model with full source document traceability.

## Graph Structure

```
Curriculum -[:HAS_KEY_STAGE]-> KeyStage -[:HAS_YEAR]-> Year -[:HAS_PROGRAMME]-> Programme
Programme -[:FOR_SUBJECT]-> Subject
Programme -[:HAS_DOMAIN]-> Domain -[:CONTAINS]-> Objective -[:TEACHES]-> Concept
Programme -[:SOURCED_FROM]-> SourceDocument
Concept -[:SOURCED_FROM]-> SourceDocument
```

## Node Types

| Label | Example | Description |
|---|---|---|
| `Curriculum` | UK National Curriculum | Root node for the entire curriculum |
| `KeyStage` | KS2 | Key Stage grouping (KS1-KS4) |
| `Year` | Y5 | Individual year groups (Y1-Y11) |
| `Subject` | Mathematics, Science | Subject areas |
| `Programme` | English-KS2, Maths-Y5 | Programme of study units |
| `Domain` | Number and Place Value | Content areas within a programme |
| `Objective` | "Count in multiples of 6, 7, 9..." | Learning objectives |
| `Concept` | "Multiples" | Specific curriculum concepts |
| `SourceDocument` | NC 2014 Mathematics | Curriculum documents |

## Data Sources

All extractions come from:
- **Primary**: `/data/extractions/primary/` — KS1/KS2 subjects (Y1-Y6)
- **Secondary**: `/data/extractions/secondary/` — KS3/KS4 subjects (Y7-Y11)

Source documents metadata: `core/data/curriculum-documents/metadata.json`

## Usage

### Import the entire UK curriculum

```bash
cd /Users/richardmorgan/Documents/GitHub/uk-curriculum-as-graph
python3 layers/uk-curriculum/scripts/import_curriculum.py
```

This will:
1. Create the root Curriculum node
2. Import all key stages, years, and subjects
3. Import all programmes, domains, objectives, and concepts
4. Link source documents with full traceability
5. Calculate coverage statistics

### Expected Output

```
UK Curriculum nodes created/updated : 3252
Programmes created                  : 48
Domains created                     : 156
Objectives created                  : 892
Concepts created                    : 2143
```

## Integration Points

This layer is the **foundation** for:
- **Assessment**: ContentDomainCode nodes link via `[:ASSESSES]->Programme`
- **Epistemic Skills**: Skill nodes link via `[:DEVELOPS_SKILL]->Programme`
- **Topics**: Topic nodes link via `[:TEACHES]->Concept`
- **Oak Content**: OakUnit/OakLesson nodes align via `[:COVERS]->Domain` and `[:TEACHES]->Concept`
- **CASE Standards**: CFItem nodes align via `[:ALIGNS_TO]->Concept`

## Key Properties

All nodes have standard properties for visualization:
- `name`: Display name (auto-generated in Neo4j Browser)
- `display_color`: Hex color for Bloom
- `display_icon`: Material icon name
- `display_category`: "UK Curriculum"

## Source Document Traceability

Every Programme and Concept node carries a `source_reference` field pointing to the exact section of the National Curriculum document. For example:

```cypher
MATCH (c:Concept {concept_id: "MA-Y5-C023"})
RETURN c.concept_name, c.source_reference
// "Fractions", "NC 2014 Mathematics - Year 5"
```

## Notes

- This layer uses **single-type labels only** (no namespace labels like `:Curriculum`)
- Provenance tracking is via `display_category` property, not labels
- All data is manually extracted from official DfE curriculum documents
- Re-running the import script is **idempotent** (uses MERGE patterns)

# EYFS Layer

**Status:** Phase 1 — Documentation only (no graph nodes yet)
**Scope:** Early Years Foundation Stage, Reception year (age 4-5)
**Source:** DfE EYFS Statutory Framework (GOV.UK)

---

## What This Is

The Early Years Foundation Stage (EYFS) is the statutory framework for children from birth to 5 in England. It precedes Key Stage 1 and is governed by a separate document from the National Curriculum.

This layer will eventually model the EYFS content in the graph, providing prerequisite links from EYFS concepts into KS1 — completing the learning progression chain from Reception through to Year 11.

---

## Current Contents

### Research
- `research/eyfs_statutory_framework.md` — Complete reference document covering:
  - 7 Areas of Learning (3 prime + 4 specific)
  - All 17 Early Learning Goals with full expected-level descriptions
  - Educational programme descriptions
  - Assessment requirements (EYFS Profile, GLD)
  - Development Matters guidance structure
  - All source URLs (GOV.UK only)

### Design
- `docs/design/PLAN_EYFS_INTEGRATION.md` (project-level) — Integration plan covering:
  - EYFS→KS1 subject mapping analysis
  - Phased approach (docs → extraction → import → learner profiles)
  - Modelling decisions and open questions
  - ID conventions and property recommendations

---

## EYFS Structure (Summary)

### 3 Prime Areas
| Area | ELGs | Maps to KS1 |
|------|------|-------------|
| Communication and Language | 1. Listening, Attention & Understanding; 2. Speaking | English (Spoken Language) |
| Personal, Social & Emotional Development | 3. Self-Regulation; 4. Managing Self; 5. Building Relationships | No direct NC subject |
| Physical Development | 6. Gross Motor Skills; 7. Fine Motor Skills | PE + English (Handwriting) |

### 4 Specific Areas
| Area | ELGs | Maps to KS1 |
|------|------|-------------|
| Literacy | 8. Comprehension; 9. Word Reading; 10. Writing | English (Reading, Writing) |
| Mathematics | 11. Number; 12. Numerical Patterns | Mathematics |
| Understanding the World | 13. Past and Present; 14. People, Culture & Communities; 15. The Natural World | History, Geography, Science |
| Expressive Arts and Design | 16. Creating with Materials; 17. Being Imaginative & Expressive | Art & Design, Music, D&T |

---

## Key Differences from KS1+

- **Not part of the National Curriculum** — separate statutory framework
- **Play-based pedagogy** — not subject-structured teaching
- **17 ELGs total** — much thinner than NC programmes of study
- **Assessment:** Expected / Emerging (no levels, no tests)
- **Single year group:** Reception only (Birth to 3 and 3-4 age bands exist in Development Matters but are out of scope)

---

## Phase 2: Future Graph Integration

When extracted, EYFS will follow the existing Programme model:

```
(:Curriculum)-[:HAS_KEY_STAGE]->(:KeyStage {key_stage_id: 'EYFS'})
  -[:HAS_YEAR]->(:Year {year_id: 'EYFS', year_number: 0, age_range: '4-5'})
    -[:HAS_PROGRAMME]->(:Programme)
      -[:HAS_DOMAIN]->(:Domain)
        -[:CONTAINS]->(:Objective)
          -[:TEACHES]->(:Concept)
```

Cross-stage prerequisites will link EYFS concepts to KS1:
```
(:Concept {concept_id: 'EY-R-C001'})-[:PREREQUISITE_OF]->(:Concept {concept_id: 'MA-Y1-C001'})
```

ID conventions:
- Domains: `EY-R-D001`
- Objectives: `EY-R-O001`
- Concepts: `EY-R-C001`

### Extraction files (planned)
```
layers/eyfs/data/extractions/
├── CommunicationAndLanguage_EYFS_extracted.json
├── PSED_EYFS_extracted.json
├── PhysicalDevelopment_EYFS_extracted.json
├── Literacy_EYFS_extracted.json
├── Mathematics_EYFS_extracted.json
├── UnderstandingTheWorld_EYFS_extracted.json
└── ExpressiveArtsAndDesign_EYFS_extracted.json
```

---

## Source Documents

All from GOV.UK:
- [EYFS Statutory Framework](https://www.gov.uk/government/publications/early-years-foundation-stage-framework--2)
- [Development Matters](https://www.gov.uk/government/publications/development-matters--2)
- [EYFS Profile 2024 Specification](https://assets.publishing.service.gov.uk/media/65f081f8133c220019cd3935/EYFSP_2024_specification_v1.1.pdf)

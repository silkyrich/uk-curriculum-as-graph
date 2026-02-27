# docs/ — Navigation Guide

Project documentation organised by purpose. Layer-specific docs live in `layers/{layer}/` not here.

---

## Directories

### `design/`
Project direction, compilation targets, and design rationale — documents describing *what* the project is and *why* it works the way it does.

| File | Description |
|---|---|
| `PROJECT_DIRECTION.md` | **Start here.** Project rationale, architecture direction, what's built vs planned |
| `OUTPUT_SCHEMAS.md` | Three compilation target specs: Teacher Planner, LLM Session, Parent Guide |
| `RESEARCH_BRIEFING.md` | Learning science evidence base for platform design decisions |
| `INTERACTION_MODES.md` | Interaction modes taxonomy — voice, text, analysis |
| `CHILD_PROFILE_CONSENT.md` | Full legal and ethical analysis for child data processing |
| `PLAN_DELIVERY_MODE_CLASSIFICATION.md` | Design rationale for delivery readiness classification |
| `PLAN_EYFS_INTEGRATION.md` | Design rationale for EYFS layer integration |
| `PLAN_POST_KS3.md` | KS4 extension plan — phased approach, GCSE layer architecture |

---

### `analysis/`
Outputs and artefacts of data work — curriculum analysis, extraction reports, stress tests.

| File | Description |
|---|---|
| `CURRICULUM_ANALYSIS.md` | UK National Curriculum structural analysis |
| `extraction_inventory.md` | Inventory of all extraction files |
| `extraction_stress_test_results.md` | Results from extraction stress testing |

---

### `archive/`
Stale or superseded documents preserved for historical context.

| File | Description |
|---|---|
| `graph_model_v2.md` | Earlier graph model spec — superseded by `CLAUDE.md` Graph Model Overview section |
| `STATUS_2026-02-16.md` | Project status snapshot from 2026-02-16 — superseded by `CLAUDE.md` Current State section |
| `LEGACY_SCRIPTS.md` | Legacy migration scripts reference — superseded by `core/migrations/` |

---

### `user-stories/`
User stories and behavioural specs for the learning platform.

- `INDEX.md` — master index of all user stories
- `README.md` — explains how AI should interpret and use these stories
- `child-experience/` — narrative design docs for the child-facing experience
- `technical/` — numbered technical stories (concrete system behaviour specs)

---

### `research/`
Evidence base for platform design decisions.

- `SOURCES.md` — annotated bibliography of all research sources
- `learning-science/` — 16 papers organised by theme:
  - `knowledge-tracing/` — DKT, GKT, DyGKT, BKT review, KG learning paths (5 papers)
  - `intelligent-tutoring/` — AI ITS review, ASSISTments, ALEKS, Carnegie Learning (4 papers)
  - `motivation-and-engagement/` — SDT, gamification ghost effect, overjustification (3 papers)
  - `cognitive-learning/` — desirable difficulties, testing effect, productive failure (3 papers)
  - `llm-in-education/` — LLM education review (1 paper)
- `interoperability/` — protocol specs (CASE standard, xAPI)
- `case-standards/` — US comparative standards research (NGSS, Common Core, TEKS, Wyoming)
- `content-sources/` — UK content provider research (Oak, NCETM, White Rose, BBC)

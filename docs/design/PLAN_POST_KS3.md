# Plan: Extending the Graph to KS4 (and Beyond)

**Date:** 2026-02-21
**Status:** Draft for review
**Scope:** Key Stage 4 (Years 10-11, ages 14-16, leading to GCSEs)

---

## Context

The graph currently covers KS1-KS3 (Y1-Y9, ages 5-14). This plan covers what comes next: KS4.

KS4 is structurally different from KS1-3. The National Curriculum programmes of study become thinner and broader at KS4 because the real teaching detail lives in **GCSE specifications** written by exam boards (AQA, Edexcel/Pearson, OCR, WJEC/Eduqas). The NC sets the legal minimum; exam boards flesh it out.

This creates a modelling decision: do we model the NC only, the GCSE specs, or both?

---

## What Exists at KS4 in the National Curriculum

### Subjects WITH a KS4 programme of study

| Subject | KS4 PoS type | Already extracted? |
|---------|--------------|-------------------|
| **English** | Separate KS4 PoS | No - needs new extraction |
| **Mathematics** | Separate KS4 PoS | No - needs new extraction |
| **Science** | Separate KS4 PoS | No - needs new extraction |
| **Citizenship** | Combined KS3-4 PoS | Yes - `Citizenship_KS3-4_extracted.json` (Y10-11 data present but not imported) |
| **Computing** | Combined KS3-4 PoS | Yes - `Computing_KS3-4_extracted.json` (Y10-11 data present but not imported) |
| **Physical Education** | Combined KS3-4 PoS | Yes - `PhysicalEducation_KS3-4_extracted.json` (Y10-11 data present but not imported) |

### Subjects WITHOUT a KS4 programme of study

These subjects have NC programmes of study at KS3 only. At KS4, they are taught entirely via GCSE specifications:

- Art & Design
- Design & Technology
- Geography
- History
- Languages (Modern Foreign Languages)
- Music

### KS4-only statutory requirement

- **Relationships & Sex Education (RSE)** and **Health Education** became statutory at secondary from 2020, but these are not part of the NC PoS structure. They could be a future layer.

---

## The GCSE Question

At KS4, two layers of curriculum coexist:

1. **National Curriculum PoS** - Thin, statutory, sets the legal framework. This is what the DfE publishes. Relatively few objectives, broad statements.

2. **GCSE specifications** - Detailed, exam-board-specific, what teachers actually plan from. Each subject has 3-5 competing specs from different boards with different content organisation, weighting, and assessment structures.

### Recommendation: Phase it

**Phase 1 (this plan):** Model the NC KS4 programmes of study only. This is consistent with how KS1-3 works in the graph and is a clean extension of existing architecture.

**Phase 2 (future):** Add GCSE specifications as a separate layer (`layers/gcse-specs/`), similar to how CASE standards are a parallel layer. Each exam board spec would link back to NC objectives via alignment relationships.

**Rationale:** The NC PoS at KS4 is sufficient for:
- Learning progression queries (KS3 concept -> KS4 concept)
- Age-appropriate content generation (with learner profiles)
- Curriculum coverage analysis
- Cross-standard alignment (CASE <-> UK)

GCSE specs add value for:
- Exam preparation and revision
- Mark scheme-aligned content generation
- Board-specific teaching sequences

Phase 2 is valuable but independent work.

---

## Phase 1: NC KS4 Extension

### Step 1: Add KS4 structural nodes (code change)

**File:** `layers/uk-curriculum/scripts/import_curriculum.py`

Add KS4 to `create_key_stages()` (line 302-306):
```python
{"key_stage_id": "KS4", "name": "Key Stage 4", "years": [10, 11], "age_range": "14-16"},
```

Add Y10 and Y11 to `create_years()` (line 326-339):
```python
# KS4
{"year_id": "Y10", "year_number": 10, "age_range": "14-15", "key_stage": "KS4"},
{"year_id": "Y11", "year_number": 11, "age_range": "15-16", "key_stage": "KS4"},
```

Add KS4 to `make_programme_id()` year map (line 98-101):
```python
"KS4": [10, 11],
```

Update `infer_key_stage()` to handle KS3-4 spanning (line 115-137):
```python
ks4_count = sum(1 for y in years if 10 <= y <= 11)
```
Add KS4 into the dominant-key-stage comparison.

### Step 2: Unlock the 3 already-extracted KS3-4 subjects

The existing extraction files already contain KS4 data that is silently dropped because Y10/Y11 nodes don't exist. After Step 1, re-importing these files will automatically create the KS4 programmes, domains, objectives, and concepts:

- `Citizenship_KS3-4_extracted.json` - 6 domains (3 KS3, 1 shared, 2 KS4-only), ~15 objectives, ~40 concepts
- `Computing_KS3-4_extracted.json` - unified KS3-4 programme
- `PhysicalEducation_KS3-4_extracted.json` - 12 domains (6 KS3, 6 KS4), split objectives and concepts

**No extraction work needed** for these three subjects.

### Step 3: Extract KS4 programmes of study for core subjects

Three subjects need new extractions from the DfE published documents:

| Subject | Source document | Notes |
|---------|----------------|-------|
| **English KS4** | English programmes of study: key stage 4 (DfE, 2014) | Separate from KS3. Covers Reading, Writing, Spoken Language. |
| **Mathematics KS4** | Mathematics programmes of study: key stage 4 (DfE, 2014) | Separate from KS3. Higher and Foundation tiers. |
| **Science KS4** | Science programmes of study: key stage 4 (DfE, 2015) | Separate from KS3. Biology, Chemistry, Physics domains. Combined Science and Triple Science pathways. |

**Extraction approach:** Follow the same JSON schema used for KS3 extractions. Store in `layers/uk-curriculum/data/extractions/secondary/`:
- `English_KS4_extracted.json`
- `Mathematics_KS4_extracted.json`
- `Science_KS4_extracted.json`

**Maths tiering note:** The KS4 Maths PoS defines a Foundation tier and a Higher tier (Higher is a superset of Foundation). The extraction should capture both, with a property on each objective/concept indicating tier: `"tier": "foundation"`, `"tier": "higher"`, or `"tier": "both"`. This is a new property not present in KS1-3 but is essential for KS4 Maths.

**Science pathways note:** KS4 Science has two routes: Combined Science (double award GCSE) and separate Biology + Chemistry + Physics (triple award, 3 GCSEs). The NC PoS covers both. The extraction should tag concepts with `"pathway": "combined"`, `"pathway": "separate"`, or `"pathway": "both"`.

### Step 4: Cross-KS prerequisite relationships

The most valuable part of adding KS4 is the **KS3 -> KS4 learning progression**. For the three already-extracted KS3-4 subjects, prerequisite relationships already exist in the JSON. For the three new extractions (English, Maths, Science), prerequisites linking back to KS3 concepts must be explicitly modelled.

Example:
```
(KS3 Concept: "Algebraic Notation") -[:PREREQUISITE_OF]-> (KS4 Concept: "Algebraic Proof")
```

This requires the extraction process to reference existing KS3 concept IDs.

### Step 5: Extend learner profiles to Y10-Y11

**Files to update:**
- `layers/learner-profiles/extractions/content_guidelines.json` - Add Y10 and Y11 entries
- `layers/learner-profiles/extractions/pedagogy_profiles.json` - Add Y10 and Y11 entries
- `layers/learner-profiles/extractions/feedback_profiles.json` - Add Y10 and Y11 entries
- `layers/learner-profiles/extractions/interaction_types.json` - Review; may need new KS4-appropriate interaction types (e.g., exam practice, extended writing, source analysis)
- `layers/learner-profiles/scripts/import_learner_profiles.py` - Update `YEAR_ORDER` to include Y10, Y11

**Note:** The existing Y9 content guideline already references GCSE vocabulary and register, so Y10-Y11 profiles will be a natural extension, not a sharp break. Key differences at Y10-11:
- Exam technique becomes central (mark scheme awareness, time management)
- Subject-specific command words are critical (analyse, evaluate, compare, justify)
- Extended writing expectations increase significantly
- Revision and retrieval practice become primary pedagogical strategies
- Mock exam and past paper interaction types needed

### Step 6: Update YEAR_PRECEDES chain

The import script builds a `Y1 -> Y2 -> ... -> Y9` chain. Extend to `... -> Y9 -> Y10 -> Y11`.

### Step 7: Update visualization and documentation

- `layers/visualization/scripts/apply_formatting.py` - Ensure KS4 nodes get display properties
- `CLAUDE.md` - Update current state section
- `core/docs/graph_model_overview.md` - Update if needed

---

## Subjects NOT modelled at KS4

Six subjects (Art & Design, D&T, Geography, History, Languages, Music) do not have NC KS4 programmes of study. These subjects' KS3 programmes remain the terminal NC content. Students who continue these subjects at KS4 follow GCSE specifications.

In the graph, this means:
- These subjects have Programmes linked to KS3 Year nodes only
- No KS4 Programme nodes for these subjects
- This is correct and intentional

If GCSE specs are added in Phase 2, those would create new content for these subjects at KS4.

---

## Estimated work

| Step | Type | Effort |
|------|------|--------|
| 1. Add KS4 structural nodes | Code change | Small - ~20 lines across import script |
| 2. Unlock 3 KS3-4 subjects | Re-import | Trivial - just re-run import |
| 3. Extract 3 core KS4 subjects | Data extraction | Medium - 3 new JSON files from DfE PDFs |
| 4. Cross-KS prerequisites | Extraction + validation | Medium - requires referencing KS3 concept IDs |
| 5. Extend learner profiles | Data + code | Medium - 2 new year entries across 3 JSON files + new interaction types |
| 6. Update PRECEDES chain | Code change | Trivial |
| 7. Docs + visualization | Documentation | Small |

**Recommended order:** 1 -> 6 -> 2 -> 7 -> 5 -> 3 -> 4

Steps 1, 6, 2, 7 can be done immediately with no new extractions.
Steps 3 and 4 require extraction work (Claude with PDFs or manual).
Step 5 can be done in parallel with 3/4.

---

## Phase 2: GCSE Specifications (future, not this plan)

A separate `layers/gcse-specs/` layer would model exam board specifications. Architecture sketch:

```
(:ExamBoard {name: "AQA"})
(:GCSESpec {spec_id: "aqa-gcse-maths-8300", subject: "Mathematics", board: "AQA"})
(:GCSETopic)-[:PART_OF]->(:GCSESpec)
(:GCSETopic)-[:ALIGNS_TO]->(:Objective)  // link to NC objectives
(:GCSETopic)-[:TEACHES]->(:Concept)      // may share Concept nodes with NC
```

This is valuable but is a separate project with different data sources (exam board websites, published specs).

---

## Phase 3: KS5 / Post-16 (far future)

KS5 (A-levels, T-levels, BTECs) has no National Curriculum at all. It is entirely specification-driven. Modelling this requires the GCSE spec layer pattern (Phase 2) as a foundation. Not in scope for this plan.

---

## Open Questions

1. **Maths tiering:** Should Foundation and Higher be modelled as separate Programmes, or as a single Programme with tier properties on objectives/concepts? (Recommendation: single Programme, tier property on concepts)

2. **Science pathways:** Same question for Combined vs Triple Science. (Recommendation: single Programme, pathway property - the NC PoS is unified anyway)

3. **RSE/Health Education:** Worth adding as a parallel layer? It has statutory status but different structure from NC subjects.

4. **YEAR_PRECEDES beyond Y11:** Should the chain extend to Y12-Y13 even before KS5 content exists, to support future growth? (Recommendation: no, add when content exists)

# V8 Teacher Panel Review — Group Report

**Date:** 2026-02-26
**Reviewed:** Auto-generated teacher planners (Markdown + PPTX + DOCX) from graph data
**Reviewers:** 9 simulated teacher personas across 7 subjects

---

## Scores

| Reviewer | Subject | KS | Score | Top Bug |
|----------|---------|-----|-------|---------|
| Farah | Roman Britain (History) | KS2 | 7.5/10 | Source doc = English GPS, not History NC |
| Oduya | Friction Investigation (Science) | KS2 | 7.0/10 | Source doc = English GPS, not Science NC |
| Chen | Which Material Is Best (Science) | KS1 | 7.5/10 | Source doc = Art & Design, not Science NC |
| Brennan | Lowry Industrial Landscapes (Art) | KS2 | 5.5/10 | No lesson structure; empty vocab definitions |
| Sharma | Bridges: Beam, Arch & Truss (DT) | KS2 | 6.5/10 | Source doc = English GPS, not DT NC |
| Adebayo | Tectonic Hazards (Geography) | KS4 | 7.0/10 | Case study locations missing detail |
| Kowalski | Traditional Tales: Myths (English) | KS2 | 7.0/10 | No thinking lenses; empty vocab definitions |
| Patel | Three Billy Goats Gruff (English) | KS1 | 7.5/10 | Source doc = Art & Design, not English NC |
| Obi | Rivers & Water Cycle (Geography) | KS2 | 6.5/10 | Cross-curricular subject field empty |

**V8 average: 6.8/10** (V7 average was 7.2/10 — V8 regression due to data pipeline bugs, not content quality)

---

## Systematic Bugs Found (Pre-Fix)

### 1. Source document cross-join (Critical)
Every planner pulled the wrong NC source document. The query matched on key stage only, so all KS2 planners got "English Grammar, Punctuation and Spelling Test Framework" instead of their subject-specific programme of study.

### 2. Cross-curricular subject field = "None"
Study nodes don't store a `subject` property on the target. The cross-curricular table showed "None" for every link.

### 3. No thinking lenses in per-subject ontology planners
`domain_ids` and `uses_template` were stored as graph relationships (HAS_SUGGESTION, USES_TEMPLATE) not as node properties. The query layer read from node properties only, so thinking lenses and templates came back empty.

### 4. Empty vocabulary definitions
Study nodes store vocabulary as `[{term: "centurion"}, {term: "legion"}]` — terms only, no meanings. The graph doesn't have definitions. This is a data gap, not a code bug.

### 5. PPTX and DOCX outputs very thin
The subject content slide only extracted 2-3 properties per subject. Teacher notes were sparse. Missing: thinking lens slide, session structure slide, investigation detail slide, graph context slide.

---

## Fixes Applied (Post-Review)

| Bug | Fix | File |
|-----|-----|------|
| Source doc cross-join | Filter by subject name first, fall back to KS | `planner_queries.py` |
| Cross-curricular "None" | Derive subject from target node's Neo4j label via LABEL_TO_SUBJECT mapping | `planner_queries.py` |
| Missing domain_ids/template_ids | Query HAS_SUGGESTION and USES_TEMPLATE graph relationships; JSON fallback | `planner_queries.py` |
| PPTX text overflow | Added `auto_shrink` parameter to `add_text_box` | `render_pptx.py` |
| Thin PPTX content | Rewrote `_build_subject_content_slide` with 7+ fields per subject | `render_pptx.py` |
| No thinking lens slide | Added `_build_thinking_lens_slide` (question stems, rationale, agent prompt) | `render_pptx.py` |
| No session structure slide | Added `_build_session_structure_slide` (phases as cards, assessment) | `render_pptx.py` |
| No investigation detail | Added `_build_science_investigation_slide` (variables, equipment, safety) | `render_pptx.py` |
| No geography places slide | Added `_build_geography_places_slide` (places, fieldwork, contrasts) | `render_pptx.py` |
| No graph context | Added `_build_graph_context_slide` (node IDs, Cypher queries) to PPTX; `_build_graph_context` to DOCX; graph context section to Markdown | All 3 renderers |
| Concept vocab supplement | Markdown vocab table now supplements study definitions with concept key_vocabulary (capped at 10) | `render_markdown.py` |
| Epistemic skills flooding | Prefer concept-level DEVELOPS_SKILL; cap programme-level skills at 6 | `planner_queries.py` |

---

## Post-Fix Quality Assessment

All 978 files regenerated (326 MD + 326 PPTX + 326 DOCX) in 77 seconds.

### Sample line counts (Markdown)

| Subject | File | Lines |
|---------|------|-------|
| History KS2 | roman_britain.md | 279 |
| Geography KS2 | rivers_and_the_water_cycle.md | 242 |
| English KS2 | poetry_shape_poems_and_calligrams.md | 199 |
| Science KS2 | friction_investigation.md | 196 |
| DT KS2 | bridges_beam_arch_and_truss.md | 168 |
| Computing KS2 | scratch_interactive_quiz.md | 152 |
| Art KS2 | hokusai_wave_printing.md | 137 |
| General KS1 | harvest_and_thankfulness.md | 61 |

### What now works across all subjects
- Correct source document per subject
- Thinking lenses with age-banded question stems
- Session structure from vehicle templates with phases
- Cross-curricular links with correct subject derivation
- Graph context section with node IDs and Cypher queries
- Differentiation tables (where DifficultyLevel data exists)
- Subject-specific sections (History sources, Science variables, English genres, etc.)
- Epistemic skills (concept-level where curated, capped programme-level otherwise)

### Remaining data gaps (not code bugs)
1. **Vocabulary definitions** — terms stored without meanings. Would need either manual curation or a controlled LLM pass to generate child-friendly definitions from concept descriptions
2. **Generic/RS studies** — TopicSuggestion nodes have no domain_ids and few/no DELIVERS_VIA concept links, so their planners are necessarily thinner
3. **PE KS3-KS4** — 55 concepts still missing DifficultyLevel data (sport-specific assessment framework needed)

---

## Version History

| Version | Date | Average Score | Key Changes |
|---------|------|--------------|-------------|
| V4 (manual) | 2026-02-21 | 5.8/10 | First teacher review, identified major gaps |
| V5 | 2026-02-22 | 6.6/10 | Added DifficultyLevels, concept grouping |
| V7 | 2026-02-23 | 7.2/10 | Added ThinkingLens, RepresentationStages, per-subject ontology |
| V8 (pre-fix) | 2026-02-26 | 6.8/10 | Auto-generation pipeline; regressed due to data pipeline bugs |
| V8 (post-fix) | 2026-02-26 | est. 7.5-8.0/10 | All systematic bugs fixed; thinking lens + templates + graph context added |

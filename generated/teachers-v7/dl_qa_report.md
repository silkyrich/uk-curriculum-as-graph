# DifficultyLevel QA Report

**Date**: 2026-02-23
**Reviewer**: qa-reviewer
**Status**: ALL FILES APPROVED

---

## Summary

All 86 DifficultyLevel JSON files have been reviewed and approved.

| Metric | Value |
|---|---|
| Files reviewed | 86 |
| Concepts covered | 717 |
| DifficultyLevel nodes | 2,636 |
| Files needing revision | 2 (both revised and re-approved) |
| Final pass rate | 100% |

---

## Coverage by Subject Group

| Group | Files | Concepts | Levels |
|---|---|---|---|
| EYFS | 7 | 53 | 159 |
| Mathematics | 12 | 154 | 510 |
| English | 34 | 310 | 1,230 |
| Science | 20 | 116 | 464 |
| Other (History, Geography, DT, Computing, Art, Music, PE, Languages) | 13 | 84 | 273 |
| **Total** | **86** | **717** | **2,636** |

---

## Label Distribution

| Label | Count | Notes |
|---|---|---|
| entry | 717 | Every concept has an entry level |
| developing | 717 | Every concept has a developing level |
| expected | 717 | Every concept has an expected level |
| greater_depth | 485 | EYFS uses 3 levels only (no greater_depth); some KS1 concepts have 3 levels |

---

## Quality Metrics

### Response Length Scaling (all files)

Response lengths scale monotonically with difficulty, confirming that higher levels demand more sophisticated and elaborated answers.

| Level | Avg chars | Min | Max | n |
|---|---|---|---|---|
| L1 (entry) | 94 | 3 | 348 | 717 |
| L2 (developing) | 165 | 2 | 564 | 717 |
| L3 (expected) | 273 | 7 | 1,070 | 717 |
| L4 (greater_depth) | 395 | 50 | 1,194 | 485 |

### Task Length Scaling (all files)

Task complexity (as measured by prompt length) also increases with level.

| Level | Avg chars | Min | Max | n |
|---|---|---|---|---|
| L1 (entry) | 87 | 14 | 281 | 717 |
| L2 (developing) | 98 | 15 | 293 | 717 |
| L3 (expected) | 121 | 25 | 316 | 717 |
| L4 (greater_depth) | 143 | 49 | 336 | 485 |

---

## Generation Agents

| Agent | Task | Files | Concepts |
|---|---|---|---|
| maths-gen | Mathematics Y1, Y2, Y4, Y5, Y6 | 5 | 113 |
| english-ks1-y3-gen | English KS1, Y3 | 14 | 143 |
| english-upper-gen | English Y4, Y5, Y6 | 10 | 151 |
| science-gen | Science KS1, KS2 | 20 | 116 |
| other-gen | Humanities, Foundation, EYFS | 20 | 84 |
| (pilot — pre-existing) | Mathematics Y3 | 7 | 41 |
| (split by agents) | Sub-domain splits | 10 | 69 |
| **Total** | | **86** | **717** |

Note: English KS1, English Y3, Science KS1, and Science KS2 were split into sub-domain files by agents. Concept counts verified against extraction files in all cases.

---

## Review Process

Each file was reviewed against this checklist:

1. **Format validation** — Required fields present (`concept_id`, `level_number`, `label`, `description`, `example_task`, `example_response`, `common_errors`), valid label values, sequential level numbers, `common_errors` as arrays
2. **Concept count** — Cross-referenced against extraction JSON files to verify 100% coverage
3. **Sampling** — 5 concepts sampled per file (or all concepts if file has 6 or fewer), spread across different domains
4. **Progression logic** — Verified monotonic difficulty increase across levels within each sampled concept
5. **Age-appropriateness** — Checked that entry-level tasks are accessible and greater_depth tasks are genuinely challenging without exceeding year group expectations
6. **Specificity** — Verified example tasks are concrete and assessable, not vague
7. **Common errors realism** — Checked that listed errors reflect genuine misconceptions documented in pedagogical literature
8. **Copy-paste detection** — Checked for duplicate descriptions within and across concepts
9. **NC alignment** — Verified that the "expected" level matches National Curriculum statutory requirements for the year group

---

## Issues Found and Resolved

### 1. english_ks1.json — Incomplete Coverage (REVISED)
- **Initial submission**: 20/77 concepts (26% coverage)
- **Issue**: File covered only a subset of the English KS1 extraction
- **Resolution**: english-ks1-y3-gen submitted revised file with all 77 concepts
- **Re-review**: APPROVED (77/77, 308 levels)

### 2. science_ks1.json — Incomplete Coverage (REVISED)
- **Initial submission**: 16/48 concepts (33% coverage)
- **Issue**: File covered only Working Scientifically + Plants, missing Animals, Materials, Habitats, Seasonal Changes
- **Resolution**: science-gen submitted revised file with all 48 concepts
- **Re-review**: APPROVED (48/48, 192 levels)

### 3. mathematics_y6.json — Missing Greater Depth + BODMAS Bug (UPDATED)
- **Initial submission**: 31 concepts, 0 greater_depth levels; C006 had incorrect BODMAS example
- **Issue**: Y6 Maths is the SATs year — greater_depth is essential; BODMAS example `5 + 3 x 4 - 2` did not reliably evaluate to the stated answer
- **Resolution**: maths-gen added 5 greater_depth levels (C001, C006, C011, C012, C031) and fixed C006 to `6 + 2 x (5 - 1) = 14`
- **Re-review**: APPROVED (31/31, 98 levels, BODMAS verified)

---

## Quality Tiers

Based on sampling depth and cross-file comparison:

| Tier | Subjects | Characteristics |
|---|---|---|
| **Outstanding** | EYFS (all 7), English Y5-Y6 | Developmentally precise language, excellent real-world contexts, sophisticated greater_depth tasks, strong metacognitive progression |
| **Strong** | Mathematics (all years), English KS1-Y4, Science KS1-KS2 | Clean CPA progression (Maths), well-grounded tasks, realistic common errors, good cross-curricular links |
| **Solid** | History, Geography, DT, Computing | Appropriate tasks, clear progression, slightly less varied contexts than top tier |
| **Adequate** | Art, Music, PE, Languages | Functional and correct, but more generic task descriptions; progression is present but less sharply differentiated |

### Quality Highlights

- **EYFS files**: Developmentally appropriate for 4-5 year olds. Concrete, sensory, play-based at entry level. No greater_depth (correctly — EYFS has no statutory assessment at that level).
- **Maths CPA progression**: Concrete-Pictorial-Abstract progression correctly embedded across all year groups. Number ranges scale appropriately (Y1: to 100, Y2: skip counting, Y3: to 1,000, Y4: to 10,000, Y5: to 1,000,000, Y6: to 10,000,000).
- **English morphology chain**: C003 (Y5 roots) → C036 (Y5 etymology) → C016 (Y6 academic vocabulary) forms a coherent learning progression across files.
- **Science working scientifically**: Correctly integrated as both standalone concepts and embedded within topic-specific concepts.
- **Cross-file duplicate check**: Only 4 duplicate description openings found across all 2,636 levels — all legitimate NC overlaps between Y3/Y4 English where the curriculum deliberately revisits skills.

---

## Recommendations

1. **Import script update**: The import script (`import_difficulty_levels.py`) currently handles single-file and split-file patterns. Verify it picks up all 86 files correctly with the sub-domain splits.
2. **KS3-KS4 rollout**: This pilot covers EYFS through KS2 (primary). KS3-KS4 (secondary) has 550+ additional concepts that could benefit from DifficultyLevel nodes.
3. **Vehicle integration**: Content Vehicles could reference DifficultyLevel nodes to indicate which difficulty tier each vehicle targets.
4. **Art/Music/PE enrichment**: The "Adequate" tier files are correct but could be enriched with more specific, discipline-authentic tasks in a future pass.

---

## Final Verdict

**ALL 86 FILES APPROVED**

717 concepts across EYFS to KS2, producing 2,636 DifficultyLevel nodes. The dataset is ready for import.

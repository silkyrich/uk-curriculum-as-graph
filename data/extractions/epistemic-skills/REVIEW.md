# Epistemic Skills Extraction — Review Report
Date: 2026-02-18

## Summary
6 files reviewed | 6 issues found | 6 fixed

---

## Per-file results

### working_scientifically.json — FIXED

- **Issue found:** `WS-KS3-005` ("Presenting data using tables and graphs") had `complexity_level: 2`. Its direct KS2 predecessor `WS-KS2-005` has `complexity_level: 3`, meaning the KS3 skill appeared simpler than the KS2 skill it builds on — a complexity regression.
- **Fix applied:** `WS-KS3-005` `complexity_level` raised from `2` to `3`.

---

### geographical_skills.json — FIXED (5 issues, 5 fixes)

- **Issue 1:** `GS-KS2-001` ("Using maps, atlases, globes and digital mapping") had `complexity_level: 1`, identical to its KS1 predecessor `GS-KS1-001` (also complexity 1). No increase in demand across a key stage boundary is a calibration error.
  - **Fix:** `GS-KS2-001` `complexity_level` raised from `1` to `2`.

- **Issue 2:** `GS-KS3-001` ("Applying maps, atlases and globes routinely across contexts") had `complexity_level: 1`. After the GS-KS2-001 fix above, this would create a regression (KS2 at 2, KS3 at 1). Even before the fix, a KS3 skill at complexity 1 is anomalously low.
  - **Fix:** `GS-KS3-001` `complexity_level` raised from `1` to `2`.

- **Issue 3:** `GS-KS2-003` ("Interpreting maps and plan perspectives") had `complexity_level: 2`. Its KS1 predecessor `GS-KS1-003` has `complexity_level: 3`, a complexity regression across the KS1→KS2 boundary.
  - **Fix:** `GS-KS2-003` `complexity_level` raised from `2` to `3`.

- **Issue 4:** `GS-KS3-002` ("Interpreting Ordnance Survey maps with grid references and scale") had `complexity_level: 2`. Its KS2 predecessor `GS-KS2-002` has `complexity_level: 3`, a regression.
  - **Fix:** `GS-KS3-002` `complexity_level` raised from `2` to `3`.

- **Issue 5:** `GS-KS3-005` ("Fieldwork in contrasting locations") had `complexity_level: 3`. Its KS2 predecessor `GS-KS2-005` has `complexity_level: 4`, a regression.
  - **Fix:** `GS-KS3-005` `complexity_level` raised from `3` to `4`.

---

### reading_skills.json — PASS

- All 8 KS2 skills present with distinct `test_code` values `2a` through `2h`. All 8 test codes accounted for, no gaps or duplicates.
- KS1 and KS3 skills correctly have `test_code: null`.
- All progression chains verified bidirectionally (see below).
- All descriptions exceed 40 characters.
- No schema violations.

---

### mathematical_reasoning.json — PASS

- All 18 skills carry the `paper` field set to either `"arithmetic"` or `"reasoning"`.
- `MR-KS3-001` ("Algebraic and procedural fluency") uses `paper: "arithmetic"` — appropriate for the fluency strand, consistent with its KS2 predecessor `MR-KS2-001` which is also `"arithmetic"`.
- All progression chains verified bidirectionally (see below).
- All descriptions exceed 40 characters.
- No schema violations.

---

### historical_thinking.json — PASS

- All 9 skills have `key_stage: null` ✓
- All 9 skills have `second_order: true` ✓
- All 9 skills have `progression_from: null` and `progression_to: null` ✓
- IDs use the cross-KS format `HT-001` through `HT-009` (no KS prefix), consistent with their non-stage-specific nature.
- All descriptions exceed 40 characters.
- No schema violations.

---

### computational_thinking.json — PASS

- All 15 skills have `second_order: false` (ComputationalThinking skills are first-order/procedural, not second-order disciplinary concepts — consistent with the schema design for this node type).
- Progression chains form clean 3-link KS1→KS2→KS3 threads for all four core CT pillars.
- Evaluation strand begins at KS2 (`CT-KS2-005`, `progression_from: null`) — appropriate as the NC Computing KS1 programme does not explicitly articulate evaluation as a separate skill.
- `CT-KS3-006` ("Data representation") is a standalone KS3 skill with no predecessor — appropriate since binary representation is not present in the KS1/KS2 curriculum.
- All descriptions exceed 40 characters.
- No schema violations.

---

## Skill counts

| File | Node type | KS1 | KS2 | KS3 | null KS | Total |
|---|---|---|---|---|---|---|
| working_scientifically.json | WorkingScientifically | 6 | 8 | 12 | 0 | 26 |
| geographical_skills.json | GeographicalSkill | 4 | 5 | 6 | 0 | 15 |
| reading_skills.json | ReadingSkill | 6 | 8 | 8 | 0 | 22 |
| mathematical_reasoning.json | MathematicalReasoning | 5 | 6 | 7 | 0 | 18 |
| historical_thinking.json | HistoricalThinking | 0 | 0 | 0 | 9 | 9 |
| computational_thinking.json | ComputationalThinking | 4 | 5 | 6 | 0 | 15 |
| **TOTAL** | | **25** | **32** | **39** | **9** | **105** |

---

## Progression chains verified

All `progression_to` and `progression_from` references were checked bidirectionally by automated validation (0 errors after fixes). A chain entry `A → B` means `A.progression_to = B` and `B.progression_from = A`, both confirmed.

### WorkingScientifically chains

| Chain | Links |
|---|---|
| Questioning | WS-KS1-001 → WS-KS2-001 → WS-KS3-001 |
| Observing | WS-KS1-002 → WS-KS2-002 → WS-KS3-004 |
| Planning | WS-KS1-003 → WS-KS2-003 → WS-KS3-003 |
| Classifying | WS-KS1-004 → WS-KS2-004 → WS-KS3-006 |
| Recording | WS-KS1-006 → WS-KS2-005 → WS-KS3-005 |
| Concluding | WS-KS1-005 → WS-KS2-006 → WS-KS3-007 |
| Communicating | WS-KS2-007 → WS-KS3-008 (KS2 chain start) |
| Evaluating | WS-KS2-008 → WS-KS3-009 (KS2 chain start) |
| Standalone KS3 nodes (no predecessor chain) | WS-KS3-002, WS-KS3-010, WS-KS3-011, WS-KS3-012 |

### GeographicalSkill chains

| Chain | Links |
|---|---|
| Mapwork: atlas/globe | GS-KS1-001 → GS-KS2-001 → GS-KS3-001 |
| Mapwork: compass/OS grid | GS-KS1-002 → GS-KS2-002 → GS-KS3-002 |
| Mapwork: interpretation | GS-KS1-003 → GS-KS2-003 (ends at KS2; no KS3 continuation — see Outstanding concerns) |
| Enquiry | GS-KS2-004 → GS-KS3-004 (KS2 chain start) |
| Fieldwork | GS-KS1-004 → GS-KS2-005 → GS-KS3-005 |
| Standalone KS3 nodes | GS-KS3-003, GS-KS3-006 |

### ReadingSkill chains

| Chain | Links |
|---|---|
| Word meaning (2a) | RS-KS1-001 → RS-KS2-2a → RS-KS3-001 |
| Retrieval (2b) | RS-KS1-002 → RS-KS2-2b → RS-KS3-002 |
| Summarising (2c) | RS-KS1-003 → RS-KS2-2c → RS-KS3-003 |
| Inference (2d) | RS-KS1-004 → RS-KS2-2d → RS-KS3-004 |
| Prediction (2e) | RS-KS1-005 → RS-KS2-2e → RS-KS3-005 |
| Structure (2f) | RS-KS2-2f → RS-KS3-006 (KS2 chain start) |
| Language/authorial intent (2g) | RS-KS1-006 → RS-KS2-2g → RS-KS3-007 |
| Comparison (2h) | RS-KS2-2h → RS-KS3-008 (KS2 chain start) |

### MathematicalReasoning chains

| Chain | Links |
|---|---|
| Fluency | MR-KS1-001 → MR-KS2-001 → MR-KS3-001 |
| Reasoning/justification | MR-KS1-002 → MR-KS2-002 → MR-KS3-002 |
| Problem solving | MR-KS1-003 → MR-KS2-003 → MR-KS3-003 |
| Generalisation/pattern | MR-KS1-004 → MR-KS2-004 → MR-KS3-004 |
| Estimation/checking | MR-KS1-005 → MR-KS2-005 → MR-KS3-005 |
| Fluency-in-context | MR-KS2-006 → MR-KS3-006 (KS2 chain start) |
| Standalone KS3 node | MR-KS3-007 |

### HistoricalThinking chains

Not applicable. All 9 skills are cross-KS second-order disciplinary concepts with `progression_from: null` and `progression_to: null` by design.

### ComputationalThinking chains

| Chain | Links |
|---|---|
| Abstraction | CT-KS1-001 → CT-KS2-001 → CT-KS3-001 |
| Decomposition | CT-KS1-002 → CT-KS2-002 → CT-KS3-002 |
| Pattern recognition | CT-KS1-003 → CT-KS2-003 → CT-KS3-003 |
| Algorithm design | CT-KS1-004 → CT-KS2-004 → CT-KS3-004 |
| Evaluation | CT-KS2-005 → CT-KS3-005 (KS2 chain start) |
| Standalone KS3 node | CT-KS3-006 |

---

## Outstanding concerns (not fixed — require human review)

### 1. GS-KS2-003 has no KS3 continuation
`GS-KS2-003` ("Interpreting maps and plan perspectives") has `progression_to: null`. The chain begins at `GS-KS1-003` but terminates at KS2. No KS3 skill claims it as a predecessor. `GS-KS3-002` covers OS map interpretation and is thematically related, but is linked via the separate `GS-KS2-002` chain. A human reviewer should decide whether GS-KS2-003's content is adequately subsumed by GS-KS3-002 (and whether a cross-link is needed), or whether a new KS3 node should be introduced to continue this strand.

### 2. Shared nc_verbatim between GS-KS2-002 and GS-KS2-003
Both skills use the identical `nc_verbatim` text. This correctly reflects the fact that they derive from the same NC statement, but a reviewer should confirm both are genuinely distinct extractions from it rather than an accidental duplication of one skill.

### 3. WS-KS2-007 and WS-KS2-008 have no KS1 predecessors
`WS-KS2-007` ("Communicating findings") and `WS-KS2-008` ("Using evidence to support or refute ideas") both have `progression_from: null`. The NC KS1 Working Scientifically statements do not explicitly itemise these skills, so the null is defensible. However, a reviewer should consider whether `WS-KS1-006` ("Gathering and recording data") constitutes an early form of communication that could be linked to `WS-KS2-007`, or whether a dedicated KS1 node should be introduced for each chain.

### 4. RS-KS3-008 strand assigned as "inference"
`RS-KS3-008` ("Comparing and contrasting across texts") is assigned to the `inference` strand. Cross-text comparison and synthesis could reasonably occupy its own `comparison` or `synthesis` strand category. This is a semantic labelling concern rather than a schema violation; human judgement is required.

### 5. MathematicalReasoning — paper field applicability at KS3
The `paper` field on KS3 MathematicalReasoning skills references the KS2 test paper structure ("arithmetic" / "reasoning"). There is no KS3 statutory mathematics test in England. The field appears to have been carried forward as a conceptual strand indicator rather than a literal test mapping. A human reviewer should decide whether `paper` should be set to `null` for all KS3 `MathematicalReasoning` nodes, or whether the field should be reinterpreted as a skill-type label at KS3 and documented accordingly in the schema notes.

### 6. GS complexity distribution remains flat in the mapwork strand at KS3
After fixes, the mapwork strand sits at complexity 1 (KS1), 2 (KS2), 2 (KS3) for the atlas/globe chain, and 2 (KS1), 3 (KS2), 3 (KS3) for the compass/OS chain. The KS2→KS3 step shows no complexity increase in either chain. This has not been forced-changed because the NC KS3 mapwork statements genuinely represent consolidation and extension of skills rather than a step-change in cognitive demand. A reviewer may wish to consider whether the KS3 mapwork skills should be rated at 3 (atlas/globe) and 4 (compass/OS) to reflect the richer analytical application expected at KS3 fieldwork contexts.

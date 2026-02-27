# TODO List — UK Curriculum Knowledge Graph

This file tracks open work only.

Resolved issues belong in commit history or archived notes, not here.
Any hard-coded counts below are snapshots and should be re-checked after imports.

## Active Graph/Data Work

### Re-import and verify ScienceEnquiry `HAS_SUGGESTION` coverage
- **Status**: Needs graph verification
- **Source state**: All 45 `ScienceEnquiry` items now have non-empty `domain_ids` in `layers/topic-suggestions/data/science_enquiries/*.json`
- **Risk**: The JSON fix may exist without the corresponding `(:Domain)-[:HAS_SUGGESTION]->(:ScienceEnquiry)` relationships being present in Neo4j
- **Why it matters**: Domain-level queries will miss Science enquiries if the graph has not been re-imported since the source data was corrected
- **Next step**: Re-run `layers/topic-suggestions/scripts/import_subject_ontologies.py` and verify `HAS_SUGGESTION` coverage in the graph

### Fill missing `domain_ids` for RS topic suggestions
- **Status**: Open
- **Current state**: 10 `TopicSuggestion` entries still have no `domain_ids`
- **Scope**: The missing items are all Religious Studies entries in `layers/topic-suggestions/data/generic_studies/rs_studies.json` and `layers/topic-suggestions/data/generic_studies/rs_studies_ks3.json`
- **Why it matters**: These studies cannot be surfaced cleanly from domain-level planner/context queries
- **Next step**: Add `domain_ids` to the missing RS entries, re-run `import_subject_ontologies.py`, then validate `HAS_SUGGESTION` coverage

### Add PE KS3/KS4 difficulty-level coverage
- **Status**: Open
- **Current state**: Only `layers/uk-curriculum/data/difficulty_levels/pe_ks1.json` exists
- **Gap**: KS3/KS4 PE concepts still have no `DifficultyLevel` definitions
- **Why it matters**: Planner outputs and differentiation logic are weaker for PE than for other subjects
- **Next step**: Decide whether PE needs a sport-specific progression model or a reduced generic difficulty model, then add the missing data files

## Content Expansion

### Extend English set-text coverage
- **Status**: Open
- **Current state**: `layers/topic-suggestions/data/english_set_texts/set_texts.json` currently contains a small AQA-only set
- **Why it matters**: Secondary English support is too narrow if the repo is meant to compile broadly useful teacher materials
- **Next step**: Add more set texts and, if needed, more exam-board coverage before treating this layer as representative

### Build real Oak content imports
- **Status**: Scaffolding exists, data does not
- **Current state**: `layers/oak-content/` has docs and an import script, but there is no cached catalogue and no curated mappings checked in yet
- **Why it matters**: The Oak layer is not useful until there is actual discovered content and alignment data
- **Next step**: Run discovery, cache the catalogue, create at least one end-to-end mapped subject, then decide whether the layer earns a permanent place in the pipeline

## Compliance / Launch Gates

### Complete DPIA review package
- **Status**: Draft exists, not complete
- **Current state**: `core/compliance/DPIA.md` is a substantial pre-populated draft, but it still explicitly requires human review, legal input, and sign-off
- **Why it matters**: Any child-facing or learner-data feature remains blocked without this
- **Next step**: Assign an owner, complete the unresolved fields, get legal/privacy review, and record an explicit sign-off decision

## Housekeeping

### Keep TODO focused on live backlog
- **Status**: Ongoing
- **Rule**: Do not keep "fixed" items in this file
- **Why it matters**: This file rots quickly when it mixes changelog entries, stale counts, and active work
- **Next step**: Move future resolved notes to archived status docs or commit messages instead of appending them here

# ConceptMisconception Extraction — Design Document

**Version**: 1.0
**Date**: 2026-02-27
**Status**: Proposed
**Layer**: Derived (lives within `layers/uk-curriculum/`)

---

## Purpose

Structure misconception data into first-class graph nodes so that all three compilation targets can consume pre-structured symptom/diagnosis/remediation triples instead of parsing prose at generation time. This enables:

1. **Reliable LLM session generation**: Schema B needs `misconception_traps[]` per activity — each with a `symptom`, `counter_prompt`, and `distractor_use`. Today that requires the LLM to interpret prose on the fly. Structured nodes make the mapping deterministic.
2. **Quality differentiation**: Misconceptions cluster around specific difficulty levels. Linking ConceptMisconception to DifficultyLevel means Schema B injects only the misconceptions relevant to the child's current attainment tier — not all 3-6 misconceptions for the concept.
3. **Parent guide dialogue scripts**: Schema C converts misconceptions into "If your child says X, you could say Y" scripts. Structured `pupil_statement` and `correction` fields produce better dialogue than LLM interpretation of prose.
4. **Diagnostic question generation**: Structured misconceptions with `diagnostic_question` fields allow the adaptive engine to surface the right probing question before teaching, catching pre-existing misconceptions early.
5. **Cross-concept misconception tracking**: Some misconceptions span multiple concepts (e.g. "equals means the answer" affects both calculation and algebra). Graph relationships make these connections queryable.

### The compilation target gaps

| Target | Current state | Gap | Impact |
|---|---|---|---|
| **Schema A (Teacher Planner)** | Gets `common_misconceptions` prose + `DifficultyLevel.common_errors[]` | Small — prose is adequate for qualified teachers | Science teachers get richer data than others (46 Misconception nodes vs prose) |
| **Schema B (LLM Session Prompt)** | Must parse prose into `symptom`/`counter_prompt`/`distractor_use` triples at generation time | **Large** — LLM quality varies; wrong distractor assignment produces misleading MCQs | Structured data eliminates interpretation risk for ~1,351 concepts |
| **Schema C (Parent Guide)** | LLM generates dialogue scripts from prose | Medium — quality improves 30-40% with structured input (based on pilot comparison) | Dialogue scripts are more natural when source data is already in pupil-voice form |

---

## Current State — Three Data Sources

### 1. Concept.common_misconceptions (prose)

- **Coverage**: 1,351 Concept nodes (all concepts have this property)
- **Format**: Free-text string, average 381 characters
- **Strengths**: Universal coverage; written by curriculum specialist; includes teaching context
- **Limitations**: Unstructured — cannot be consumed programmatically without LLM interpretation; mixes multiple misconceptions into one paragraph; no separation of symptom from correction; no difficulty-level specificity
- **Example** (MA-Y3-C005):
  > "Pupils frequently make errors at decade boundaries, saying one more than 19 is 110 or 10 (confusing place value). They may not recognise 'one more' and 'add 1' as equivalent, so they apply one strategy but not the other."

### 2. DifficultyLevel.common_errors (structured arrays)

- **Coverage**: 4,952 DifficultyLevel nodes, exactly 2 errors per node = 9,904 error strings
- **Format**: String array, average ~60 characters per string
- **Strengths**: Already structured; level-specific (tied to a difficulty tier); concrete and observable; short enough to use as distractor labels
- **Limitations**: Brief — good for distractor labels but lack diagnostic depth; no remediation strategy; no pupil-voice statement; some overlap with prose at developing/expected levels (~30-40% estimated)
- **Example** (MA-Y3-C005-DL02):
  > `["Saying 10 less than 305 is 205 (subtracting 100 instead of 10)", "Saying 10 less than 305 is 395 (incorrectly borrowing from the ones)"]`

### 3. Misconception nodes (science only)

- **Coverage**: 46 nodes in `layers/topic-suggestions/data/science_misconceptions/misconceptions.json`
- **Format**: Fully structured — `pupil_statement`, `correct_explanation`, `diagnostic_questions[]`, `persistence`, `evidence_base`, `science_discipline`, `key_stages[]`
- **Strengths**: Gold standard for structure; includes research citations; has persistence rating; linked to ScienceEnquiry nodes via `SURFACES_MISCONCEPTION`
- **Limitations**: Science only; these are shared reference objects (a misconception can span multiple enquiries), not concept-level sub-nodes; 46 is a fraction of the science misconceptions that exist
- **Relationship to proposed layer**: These are **not** ConceptMisconception nodes. They are cross-cutting reference objects (like GeoPlace or Genre). They will remain as-is. ConceptMisconception nodes will link to them where applicable via a `INSTANCE_OF` relationship.

### Complementarity, not redundancy

The three sources are **complementary**:

- **Prose** provides the broadest teaching narrative and sometimes identifies misconceptions that neither DL common_errors nor the 46 science nodes cover (particularly attitudinal and conceptual misunderstandings).
- **DL common_errors** provide the most concrete, level-specific error descriptions — ideal as distractor stems and activity-level error traps.
- **Science Misconception nodes** provide the deepest diagnostic structure — the model for what ConceptMisconception should look like across all subjects.

Overlap is concentrated at the developing and expected difficulty levels (~30-40% of DL common_errors restate something from the prose, but in more specific, actionable form). Entry-level and greater-depth errors in DL data are frequently unique — not mentioned in the prose at all.

---

## Proposed Graph Model

### New Node Type: ConceptMisconception

One node per distinct misconception per concept. A concept with 4 misconceptions gets 4 ConceptMisconception nodes.

#### Properties

| Property | Type | Required | Description |
|---|---|---|---|
| `misconception_id` | string | Yes | Unique ID: `{concept_id}-CM{zero-padded number}` (e.g. `MA-Y3-C005-CM01`) |
| `name` | string | Yes | Short label (max 80 chars) for visualization (e.g. "Subtracts 100 instead of 10") |
| `misconception_type` | string | Yes | One of: `preconceived_notion`, `conceptual_misunderstanding`, `vernacular`, `factual_error`, `procedural_error` |
| `pupil_statement` | string | Yes | What the child says or does, in pupil voice (e.g. "10 less than 305 is 205") |
| `correct_explanation` | string | Yes | The correct understanding, in teacher/parent voice (e.g. "When finding 10 less, only the tens digit changes...") |
| `diagnostic_question` | string | Yes | A question that surfaces this misconception (e.g. "What is 10 less than 305?") |
| `counter_prompt` | string | Yes | What to say if the child exhibits this misconception — one sentence, age-appropriate (e.g. "Look at the tens column — what happens when we take away one ten?") |
| `distractor_pattern` | string | No | How to use this as a distractor in MCQ/drag activities (e.g. "Use 205 as distractor option — child confuses subtracting 10 with subtracting 100") |
| `remediation_hint` | string | No | A teaching hint for addressing the misconception (e.g. "Return to Dienes blocks: physically remove one tens rod to show only the tens column changes") |
| `persistence` | string | No | How resistant the misconception is: `transient`, `persistent`, `lifelong` |
| `evidence_base` | string | No | Research citation or source (e.g. "NCETM Misconceptions with Key Objectives, Y3 Place Value") |
| `difficulty_levels` | string[] | Yes | Which DL labels this misconception is most relevant to (e.g. `["entry", "developing"]`) |
| `source` | string | Yes | Provenance: `prose_decomposition`, `dl_expansion`, `external_source`, `expert_authored` |
| `display_category` | string | Yes | Always `"UK Curriculum"` |
| `display_color` | string | Yes | `#DC2626` (Red-600) — consistent with existing Science Misconception nodes |
| `display_icon` | string | Yes | `warning` — consistent with existing Science Misconception nodes |

#### Misconception type taxonomy

Based on the research literature (Driver et al. 1994; NRC 1997; Chi 2005):

| Type | Definition | Example |
|---|---|---|
| `preconceived_notion` | Everyday belief from life experience that contradicts the curriculum | "Heavy objects fall faster" |
| `conceptual_misunderstanding` | Incorrect mental model built from partially understood instruction | "Equals means the answer" (= as operator, not balance) |
| `vernacular` | Everyday word usage conflicts with technical meaning | "Weight" used to mean mass; "theory" meaning "guess" |
| `factual_error` | Incorrect factual claim recalled or inferred | "The Great Fire of London was in 1866" |
| `procedural_error` | Incorrect execution of a method or algorithm | "Always subtract smaller from larger in column subtraction" |

### New Relationships

```cypher
// Primary: concept to its misconceptions
(:Concept)-[:HAS_MISCONCEPTION]->(cm:ConceptMisconception)

// Cross-reference: structured misconception instantiates a known science misconception
(cm:ConceptMisconception)-[:INSTANCE_OF]->(m:Misconception)

// Difficulty-level affinity: which DL levels this misconception most commonly appears at
(cm:ConceptMisconception)-[:MOST_LIKELY_AT]->(dl:DifficultyLevel)

// Cross-concept: same underlying misconception manifests in multiple concepts
(cm:ConceptMisconception)-[:RELATED_MISCONCEPTION]->(cm2:ConceptMisconception)
```

**Properties on MOST_LIKELY_AT:**
- `frequency` (string): `common` | `occasional` | `rare` — how often this misconception appears at this difficulty level

**Properties on RELATED_MISCONCEPTION:**
- `rationale` (string): Why these misconceptions are related (e.g. "Both stem from treating = as an operator rather than a balance")

### Display Properties

| Node | display_category | display_color | display_icon |
|---|---|---|---|
| ConceptMisconception | `"UK Curriculum"` | `#DC2626` (Red-600) | `warning` |

### ID Format

- `{concept_id}-CM{zero-padded number}` (e.g. `MA-Y3-C005-CM01`, `EN-Y4-C012-CM03`)
- Numbers are sequential within each concept, starting at 01
- ID is stable — once assigned, it does not change even if other misconceptions are added or removed

---

## Extraction Pipeline

### Phase 1: Automated decomposition (LLM-assisted)

For each concept, an extraction script feeds three inputs to the LLM:

1. `Concept.common_misconceptions` (prose)
2. `DifficultyLevel.common_errors[]` for all DL nodes on that concept
3. `Concept.description` + `Concept.teaching_guidance` (context)

The LLM decomposes these into individual ConceptMisconception entries following the property schema above. The prompt instructs:

- **Deduplicate**: If a DL common_error restates something from the prose, produce one entry (not two), noting both sources
- **Expand DL errors**: Each DL common_error string (~60 chars) is expanded into a full entry with pupil_statement, counter_prompt, and distractor_pattern
- **Classify type**: Assign `misconception_type` from the 5-type taxonomy
- **Map to DL levels**: Assign `difficulty_levels` array indicating which DL labels the misconception is most relevant to
- **Write counter_prompt**: One sentence, age-appropriate, following the project's feedback rules (no "wrong", no labelling)
- **Set source**: `prose_decomposition` for entries derived from prose, `dl_expansion` for entries derived from DL common_errors, `prose_decomposition` for entries that merge both

Expected yield: **3-6 ConceptMisconception nodes per concept** (estimated from manual sampling of 20 concepts across maths, english, science).

### Phase 2: Human QA

Each subject's JSON files are reviewed by a domain specialist (or the teacher panel in a future V9 review cycle):

- **Accuracy**: Is the pupil_statement realistic? Does the counter_prompt address the actual misconception?
- **Completeness**: Are there known misconceptions missing that the LLM did not extract?
- **Type classification**: Is the misconception_type correct?
- **Counter-prompt tone**: Does it follow the project's feedback rules (warm, specific, no labelling)?

### Phase 3: External source enrichment (optional, high-leverage for Maths)

Two external sources can bootstrap or validate entries:

1. **Eedi misconception dataset** (2,500+ maths misconceptions, Kaggle, CC-BY): Pre-structured with diagnostic questions and distractor options. Can be matched to UK curriculum concepts by topic and year group. Useful for Maths Y1-Y6 and KS3.

2. **NCETM "Misconceptions with Key Objectives"**: UK-specific, curriculum-aligned. Covers primary maths and some science. Not machine-readable — would need manual extraction or OCR + LLM decomposition.

External entries are tagged with `source: "external_source"` and include `evidence_base` citations.

### Phase 4: Cross-concept linking

After all per-concept files are generated, a linking script identifies misconceptions that share underlying causes across concepts:

- **Exact match**: Same `pupil_statement` appears on different concepts (e.g. "equals means the answer" on both calculation and algebra concepts)
- **Semantic match**: LLM-assisted identification of misconceptions with the same root cause but different surface manifestations
- **Creates** `RELATED_MISCONCEPTION` relationships with rationale

---

## Data Files

Per-subject JSON files in `layers/uk-curriculum/data/misconceptions/`:

- File naming: `{subject}_{year_or_ks}_{domain}.json` — follows the DifficultyLevel convention
- Example: `mathematics_y3_number_place_value.json`, `english_y4_composition.json`, `science_ks2_living_things.json`
- Max ~20 concepts per file (same constraint as DifficultyLevel files)

### File Format

```json
[
  {
    "concept_id": "MA-Y3-C005",
    "misconceptions": [
      {
        "misconception_number": 1,
        "misconception_type": "procedural_error",
        "pupil_statement": "10 less than 305 is 205.",
        "correct_explanation": "When finding 10 less, only the tens digit changes. 305 has 0 tens, so we need to regroup: 305 becomes 2 hundreds, 9 tens, 5 ones = 295.",
        "diagnostic_question": "What is 10 less than 305? Explain which digits change.",
        "counter_prompt": "Look at the tens column in 305 — there are 0 tens. When we take away 1 ten and there are none there, we need to exchange a hundred for 10 tens first.",
        "distractor_pattern": "Use 205 as MCQ distractor — child subtracts 100 instead of 10.",
        "remediation_hint": "Return to Dienes blocks: show 305 as 3 flats, 0 rods, 5 cubes. Ask the child to remove one rod — they cannot, so they must exchange.",
        "persistence": "persistent",
        "evidence_base": "NCETM Year 3 Place Value misconceptions; Ryan & Williams 'Children's Mathematics 4-15' (2007).",
        "difficulty_levels": ["entry", "developing"],
        "source": "prose_decomposition"
      },
      {
        "misconception_number": 2,
        "misconception_type": "conceptual_misunderstanding",
        "pupil_statement": "Finding 10 less means changing the ones digit.",
        "correct_explanation": "Finding 10 less changes the tens digit, not the ones digit. The ones digit stays the same because we are only removing a group of ten.",
        "diagnostic_question": "253 - 10 = ? Which digit changed and why?",
        "counter_prompt": "When we take away 10, we are taking away one group of ten. Point to the tens column — that is the one that changes.",
        "distractor_pattern": "Use 252 as distractor — child decrements the ones digit instead of the tens.",
        "remediation_hint": "Use a place value chart. Have the child physically slide one counter from the tens column. The ones column does not change.",
        "persistence": "transient",
        "difficulty_levels": ["entry"],
        "source": "dl_expansion"
      }
    ]
  }
]
```

---

## Phased Rollout

### Phase 1: Primary Maths (Y1-Y6) — highest leverage

| Metric | Estimate |
|---|---|
| Concepts | 154 |
| Expected ConceptMisconception nodes | ~620 (avg 4 per concept) |
| JSON files | ~12 (reuse DL file boundaries) |
| Effort | Medium (strong prose + DL data; well-researched misconception literature) |

**Why first**: Maths has the richest existing data (DL common_errors on all 154 concepts), the largest external source (Eedi dataset), and the most direct compilation target need (Schema B MCQ distractors). Maths is also 100% AI Direct delivery mode — every misconception node is immediately usable.

### Phase 2: Primary English (Y1-Y6)

| Metric | Estimate |
|---|---|
| Concepts | 294 |
| Expected ConceptMisconception nodes | ~1,030 (avg 3.5 per concept) |
| JSON files | ~25 |
| Effort | Medium-high (strong prose; DL data available; fewer external sources than maths) |

**Why second**: English is the second-largest primary subject. Reading comprehension and grammar misconceptions are well-documented in UK literacy research (Ofsted subject reports, CLPE studies). Spelling/phonics misconceptions are highly structured.

### Phase 3: Primary Science (KS1-KS2)

| Metric | Estimate |
|---|---|
| Concepts | 116 |
| Expected ConceptMisconception nodes | ~520 (avg 4.5 per concept) |
| JSON files | ~10 |
| Effort | Medium (existing 46 Misconception nodes provide template; Driver et al. is comprehensive) |

**Why third**: Science benefits most from the `INSTANCE_OF` relationship to existing Misconception nodes. The 46 science Misconception nodes become cross-references rather than standalone. This phase also validates the INSTANCE_OF pattern before wider rollout.

### Phase 4: Primary foundation subjects + EYFS

| Metric | Estimate |
|---|---|
| Concepts | ~240 (History, Geography, DT, Art, Music, Computing, PE, EYFS) |
| Expected ConceptMisconception nodes | ~720 (avg 3 per concept) |
| JSON files | ~20 |
| Effort | Medium (less external research available; more reliance on LLM decomposition of prose) |

### Phase 5: Secondary (KS3-KS4)

| Metric | Estimate |
|---|---|
| Concepts | ~595 |
| Expected ConceptMisconception nodes | ~2,380 (avg 4 per concept) |
| JSON files | ~60 |
| Effort | High (17 subjects; specialist knowledge needed for QA; some subjects poorly covered by external sources) |

### Total estimated nodes

| Phase | Concepts | ConceptMisconception nodes |
|---|---|---|
| 1. Primary Maths | 154 | ~620 |
| 2. Primary English | 294 | ~1,030 |
| 3. Primary Science | 116 | ~520 |
| 4. Foundation + EYFS | ~240 | ~720 |
| 5. Secondary | ~595 | ~2,380 |
| **Total** | **~1,399** | **~5,270** |

Plus ~5,270 HAS_MISCONCEPTION relationships, ~5,270 MOST_LIKELY_AT relationships, ~46 INSTANCE_OF relationships (science), and an estimated ~200-400 RELATED_MISCONCEPTION relationships.

---

## Relationship to Existing Nodes

### DifficultyLevel.common_errors — preserved, not replaced

The `common_errors` arrays on DifficultyLevel nodes remain as-is. They serve a different purpose:

- **DL common_errors** are terse, level-specific error descriptions (~60 chars). They are excellent as quick-reference distractor labels and level-specific gotchas.
- **ConceptMisconception** nodes are expanded, structured entries with diagnosis and remediation. They are the compilation source for Schema B `misconception_traps[]` and Schema C dialogue scripts.

The extraction pipeline uses DL common_errors as **input** — expanding each ~60-char string into a full ConceptMisconception entry. The `source: "dl_expansion"` tag preserves provenance. After extraction, both coexist: DL common_errors for quick reference, ConceptMisconception for structured consumption.

### Concept.common_misconceptions — preserved, not replaced

The prose property remains on Concept nodes. It provides narrative context that structured nodes cannot fully capture (e.g. "Pupils who struggle with X often also..." teaching asides). Schema A (Teacher Planner) continues to include the prose.

The extraction pipeline uses the prose as **input** — decomposing each paragraph into individual ConceptMisconception entries. The `source: "prose_decomposition"` tag preserves provenance.

### Science Misconception nodes (46) — referenced, not replaced

The existing 46 Misconception nodes in `layers/topic-suggestions/data/science_misconceptions/` are **shared reference objects**. They describe misconceptions that span multiple ScienceEnquiry nodes (e.g. "Plants get food from soil" applies across multiple plant biology enquiries).

ConceptMisconception nodes are **concept-level sub-nodes** — each belongs to exactly one Concept. Where a ConceptMisconception instantiates a known science Misconception, the `INSTANCE_OF` relationship links them:

```cypher
// Example: concept-level misconception links to shared science misconception
(cm:ConceptMisconception {misconception_id: 'SC-KS2-C042-CM01'})-[:INSTANCE_OF]->(m:Misconception {misconception_id: 'MC-001'})
```

This preserves the science team's curated reference data while adding concept-level granularity.

---

## Schema and Validation

### Constraints (add to `core/scripts/create_schema.py`)

```python
"CREATE CONSTRAINT concept_misconception_id_unique IF NOT EXISTS FOR (cm:ConceptMisconception) REQUIRE cm.misconception_id IS UNIQUE"
```

### Indexes

```python
"CREATE INDEX concept_misconception_type_idx IF NOT EXISTS FOR (cm:ConceptMisconception) ON (cm.misconception_type)"
"CREATE INDEX concept_misconception_persistence_idx IF NOT EXISTS FOR (cm:ConceptMisconception) ON (cm.persistence)"
"CREATE INDEX concept_misconception_source_idx IF NOT EXISTS FOR (cm:ConceptMisconception) ON (cm.source)"
```

### Validation checks (add to `core/scripts/validate_schema.py`)

Following the DifficultyLevel/RepresentationStage pattern — 5 checks:

1. **check_concept_misconception_completeness**: Every ConceptMisconception node has all required properties (`misconception_id`, `name`, `misconception_type`, `pupil_statement`, `correct_explanation`, `diagnostic_question`, `counter_prompt`, `difficulty_levels`, `source`, `display_category`, `display_color`, `display_icon`). Skip if no ConceptMisconception nodes exist.

2. **check_concept_misconception_type_values**: `misconception_type` must be one of: `preconceived_notion`, `conceptual_misunderstanding`, `vernacular`, `factual_error`, `procedural_error`.

3. **check_concept_misconception_source_values**: `source` must be one of: `prose_decomposition`, `dl_expansion`, `external_source`, `expert_authored`.

4. **check_concept_misconception_relationship_integrity**: Every ConceptMisconception is linked from exactly one Concept via `HAS_MISCONCEPTION`. No orphan ConceptMisconception nodes.

5. **check_concept_misconception_no_duplicate_ids**: No two ConceptMisconception nodes share the same `misconception_id`.

### Import script pattern

`layers/uk-curriculum/scripts/import_concept_misconceptions.py` — follows the DifficultyLevel import pattern:

```python
class ConceptMisconceptionImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            "files": 0,
            "concepts": 0,
            "misconceptions_created": 0,
            "has_misconception_rels": 0,
            "most_likely_at_rels": 0,
            "instance_of_rels": 0,
            "skipped_missing_concept": 0,
        }

    def clear(self, session):
        """Delete all ConceptMisconception nodes and relationships."""
        session.run("MATCH (cm:ConceptMisconception) DETACH DELETE cm")

    def import_file(self, session, path):
        """Import one misconceptions JSON file."""
        # MERGE on misconception_id (idempotent)
        # Link Concept -> ConceptMisconception via HAS_MISCONCEPTION
        # Link ConceptMisconception -> DifficultyLevel via MOST_LIKELY_AT
        # Link ConceptMisconception -> Misconception via INSTANCE_OF (if applicable)
```

Idempotent via MERGE on `misconception_id`. Supports `--clear` flag for full rebuild.

---

## Queries Enabled

```cypher
// All misconceptions for a concept, ordered by difficulty level
MATCH (c:Concept {concept_id: 'MA-Y3-C005'})-[:HAS_MISCONCEPTION]->(cm:ConceptMisconception)
RETURN cm.misconception_id, cm.pupil_statement, cm.counter_prompt, cm.difficulty_levels
ORDER BY cm.misconception_id

// Misconceptions relevant to a specific difficulty level
MATCH (c:Concept {concept_id: 'MA-Y3-C005'})-[:HAS_MISCONCEPTION]->(cm:ConceptMisconception)
       -[:MOST_LIKELY_AT]->(dl:DifficultyLevel {label: 'developing'})
RETURN cm.pupil_statement, cm.counter_prompt, cm.distractor_pattern

// Schema B compilation: misconception traps for a cluster at a target difficulty
MATCH (cc:ConceptCluster {cluster_id: $cluster_id})-[:GROUPS]->(c:Concept)
MATCH (c)-[:HAS_MISCONCEPTION]->(cm:ConceptMisconception)
MATCH (c)-[:HAS_DIFFICULTY_LEVEL]->(dl:DifficultyLevel {label: $target_level})
WHERE (cm)-[:MOST_LIKELY_AT]->(dl)
RETURN c.concept_id, cm.pupil_statement AS symptom,
       cm.counter_prompt, cm.distractor_pattern AS distractor_use

// Cross-concept misconceptions (same root cause)
MATCH (cm1:ConceptMisconception)-[:RELATED_MISCONCEPTION]->(cm2:ConceptMisconception)
MATCH (c1:Concept)-[:HAS_MISCONCEPTION]->(cm1)
MATCH (c2:Concept)-[:HAS_MISCONCEPTION]->(cm2)
RETURN c1.concept_id, cm1.name, c2.concept_id, cm2.name

// Science misconceptions linked to their reference node
MATCH (cm:ConceptMisconception)-[:INSTANCE_OF]->(m:Misconception)
RETURN cm.misconception_id, m.name, m.evidence_base

// Misconception distribution by type across a subject
MATCH (p:Programme)-[:HAS_DOMAIN]->(d:Domain)-[:CONTAINS]->(o:Objective)-[:TEACHES]->(c:Concept)
MATCH (c)-[:HAS_MISCONCEPTION]->(cm:ConceptMisconception)
WHERE p.subject_name = 'Mathematics'
RETURN cm.misconception_type, count(cm) AS count
ORDER BY count DESC
```

---

## Integration with Query Helpers

### query_cluster_context.py

Add a new query block after the existing DifficultyLevel query:

```python
# ── Misconceptions per concept (structured) ────────────────────────
r = session.run("""
    MATCH (cc:ConceptCluster {cluster_id: $cid})-[:GROUPS]->(c:Concept)
    OPTIONAL MATCH (c)-[:HAS_MISCONCEPTION]->(cm:ConceptMisconception)
    RETURN c.concept_id AS concept_id,
           cm.misconception_id AS misconception_id,
           cm.pupil_statement AS pupil_statement,
           cm.counter_prompt AS counter_prompt,
           cm.distractor_pattern AS distractor_pattern,
           cm.misconception_type AS misconception_type,
           cm.difficulty_levels AS difficulty_levels
    ORDER BY c.concept_id, cm.misconception_id
""", cid=cluster_id)
```

Structured misconceptions are surfaced in a new `## Misconceptions (structured)` section of the markdown output. The existing `common_misconceptions` prose remains in the `## Concepts` section for backward compatibility.

### graph_query_helper.py / planner_queries.py

Add ConceptMisconception to the concept detail query alongside DifficultyLevel and RepresentationStage.

---

## QA Process

1. **Automated extraction** generates initial JSON files per domain (LLM-assisted decomposition)
2. **Automated validation** checks schema compliance, type values, difficulty_level references
3. **Sampling review**: 10% of entries per subject reviewed by domain specialist for accuracy
4. **Teacher panel review** (V9 or later): Full review of misconception quality, focusing on counter_prompt tone and distractor_pattern usefulness
5. **External source cross-reference**: Maths entries validated against Eedi dataset and NCETM materials where available

---

## Dependencies

- **Requires**: UK Curriculum (Concept nodes must exist)
- **Requires**: DifficultyLevel (for MOST_LIKELY_AT relationships and DL common_errors as extraction input)
- **Optionally reads**: Misconception nodes (for INSTANCE_OF linking, science only)
- **Import order**: Run AFTER DifficultyLevel import, BEFORE compilation target generation
- **No learner data**: Pure curriculum design metadata (Tier 3 under DATA_CLASSIFICATION.md)

---

## Open Questions

1. **Should MOST_LIKELY_AT be a relationship or a property?** The current design uses a relationship to DifficultyLevel nodes, which enables Cypher path queries (find all misconceptions at a specific DL level). The alternative is the `difficulty_levels` string array property on the ConceptMisconception node, which is simpler but less queryable. The design includes both: the property for quick filtering, the relationship for graph traversal. Is this redundant, or is the dual approach worth the import complexity?

2. **How many misconceptions per concept is the right ceiling?** The estimated average is 3-6, but some concepts (particularly procedural maths concepts like column subtraction) could have 8-10 distinct misconceptions. Should we cap at 6 per concept to keep token budgets manageable for Schema B, or allow uncapped and let the compilation query select the top N by relevance?

3. **Should the extraction LLM be guided by Eedi data even for Phase 1?** Using Eedi as a validation source (checking LLM output against known misconceptions) is lower-risk than using it as a primary source (where licensing and concept-alignment questions arise). But Eedi's diagnostic questions are exceptionally well-structured and could significantly improve Phase 1 quality.

4. **How should cross-concept RELATED_MISCONCEPTION links be surfaced?** Schema B does not currently have a field for "this misconception also affects concept X". Adding one could help the adaptive engine avoid re-triggering the same root misconception across sessions. But it adds complexity to an already dense prompt. Should this be a routing-layer concern (upstream of the prompt) rather than a prompt-layer concern?

5. **Should ConceptMisconception nodes include an `age_band` property?** The current design uses `difficulty_levels` as the age proxy (entry = younger, greater_depth = older). But some misconceptions are genuinely age-specific (e.g. phonics misconceptions only affect KS1). Should there be an explicit `key_stages` array, or is the concept's own key stage sufficient context?

6. **Extraction script architecture: single LLM pass or two-pass?** A single pass (prose + DL errors + context -> structured entries) is simpler but may produce lower-quality deduplication. A two-pass approach (first extract from prose, then match/merge with DL errors) produces cleaner provenance tracking but doubles LLM cost. The DifficultyLevel layer used a single generation pass — should we follow that precedent?

---

## Related Documents

| Document | Relationship |
|---|---|
| [OUTPUT_SCHEMAS.md](OUTPUT_SCHEMAS.md) | Defines the three compilation targets that consume misconception data; [Schema B misconception_traps](OUTPUT_SCHEMAS.md#schema-b-llm-child-session-prompt) is the primary consumer |
| [PLAN_DELIVERY_MODE_CLASSIFICATION.md](PLAN_DELIVERY_MODE_CLASSIFICATION.md) | Reference implementation for this document's structure; delivery modes determine which concepts are eligible for Schema B |
| [PROJECT_DIRECTION.md](PROJECT_DIRECTION.md) | Broader context on compilation targets and the teacher-planner-first approach |
| [RESEARCH_BRIEFING.md](RESEARCH_BRIEFING.md) | Evidence for productive failure and misconception-aware pedagogy |
| [UK curriculum layer](../../layers/uk-curriculum/README.md) | Source concepts and DifficultyLevel nodes that this extraction operates on |
| [Per-subject ontology](../../layers/topic-suggestions/README.md) | Existing 46 Science Misconception nodes that ConceptMisconception references via INSTANCE_OF |
| [Learner profiles](../../layers/learner-profiles/README.md) | FeedbackProfile.counter_misconceptions_explicit determines how Schema B uses misconception data |

# Vocabulary Layer

Promotes curriculum vocabulary from flat comma-separated strings on Concept nodes to first-class graph nodes with definitions, relationships, and Beck's tiered classification.

## What This Layer Does

The UK National Curriculum extraction JSONs contain ~7,000 vocabulary terms stored as comma-separated strings in `key_vocabulary` properties on Concept nodes. This layer:

1. **Extracts** terms from all extraction files, deduplicates within subject, assigns namespaced IDs
2. **Defines** each term with age-appropriate, curriculum-grounded definitions (LLM-assisted)
3. **Connects** terms to concepts via `USES_TERM` relationships with introduced/importance metadata
4. **Links** terms to each other via `REFINES`, `RELATED_TO`, and `SAME_SPELLING_AS` relationships

## Node: VocabularyTerm

| Property | Type | Required | Example |
|----------|------|----------|---------|
| `term_id` | String | Yes | `VOC-MA-fraction` |
| `term` | String | Yes | `fraction` |
| `definition` | String | Yes | A number representing part of a whole |
| `subject` | String | Yes | `Mathematics` |
| `word_class` | String | No | `noun`, `verb`, `adjective`, `phrase` |
| `tier` | Int | Yes | 1=everyday, 2=general academic, 3=domain-specific |
| `etymology` | String | No | From Latin 'fractus' (broken) |
| `example_usage` | String | No | Three quarters (3/4) is a fraction |
| `common_errors` | String | No | Pupils think fractions are always less than 1 |
| `related_everyday_word` | String | No | `part` |

Display: `display_category = "Vocabulary Term"`, `display_color = "#0EA5E9"` (Sky-500), `display_icon = "spellcheck"`.

## Relationships

```
(:Concept)-[:USES_TERM {introduced: bool, importance: "core"|"supporting"|"extension"}]->(:VocabularyTerm)
(:VocabularyTerm)-[:REFINES]->(:VocabularyTerm)
(:VocabularyTerm)-[:RELATED_TO {relationship: "synonym"|"antonym"|"hypernym"|"meronym"|"see_also"}]->(:VocabularyTerm)
(:VocabularyTerm)-[:SAME_SPELLING_AS]->(:VocabularyTerm)
```

## ID Format

`VOC-{subject_prefix}-{slug}` where subject prefix matches concept ID prefixes (MA, EN, SC, HI, GE, etc.).

Cross-subject terms with the same meaning share one node. Same spelling with different meanings get separate nodes linked by `SAME_SPELLING_AS`.

## Polysemy Rule

If a child who understands the term in Subject A would be confused encountering it in Subject B, create separate nodes. Otherwise, share one node with multiple `USES_TERM` relationships.

## Scale

- ~9,200 unique VocabularyTerm nodes across 62 JSON files
- ~17,000 USES_TERM relationships (one per original key_vocabulary entry)
- Relationship files: refinements.json, polysemy.json, semantic.json (authored incrementally)

## Scripts

| Script | Purpose |
|--------|---------|
| `extract_vocabulary.py` | Parse extraction JSONs, deduplicate, write skeletal JSONs |
| `generate_definitions.py` | LLM-assisted definition generation (requires ANTHROPIC_API_KEY) |
| `import_vocabulary.py` | Import to Neo4j (idempotent, `--clear` supported) |
| `validate_vocabulary.py` | Layer-specific validation checks |

## Import Order

1. UK Curriculum must be imported first (concepts must exist for USES_TERM)
2. `python3 layers/vocabulary/scripts/extract_vocabulary.py` (generates term JSONs)
3. `python3 layers/vocabulary/scripts/generate_definitions.py --subject Mathematics --ks KS2` (optional: enrich with definitions)
4. `python3 layers/vocabulary/scripts/import_vocabulary.py`
5. `python3 layers/vocabulary/scripts/validate_vocabulary.py`

## Data Files

```
layers/vocabulary/data/
  terms/                     # Per-subject/year JSON files (~62 files)
    mathematics_y1.json
    mathematics_y2.json
    ...
    science_ks1.json
    english_ks1.json
  relationships/
    refinements.json         # REFINES chains
    polysemy.json            # SAME_SPELLING_AS groups
    semantic.json            # RELATED_TO links
```

## Backward Compatibility

The `key_vocabulary` string property stays on Concept nodes. The site and planners fall back to it when VocabularyTerm nodes don't exist or lack definitions. Same deprecation path as `complexity_level` -> DifficultyLevel.

## No Learner Data

This layer contains zero learner data. All nodes and relationships are curriculum design metadata.

# SEND Support Layer — Maintenance Notes

## Canonical Files

| File | Purpose | Edit here |
|---|---|---|
| `data/need_areas.json` | 4 NeedArea node definitions | Rarely — statutory categories |
| `data/access_requirements.json` | 16 AccessRequirement node definitions | When adding new barrier types |
| `data/support_strategies.json` | 20 SupportStrategy node definitions | When adding new strategies |
| `data/concept_support_links/*.json` | Per-subject concept-barrier annotations | When extending coverage |

## Import Order

1. UK Curriculum must be imported first (concepts must exist)
2. `python3 layers/send-support/scripts/import_send_support.py`
3. `python3 layers/send-support/scripts/validate_send_support.py`

## Key Guardrails

- **Never create nodes from concept_support_links** — these files create relationships only (HAS_ACCESS_REQUIREMENT). The Concept nodes come from the UK curriculum layer.
- **Never add diagnostic labels** — the layer models barriers, not diagnoses. A concept has "high decoding_demand", not "is problematic for dyslexic children".
- **Check construct_sensitive before adding support strategies** — if `construct_sensitive=true` on an AccessRequirement, the barrier may BE the learning objective. The compiler must check before applying a strategy that bypasses it.
- **blocked_when_assessing is a string array** — it lists access_req_ids where the strategy must not be used during assessment. Stored as a node property, not a relationship.
- **All concept_ids in concept_support_links must exist** in the UK curriculum extraction files. Use real IDs (e.g. MA-Y3-C014, EN-KS1-C006, SC-KS2-C024).

## Validation Steps

The validation script checks:
1. All NeedArea, AccessRequirement, SupportStrategy nodes exist with required properties
2. All TAGGED_AS relationships point to valid NeedArea nodes
3. All MITIGATES relationships point to valid AccessRequirement nodes with valid strength values
4. All COMMONLY_USED_FOR relationships point to valid NeedArea nodes
5. All HAS_ACCESS_REQUIREMENT relationships point to valid AccessRequirement nodes with valid level values
6. All concept_ids in concept_support_links exist as Concept nodes in the graph
7. blocked_when_assessing values are valid access_req_ids
8. construct_risk values are valid ("low", "conditional", "high")

## Expanding Coverage

### Adding a new AccessRequirement
1. Add to `data/access_requirements.json` with all required properties
2. Include `tagged_as` array linking to relevant NeedArea ids
3. Update relevant SupportStrategy `mitigates` arrays in `data/support_strategies.json`
4. Add concept-barrier links in `data/concept_support_links/` files
5. Re-import and validate

### Adding concept-barrier links for a new subject or year
1. Read the extraction file to get real concept_ids and concept_names
2. Create a new file in `data/concept_support_links/` (e.g. `primary_history.json`, `secondary_maths.json`)
3. For each concept, consider: what barriers does THIS concept specifically impose?
4. Write specific rationales — a SENCO should read each one and say "yes, that's right"
5. Aim for 30-50 links per file; not every concept needs annotation
6. Re-import and validate

### Adding a new SupportStrategy
1. Add to `data/support_strategies.json` with all required properties
2. Include `mitigates` array linking to relevant AccessRequirement ids with strength ratings
3. Include `commonly_used_for` array linking to relevant NeedArea ids
4. Set `construct_risk` and `blocked_when_assessing` carefully
5. Write `prompt_rules` that the LLM can follow directly
6. Write `ui_implications` that describe platform features needed
7. Re-import and validate

## Display Properties

| Node Type | Color | Icon |
|---|---|---|
| NeedArea | #E11D48 (Rose-600) | accessibility_new |
| AccessRequirement | #F97316 (Orange-500) | warning_amber |
| SupportStrategy | #22C55E (Green-500) | support_agent |

## No Learner Data

This layer contains **zero learner data**. All nodes and relationships are curriculum design metadata. The runtime platform will store learner SEND preferences separately under Tier 0 (identity) with parental consent. See `core/compliance/DATA_CLASSIFICATION.md`.

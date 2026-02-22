# Cluster Definitions

Agent-curated ConceptCluster definitions for the UK National Curriculum knowledge graph.

## Why this exists

The `generate_concept_clusters.py` script produces cluster names automatically by concatenating concept names:
> `"Practice: Addition, Subtraction, Multiplication (+1)"`

That's a scaffold, not a pedagogical statement. This directory stores **hand-authored replacements** with meaningful titles and documented rationale — following the pattern CC Math uses for its cluster-level organisation:
> `"Perform arithmetic operations on polynomials"`
> `"Understand the relationship between zeros and factors of polynomials"`

These definitions are **the authoritative source**. They survive graph wipes. When `generate_concept_clusters.py --clean` is run, curated names are restored from these files.

---

## File layout

One JSON file per subject group:

```
cluster_definitions/
├── README.md              ← this file
├── mathematics.json
├── english.json
├── science.json
├── humanities.json        ← History, Geography, Religious Studies, Citizenship
├── arts.json              ← Art and Design, Music, Drama, Physical Education
└── applied.json           ← DT, Languages, Computing, Business, Food, Media
```

---

## JSON schema

```json
{
  "version": "1.0",
  "subject_group": "Mathematics",
  "authored_by": "agent-name",
  "authored_date": "YYYY-MM-DD",
  "note": "Free-text notes about decisions or coverage gaps",
  "domains": {
    "DOMAIN_ID": {
      "domain_name": "Name from extraction file (for human readability — not imported)",
      "clusters": [
        {
          "cluster_name": "Verb-phrase pedagogical title",
          "cluster_type": "introduction | practice",
          "concept_ids": ["CONCEPT_ID_1", "CONCEPT_ID_2"],
          "rationale": "Why these concepts belong together and what this cluster achieves pedagogically",
          "inspired_by": "Optional: CC Math cluster or NGSS practice this is modelled on"
        }
      ]
    }
  }
}
```

### Rules

| Field | Rule |
|---|---|
| `cluster_name` | Verb phrase, 4–10 words, describes what pupils *do or understand*. CC Math style: "Extend the counting sequence", "Use place value to add and subtract". Not a concept list. |
| `cluster_type` | `introduction` or `practice` only. Consolidation and assessment clusters are inserted automatically. |
| `concept_ids` | Must match `concept_id` values in the extraction JSON files. Every concept in a domain must appear in exactly one cluster. |
| `rationale` | 1–3 sentences. Explain *why* these concepts belong together and what this cluster achieves. If splitting from a larger grouping, explain the split. |
| `inspired_by` | Optional. Reference the CC Math/NGSS cluster or standard that influenced this grouping. |

### concept_type classification guide
When grouping, bear in mind each concept has a `concept_type` in the extraction JSON:
- `knowledge` — declarative facts/content to know
- `skill` — procedural ability to practise
- `understanding` — conceptual grasp
- `application` — using knowledge in context
- `metacognition` — reflecting on learning

Clusters work best when they unify a coherent conceptual or procedural step, not just lump by type. A cluster teaching "reading the clock face" (knowledge + skill) is more useful than one grouping all knowledge concepts together.

---

## CC Math cluster naming conventions (use these as a model)

These real CC Math cluster titles show the naming style to aim for:

**Number and operations:**
- "Extend the counting sequence" (1.NBT.A)
- "Understand place value" (1.NBT.B, 2.NBT.A)
- "Use place value understanding and properties of operations" (2.NBT.B)
- "Represent and solve problems involving addition and subtraction" (2.OA.A)
- "Understand and apply properties of operations" (3.OA.B)
- "Multiply and divide within 100" (3.OA.C)
- "Solve problems involving the four operations" (3.OA.D)

**Fractions / ratios:**
- "Develop understanding of fractions as numbers" (3.NF.A)
- "Extend understanding of fraction equivalence and ordering" (4.NF.A)
- "Build fractions from unit fractions" (4.NF.B)
- "Understand ratio concepts and use ratio reasoning to solve problems" (6.RP.A)

**Algebra / functions:**
- "Interpret the structure of expressions" (HSA-SSE.A)
- "Create equations that describe numbers or relationships" (HSA-CED.A)
- "Understand the concept of a function and use function notation" (HSF-IF.A)
- "Build a function that models a relationship between two quantities" (HSF-BF.A)

**Statistics:**
- "Investigate patterns of association in bivariate data" (8.SP.A)
- "Summarize, represent, and interpret data on a single count or measurement variable" (HSS-ID.A)

---

## What agents should NOT define

- **Consolidation clusters** — automatically inserted every 3–4 content clusters
- **Assessment clusters** — automatically inserted after keystone concepts and at teaching_weight intervals
- **Specific teaching strategies** — those belong in the learner-profiles layer, not here

---

## Validation

After writing definitions, run:
```bash
python3 layers/uk-curriculum/scripts/validate_cluster_definitions.py
```

This checks:
- All concept_ids exist in the extraction files
- Every concept in each domain is covered exactly once
- No duplicate concept_ids within a domain
- cluster_type is valid
- cluster_name is non-empty

---

## Coverage tracker

| Subject group | File | Domains | Status |
|---|---|---|---|
| Mathematics | `mathematics.json` | 62 | ⬜ pending |
| English | `english.json` | 51 | ⬜ pending |
| Science | `science.json` | 61 | ⬜ pending |
| Humanities | `humanities.json` | 43 | ⬜ pending |
| Arts & PE | `arts.json` | 47 | ⬜ pending |
| Applied / Other | `applied.json` | 55 | ⬜ pending |

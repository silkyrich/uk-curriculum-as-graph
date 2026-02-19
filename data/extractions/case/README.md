# CASE Standards Layer — Data Extractions

This directory holds CASE (IMS Global Competencies and Academic Standards Exchange) packages
for the curriculum knowledge graph's `:CASE` namespace layer (graph model v3.5).

## Directory Structure

```
case/
├── case_sources.json          # Framework definitions and fetch config
├── packages/                  # Cached CFPackage JSON (one file per framework)
│   └── *.json
├── mappings/                  # Cross-layer alignment files (CASE ↔ UK curriculum)
│   └── ngss_to_uk_science.json
└── README.md
```

## Workflow

### 1. Fetch packages

Downloads CFPackage JSON from the IMS CASE Network (no auth required) and caches locally:

```bash
python3 scripts/import_case_standards.py --fetch
```

This reads `case_sources.json` and calls the CASE Network API at
`https://casenetwork.imsglobal.org/ims/case/v1p0`.

The fetch step:
- Lists available CFDocuments (`GET /CFDocuments`)
- Matches by `search_title` from `case_sources.json`
- Downloads the full CFPackage (`GET /CFPackages/{id}`)
- Caches to `packages/{framework_id}.json`

If a framework cannot be found (e.g. Texas TEA endpoint differs), a stub file is written
with `"_fetch_status": "not_found"` so the failure is tracked.

To fetch only science frameworks:

```bash
python3 scripts/import_case_standards.py --fetch --subject science
```

### 2. Review and update alignment mappings

After fetching, open the cached packages to find real `cf_item_id` UUIDs and update
the mapping files in `mappings/`. Replace `PLACEHOLDER_*` values with actual UUIDs.

The initial mapping (`ngss_to_uk_science.json`) covers:
- **NGSS Science and Engineering Practices (SEP 1–8)** ↔ **UK KS3 Working Scientifically**

This is the most pedagogically direct comparison: both frameworks define the same
inquiry cycle but with different vocabulary and emphasis.

### 3. Import into Neo4j

```bash
# Import all frameworks
python3 scripts/import_case_standards.py --import

# Import science frameworks only
python3 scripts/import_case_standards.py --import --subject science
```

### 4. Validate

```bash
python3 scripts/validate_schema.py
```

The validator includes Category I checks (CASE layer):
- `check_jurisdiction_completeness`
- `check_cf_document_completeness`
- `check_cf_item_completeness`
- `check_cf_item_child_of_integrity`

All checks PASS gracefully with an "import pending" note if no CASE nodes exist yet.

---

## Mapping File Format

```json
{
  "metadata": {
    "framework_id": "ngss-science-2013",
    "aligns_to": "UK National Curriculum Science",
    "mapping_version": "0.1",
    "status": "stub",
    "notes": "...",
    "created": "2026-02-19"
  },
  "alignments": [
    {
      "cf_item_id": "<UUID from fetched package>",
      "human_coding_scheme": "NGSS.SEP.1",
      "label": "Asking Questions and Defining Problems",
      "aligns_to_concept_ids": ["SC-KS3-C001"],
      "aligns_to_objective_ids": [],
      "aligns_to_skill_ids": ["WS-KS3-001"],
      "confidence": "inferred",
      "notes": "Direct structural match to KS3 Working Scientifically"
    }
  ]
}
```

| Field | Values |
|---|---|
| `confidence` | `"explicit"` (formal crosswalk), `"inferred"` (structural match), `"fuzzy"` (loose) |
| `aligns_to_concept_ids` | IDs of UK Concept nodes |
| `aligns_to_objective_ids` | IDs of UK Objective nodes |

---

## Frameworks Included

| Framework ID | Title | Subject | Jurisdiction | Licence |
|---|---|---|---|---|
| `ngss-science-2013` | Next Generation Science Standards | Science | US-NGSS | CC-BY |
| `ccss-math-2010` | Common Core State Standards for Mathematics | Mathematics | US-CCSS | CC-BY-SA |
| `ccss-ela-2010` | Common Core State Standards for English Language Arts | ELA | US-CCSS | CC-BY-SA |
| `texas-teks-science` | Texas Essential Knowledge and Skills for Science | Science | US-TX | Public domain |
| `wyoming-science-2016` | Wyoming Science Standards | Science | US-WY | Public domain |

---

## Comparison Queries

### Evolution coverage: Texas TEKS vs NGSS

```cypher
MATCH (j:Jurisdiction)-[:PUBLISHES]->(doc:CFDocument)-[:CONTAINS_ITEM]->(i:CFItem)
WHERE j.name IN ['Texas', 'Next Generation Science Standards']
  AND (i.full_statement CONTAINS 'evolution'
       OR any(k IN i.concept_keywords WHERE k CONTAINS 'evolution'))
RETURN j.name, i.human_coding_scheme, i.full_statement
ORDER BY j.name
```

### Climate change coverage across all jurisdictions

```cypher
MATCH (j:Jurisdiction)-[:PUBLISHES]->(doc:CFDocument)-[:CONTAINS_ITEM]->(i:CFItem)
WHERE i.full_statement CONTAINS 'climate'
RETURN j.name, count(i) AS items
ORDER BY items DESC
```

### UK science concepts with no CASE equivalent

```cypher
MATCH (c:Concept)<-[:HAS_CONCEPT]-(:Domain)<-[:HAS_DOMAIN]-(:Programme {subject_name: 'Science'})
WHERE NOT (:CFItem)-[:ALIGNS_TO]->(c)
RETURN c.concept_name, c.source_reference
ORDER BY c.source_reference
```

### NGSS Science Practices ↔ UK Working Scientifically

```cypher
MATCH (i:CFItem)-[:ALIGNS_TO]->(c:Concept)<-[:HAS_CONCEPT]-(:Domain)
WHERE i.cf_doc_id STARTS WITH 'ngss'
RETURN i.human_coding_scheme, i.abbreviated_statement, c.concept_name
```

### Standards at a given education level

```cypher
MATCH (j:Jurisdiction)-[:PUBLISHES]->(doc:CFDocument)-[:CONTAINS_ITEM]->(i:CFItem)
WHERE '8' IN i.education_level
RETURN j.name, doc.title, count(i) AS standards
ORDER BY j.name
```

---

## Research Context

See `docs/research/case-standards/` for detailed notes on each framework, including:
- Adoption history and political context
- Comparison with UK National Curriculum
- Controversial topics (evolution, climate change)
- Structural differences (US grade bands vs UK key stages)

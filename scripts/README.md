# Curriculum Graph Scripts

## Script sequence

```
validate_extractions.py   ← run first — checks JSON files before touching Neo4j
import_curriculum.py      ← loads curriculum subjects into Neo4j
import_test_frameworks.py ← loads KS2 STA test framework data (run after curriculum)
validate_schema.py        ← post-import checks against Neo4j
create_schema.py          ← one-off: creates Neo4j constraints and indexes
```

## Neo4j connection

All scripts hardcode:
```
URI:      neo4j://127.0.0.1:7687
User:     neo4j
Password: password123
```

Running via Neo4j Desktop. Start the DBMS before running any script.

## Typical workflow

```bash
# 1. Pre-flight — check extraction JSONs are valid
python3 scripts/validate_extractions.py

# 2. Clear graph and reimport curriculum
python3 scripts/import_curriculum.py

# 3. Import test framework layer (KS2 Maths, English Reading, English GPS)
python3 scripts/import_test_frameworks.py

# 4. Validate the graph
python3 scripts/validate_schema.py
```

## Data locations

```
data/extractions/primary/      # KS1–KS2 subject extraction JSONs
data/extractions/secondary/    # KS3–KS4 subject extraction JSONs
data/extractions/test-frameworks/  # KS2 STA test framework JSONs + PROVENANCE.md
data/curriculum-documents/     # Source PDFs (subjects + test frameworks)
```

## Known data notes

- `data/extractions/_quarantine/DesignAndTechnology_KS1_extracted_v2.json` — a richer
  Feb 12 extraction (57 concepts vs 7 in the active file) that was found in the wrong
  directory and never imported. Review before discarding.
- `docs/graph_model_v2.md` — documents the v2 schema. Current implementation is v3.0
  (Programme-based model, see import_curriculum.py header).

# Curriculum Graph Scripts

## Script sequence

```
create_schema.py           ← one-off: creates Neo4j constraints and indexes (v3.5)
validate_extractions.py    ← run first — checks JSON files before touching Neo4j
import_curriculum.py       ← loads curriculum subjects into Neo4j (core :Curriculum layer)
import_test_frameworks.py  ← loads KS2 STA test framework data (:Assessment layer)
import_epistemic_skills.py ← loads epistemic skill nodes (:Epistemic layer)
import_topics.py           ← loads topic layer (:Topic layer, v3.3)
import_oak_content.py      ← loads Oak National Academy content (:Content layer, v3.4 skeleton)
import_case_standards.py   ← loads CASE standards (:CASE layer, v3.5)
validate_schema.py         ← post-import checks against Neo4j (41 checks)
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
# 1. One-time setup: create Neo4j schema (v3.5 includes CASE layer)
python3 scripts/create_schema.py

# 2. Pre-flight — check extraction JSONs are valid
python3 scripts/validate_extractions.py

# 3. Clear graph and reimport curriculum (core :Curriculum layer)
python3 scripts/import_curriculum.py

# 4. Import test framework layer (KS2 Maths, English Reading, English GPS)
python3 scripts/import_test_frameworks.py

# 5. Import epistemic skill layer
python3 scripts/import_epistemic_skills.py

# 6. Import topic layer (History, Geography content choices)
python3 scripts/import_topics.py

# 7. OPTIONAL: Import CASE standards layer (US curriculum comparison)
python3 scripts/import_case_standards.py --fetch    # Download CASE packages from OpenSALT
python3 scripts/import_case_standards.py --import   # Load into Neo4j

# 8. Validate the graph (41 checks including CASE)
python3 scripts/validate_schema.py
```

## Data locations

```
data/extractions/primary/          # KS1–KS2 subject extraction JSONs
data/extractions/secondary/        # KS3–KS4 subject extraction JSONs
data/extractions/test-frameworks/  # KS2 STA test framework JSONs + PROVENANCE.md
data/extractions/epistemic-skills/ # Epistemic skill JSONs (WorkingScientifically, ReadingSkill, etc.)
data/extractions/topics/           # Topic layer JSONs (History, Geography)
data/extractions/oak/              # Oak National Academy mappings (v3.4)
data/extractions/case/             # CASE standards (v3.5): sources, packages, mappings
data/curriculum-documents/         # Source PDFs (subjects + test frameworks)
```

## CASE standards layer (v3.5)

The CASE layer enables comparative curriculum analysis between UK and US standards.

**Fetch workflow:**
```bash
# Download CASE packages from OpenSALT (public, no auth required)
python3 scripts/import_case_standards.py --fetch

# Check what was downloaded
ls -lh data/extractions/case/packages/

# Import into Neo4j
python3 scripts/import_case_standards.py --import
```

**Included frameworks:**
- NGSS (Next Generation Science Standards): 1,037 items
- Common Core State Standards for Mathematics: 746 items

**Comparison queries:**
See `data/extractions/case/README.md` for example queries comparing NGSS 3D learning model
vs UK subject-domain structure, science practices alignment, and grade band progressions.

**Research notes:**
Framework comparisons (evolution/climate controversies, state-level control) documented
in `docs/research/case-standards/`.

## Known data notes

- `data/extractions/_quarantine/DesignAndTechnology_KS1_extracted_v2.json` — a richer
  Feb 12 extraction (57 concepts vs 7 in the active file) that was found in the wrong
  directory and never imported. Review before discarding.
- `docs/graph_model_v2.md` — documents the v2 schema. Current implementation is v3.5
  (Programme-based model with Topic, Oak, and CASE layers).

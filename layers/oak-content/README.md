# Oak Content Layer

## Purpose

The **Oak National Academy content** layer — free, high-quality lessons and units mapped onto the UK curriculum. Provides a browseable content catalogue for teachers with curriculum alignment.

## Graph Structure

```
OakUnit -[:HAS_LESSON]-> OakLesson
OakUnit -[:COVERS]-> Domain  (cross-layer to uk-curriculum)
OakLesson -[:TEACHES]-> Concept  (cross-layer to uk-curriculum)
```

## Node Types

| Label | Example | Description |
|---|---|---|
| `OakUnit` | "Fractions in Y5" | A unit of lessons (typically 6-12 lessons) |
| `OakLesson` | "Equivalent fractions" | A single lesson with video, slides, worksheet |

## Data Sources

All data from `/data/extractions/oak/`:
- **Catalogue** (from Oak API): `/catalogue/oak_catalogue.json` — full discovery of all units/lessons
- **Mappings** (manual alignment): `/mappings/{subject}_mappings.json` — curriculum alignment

**Source**: [Oak National Academy Open API](https://open-api.thenational.academy)

## Usage

### 1. Get an Oak API key

Visit https://open-api.thenational.academy/ and register for a free API key.

Set it as an environment variable:

```bash
export OAK_API_KEY=your-key-here
```

### 2. Discover all Oak units and lessons

```bash
cd /Users/richardmorgan/Documents/GitHub/uk-curriculum-as-graph
python3 layers/oak-content/scripts/import_oak_content.py --discover
```

This will:
1. Query the Oak API for all programmes (subjects × key stages)
2. Fetch all units for each programme
3. Fetch all lessons for each unit
4. Cache the full catalogue to `/data/extractions/oak/catalogue/oak_catalogue.json`

**Note**: This can take 10-15 minutes as it fetches 1000+ units and 10,000+ lessons.

### 3. Create mapping files

Review the catalogue and create mapping files in `/data/extractions/oak/mappings/` to align Oak units/lessons to curriculum Domains and Concepts.

Example mapping file (`mathematics_mappings.json`):

```json
{
  "metadata": {
    "subject": "Mathematics",
    "oak_subject_slug": "maths",
    "notes": "Mapping Oak Y5 Fractions unit to NC Fractions domain"
  },
  "unit_mappings": [
    {
      "oak_unit_slug": "fractions-y5-autumn",
      "covers_domain_id": "MA-Y5-D02"
    }
  ],
  "lesson_mappings": [
    {
      "oak_lesson_slug": "equivalent-fractions-y5",
      "teaches_concept_ids": ["MA-Y5-C023", "MA-Y5-C024"]
    }
  ]
}
```

### 4. Import Oak content into Neo4j

```bash
python3 layers/oak-content/scripts/import_oak_content.py --import
```

Or import a single subject:

```bash
python3 layers/oak-content/scripts/import_oak_content.py --import --subject mathematics
```

This will:
1. Read the catalogue
2. Load mapping files for each subject
3. Create OakUnit and OakLesson nodes
4. Create COVERS and TEACHES relationships based on mappings

### Expected Output

```
Oak Units Created       : 256
Oak Lessons Created     : 3,421
COVERS Links Created    : 128  (units → domains)
TEACHES Links Created   : 892  (lessons → concepts)
```

## OakUnit Properties

| Property | Example | Description |
|---|---|---|
| `unit_slug` | `fractions-y5-autumn` | Oak API unique identifier |
| `unit_title` | "Fractions" | Human-readable title |
| `subject` | "Mathematics" | Subject area |
| `key_stage` | `KS2` | Key stage |
| `year` | `Y5` | Specific year (if applicable) |
| `unit_order` | 3 | Sequence within the year/key stage |
| `num_lessons` | 12 | Number of lessons in the unit |
| `oak_url` | `https://...` | Link to Oak website |

## OakLesson Properties

| Property | Example | Description |
|---|---|---|
| `lesson_slug` | `equivalent-fractions-y5` | Oak API unique identifier |
| `lesson_title` | "Equivalent fractions" | Human-readable title |
| `subject` | "Mathematics" | Subject area |
| `key_stage` | `KS2` | Key stage |
| `lesson_order` | 3 | Sequence within the unit |
| `has_video` | `true` | Video available? |
| `has_slide_deck` | `true` | Slide deck available? |
| `has_worksheet` | `true` | Worksheet available? |
| `has_quiz` | `true` | Quiz available? |
| `oak_url` | `https://...` | Link to Oak website |

## Integration Points

This layer **depends on**:
- **UK Curriculum**: Domain and Concept nodes must exist for mappings
- **Oak API key**: Required for discovery step

This layer **enables**:
- Content browsing (e.g., "Show me all Oak lessons that teach fractions")
- Curriculum coverage analysis (e.g., "Which concepts have Oak content?")
- Teacher resources (e.g., "Find lessons for this concept")

## Example Queries

### Find Oak lessons for a specific concept

```cypher
MATCH (l:OakLesson)-[:TEACHES]->(c:Concept {concept_name: 'Fractions'})
RETURN l.lesson_title, l.oak_url, c.concept_name
ORDER BY l.lesson_order
```

### Find Oak units for a domain

```cypher
MATCH (u:OakUnit)-[:COVERS]->(d:Domain {domain_name: 'Number and Place Value'})
RETURN u.unit_title, u.num_lessons, d.programme_id
ORDER BY u.unit_order
```

### Concepts with NO Oak content

```cypher
MATCH (c:Concept)<-[:HAS_CONCEPT]-(d:Domain {subject: 'Mathematics'})
WHERE NOT (:OakLesson)-[:TEACHES]->(c)
RETURN d.domain_name, c.concept_name
ORDER BY d.domain_name
```

### Oak catalogue stats by subject

```cypher
MATCH (u:OakUnit)
RETURN u.subject, count(u) AS num_units, sum(u.num_lessons) AS total_lessons
ORDER BY num_units DESC
```

## Oak Subject Slugs

Oak uses short subject slugs in the API:

| Oak Slug | Curriculum Subject |
|---|---|
| `maths` | Mathematics |
| `english` | English |
| `science` | Science |
| `history` | History |
| `geography` | Geography |
| `art` | Art and Design |
| `computing` | Computing |
| `pe` | Physical Education |

The import script automatically maps these slugs to full subject names.

## Mapping Strategy

**Units** are mapped to **Domains** (broad alignment):
- One Oak unit typically covers 1-2 curriculum domains
- Example: "Fractions Y5" unit → "Fractions, Decimals, and Percentages" domain

**Lessons** are mapped to **Concepts** (specific alignment):
- One Oak lesson typically teaches 1-3 specific concepts
- Example: "Equivalent fractions" lesson → ["Equivalence", "Simplifying fractions"] concepts

Mappings are **manually curated** to ensure accuracy (no automated text matching).

## API Rate Limits

The Oak API has rate limits:
- **100 requests per minute**
- **10,000 requests per day**

The discovery script respects these limits with automatic throttling (0.6s delay between requests).

If you hit the daily limit, the catalogue is cached, so you can resume the next day without re-fetching completed data.

## Notes

- Oak content is **free and openly licensed** (CC-BY-NC-SA)
- Not all curriculum content has Oak lessons (coverage is ~60% across KS1-KS3)
- Oak is expanding rapidly — re-run discovery periodically to update the catalogue
- Mappings are **version-controlled** in the repository (manually maintained)
- Re-running import is **idempotent** (uses MERGE patterns)
- The catalogue includes **retired/archived units** — filter by `is_active` if needed

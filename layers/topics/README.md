# Topics Layer

## Purpose

The **curriculum content choices** layer — captures how the statutory curriculum organizes content into teachable topics, especially for subjects where teachers choose from prescribed options (e.g., History, Geography).

## Graph Structure

```
Topic -[:TEACHES]-> Concept
```

## Node Types

| Label | Example | Description |
|---|---|---|
| `Topic` | "The Roman Empire" | A curriculum topic or unit of study |

## Topic Types

Topics are classified by `topic_type`:

- **`substantive`**: Core content topics (e.g., "Rivers and the water cycle")
- **`thematic`**: Cross-cutting themes (e.g., "Locational knowledge")
- **`skills`**: Skills-focused topics (e.g., "Fieldwork and enquiry")

## Data Sources

All extractions from `/data/extractions/topics/`:
- `history_ks2_topics.json` — KS2 History (6 prescribed topics, 6 optional)
- `history_ks3_topics.json` — KS3 History (thematic topics)
- `geography_ks2_topics.json` — KS2 Geography (locational/place/thematic knowledge)
- `geography_ks3_topics.json` — KS3 Geography (thematic topics)

Source: National Curriculum 2014 Programmes of Study

## Usage

### Import all topics

```bash
cd /Users/richardmorgan/Documents/GitHub/uk-curriculum-as-graph
python3 layers/topics/scripts/import_topics.py
```

This will:
1. Create Topic nodes for all subjects
2. Create TEACHES relationships linking topics to Concept nodes
3. Handle optional/choice topics with `choice_group` grouping

### Expected Output

```
Topics Created/Updated      : 48
TEACHES Links Created       : 287
Concept IDs Not Found       : 0  (all concepts exist in UK curriculum layer)
```

## Topic Properties

| Property | Example | Description |
|---|---|---|
| `topic_id` | `HI-KS2-T01` | Unique identifier |
| `topic_name` | "The Roman Empire" | Human-readable name |
| `subject` | "History" | Subject area |
| `key_stage` | `KS2` | Key stage |
| `topic_type` | `substantive` | Type of topic (substantive, thematic, skills) |
| `is_prescribed` | `true` | Is this topic mandatory/prescribed? |
| `is_optional` | `false` | Is this topic part of a choice set? |
| `choice_group` | `"ancient-civilisation"` | Grouping label for choice sets (or null) |
| `curriculum_note` | "...up to 1066" | Free-text annotation from NC document |
| `teaches_concept_ids` | `["HI-KS2-C001", ...]` | List of Concept IDs taught (not stored, used for TEACHES links) |

## Optional Topics and Choice Groups

Some subjects require teachers to **choose** topics from a set. For example, KS2 History:

> "Pupils should be taught about... a non-European society that provides contrasts with British history – one study chosen from: early Islamic civilization, including a study of Baghdad c. AD 900; Mayan civilization c. AD 900; Benin (West Africa) c. AD 900-1300."

These are modeled as:
- `is_prescribed`: `false`
- `is_optional`: `true`
- `choice_group`: `"non-european-society"`

This allows queries like:

```cypher
// Find all optional topic choices in History KS2
MATCH (t:Topic {subject: 'History', key_stage: 'KS2', is_optional: true})
RETURN t.choice_group, collect(t.topic_name) AS choices
```

## Integration Points

This layer **depends on**:
- **UK Curriculum**: Concept nodes must exist first (Topic → Concept via TEACHES)

This layer **enables**:
- Topic-based curriculum browsing (e.g., "Show me all concepts in 'The Roman Empire'")
- Coverage analysis (e.g., "Which concepts are NOT covered by any topic?")
- Choice analysis (e.g., "How many schools teach 'Early Islamic civilization' vs 'Mayan civilization'?")

## Example Queries

### Find all concepts taught in a specific topic

```cypher
MATCH (t:Topic {topic_name: 'The Roman Empire'})-[:TEACHES]->(c:Concept)
RETURN c.concept_name, c.source_reference
ORDER BY c.concept_name
```

### Find topics that teach a specific concept

```cypher
MATCH (t:Topic)-[:TEACHES]->(c:Concept {concept_name: 'Empire'})
RETURN t.subject, t.topic_name, t.key_stage
ORDER BY t.subject, t.key_stage
```

### Find all optional topic choices by choice group

```cypher
MATCH (t:Topic {is_optional: true})
WHERE t.choice_group IS NOT NULL
RETURN t.subject, t.key_stage, t.choice_group, collect(t.topic_name) AS choices
ORDER BY t.subject, t.key_stage, t.choice_group
```

### Concepts NOT covered by any topic

```cypher
MATCH (c:Concept)<-[:HAS_CONCEPT]-(d:Domain {subject: 'History'})
WHERE NOT (:Topic)-[:TEACHES]->(c)
RETURN d.domain_name, c.concept_name
ORDER BY d.domain_name
```

## Subject Coverage

### History
- **KS2**: 6 prescribed topics (Romans, Anglo-Saxons, Vikings, Ancient Greece, etc.) + 3 choice groups
- **KS3**: Thematic topics (Medieval Britain, Reformation, Empire, etc.)

### Geography
- **KS2**: Locational knowledge, place knowledge, thematic topics (Rivers, Mountains, Earthquakes, etc.)
- **KS3**: Thematic topics (Glaciation, Rivers, Weather & Climate, etc.)

### Other subjects
- Topics layer is currently **only implemented for History and Geography**
- Other subjects (Science, Maths, English) have linear progression models, not topic-based organization

## Notes

- Topics are **manually extracted** from National Curriculum programmes of study
- The `teaches_concept_ids` field in source JSON is used to create TEACHES relationships (not stored as a property)
- Not all subjects use a topic-based organization (e.g., Maths is year-by-year, not topic-based)
- Re-running import is **idempotent** (uses MERGE patterns)
- Concepts not found during import are reported but do not block the import

# Epistemic Skills Layer

## Purpose

The **discipline-specific thinking skills** layer — captures "working like a scientist/historian/mathematician" skills that cut across content domains. These are the second-order concepts and practices that define how knowledge is constructed in each subject.

## Graph Structure

```
Programme -[:DEVELOPS_SKILL]-> <SkillType>
<SkillType> -[:PROGRESSION_OF]-> <SkillType>  (within same skill type)
ContentDomainCode -[:ASSESSES_SKILL]-> ReadingSkill
```

## Node Types (Skill Types)

| Label | Subject | Description | Example Skills |
|---|---|---|---|
| `WorkingScientifically` | Science | Scientific enquiry skills | "Planning different types of scientific enquiries" |
| `ReadingSkill` | English | Reading comprehension skills (with STA test codes) | "Make inferences from the text" (code: 2d) |
| `HistoricalThinking` | History | Second-order disciplinary concepts | "Cause and consequence", "Historical significance" |
| `MathematicalReasoning` | Mathematics | Fluency, reasoning, problem-solving | "Reason mathematically using abstract notation" |
| `GeographicalSkill` | Geography | Fieldwork and enquiry skills | "Use maps, atlases, globes" |
| `ComputationalThinking` | Computing | CT pillars | "Algorithms", "Decomposition", "Abstraction" |

## Data Sources

All extractions from `/data/extractions/epistemic-skills/`:
- `working_scientifically.json` — Science KS1/KS2/KS3
- `reading_skills.json` — English reading (with STA test codes)
- `historical_thinking.json` — History second-order concepts
- `mathematical_reasoning.json` — Mathematics practices
- `geographical_skills.json` — Geography fieldwork/enquiry
- `computational_thinking.json` — Computing CT pillars

## Usage

### Import all epistemic skills

```bash
cd /Users/richardmorgan/Documents/GitHub/uk-curriculum-as-graph
python3 layers/epistemic-skills/scripts/import_epistemic_skills.py
```

This will:
1. Create skill nodes for all 6 skill types
2. Create PROGRESSION_OF relationships (skills that build on each other)
3. Create DEVELOPS_SKILL relationships (Programme → Skill)
4. Create ASSESSES_SKILL relationships (ContentDomainCode → ReadingSkill)

### Expected Output

```
Skill Nodes Created         : 87
PROGRESSION_OF Links        : 34
DEVELOPS_SKILL Links        : 156
ASSESSES_SKILL Links        : 45  (reading skills only)
```

## Integration Points

This layer **depends on**:
- **UK Curriculum**: Programme nodes must exist first
- **Assessment**: ContentDomainCode nodes (for ReadingSkill links only)

This layer **enables**:
- Skills progression analysis (e.g., "How does 'asking questions' develop from KS1 → KS3?")
- Cross-curricular skills comparison (e.g., "What practices are shared across STEM subjects?")
- Assessment-skills alignment (e.g., "Which reading skills are tested in KS2?")

## Skill Properties

All skill nodes share these core properties:

| Property | Example | Description |
|---|---|---|
| `skill_id` | `WS-KS2-001` | Unique identifier |
| `skill_name` | "Planning enquiries" | Human-readable name |
| `description` | "Plan different types of scientific enquiries..." | Full text from NC |
| `key_stage` | `KS2` | Which key stage(s) this skill appears in |
| `complexity_level` | 2 | Progression level (1=basic, 2=intermediate, 3=advanced) |
| `source_reference` | "NC 2014 Science KS2" | Source document reference |
| `subject` | "Science" | Subject area |

### Optional Properties (skill-type specific)

| Property | Node Types | Example | Description |
|---|---|---|---|
| `test_code` | ReadingSkill | `2d` | STA test framework code |
| `strand` | ReadingSkill | "Word reading", "Comprehension" | Reading strand |
| `second_order` | HistoricalThinking | true | Second-order vs substantive concept flag |
| `paper` | ReadingSkill | `1`, `2` | Which test paper(s) assess this skill |

## Progression Modeling

Skills within the same type can form progression chains via `[:PROGRESSION_OF]` relationships:

```cypher
// Example: Working Scientifically progression KS1 → KS2 → KS3
MATCH path = (ks1:WorkingScientifically {key_stage: 'KS1'})
             -[:PROGRESSION_OF*]->(ks3:WorkingScientifically {key_stage: 'KS3'})
WHERE ks1.skill_name CONTAINS 'observ'
RETURN path
```

This shows how "making observations" in KS1 progresses to "making systematic observations" in KS2, then "using appropriate techniques and apparatus" in KS3.

## Example Queries

### Find all programmes that develop a specific skill

```cypher
MATCH (p:Programme)-[:DEVELOPS_SKILL]->(s:WorkingScientifically)
WHERE s.skill_name CONTAINS 'recording'
RETURN p.subject_name, p.key_stage, s.skill_name
```

### Reading skills tested in KS2

```cypher
MATCH (cdc:ContentDomainCode)-[:ASSESSES_SKILL]->(rs:ReadingSkill)
RETURN rs.test_code, rs.skill_name, count(cdc) AS num_codes
ORDER BY rs.test_code
```

### Cross-curricular skills comparison

```cypher
MATCH (s)
WHERE s:WorkingScientifically OR s:MathematicalReasoning OR s:HistoricalThinking
  AND s.skill_name CONTAINS 'reason'
RETURN labels(s)[0] AS skill_type, s.skill_name, s.key_stage
ORDER BY skill_type
```

## Notes

- Skills are **extracted manually** from the National Curriculum programmes of study
- ReadingSkill nodes are the only skill type with test_code properties (linked to STA assessment)
- PROGRESSION_OF relationships are **inferred** based on key_stage and complexity_level
- Not all subjects have epistemic skills modeled yet (e.g., Art, Music, PE, Languages)
- Re-running import is **idempotent** (uses MERGE patterns)

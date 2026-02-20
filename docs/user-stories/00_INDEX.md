# User Stories: Technical Pedagogy Breakdown

Each story shows:
1. **The narrative** (what the child experiences)
2. **The data collected** (what we measure and store)
3. **The inference** (how the AI detects the pattern)
4. **The pedagogical action** (what the AI does and why)
5. **Privacy boundary** (what we DON'T store)

---

## Learning Pattern Data (✅ Store and Learn From)

| Data Type | Example | Purpose |
|---|---|---|
| **Response accuracy** | 7/10 correct on 6× table | Mastery tracking |
| **Response time** | 2.3s (fast), 8.7s (slow) | Retrieval strength indicator |
| **Error patterns** | Confuses /e/ and /i/ in 12/15 CVC words | Misconception detection |
| **Hesitation markers** | Changed answer from 'e' to 'i' | Uncertainty, partial knowledge |
| **Scaffold effectiveness** | Visual > verbal for fractions | Personalized pedagogy |
| **Spacing intervals** | Recalls 6×4 after 2 days, forgets after 7 | Optimal review schedule |
| **Productive failure responses** | Tried 1/2+1/3=2/5, then self-corrected | Conceptual exploration |
| **Difficulty calibration** | 6×7 is ZPD, 6×12 is too hard | Challenge level tuning |

## Personal/Emotional Data (❌ Never Store)

| Data Type | Why Prohibited |
|---|---|
| **Personal revelations** | "My parents are fighting" |
| **Emotional states** | "I'm sad today" |
| **Preferences unrelated to learning** | "I like dogs" |
| **Social relationships** | "My best friend is Sarah" |
| **Home life details** | "We're moving house" |

**Enforcement**: Prompt classifier flags and discards any response containing personal/emotional content. Parent notified if child attempts to share personal information.

---

## Story Index

### Foundation Stories (Y1-Y2, ages 5-7)

1. **[Number Line Direction](01_number_line_direction.md)**
   - Pattern: Child taps randomly, then realizes direction matters
   - Data: Tap sequence, self-correction timing
   - Inference: Discovers subtraction as direction, not just "taking away"
   - Pedagogy: Productive failure → delayed explanation

2. **[Phoneme Confusion (/e/ vs /i/)](02_phoneme_confusion.md)**
   - Pattern: Systematic vowel substitution error
   - Data: Error matrix (which sounds confused with which)
   - Inference: Phonetic proximity causing interference
   - Pedagogy: Contrastive minimal pairs, articulatory diagram

3. **[Plant Observation](03_scientific_observation.md)**
   - Pattern: Jumps to naming before observing
   - Data: Observation order (names vs descriptions)
   - Inference: Needs scaffolding for "notice before label"
   - Pedagogy: Voice recording forces description before categorization

### Intermediate Stories (Y3-Y4, ages 7-9)

4. **[Times Table Retrieval](04_times_table_retrieval.md)**
   - Pattern: Fluent on some facts, hesitant on others
   - Data: Response time distribution per fact
   - Inference: Retrieval strength varies by fact
   - Pedagogy: Spaced repetition schedule per fact

5. **[Fraction Misconception](05_fraction_addition.md)**
   - Pattern: Adds numerators/denominators separately
   - Data: Error type, self-correction after visual
   - Inference: Common misconception (treating fractions as two separate numbers)
   - Pedagogy: Visual refutation → independent discovery

6. **[Reading Inference](06_reading_inference.md)**
   - Pattern: Retrieves explicitly stated info, struggles with implicit
   - Data: Question type success rate (literal vs inferential)
   - Inference: Can decode but not infer from context clues
   - Pedagogy: Highlight-and-explain scaffold

### Advanced Stories (Y5-Y6, ages 9-11)

7. **[Equivalent Fractions](07_equivalent_fractions.md)**
   - Pattern: Knows procedure but not why it works
   - Data: Correct answers but can't explain
   - Inference: Procedural knowledge without conceptual understanding
   - Pedagogy: Challenge conceptual understanding, force explanation

8. **[Shakespeare Language](08_shakespeare_archaic.md)**
   - Pattern: Modern vocabulary interference with archaic meaning
   - Data: Which archaic terms guessed vs looked up
   - Inference: Context clues not sufficient for pre-1600 English
   - Pedagogy: Annotate-first, then analyze patterns

### Adversarial Stories (Bad User Stories)

9. **[Sibling Gaming Detection](09_sibling_gaming.md)**
   - Pattern: Sudden pace/difficulty spike
   - Data: Session-level anomaly metrics
   - Detection: Multi-factor anomaly score
   - Response: Flag session, don't save progress

10. **[Personal Information Sharing](10_personal_sharing.md)**
    - Pattern: Child tries to tell AI about home life
    - Detection: Prompt classifier flags emotional/personal content
    - Response: Gentle redirect, parent notification
    - Privacy: Content discarded, not stored

11. **[Inappropriate LLM Prompting](11_inappropriate_prompts.md)**
    - Pattern: Off-curriculum or unsafe prompts
    - Detection: Multi-layer safety classifier
    - Response: Immediate session termination
    - Logging: Flagged for parent review

---

## Technical Architecture

Each story will explain:

### 1. Session Data Structure
```json
{
  "session_id": "uuid",
  "child_id": "uuid",
  "concept_id": "MA-Y3-C042",
  "responses": [
    {
      "timestamp": "2026-02-19T16:23:45Z",
      "response_time_ms": 2300,
      "answer": "24",
      "correct": true,
      "hesitation_markers": [],
      "self_correction": false
    }
  ]
}
```

### 2. Learner Model Structure
```json
{
  "child_id": "uuid",
  "concept_mastery": {
    "MA-Y3-C042": {
      "status": "mastered",
      "success_rate": 0.85,
      "avg_response_time_ms": 2100,
      "last_reviewed": "2026-02-19",
      "next_review": "2026-02-26",
      "retrieval_strength": 0.82
    }
  },
  "error_patterns": {
    "fraction_addition": {
      "misconception": "adds_numerators_denominators_separately",
      "frequency": 0.75,
      "last_seen": "2026-02-18"
    }
  },
  "scaffold_preferences": {
    "fractions": "visual_preferred",
    "phonics": "auditory_effective"
  }
}
```

### 3. What's NOT Stored
```json
// ❌ NEVER stored:
{
  "emotional_state": "sad",
  "personal_interests": ["dogs", "minecraft"],
  "family_situation": "parents divorcing",
  "social_relationships": ["best friend: Sarah"]
}
```

---

## Next: Individual Story Files

Each story in its own file with:
- Full narrative (child's experience)
- Technical breakdown (data → inference → action)
- Code snippets showing detection logic
- Privacy boundary explanation

# Story 04: Times Table Retrieval (Spaced Repetition)

**Age**: 8 (Y3) | **Subject**: Mathematics | **Concept**: 6× table fluency

---

## The Narrative (What the Child Experiences)

Marcus, age 8, is learning his 6× table. He knows 2×, 5×, and 10× fluently. Today is session 3 on the 6× table.

**Screen: Rapid-fire retrieval practice** (no explanation, just recall)

**AI**: "6 times 4?"

*[Marcus types: 24]*

**On screen**: ✓ (immediate, no fanfare)

---

**AI**: "7 times 6?"

*[Marcus pauses... types: 42]*

**On screen**: ✓

---

**AI**: "6 times 6?"

*[Marcus types quickly: 36]*

**On screen**: ✓

---

**AI**: "9 times 6?"

*[Marcus pauses longer... types: 54]*

**On screen**: ✓

---

**AI**: "6 times 8?"

*[Pause... Marcus types: 42. Incorrect — he carried over the previous answer.]*

**On screen**: That was 7×6. Let's try again: 6×8 = ?

*[Marcus thinks: "Oh... 48"]*

**On screen**: ✓ Good catch.

---

**AI**: "That one took longer. That's fine — your brain was working hard. Tomorrow I'll ask you 6×8 again and it'll be faster."

---

## The Data (What We Collect)

### Raw Response Log (Session 3)

```json
{
  "session_id": "sess_2026_02_19_003",
  "child_id": "child_marcus_y3",
  "concept_id": "MA-Y3-MULT-006",  // 6× table
  "responses": [
    {
      "fact": "6×4",
      "answer": 24,
      "correct": true,
      "response_time_ms": 1200,  // FAST — fluent retrieval
      "hesitation": false,
      "self_correction": false
    },
    {
      "fact": "6×7",
      "answer": 42,
      "correct": true,
      "response_time_ms": 3400,  // SLOW — effortful
      "hesitation": true,
      "self_correction": false
    },
    {
      "fact": "6×6",
      "answer": 36,
      "correct": true,
      "response_time_ms": 1800,  // MODERATE — consolidating
      "hesitation": false,
      "self_correction": false
    },
    {
      "fact": "6×9",
      "answer": 54,
      "correct": true,
      "response_time_ms": 4100,  // VERY SLOW — deriving, not recalling
      "hesitation": true,
      "self_correction": false
    },
    {
      "fact": "6×8",
      "answer": 42,
      "correct": false,
      "response_time_ms": 2900,
      "hesitation": true,
      "self_correction": true,  // Corrected after feedback
      "error_type": "interference",  // Previous answer carried over
      "corrected_answer": 48,
      "corrected_time_ms": 3200
    }
  ]
}
```

### Historical Data (Accumulated Over 3 Sessions)

```json
{
  "child_id": "child_marcus_y3",
  "multiplication_facts": {
    "6×4": {
      "session_1": {"correct": true, "response_time_ms": 5200, "derived": true},
      "session_2": {"correct": true, "response_time_ms": 2100, "derived": false},
      "session_3": {"correct": true, "response_time_ms": 1200, "derived": false},
      "status": "fluent",  // < 2000ms consistently
      "retrieval_strength": 0.92,
      "next_review": "2026-02-26"  // 7 days (long interval)
    },
    "6×7": {
      "session_1": {"correct": false, "response_time_ms": null, "guessed": 40},
      "session_2": {"correct": true, "response_time_ms": 4800, "derived": true},
      "session_3": {"correct": true, "response_time_ms": 3400, "derived": false},
      "status": "consolidating",  // 2000-4000ms
      "retrieval_strength": 0.61,
      "next_review": "2026-02-21"  // 2 days (medium interval)
    },
    "6×8": {
      "session_1": {"correct": false, "response_time_ms": null},
      "session_2": {"correct": true, "response_time_ms": 6100, "derived": true},
      "session_3": {"correct": false, "response_time_ms": 2900, "error": "interference"},
      "status": "learning",  // errors + slow retrieval
      "retrieval_strength": 0.32,
      "next_review": "2026-02-20"  // 1 day (short interval — TOMORROW)
    },
    "6×9": {
      "session_1": {"correct": true, "response_time_ms": 7200, "derived": true},
      "session_2": {"correct": true, "response_time_ms": 5300, "derived": true},
      "session_3": {"correct": true, "response_time_ms": 4100, "derived": true},
      "status": "deriving",  // slow but consistent — needs more practice
      "retrieval_strength": 0.48,
      "next_review": "2026-02-20"  // 1 day (frequent practice needed)
    }
  }
}
```

---

## The Inference (How the AI Detects Retrieval Strength)

### Retrieval Strength Algorithm

**Based on**: Response time as proxy for memory strength (Anderson's ACT-R theory)

**Classification**:
| Response Time | Status | Interpretation |
|---|---|---|
| < 2000ms | **Fluent** | Direct retrieval from long-term memory |
| 2000-4000ms | **Consolidating** | Partial retrieval + verification |
| 4000-6000ms | **Deriving** | Computing from known facts (e.g., 6×9 = 6×10 - 6) |
| > 6000ms | **Guessing** | No confident retrieval or derivation |

**Retrieval strength formula** (simplified):
```python
def calculate_retrieval_strength(fact_history):
    # Weight recent sessions more heavily
    weights = [0.5, 0.3, 0.2]  # Most recent session = 50% weight
    scores = []

    for session, weight in zip(fact_history[-3:], weights):
        if not session['correct']:
            score = 0.0
        elif session['response_time_ms'] < 2000:
            score = 1.0  # Fluent
        elif session['response_time_ms'] < 4000:
            score = 0.7  # Consolidating
        elif session['response_time_ms'] < 6000:
            score = 0.4  # Deriving
        else:
            score = 0.2  # Slow/guessing

        scores.append(score * weight)

    return sum(scores)
```

**For Marcus's 6×8**:
- Session 1: Incorrect → score = 0.0 × 0.2 = 0.0
- Session 2: 6100ms (deriving) → score = 0.4 × 0.3 = 0.12
- Session 3: Incorrect (interference) → score = 0.0 × 0.5 = 0.0
- **Total retrieval strength = 0.12** (very weak)

**For Marcus's 6×4**:
- Session 1: 5200ms (deriving) → score = 0.4 × 0.2 = 0.08
- Session 2: 2100ms (consolidating) → score = 0.7 × 0.3 = 0.21
- Session 3: 1200ms (fluent) → score = 1.0 × 0.5 = 0.5
- **Total retrieval strength = 0.79** (strong)

---

## The Pedagogical Action (Spaced Repetition Schedule)

### Spacing Algorithm

**Based on**: Ebbinghaus forgetting curve + testing effect

**Review interval formula**:
```python
def calculate_next_review(fact_id, retrieval_strength, last_review_date):
    # Base intervals by retrieval strength
    if retrieval_strength > 0.8:
        base_interval_days = 7  # Strong: review in a week
    elif retrieval_strength > 0.6:
        base_interval_days = 3  # Moderate: review in 3 days
    elif retrieval_strength > 0.4:
        base_interval_days = 2  # Weak: review in 2 days
    else:
        base_interval_days = 1  # Very weak: review tomorrow

    # Apply jitter (±20%) to avoid massed practice feel
    import random
    jitter = random.uniform(0.8, 1.2)
    interval = int(base_interval_days * jitter)

    next_review = last_review_date + timedelta(days=interval)
    return next_review
```

### Marcus's Schedule (After Session 3)

| Fact | Retrieval Strength | Next Review | Interval |
|---|---|---|---|
| 6×4 | 0.79 (strong) | 2026-02-26 | 7 days |
| 6×6 | 0.68 (moderate) | 2026-02-23 | 4 days |
| 6×7 | 0.61 (moderate) | 2026-02-21 | 2 days |
| 6×9 | 0.48 (weak) | 2026-02-20 | 1 day |
| 6×8 | 0.12 (very weak) | 2026-02-20 | 1 day (TOMORROW) |

**Session 4 plan** (tomorrow):
- **Prioritize**: 6×8, 6×9 (weakest facts)
- **Interleave**: 6×7 (to prevent forgetting)
- **Skip**: 6×4 (too fluent, don't need daily practice)

### What the AI Says

**After 6×9** (slow but correct):
> "That one took longer. That's fine — your brain was working hard."

**Why this response**:
- ✅ Normalizes effortful retrieval (desirable difficulty)
- ✅ Effort attribution ("your brain was working" = growth mindset)
- ❌ Doesn't say "good job" (not controlling reward, just informational)

**After 6×8 error** (interference):
> "That was 7×6. Let's try again: 6×8 = ?"

**Why this response**:
- ✅ Identifies the error type (interference, not random)
- ✅ Immediate re-attempt (testing effect — retrieval practice strengthens memory)
- ❌ Doesn't give the answer (forces retrieval effort)

**After correct answer on retry**:
> "Good catch."

**Why this response**:
- ✅ Acknowledges self-correction (metacognitive skill)
- ❌ Not effusive praise (keeps it informational)

**End of session**:
> "Tomorrow I'll ask you 6×8 again and it'll be faster."

**Why this response**:
- ✅ Previews the spacing schedule (transparent pedagogy)
- ✅ Prediction of improvement (builds expectation of growth)
- ✅ Specific (names the fact, not vague "we'll practice more")

---

## Data Storage (What Persists)

### Updated Learner Model

```json
{
  "child_id": "child_marcus_y3",
  "multiplication_facts": {
    "6×8": {
      "retrieval_strength": 0.12,
      "status": "learning",
      "error_history": [
        {"session": 1, "error": "unknown"},
        {"session": 3, "error": "interference", "previous_fact": "6×7"}
      ],
      "next_review": "2026-02-20",
      "priority": "high"  // Flag for tomorrow's session
    }
  },
  "session_stats": {
    "session_3": {
      "facts_attempted": 10,
      "facts_correct": 9,
      "avg_response_time_ms": 2980,
      "fluent_facts": ["6×4", "6×6"],
      "consolidating_facts": ["6×7"],
      "weak_facts": ["6×8", "6×9"]
    }
  }
}
```

### Curriculum Graph Query (To Generate Tomorrow's Session)

```cypher
// Find facts due for review tomorrow
MATCH (child:Child {child_id: 'child_marcus_y3'})-[:WORKING_ON]->(fact:MultiplicationFact)
WHERE fact.next_review <= date('2026-02-20')
  AND fact.retrieval_strength < 0.8
RETURN fact.expression, fact.retrieval_strength, fact.priority
ORDER BY fact.priority DESC, fact.retrieval_strength ASC
LIMIT 10

// Result: [6×8, 6×9, 6×7, ...] (weakest first)
```

---

## Privacy Boundary

**What the AI knows**:
- ✅ Marcus is fluent on 6×4 (1200ms response time)
- ✅ Marcus struggles with 6×8 (interference error, weak retrieval)
- ✅ Marcus derives 6×9 (4100ms = computing, not recalling)
- ✅ Optimal review schedule: 6×8 tomorrow, 6×4 next week

**What the AI does NOT know**:
- ❌ That Marcus plays football (interest unrelated to maths)
- ❌ That Marcus's dad helps him with homework (family context)
- ❌ That Marcus "hates maths" (emotional state — parent might mention, but AI shouldn't use it)

**Why not use emotional context?**
- If parent says "Marcus hates maths," the AI should NOT adapt its tone to be more cheerful/encouraging
- That would be *personalizing based on emotional state*, which crosses the privacy line
- The AI's job: optimize learning, not form emotional relationship

**What the AI CAN adapt**:
- ✅ Difficulty level (based on retrieval strength data)
- ✅ Review timing (based on forgetting curves)
- ✅ Scaffolding type (visual vs verbal, based on what works)

---

## Validation Query (Curriculum Grounding)

```cypher
// Verify 6× table is age-appropriate
MATCH (c:Concept {concept_id: 'MA-Y3-MULT-006'})
RETURN c.concept_name, c.source_reference

// Expected: "Recall multiplication facts for 3, 4, 8 times tables"
// Note: NC says 3/4/8 for Y3, but 6/7/9 for Y4
// Graph should flag: "6× table is Y4 content, early for Y3"

// Check if prerequisites are mastered
MATCH (prereq:Concept)-[:PREREQUISITE_OF]->(c:Concept {concept_id: 'MA-Y3-MULT-006'})
RETURN prereq.concept_name

// Expected prerequisites: 2× table, 5× table, 10× table (all mastered ✓)
```

**Curriculum adherence check**:
- Marcus (Y3) is working on 6× table
- National Curriculum specifies 6× for Y4
- **Question**: Is this appropriate?
- **Answer**: Yes, if prerequisites (2×, 5×, 10×) are mastered, moving ahead is fine
- Parent dashboard shows: "Marcus is working ahead of Y3 curriculum (6× table is Y4). This is appropriate because he's mastered all Y3 multiplication facts."

---

## Technical Summary

**Data collected**: Response times, accuracy, error types, self-corrections
**Pattern detected**: Fluent on some facts (6×4), weak on others (6×8, 6×9)
**Inference**: Retrieval strength varies by fact; spacing intervals should be individualized per fact
**Action**: Spaced repetition schedule — weak facts reviewed daily, strong facts reviewed weekly
**Storage**: Per-fact retrieval strength, next review date, error history
**Privacy**: No emotional data, no personal interests, pure memory strength metrics

This is how the AI "magically" knows when to review each fact — it's tracking retrieval strength per fact and applying spaced repetition algorithms from cognitive science (Ebbinghaus, Bjork, Pashler).

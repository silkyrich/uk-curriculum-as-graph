# User Stories: Technical Pedagogy Documentation

**Status**: In development (3 of 11 stories complete)

---

## What This Is

Each user story shows **how the AI actually works** — not just the narrative, but the technical mechanics:

1. **The narrative**: What the child experiences on screen
2. **The data**: What we measure and store (with exact data structures)
3. **The inference**: How the AI detects patterns (with algorithms)
4. **The action**: What the AI does and why (pedagogical grounding)
5. **The privacy boundary**: What we explicitly DON'T store or learn

---

## The Core Principle

**The AI learns deeply about HOW the child learns, but NOTHING about WHO the child is.**

### ✅ What We Store and Learn From

| Data Type | Example | Why |
|---|---|---|
| **Error patterns** | Confuses /e/ and /i/ 58% of the time | Misconception detection |
| **Response times** | 1200ms (fluent) vs 4100ms (deriving) | Retrieval strength indicator |
| **Hesitation markers** | Paused, changed answer | Uncertainty, partial knowledge |
| **Scaffold effectiveness** | Visual > verbal for fractions | Personalized pedagogy |
| **Spacing intervals** | Forgets after 7 days, recalls after 2 days | Optimal review schedule |
| **Difficulty calibration** | 6×7 is ZPD, 6×12 is too hard | Challenge level tuning |

### ❌ What We Never Store

| Data Type | Why Prohibited |
|---|---|
| **Personal revelations** | "My parents are fighting" | Emotional/family information |
| **Preferences** | "I like dinosaurs" | Interest unrelated to learning |
| **Emotional states** | "I'm sad today" | Prevents parasocial relationship |
| **Social context** | "My best friend is Sarah" | Personal information |

**Enforcement**: Prompt classifier flags and discards personal/emotional content. Parent notified if child attempts repeated personal sharing.

---

## Story Index

### ✅ Complete (Technical Depth)

1. **[Index and Privacy Architecture](00_INDEX.md)** — Overview of data boundaries
2. **[Phoneme Confusion (/e/ vs /i/)](02_phoneme_confusion.md)** — Error pattern detection, contrastive intervention
3. **[Times Table Retrieval](04_times_table_retrieval.md)** — Spacing algorithm, retrieval strength calculation
4. **[Sibling Gaming Detection](09_sibling_gaming.md)** — Anomaly detection, adversarial resistance

### 🚧 Planned (To Be Written)

5. **Number Line Direction** (Y1) — Productive failure, self-discovery
6. **Scientific Observation** (Y2) — "Notice before label" scaffolding
7. **Fraction Misconception** (Y5) — Visual refutation of common error
8. **Reading Inference** (Y4) — Literal vs inferential question routing
9. **Equivalent Fractions** (Y5) — Procedural vs conceptual understanding
10. **Shakespeare Language** (Y6) — Archaic vocabulary, rhythm analysis
11. **Personal Information Sharing** (adversarial) — Safety classifier, gentle redirect
12. **Inappropriate LLM Prompting** (adversarial) — Prompt injection defense

---

## Technical Patterns Demonstrated

### Pattern 1: Error Type Detection (Story 02)

**Use case**: Child systematically confuses two similar concepts

**Data structure**:
```json
{
  "error_patterns": {
    "vowel_confusion_e_i": {
      "confusion_matrix": {"/e/": {"confused_with_/i/": 7}},
      "frequency": 0.58,
      "intervention": "contrastive_minimal_pairs"
    }
  }
}
```

**Algorithm**: Detect when error rate > 50%, substitution is consistent, and confusion is asymmetric

**Pedagogy**: Contrastive presentation (always show /e/ and /i/ adjacent), visual scaffold (mouth diagram), metacognitive framing ("these are close")

---

### Pattern 2: Retrieval Strength Tracking (Story 04)

**Use case**: Track fluency per individual math fact, optimize review schedule

**Data structure**:
```json
{
  "multiplication_facts": {
    "6×8": {
      "retrieval_strength": 0.32,
      "response_time_ms": 4100,
      "next_review": "2026-02-20",
      "priority": "high"
    }
  }
}
```

**Algorithm**: Response time < 2000ms = fluent, 2000-4000ms = consolidating, >4000ms = deriving. Retrieval strength = weighted average over last 3 sessions.

**Pedagogy**: Spaced repetition (Ebbinghaus curve) — weak facts reviewed daily, strong facts weekly. Interleave to prevent interference.

---

### Pattern 3: Anomaly Detection (Story 09)

**Use case**: Detect when older sibling/adult uses child's account

**Data structure**:
```json
{
  "anomaly_flags": [
    {"factor": "response_time", "severity": "high", "ratio": 19.5},
    {"factor": "accuracy_spike", "severity": "high", "delta": 0.32}
  ],
  "anomaly_score": 120,
  "parent_notified": true
}
```

**Algorithm**: Multi-factor score comparing session behavior to baseline. Score > 50 = flag for review.

**Response**: Block progress updates, notify parent, offer session review/discard options.

---

## Implementation Architecture

### Data Flow

```
Child Interaction
    ↓
[Session Data Collection]
    ↓
[Real-time Analysis]
    ├→ Pattern Detection (errors, hesitation, pace)
    ├→ Anomaly Detection (gaming, device sharing)
    └→ Curriculum Grounding (graph query for next concept)
    ↓
[Pedagogical Decision]
    ├→ Next question difficulty
    ├→ Scaffold type (visual/verbal)
    ├→ Review schedule (spacing)
    └→ Intervention trigger (contrastive pairs, etc.)
    ↓
[Learner Model Update]  ← BLOCKED if session flagged
    ↓
[Parent Dashboard]  ← Always updated, full transparency
```

### Privacy Enforcement Layers

**Layer 1: Prompt Classification** (before LLM)
- Flags personal/emotional content
- Discards flagged responses (not stored)
- Parent notified if repeated attempts

**Layer 2: Data Minimization** (after interaction)
- Store only learning-relevant data
- No cross-session behavioral profiling beyond curriculum mastery
- 30-day auto-delete of session transcripts

**Layer 3: Parent Control** (dashboard)
- Full visibility into all data stored
- One-click data deletion
- Granular sharing controls (teachers, other parents)
- Opt-out of anonymized analytics

---

## Curriculum Grounding (Every Decision)

**Every pedagogical action is validated against the curriculum graph:**

```cypher
// Example: Is this intervention appropriate?
MATCH (c:Concept {concept_id: 'EN-Y1-PHON-002'})
RETURN c.source_reference, c.description

// Example: Are prerequisites met?
MATCH (prereq:Concept)-[:PREREQUISITE_OF]->(c:Concept {concept_id: 'MA-Y3-MULT-006'})
WHERE NOT (child)-[:MASTERED]->(prereq)
RETURN prereq.concept_name  // Should return empty if all mastered

// Example: What's next in the outer fringe?
MATCH (mastered:Concept)<-[:MASTERED]-(child)
MATCH (mastered)-[:PREREQUISITE_OF*]->(candidate:Concept)
WHERE NOT (child)-[:MASTERED]->(candidate)
  AND ALL(p IN [(candidate)<-[:PREREQUISITE_OF]-(prereq) | prereq]
          WHERE (child)-[:MASTERED]->(p))
RETURN candidate.concept_id, candidate.concept_name
ORDER BY candidate.complexity_level
LIMIT 3
```

Every question, every intervention, every difficulty adjustment is **grounded in the curriculum graph**, not arbitrary AI decisions.

---

## Next Steps

1. **Complete remaining stories** (7 more to write)
2. **Create parent dashboard mockups** (showing curriculum-mapped progress)
3. **Define data schemas** (formal JSON schemas for session data, learner models)
4. **Write detection algorithms** (production-ready pseudocode for all patterns)
5. **Build privacy compliance doc** (GDPR, Children's Code UK, COPPA)

---

## Philosophy

This is **not a chatbot that becomes your friend.**

This is **a curriculum-grounded adaptive system that optimizes learning while respecting children's privacy and developmental reality.**

The AI:
- ✅ Knows you struggle with /e/ vs /i/ sounds
- ✅ Knows you need visual scaffolds for fractions
- ✅ Knows your retrieval strength for each multiplication fact
- ❌ Doesn't know you like dinosaurs
- ❌ Doesn't know your parents are divorcing
- ❌ Doesn't form an emotional relationship with you

**It teaches. It doesn't befriend.**

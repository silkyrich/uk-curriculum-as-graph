# Story 02: Phoneme Confusion (/e/ vs /i/)

**Age**: 6 (Y1) | **Subject**: English Phonics | **Concept**: Short vowel discrimination

---

## The Narrative (What the Child Experiences)

Reuben, age 6, is working on CVC words with short vowel sounds. He's done this before — the AI knows he can decode simple words.

**Screen 1: Image of a hen**

**AI voice**: "What's in the middle? Listen: h... e... n."

*[Three tiles: **e** · **i** · **a**]*

*[Reuben taps **e**.]*

**AI**: "Yes! Short 'e' sound."

---

**Screen 2: Image of a pin**

**AI voice**: "What about this? P... i... n."

*[Same tiles]*

*[Reuben pauses, then taps **e**.]*

**AI** (neutral): "Let's hear it again. P... i... n. The sound in the middle is short 'i'."

*[Animated mouth shows /i/ vs /e/ articulation.]*

**AI**: "They're close. Even grown-ups mix them up."

---

**Screen 3: More practice**

*[Image of "bed"]*

*[Reuben taps **e**. Correct.]*

*[Image of "big"]*

*[Reuben hesitates... taps **i**. Correct!]*

**AI**: "You got that one. Last week you were mixing those sounds. Not this time."

---

## The Data (What We Collect)

### Raw Response Log

```json
{
  "session_id": "sess_2026_02_19_001",
  "child_id": "child_reuben_y1",
  "concept_id": "EN-Y1-PHON-002",  // Short vowel sounds /e/ vs /i/
  "responses": [
    {
      "timestamp": "2026-02-19T16:23:12Z",
      "stimulus": "hen",
      "target_phoneme": "/e/",
      "response": "/e/",
      "correct": true,
      "response_time_ms": 1800,
      "hesitation": false
    },
    {
      "timestamp": "2026-02-19T16:23:34Z",
      "stimulus": "pin",
      "target_phoneme": "/i/",
      "response": "/e/",  // ERROR
      "correct": false,
      "response_time_ms": 2100,
      "hesitation": true,  // pause detected before tap
      "error_type": "vowel_substitution"
    },
    {
      "timestamp": "2026-02-19T16:24:01Z",
      "stimulus": "bed",
      "target_phoneme": "/e/",
      "response": "/e/",
      "correct": true,
      "response_time_ms": 1600,
      "hesitation": false
    },
    {
      "timestamp": "2026-02-19T16:24:18Z",
      "stimulus": "big",
      "target_phoneme": "/i/",
      "response": "/i/",
      "correct": true,
      "response_time_ms": 3200,  // LONG hesitation
      "hesitation": true
    }
  ]
}
```

### Error Pattern Detection (Accumulated Over Past 5 Sessions)

```json
{
  "child_id": "child_reuben_y1",
  "error_patterns": {
    "vowel_confusion_e_i": {
      "misconception_type": "phonetic_proximity",
      "confusion_matrix": {
        "/e/": {
          "correct": 8,
          "confused_with_/i/": 2,
          "confused_with_/a/": 0
        },
        "/i/": {
          "correct": 5,
          "confused_with_/e/": 7,  // HIGH ERROR RATE
          "confused_with_/a/": 1
        }
      },
      "pattern_detected": "2026-02-17",  // Two sessions ago
      "frequency": 0.58,  // 7 out of 12 /i/ trials confused with /e/
      "direction": "asymmetric",  // /i/ → /e/ more than /e/ → /i/
      "intervention_triggered": "2026-02-19"  // Today's session
    }
  }
}
```

---

## The Inference (How the AI Detects the Pattern)

### Detection Algorithm

**Trigger conditions**:
1. Error rate on `/i/` phoneme > 50% over last 3 sessions
2. Substitution error is *consistent* (always `/e/`, not random)
3. Asymmetric confusion (child correctly identifies `/e/` most of the time)

**Code (pseudocode)**:
```python
def detect_vowel_confusion(child_id, target_phoneme):
    # Get last 3 sessions for this phoneme
    sessions = get_recent_sessions(child_id, phoneme=target_phoneme, n=3)

    # Build confusion matrix
    confusion = defaultdict(int)
    for response in sessions:
        if not response.correct:
            confusion[response.response] += 1

    # Check for systematic error
    if len(confusion) == 1:  # Only ONE type of error
        error_phoneme = list(confusion.keys())[0]
        error_rate = sum(confusion.values()) / len(sessions)

        if error_rate > 0.5:  # More than 50% error rate
            # Check if confusion is asymmetric
            reverse_error_rate = get_error_rate(child_id, error_phoneme, target_phoneme)

            if error_rate > 2 * reverse_error_rate:  # Asymmetric
                return {
                    "pattern": "systematic_confusion",
                    "target": target_phoneme,
                    "confused_with": error_phoneme,
                    "error_rate": error_rate,
                    "intervention": "contrastive_minimal_pairs"
                }

    return None
```

### Why This Pattern Matters

**Phonetic proximity**: `/e/` and `/i/` are articulated very similarly:
- Both are front vowels
- `/e/` has slightly more open mouth
- `/i/` has almost closed mouth

**Typical developmental trajectory**:
- Age 5-6: Confusion is normal
- Age 6-7: Should resolve with practice
- If persistent → needs explicit contrastive teaching

**The AI's hypothesis**:
> "Reuben hears the difference but his motor plan for articulation is imprecise. He needs visual feedback (mouth diagram) and contrastive practice (minimal pairs like 'pin' vs 'pen')."

---

## The Pedagogical Action (What the AI Does)

### Session Plan Modification

**Before pattern detection** (sessions 1-4):
- Randomly interleave all short vowels
- No special focus on /e/ vs /i/

**After pattern detection** (session 5 onwards):
- **Increased contrast**: Always present /e/ and /i/ in adjacent trials
- **Minimal pairs**: Use words that differ only in this sound (pin/pen, big/beg, hit/het)
- **Visual scaffold**: Show articulatory diagram every time
- **Explicit metacognition**: "These two are close. Even grown-ups mix them up."

### What the AI Says (and Why)

**After error on "pin"**:
> "Let's hear it again. P... i... n. The sound in the middle is short 'i'."

**Why this response**:
- ✅ Non-judgmental ("Let's hear it again" not "Wrong!")
- ✅ Repeats stimulus (gives second chance)
- ✅ Explicit labels the correct answer ("short 'i'")
- ❌ Doesn't explain WHY yet (productive failure — let him notice pattern first)

**After showing mouth diagram**:
> "They're close. Even grown-ups mix them up."

**Why this response**:
- ✅ Normalizes the error (reduces anxiety)
- ✅ Provides explanation (phonetic proximity)
- ✅ Effort attribution ("close" = you're nearly there, not "you're bad at this")

**After correct answer on "big"** (after long hesitation):
> "You got that one. Last week you were mixing those sounds. Not this time."

**Why this response**:
- ✅ Self-comparative feedback (not absolute praise)
- ✅ Acknowledges the *improvement* (growth mindset)
- ✅ Informational, not controlling (SDT: supports competence without being patronizing)

---

## Data Storage (What Persists)

### Learner Model Update

```json
{
  "child_id": "child_reuben_y1",
  "phoneme_confusions": {
    "/i/": {
      "primary_confusion": "/e/",
      "error_rate": 0.58,
      "status": "intervention_active",
      "intervention_start": "2026-02-19",
      "last_updated": "2026-02-19T16:24:30Z"
    }
  },
  "intervention_schedule": {
    "EN-Y1-PHON-002": {
      "type": "contrastive_minimal_pairs",
      "frequency": "daily",
      "next_session": "2026-02-20",
      "exit_criteria": "3_consecutive_sessions_80%_accuracy"
    }
  }
}
```

### What's NOT Stored

```json
// ❌ These are NEVER stored:
{
  "child_emotional_state": "frustrated when making errors",
  "personal_context": "Reuben mentioned his teacher said...",
  "cross_domain_interests": "likes dinosaurs, should use dinosaur examples"
}
```

**Why not store interests?**
- Child's preference for dinosaurs is *personal information* unrelated to phonics mastery
- Using "personalized" examples based on inferred interests creates parasocial relationship
- Violates privacy principle: AI learns HOW child learns, not WHO child is

**What we DO store**:
- Error patterns (phoneme confusion)
- Optimal scaffolding type (visual > auditory for this child)
- Retrieval schedule (when to review)

---

## Validation Query (From Curriculum Graph)

**How we know this intervention is valid**:

```cypher
// Check that /e/ vs /i/ discrimination is in the curriculum
MATCH (c:Concept {concept_id: 'EN-Y1-PHON-002'})
WHERE c.concept_name CONTAINS 'short vowel'
RETURN c.description, c.source_reference

// Check prerequisites
MATCH (prereq:Concept)-[:PREREQUISITE_OF]->(c:Concept {concept_id: 'EN-Y1-PHON-002'})
RETURN prereq.concept_name

// Expected prerequisite: "Can hear and identify initial sounds"
```

**Curriculum grounding**:
- KS1 English Programme of Study: "apply phonic knowledge and skills as the route to decode words"
- Specifically: distinguish between short vowel phonemes in CVC words
- This is a PREREQUISITE for reading fluency

---

## Success Criteria (When to Exit Intervention)

**Exit criteria** (moves back to general phonics practice):
1. 3 consecutive sessions with ≥80% accuracy on /i/ vs /e/ discrimination
2. Response time < 3000ms (indicating fluent retrieval, not effortful processing)
3. No hesitation markers (confidence increasing)

**Monitoring** (next 5 sessions):
```python
def check_exit_criteria(child_id, phoneme="/i/"):
    recent_sessions = get_sessions(child_id, phoneme, n=3)

    accuracy = [s.accuracy for s in recent_sessions]
    avg_response_time = [s.avg_response_time for s in recent_sessions]

    if all(a >= 0.8 for a in accuracy) and all(rt < 3000 for rt in avg_response_time):
        return "exit_intervention"
    else:
        return "continue_intervention"
```

**If intervention fails after 10 sessions**:
- Flag for parent review
- Suggest: "Reuben is working hard on distinguishing /e/ and /i/ sounds. This is tricky for many children at this age. You might want to mention it to his teacher at the next parents' evening."

---

## Privacy Boundary

**What the AI knows**:
- ✅ Reuben confuses /i/ with /e/ 58% of the time
- ✅ Visual scaffolds work better than auditory for him
- ✅ He showed improvement from last week (data-based, not emotional)

**What the AI does NOT know**:
- ❌ That Reuben has dyslexia (parent hasn't shared, AI shouldn't infer)
- ❌ That Reuben's parents are worried about his reading (personal/emotional)
- ❌ That Reuben likes dinosaurs (interest unrelated to phonics)

**Parent dashboard shows**:
> **Phonics progress (session 5)**
>
> Reuben is working on distinguishing /e/ (as in 'hen') and /i/ (as in 'pin'). This is one of the most common confusions at Y1. Today he got 3/4 correct, including a self-correction. That's progress from last week (1/3 correct).
>
> **Curriculum map**: KS1 English → Reading → Phonics → "distinguish between short vowel sounds in CVC words"
>
> **Next steps**: We'll continue focused practice on these two sounds for the next few sessions. Once he's consistently accurate, we'll move on to other vowel pairs.

---

## Technical Summary

**Data collected**: Response accuracy, response times, hesitation markers, error types
**Pattern detected**: Systematic /i/ → /e/ confusion (58% error rate, asymmetric)
**Inference**: Phonetic proximity causing articulatory interference
**Action**: Contrastive minimal pairs + visual articulation scaffold
**Storage**: Error pattern, intervention type, exit criteria
**Privacy**: No emotional/personal data, no inferred interests, pure learning pattern data

This is how the AI "magically" knew what to do — it's not magic, it's systematic error pattern detection and evidence-based pedagogical response.

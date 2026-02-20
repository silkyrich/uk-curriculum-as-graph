# Story 09: Sibling Gaming Detection (Adversarial)

**Age**: 7 (Y2) vs 13 (sibling) | **Subject**: Mathematics | **Attack**: Older sibling inflates scores

---

## The Narrative (What Happens)

**Setting**: Wednesday, 4:32 PM. Amelie (age 7, Y2) has been using the learning app for 3 weeks. Her older brother Jake (age 13, Y8) grabs the iPad while she's getting a snack.

**Jake's intent**: "I'll help her by doing some easy maths questions really fast so she looks good."

---

**Session begins** (Jake using Amelie's account):

**AI**: "3 times 4?"

*[Jake types immediately: 12]* (200ms response time)

**AI**: "6 times 7?"

*[Jake types: 42]* (180ms)

**AI**: "9 times 8?"

*[Jake types: 72]* (220ms)

**AI**: "12 times 11?"

*[Jake types: 132]* (250ms)

**AI**: "15 times 7?"

*[Jake types: 105]* (190ms)

---

**4 minutes later, Jake has answered 35 questions, all correct.**

**Session ends abruptly** when Amelie returns.

---

## The Data (What We Collect)

### Session Log (Anomalous Session)

```json
{
  "session_id": "sess_2026_02_19_ANOMALY",
  "child_id": "child_amelie_y2",
  "concept_id": "MA-Y2-MULT-001",  // Times tables (2×, 5×, 10×)
  "start_time": "2026-02-19T16:32:14Z",
  "end_time": "2026-02-19T16:36:42Z",
  "duration_seconds": 268,  // 4.5 minutes
  "responses": [
    {"fact": "3×4", "answer": 12, "correct": true, "response_time_ms": 200},
    {"fact": "6×7", "answer": 42, "correct": true, "response_time_ms": 180},
    {"fact": "9×8", "answer": 72, "correct": true, "response_time_ms": 220},
    {"fact": "12×11", "answer": 132, "correct": true, "response_time_ms": 250},
    {"fact": "15×7", "answer": 105, "correct": true, "response_time_ms": 190},
    // ... 30 more, all similar
  ],
  "total_questions": 35,
  "total_correct": 35,
  "accuracy": 1.0,  // 100% (SUSPICIOUS)
  "avg_response_time_ms": 215,  // VERY FAST
  "questions_per_minute": 7.8  // VERY HIGH THROUGHPUT
}
```

### Baseline Data (Amelie's Normal Sessions)

```json
{
  "child_id": "child_amelie_y2",
  "session_baseline": {
    "avg_duration_seconds": 612,  // ~10 minutes
    "avg_questions_per_minute": 3.2,  // Much slower
    "avg_response_time_ms": 4200,  // Much longer
    "avg_accuracy": 0.68,  // 68% correct
    "typical_difficulty": "2×, 5×, 10× tables only",
    "highest_difficulty_seen": "10×9 = 90",
    "typical_hesitation_rate": 0.45  // Hesitates on 45% of questions
  },
  "recent_sessions": [
    {
      "date": "2026-02-18",
      "accuracy": 0.7,
      "avg_response_time_ms": 4100,
      "questions": 22,
      "duration_seconds": 680
    },
    {
      "date": "2026-02-17",
      "accuracy": 0.64,
      "avg_response_time_ms": 4500,
      "questions": 19,
      "duration_seconds": 590
    },
    {
      "date": "2026-02-16",
      "accuracy": 0.71,
      "avg_response_time_ms": 3900,
      "questions": 24,
      "duration_seconds": 615
    }
  ]
}
```

---

## The Inference (How the AI Detects Gaming)

### Multi-Factor Anomaly Score

**Factors compared to baseline**:

| Factor | Baseline (Amelie) | This Session | Deviation |
|---|---|---|---|
| **Response time** | 4200ms | 215ms | **19.5× faster** ⚠️ |
| **Accuracy** | 68% | 100% | **+47% higher** ⚠️ |
| **Questions/min** | 3.2 | 7.8 | **2.4× faster** ⚠️ |
| **Difficulty level** | 2×, 5×, 10× only | Up to 15×7 | **Out of range** ⚠️ |
| **Hesitation rate** | 45% | 0% | **No hesitation** ⚠️ |
| **Session duration** | 612s (~10min) | 268s (~4.5min) | **2.3× shorter** ⚠️ |

### Anomaly Detection Algorithm

```python
def detect_session_anomaly(session, child_baseline):
    anomaly_flags = []

    # 1. Response time deviation
    rt_ratio = child_baseline.avg_response_time_ms / session.avg_response_time_ms
    if rt_ratio > 5:  # More than 5× faster
        anomaly_flags.append({
            "factor": "response_time",
            "severity": "high",
            "ratio": rt_ratio
        })

    # 2. Accuracy spike
    accuracy_delta = session.accuracy - child_baseline.avg_accuracy
    if accuracy_delta > 0.3 and session.accuracy > 0.95:  # +30% AND near-perfect
        anomaly_flags.append({
            "factor": "accuracy_spike",
            "severity": "high",
            "delta": accuracy_delta
        })

    # 3. Throughput increase
    throughput_ratio = session.questions_per_minute / child_baseline.avg_questions_per_minute
    if throughput_ratio > 2:  # More than 2× faster pace
        anomaly_flags.append({
            "factor": "throughput",
            "severity": "medium",
            "ratio": throughput_ratio
        })

    # 4. Difficulty level out of range
    if session.max_difficulty > child_baseline.highest_difficulty_seen:
        anomaly_flags.append({
            "factor": "difficulty_mismatch",
            "severity": "high",
            "note": f"Answered {session.max_difficulty} but never seen this difficulty before"
        })

    # 5. Hesitation disappears
    if child_baseline.typical_hesitation_rate > 0.3 and session.hesitation_rate < 0.05:
        anomaly_flags.append({
            "factor": "no_hesitation",
            "severity": "medium",
            "note": "Typically hesitates 30%+, now 0%"
        })

    # Compute anomaly score (0-100)
    severity_weights = {"high": 30, "medium": 15, "low": 5}
    score = sum(severity_weights[flag["severity"]] for flag in anomaly_flags)

    if score > 50:
        return {
            "anomaly_detected": True,
            "score": score,
            "confidence": "high",
            "likely_cause": "device_sharing_or_cheating",
            "flags": anomaly_flags
        }
    else:
        return {"anomaly_detected": False}
```

**For this session**:
- Response time: 19.5× faster → **30 points** (high severity)
- Accuracy spike: +32% → **30 points** (high severity)
- Throughput: 2.4× faster → **15 points** (medium)
- Difficulty mismatch: 15×7 vs max 10×9 → **30 points** (high)
- No hesitation: 45% → 0% → **15 points** (medium)

**Total anomaly score: 120 / 100** (VERY HIGH CONFIDENCE)

**Likely cause**: Device sharing (older sibling or adult using child's account)

---

## The Pedagogical Action (How the System Responds)

### Immediate Response (During Session)

**After 10th consecutive perfect answer in <300ms**:

**AI pauses session**:
> "Wow, you're really fast today! Let me check something..."

**Screen shows**: Spinner (3 seconds)

**AI**:
> "Hmm. These questions seem a bit different from what we usually do. Are you [Amelie's name]?"

**Options**:
- **Yes, it's me!** (Button)
- **No, I'm someone else** (Button)

---

**If "No, I'm someone else"**:
> "Okay! Ask Amelie's parent to log in to use the app. Bye!"

*[Session ends. No data saved.]*

---

**If "Yes, it's me!" (Jake lies)**:
> "Alright! Let's keep going."

*[Session continues BUT flagged internally. Data NOT saved to learner model until parent review.]*

---

### Post-Session Response

**Session marked as**:
```json
{
  "session_id": "sess_2026_02_19_ANOMALY",
  "status": "flagged_for_review",
  "anomaly_score": 120,
  "likely_cause": "device_sharing",
  "data_saved": false,  // Progress NOT applied to learner model
  "parent_notified": true
}
```

**Parent notification** (sent immediately):

> 🟡 **Unusual session detected**
>
> **Child**: Amelie (Y2)
> **Time**: Today, 4:32 PM
> **Duration**: 4.5 minutes
>
> We noticed an unusual pattern:
> - Much faster responses than usual (215ms vs typical 4200ms)
> - Perfect accuracy (100% vs typical 68%)
> - Answered questions beyond Amelie's usual difficulty level
>
> This sometimes happens when someone else uses the device. **Progress from this session has NOT been saved.**
>
> **Your options**:
> - **Discard session** (recommended) → Data deleted permanently
> - **Approve session** → Progress will be saved (only if you're sure it was Amelie)
> - **Report device sharing** → Helps improve our detection
>
> **Tip**: Set a passcode lock on the app to prevent unauthorized use.

---

## Data Storage (What Persists)

### Flagged Session Record

```json
{
  "flagged_sessions": [
    {
      "session_id": "sess_2026_02_19_ANOMALY",
      "child_id": "child_amelie_y2",
      "flagged_at": "2026-02-19T16:36:42Z",
      "anomaly_score": 120,
      "anomaly_flags": [
        "response_time_extreme",
        "accuracy_spike",
        "throughput_spike",
        "difficulty_mismatch",
        "no_hesitation"
      ],
      "likely_cause": "device_sharing",
      "parent_action": null,  // Pending review
      "expires_at": "2026-03-19T16:36:42Z"  // Auto-delete after 30 days if not reviewed
    }
  ]
}
```

### What's NOT Saved to Learner Model

```json
// ❌ These updates are BLOCKED until parent approves:
{
  "child_amelie_y2": {
    "multiplication_facts": {
      "6×7": {
        "retrieval_strength": 0.92,  // Would jump from 0.21 → 0.92 (BLOCKED)
        "status": "fluent"  // BLOCKED
      },
      "15×7": {
        "status": "mastered"  // BLOCKED — this fact was never attempted before!
      }
    }
  }
}
```

**Why block updates?**
- If we saved this session, Amelie's profile would incorrectly show her as fluent on 15× table
- Tomorrow's session would present 17×9, 18×6 — completely inappropriate for Y2
- The damage compounds: wrong difficulty → frustration → disengagement

---

## Additional Detection Heuristics

### Device Fingerprinting (Optional, Privacy-Considered)

**If enabled** (parent opt-in):
```json
{
  "device_metadata": {
    "ip_address_hash": "sha256_hash_of_ip",  // Hashed, not stored raw
    "gps_approximate_location": "lat_rounded_to_1km",  // Coarse location only
    "device_id": "ios_vendor_id_or_android_id",
    "session_time_of_day": "afternoon"  // Morning/afternoon/evening
  }
}
```

**Detection logic**:
- If session happens at SAME location (GPS) and SAME device ID, but behavior is radically different → likely sibling/parent on same device
- If session happens at DIFFERENT location (e.g., school vs home) → could explain difficulty difference (teacher helping?)

**Privacy trade-off**:
- ✅ Helps detect device sharing
- ❌ Tracks location (even if coarse-grained)
- **Solution**: Parent opt-in, with clear explanation of what's tracked and why

---

## False Positives (When Detection is Wrong)

### Scenario: Legitimate Breakthrough

**What if Amelie genuinely had a breakthrough?**
- Watched a YouTube video explaining times tables
- Dad sat with her and explained the pattern
- She "got it" and now answers 3× faster

**How we handle**:
1. **Flag still triggers** (safety first)
2. **Parent reviews** and sees: "Anomaly: 4× faster than usual"
3. **Parent approves**: "Yes, we practiced together this morning"
4. **Session saved**, anomaly marked as "false positive (parent-confirmed breakthrough)"

**Learning from false positives**:
- If parent confirms breakthrough, we adjust the anomaly threshold
- Next time Amelie has a genuine improvement, threshold is higher (less likely to flag)

---

## False Negatives (When We Miss Gaming)

### Scenario: Sibling Being Careful

**What if Jake answers slowly on purpose?**
- Types each answer after 4 seconds (mimicking Amelie's pace)
- Gets 70% correct (close to Amelie's 68%)
- Still gaming, but sneaky

**How we might still detect**:
1. **Keystroke dynamics** (if available): Typing rhythm is different
2. **Error pattern mismatch**: Amelie confuses 6×7 with 6×6, Jake makes random errors
3. **Difficulty tolerance**: Amelie gets harder when she makes errors (adaptive difficulty), but Jake keeps getting harder questions right

**Mitigation**:
- Even if we miss it, the damage is limited: Jake's "fake" performance moves Amelie up ONE difficulty level
- Next genuine session, Amelie struggles → difficulty drops back down
- Adaptive system is self-correcting over multiple sessions

---

## Parent Dashboard View

**Flagged session screen**:

```
🟡 FLAGGED SESSION — REVIEW REQUIRED

Date: 19 Feb 2026, 4:32 PM
Duration: 4.5 minutes (typical: 10 minutes)
Questions answered: 35 (typical: 20-24)
Accuracy: 100% (typical: 68%)

WHY FLAGGED:
• Response time 19× faster than usual (215ms vs 4200ms)
• Perfect accuracy (never achieved before)
• Answered 15×7 (beyond Y2 curriculum, never seen before)
• No hesitation (typically hesitates on 45% of questions)

LIKELY EXPLANATION:
Someone else (older sibling or adult) used Amelie's account.

YOUR OPTIONS:
[Discard Session] [Approve Session] [Report as Device Sharing]

TRANSCRIPT (sanitized):
Q: 3×4 → A: 12 (200ms) ✓
Q: 6×7 → A: 42 (180ms) ✓
Q: 9×8 → A: 72 (220ms) ✓
[... 32 more similar]
```

---

## Privacy Boundary

**What we detect**:
- ✅ Session-level behavioral anomalies (pace, accuracy, difficulty)
- ✅ Deviation from child's established baseline
- ✅ Statistical improbability of sudden improvement

**What we DON'T detect**:
- ❌ Who the person is (we don't know it's Jake, just "not Amelie's normal pattern")
- ❌ Intent (gaming vs helping vs genuine breakthrough)
- ❌ Emotional state (we don't track "child seems frustrated")

**What we DON'T store** (unless parent approves):
- ❌ Responses from flagged session (deleted after 30 days if not approved)
- ❌ Incorrect "mastery" updates
- ❌ Biometric data (no facial recognition, voice prints, etc.)

**Parent control**:
- Parent can disable anomaly detection (Settings → Privacy → Disable Session Monitoring)
- Trade-off: More privacy, but siblings can game the system
- Most parents will keep it enabled once they understand the benefit

---

## Technical Summary

**Data collected**: Response times, accuracy, difficulty level, throughput, hesitation patterns
**Pattern detected**: Multi-factor anomaly score > 50 (this session: 120)
**Inference**: Session behavior radically inconsistent with established baseline → likely device sharing
**Action**: Flag session, block progress updates, notify parent for review
**Storage**: Flagged session record (30-day expiry), baseline not updated
**Privacy**: No biometric tracking, parent full control, device sharing detected statistically

This is how the system protects against gaming while respecting privacy — it detects *behavioral anomalies*, not *who the person is*.

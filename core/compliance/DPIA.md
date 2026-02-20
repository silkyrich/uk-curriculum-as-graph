# Data Protection Impact Assessment (DPIA)

**Following ICO Annex D template for Children's Code compliance**

**Status**: SKELETON — sections pre-populated from existing analysis. Requires human review, legal counsel input, and sign-off before launch.

**Service name**: [Platform name TBD]
**Assessment date**: 2026-02-20
**Assessment author**: [To be completed]
**DPO review**: [Not yet appointed — see Section 9]
**Next review date**: [Before beta launch, and after any material processing change]

---

## 1. Description of Processing

### 1.1 What personal data will you process?

**Tier 0 — Identity (separate service)**:
- Parent email address
- Child first name
- Year group (e.g., Y3)
- Subjects enabled (e.g., Maths, English)
- Consent records per processing purpose

**Tier 1 — Learning Events (pseudonymous event store)**:
- Learner UUID (no name)
- Question attempt results (correct/incorrect)
- Response time (milliseconds)
- Error pattern identifiers (e.g., "vowel_confusion_e_i")
- Scaffold type used (visual/verbal/manipulative)
- Hint requested (boolean)
- Session ID and timestamps
- Anomaly detection scores

**Tier 2 — Derived (computed, not stored independently)**:
- Mastery probability per curriculum concept
- Retrieval strength per fact
- Optimal spacing intervals
- Scaffold preference
- Outer fringe (next recommended concepts)

**Full classification**: `core/compliance/DATA_CLASSIFICATION.md`

### 1.2 Why do you need to process it?

To provide personalised, curriculum-aligned adaptive learning for children aged 5-14. The core educational value depends on tracking what the child knows (mastery), how they learn best (scaffolding), and what they should learn next (curriculum sequencing). Without this processing, the service cannot adapt to the individual child and degrades to a static question bank.

### 1.3 Who will the data be shared with?

| Recipient | Data Shared | Basis | Parent Control |
|---|---|---|---|
| Child (on screen) | Current session only | Service delivery | N/A |
| Parent (dashboard) | All Tier 0 + Tier 1 + Tier 2 for their child | Service delivery | Always visible |
| Teachers (if shared) | Mastery progress + optional error patterns + optional session summaries | Parental consent (Purpose B) | Per-teacher, per-data-type toggle |
| LLM inference provider | Concept IDs, error patterns, scaffold types, possibly child first name | Processor agreement (Art. 28) | Part of core consent (Purpose A) |
| Cloud infrastructure | Encrypted Tier 0 and Tier 1 data | Processor agreement (Art. 28) | N/A (infrastructure) |
| No other recipients | — | — | — |

**Not shared with**: Other parents, other children, advertisers, data brokers, researchers (unless Tier 3 anonymised aggregates with separate consent).

### 1.4 How long will you keep it?

| Data | Retention | Deletion Method |
|---|---|---|
| Learning events | 12 months rolling | Automated hard delete |
| Session transcripts | 30 days | Automated hard delete |
| Identity data | Until account deletion | Hard delete within 72 hours of request |
| Consent records | 6 years after withdrawal | Hard delete after 6 years |
| Anonymised aggregates | Indefinite | Cannot be attributed to individual |

### 1.5 Lawful basis for each purpose

| Purpose | Lawful Basis | Justification |
|---|---|---|
| Core adaptive learning (Purpose A) | Consent — Art. 6(1)(a) + Art. 8 | Parent actively consents; under-13 age threshold |
| Teacher sharing (Purpose B) | Consent — Art. 6(1)(a) | Optional, per-teacher, per-data-type |
| Anonymised analytics (Purpose C) | Consent — Art. 6(1)(a) | Optional, separate toggle |
| Camera/microphone (Purpose D) | Consent — Art. 6(1)(a) | Per-activity, per-modality |
| Safety/anomaly detection (Purpose E) | Legitimate interests — Art. 6(1)(f) | Safety of child; cannot be consent-gated |

**Legitimate Interests Assessment for Purpose E**:
- Purpose: Detect sibling gaming, device sharing, prompt injection, off-curriculum requests
- Necessity: Cannot achieve safety goals without monitoring session patterns
- Balance: Minimal additional data (one score field); full parent transparency; protects child's interests
- Conclusion: Child's safety interest outweighs minimal privacy impact

---

## 2. Necessity and Proportionality

### 2.1 Is the processing necessary?

| Data Element | Necessity Argument | Less Intrusive Alternative? |
|---|---|---|
| Attempt result (correct/incorrect) | Core input to knowledge tracing model; cannot estimate mastery without it | None — this is the minimum viable signal |
| Response time | Distinguishes fluent retrieval from derivation; critical for spacing algorithm | Could omit, but significantly degrades spacing quality |
| Error pattern | Enables targeted intervention (e.g., contrastive pairs for phoneme confusion) | Could omit, but child gets generic rather than targeted remediation |
| Scaffold type | Enables personalised pedagogy (visual vs verbal) | Could omit, but all children get same scaffold regardless of effectiveness |
| Session timestamps | Required for spacing algorithm (days since last review) | Could use session count instead, but less accurate |
| Anomaly score | Detects gaming, device sharing; protects integrity of learner model | None — safety processing requires this |

### 2.2 Could you achieve the purpose with less data?

The minimum viable learner model schema (documented in `docs/design/RESEARCH_BRIEFING.md` Section 6) is already the result of a minimisation exercise. Every element has a specific pedagogical justification. The schema is:

```
learner_id, timestamp, event_type, concept_id, item_id, correct, response_ms, attempt_number
```

Removing any element measurably degrades adaptive quality. This has been benchmarked against the knowledge tracing literature (BKT, PFA, DKT variants).

### 2.3 Are privacy settings at the highest level by default?

Yes:
- All consent toggles default to OFF
- No profiling until parent actively consents
- No teacher sharing until parent actively enables per teacher
- No camera/microphone until parent actively enables per activity
- No analytics until parent actively opts in

---

## 3. Risk Assessment

### 3.1 Risks to Children

| # | Risk | Likelihood | Impact | Inherent Risk |
|---|---|---|---|---|
| R1 | Data breach exposing learning profiles | Low | High | Medium |
| R2 | Profiling creates stigmatising labels visible to child | Medium | High | High |
| R3 | AI makes incorrect pedagogical decision | Medium | Medium | Medium |
| R4 | Parent uses data to pressure child academically | Low | High | Medium |
| R5 | Child feels surveilled / monitored | Medium | Medium | Medium |
| R6 | Scope creep — data used for unintended purposes | Low | High | Medium |
| R7 | LLM generates harmful or incorrect content | Medium | High | High |
| R8 | Consent fatigue — parent doesn't understand what they're consenting to | Medium | Medium | Medium |
| R9 | Child forms emotional attachment to AI tutor | Medium | High | High |
| R10 | Third-party processor breach or misuse | Low | High | Medium |
| R11 | Re-identification from anonymised aggregates | Low | Medium | Low |

### 3.2 Mitigation Measures

| # | Risk | Mitigation | Residual Risk |
|---|---|---|---|
| R1 | Data breach | Pseudonymised event log; identity architecturally separated; encryption at rest and in transit; access controls | Low |
| R2 | Stigmatising labels | Profile expressed ONLY as pedagogical actions (next question, scaffold type); child never sees labels like "struggling" or "below average"; no competitive framing | Low |
| R3 | Incorrect pedagogy | All decisions grounded in curriculum graph; prerequisite chain validation; parent can see reasoning and override mastery status | Low |
| R4 | Parental pressure | Dashboard shows mastery against curriculum, never against other children; no predictive analytics; guidance on healthy engagement | Low |
| R5 | Surveillance feeling | Child informed of monitoring in age-appropriate language; warm non-evaluative UI tone; no time-tracking or engagement metrics | Low |
| R6 | Scope creep | Purpose limitation enforced in architecture (event store schema rejects non-schema fields); no third-party data access; code review process requires data classification | Low |
| R7 | Harmful LLM content | Curriculum grounding (LLM constrained to concept nodes); output classifier; no open-ended generation; session termination for safety flags | Low |
| R8 | Consent fatigue | Layered consent (short summary + detailed per-purpose); specific toggles not bundled; "Learn more" expandable sections; child-friendly summary | Low |
| R9 | Emotional attachment | AI persona is a tutor, not a friend; prompt classifier discards personal/emotional content; no relationship-forming language; no memory of personal details | Low |
| R10 | Processor breach | Art. 28 agreements; training exclusion clauses; sub-processor transparency; PII audit of what enters each processor | Low |
| R11 | Re-identification | k=1000+ minimum aggregation; differential privacy consideration for small concept sets | Low |

---

## 4. Children's Code Compliance

| Standard | Compliant? | Evidence |
|---|---|---|
| 1. Best interests | Yes | Every design decision documented with child welfare rationale (RESEARCH_BRIEFING.md) |
| 2. DPIA | In progress | This document |
| 3. Age appropriate | Yes | Learner profiles layer: 9 year-group profiles with interaction, content, pedagogy, feedback constraints |
| 4. Transparency | Designed | Parent dashboard with full data visibility; child-friendly explanations; layered consent |
| 5. Detrimental use | Yes | No engagement maximisation; no commercial profiling; no addictive patterns; no gamification |
| 6. Policies | TODO | Need to write published, child-appropriate terms of service |
| 7. Default settings | Yes | All consent off by default; highest privacy |
| 8. Data minimisation | Yes | Minimum viable schema documented and justified (RESEARCH_BRIEFING.md Section 6) |
| 9. Data sharing | Yes | No third-party sharing; parent controls teacher access per teacher per data type |
| 10. Geolocation | Yes | Not collected |
| 11. Parental controls | Designed | Full dashboard; child notified of monitoring |
| 12. Profiling | Yes (with compelling reason) | Compelling reason documented in CHILD_PROFILE_CONSENT.md Section 3; safeguards in place |
| 13. Nudge techniques | Yes | No dark patterns; no gamification; no streaks or badges |
| 14. Connected toys | N/A | Unless camera/mic features enabled (separate consent per modality) |
| 15. Online tools | Designed | One-click deletion; account removal; consent withdrawal; data export |

---

## 5. Consultation

### 5.1 DPO Review

| Item | Status |
|---|---|
| DPO appointed? | TODO — likely required given systematic monitoring of children |
| DPO reviewed this DPIA? | Not yet |

### 5.2 Expert Consultation

| Item | Status |
|---|---|
| Legal counsel reviewed consent architecture? | TODO |
| Children's rights expert consulted? | TODO |
| Parent user testing of consent flow? | TODO |
| Child user testing of transparency messaging? | TODO |

### 5.3 ICO Engagement

| Item | Status |
|---|---|
| ICO Regulatory Sandbox application? | TODO — recommended for novel AI + children use case |
| ICO prior consultation required? | Assess after completing risk analysis — if residual risks remain high, Art. 36 prior consultation required |

---

## 6. Sign-Off

| Role | Name | Date | Signature |
|---|---|---|---|
| Assessment author | | | |
| Data Protection Officer | | | |
| Senior responsible owner | | | |
| Legal counsel | | | |

**This DPIA must be reviewed and updated**:
- Before beta launch
- When processing operations change materially
- When new data elements are introduced
- When new third-party processors are engaged
- At minimum annually

---

## 7. Appendices

### Appendix A: Data Flow Diagram

```
[Parent Account]                    [Child Session]
      |                                   |
      v                                   v
[Identity Service]              [Session Service]
  - email                        - joins identity + graph
  - child name                   - runs prompt classifier
  - year group                   - enforces session limits
  - consent records              - generates pedagogical decisions
      |                                   |
      |        [IDENTITY BOUNDARY]        |
      |                                   v
      |                          [Learning Event Store]
      |                            - learner_id (UUID)
      |                            - concept_id
      |                            - correct/incorrect
      |                            - response_time_ms
      |                            - scaffold_type
      |                            - anomaly_score
      |                                   |
      |                                   v
      |                          [Knowledge Tracing Model]
      |                            - mastery per concept
      |                            - retrieval strength
      |                            - spacing intervals
      |                            - scaffold preference
      |                                   |
      +----> [Parent Dashboard] <---------+
               - full visibility
               - deletion controls
               - sharing toggles
               - consent management
```

### Appendix B: Related Documents

| Document | Location |
|---|---|
| Data classification | `core/compliance/DATA_CLASSIFICATION.md` |
| Consent rules | `core/compliance/CONSENT_RULES.md` |
| Full legal analysis | `docs/design/CHILD_PROFILE_CONSENT.md` |
| Research briefing | `docs/design/RESEARCH_BRIEFING.md` |
| Privacy architecture | `docs/user-stories/README.md` |
| Child experience design | `docs/user-stories/child-experience/CHILD_EXPERIENCE.md` |
| Regulatory research | `docs/research/privacy-compliance/` |
| Learner profiles layer | `layers/learner-profiles/README.md` |

### Appendix C: Regulatory References

| Regulation | Relevant Provisions |
|---|---|
| UK GDPR | Art. 5 (principles), Art. 6 (lawful bases), Art. 7 (consent conditions), Art. 8 (child consent), Art. 13-14 (transparency), Art. 15-22 (data subject rights), Art. 25 (privacy by design), Art. 28 (processors), Art. 30 (ROPA), Art. 35 (DPIA), Art. 36 (prior consultation) |
| ICO Children's Code | All 15 standards |
| Data Protection Act 2018 | s.9 (age of consent = 13), s.25 (ICO registration) |
| Online Safety Act 2023 | Protection of Children Codes (from July 2025) |
| Data (Use and Access) Act 2025 | ICO guidance under review from June 2025 |

# Data Classification — Developer Reference

**Purpose**: Every data element in the platform must be classified into one of these tiers. This is not optional. If you are adding a new data element and it doesn't fit a tier, stop and ask.

**Authority**: This classification implements the requirements of the ICO Children's Code (Standards 5, 8, 12), UK GDPR data minimisation (Art. 5(1)(c)), and the platform's ethical framework. Full analysis: `docs/design/CHILD_PROFILE_CONSENT.md`.

---

## Tier 0: Identity

**Stored in**: Separate identity service (NEVER in the learning event store)
**Retention**: Until account deletion
**Access**: Account management only; joined to events at runtime, never persisted in joined form

| Data Element | Purpose | Notes |
|---|---|---|
| Parent email | Account, notifications | Verified at sign-up |
| Child first name | Personalise UI | Display only |
| Year group | Select age-appropriate constraints | Maps to learner-profiles layer |
| Subjects enabled | Scope the curriculum | Parent-configurable |
| Consent records | Proof of consent per purpose | Retained 6 years after withdrawal (legal requirement) |
| Sharing permissions | Teacher sharing grants | Per-teacher, per-data-type |

**Not in Tier 0** (not collected at all): Surname, school name, address, date of birth, photo, device fingerprint.

---

## Tier 1: Learning Events

**Stored in**: Pseudonymous event store (learner_id is a UUID, not a name)
**Retention**: 12 months rolling (auto-delete)
**Format**: xAPI-compatible
**Lawful basis**: Parental consent (Art. 6(1)(a) + Art. 8)

| Data Element | Example | Purpose | Notes |
|---|---|---|---|
| learner_id | UUID | Link events to one learner | Pseudonymous — no name |
| concept_id | `MA-Y3-C042` | Curriculum grounding | Neo4j node reference |
| item_id | Question bank reference | Track which question | Not the question text |
| correct | true/false | Mastery estimation | Core BKT input |
| response_time_ms | 1200 | Retrieval strength | <2000ms = fluent, >4000ms = deriving |
| attempt_number | 2 | Within this item | For multi-attempt analysis |
| hint_requested | true/false | Scaffold effectiveness | Tier 1 only if no PII in hint |
| scaffold_type | "visual" | Personalise intervention | Categorical, not free-text |
| error_pattern_id | "vowel_confusion_e_i" | Misconception tracking | Systematic patterns only |
| session_id | UUID | Group events | 30-day retention for transcripts |
| timestamp | ISO 8601 | Ordering, spacing calc | Not used for time-of-day profiling |
| anomaly_score | 120 | Safety (sibling detection) | Legitimate interests basis |

### What makes a valid Tier 1 element?

Ask these three questions:
1. **Is it necessary for a pedagogical decision?** (mastery, spacing, scaffolding, difficulty)
2. **Is it pseudonymous?** (no names, no school, no identifying context)
3. **Does it avoid inferring who the child is?** (no emotional state, no interests, no personal context)

All three must be YES. If any is NO, it is either Tier 0 (identity), Tier 3 (aggregate only), or PROHIBITED.

---

## Tier 2: Derived Learner Model

**Stored as**: Computed projections over Tier 1 events (not independently stored)
**Retention**: Recomputed; deleting Tier 1 events makes the model empty
**Characteristic**: These are OUTPUTS of computation, not new data collection

| Derived State | Computed From | Purpose |
|---|---|---|
| Mastery probability per concept | Attempt results + BKT/PFA | "What does the child know?" |
| Retrieval strength per fact | Response times over sessions | "Is this fluent or derived?" |
| Optimal spacing interval | Forgetting curve per concept | "When should we review?" |
| Scaffold preference | Historical scaffold effectiveness | "Visual or verbal?" |
| Outer fringe (next concepts) | Mastery + prerequisite graph | "What is the child ready for?" |
| Zone of Proximal Development | Mastery + difficulty calibration | "How hard should the next question be?" |

**Rule**: If you can compute it from Tier 1 events, it is Tier 2. Do not store Tier 2 state independently — it must always be derivable from the event log (event sourcing principle).

---

## Tier 3: Aggregated Analytics

**Stored in**: Analytics store (fully anonymised)
**Retention**: Indefinite (cannot be attributed to any individual)
**Lawful basis**: Parental consent (separate opt-out toggle)
**Minimum aggregation**: 1000+ children before any aggregate is computed or released

| Data Element | Aggregation | Purpose |
|---|---|---|
| Common misconceptions per concept | Across 1000+ learners | Improve item bank |
| Average sessions to mastery | Per concept, anonymised | Inform curriculum sequencing |
| Scaffold effectiveness rates | Per intervention type | Improve pedagogy |

---

## PROHIBITED — Never Collected Under Any Circumstances

These data elements are prohibited regardless of parental consent. Consent cannot override data minimisation or the child's best interests.

| Data Element | Why Prohibited |
|---|---|
| Emotional state (inferred or stated) | Not needed for pedagogy; creates false intimacy; unreliable inference |
| Interests / preferences ("I like dinosaurs") | Not needed for curriculum adaptation; creates engagement-optimisation incentive |
| Personal disclosures ("My parents are fighting") | Privacy violation; no educational purpose; must be discarded by prompt classifier |
| Social context ("My best friend is Sarah") | Privacy violation; no educational purpose |
| Home life details ("We're moving house") | Privacy violation; no educational purpose |
| Device fingerprint | No curriculum purpose; enables cross-device tracking |
| IP address | No curriculum purpose; enables location inference |
| Browsing history / cross-app data | No curriculum purpose; prohibited by Children's Code |
| Time-of-day usage patterns **for behavioural profiling** | Using temporal patterns to schedule push notifications or infer "best learning times" is engagement optimisation, not pedagogy. Note: event timestamps and session start/end ARE stored (Tier 1) — they are essential for spacing algorithms. The prohibition is on analysing *when* the child uses the service to drive re-engagement. |
| Engagement-maximising metrics (scroll depth, tap heatmaps, dwell time, session frequency trends) | Enables engagement optimisation, which we explicitly reject. Note: response_time_ms IS stored (Tier 1) because it measures retrieval fluency, a pedagogical signal. The prohibition is on metrics whose purpose is measuring or increasing time-on-platform. |
| Biometric data (face, voice print, fingerprint) | Disproportionate; local pose/shape processing is permitted but biometric templates are not |
| Predictive analytics ("will pass SATs") | Stigmatising; uncertain; parents over-index on predictions |

### Enforcement

1. **Prompt classifier**: Flags and discards personal/emotional content before it reaches the LLM or event store
2. **Event store schema validation**: Rejects any field not in the Tier 1 schema
3. **Code review**: Any PR introducing a new data element must reference this classification
4. **Parent notification**: If the child repeatedly attempts personal sharing, the parent is notified

---

## How to Use This Document

### Adding a new data element

1. Identify which tier it belongs to
2. If Tier 1: confirm it passes the three-question test above
3. If it doesn't fit any tier: it is likely PROHIBITED — check the prohibited list
4. Update this document with the new element
5. Update `CONSENT_RULES.md` if a new consent purpose is needed
6. Update `DPIA.md` if the processing has materially changed

### Adding a new feature

1. List every data element the feature reads, writes, or computes
2. Classify each one against this document
3. Confirm no PROHIBITED data is being collected, even indirectly
4. Include the classification in the feature's user story / design doc
5. Get review from another developer before merging

### LLM Prompt Construction

When building prompts sent to the LLM inference provider:
- **Permitted**: Concept ID, error pattern ID, scaffold type, mastery state, curriculum text from graph
- **Permitted with processor agreement**: Child first name (for personalisation — "Well done, Zara")
- **Never permitted**: Session transcripts containing personal disclosures, cross-session behavioural summaries, any Tier 0 data beyond first name
- Check `CONSENT_RULES.md` for the LLM processor requirements

---

## Related documents

| Document | Relationship |
|---|---|
| [README](../../README.md) | Links here from the [privacy section](../../README.md#privacy-and-compliance) |
| [CONSENT_RULES.md](CONSENT_RULES.md) | [Consent per processing purpose](CONSENT_RULES.md#1-consent-purposes-unbundled) -- what lawful basis permits each tier |
| [CHILD_PROFILE_CONSENT.md](../../docs/design/CHILD_PROFILE_CONSENT.md) | Full legal analysis defining [data tiers](../../docs/design/CHILD_PROFILE_CONSENT.md#2-what-we-need-to-know-about-the-child-data-tiers) and [prohibited data](../../docs/design/CHILD_PROFILE_CONSENT.md#what-is-explicitly-excluded-hard-boundaries) |
| [DPIA.md](DPIA.md) | Data Protection Impact Assessment -- must be updated when processing changes |
| [OUTPUT_SCHEMAS.md](../../docs/design/OUTPUT_SCHEMAS.md) | [Schema B hard constraints](../../docs/design/OUTPUT_SCHEMAS.md#output-contract-1) enforce these classification rules at the session prompt level |
| [PROJECT_DIRECTION.md](../../docs/design/PROJECT_DIRECTION.md) | [Architecture direction](../../docs/design/PROJECT_DIRECTION.md#architecture-direction) -- event-stream architecture that this classification governs |

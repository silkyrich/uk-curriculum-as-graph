# Consent Rules — Developer Reference

**Purpose**: Defines what lawful basis applies to each processing purpose, what consent is required, and the operational rules for obtaining, recording, and withdrawing consent.

**Authority**: Implements UK GDPR Art. 6 (lawful bases), Art. 7 (conditions for consent), Art. 8 (child's consent), Art. 13-14 (transparency), and ICO Children's Code Standards 4, 7, 11, 12, 15. Full analysis: `docs/design/CHILD_PROFILE_CONSENT.md`.

---

## 1. Consent Purposes (Unbundled)

Each purpose has its own consent toggle. They must NEVER be bundled into a single "I agree" checkbox.

### Purpose A: Core Adaptive Learning

| Property | Value |
|---|---|
| **What it covers** | Knowledge tracing, error pattern detection, spacing optimisation, scaffold selection, difficulty calibration |
| **Data tier** | Tier 1 (learning events) → Tier 2 (derived model) |
| **Lawful basis** | Parental consent (Art. 6(1)(a) + Art. 8) |
| **Required for service?** | Yes — without this, the service degrades to static practice mode |
| **Default** | Off (must be actively consented before any learning events are recorded) |
| **Profiling?** | Yes — compelling reason documented in `CHILD_PROFILE_CONSENT.md` Section 3 |
| **Withdrawal effect** | Service enters static mode: random questions within year group, no adaptation, no learner model |
| **Retention on withdrawal** | Existing events retained for 30 days then deleted (unless parent requests immediate deletion) |

### Purpose B: Teacher Sharing

| Property | Value |
|---|---|
| **What it covers** | Sharing mastery progress, error patterns, and session summaries with designated teachers |
| **Data tier** | Tier 1 + Tier 2 (read-only sharing, no new collection) |
| **Lawful basis** | Parental consent (Art. 6(1)(a)) |
| **Required for service?** | No |
| **Default** | Off |
| **Granularity** | Per teacher, per data type (mastery only / mastery + errors / mastery + errors + session transcripts) |
| **Withdrawal effect** | Teacher access revoked immediately; previously exported reports remain with teacher |

### Purpose C: Anonymised Analytics

| Property | Value |
|---|---|
| **What it covers** | Contributing anonymised learning data to population-level curriculum research |
| **Data tier** | Tier 3 (aggregated, 1000+ minimum) |
| **Lawful basis** | Parental consent (Art. 6(1)(a)) |
| **Required for service?** | No |
| **Default** | Off |
| **Withdrawal effect** | Future events excluded from aggregation; previously contributed data cannot be extracted from aggregates (truly anonymised) |

### Purpose D: Camera/Microphone (Per Activity)

| Property | Value |
|---|---|
| **What it covers** | Camera for movement/pose activities (e.g., phonics mouth shape); microphone for voice recording activities |
| **Data tier** | Processed locally (MediaPipe/TF Lite on-device); only derived data (pose coordinates, transcription text) enters Tier 1 |
| **Lawful basis** | Parental consent (Art. 6(1)(a)) — separate per modality per activity type |
| **Required for service?** | No — activities requiring camera/mic have fallback modes |
| **Default** | Off, requested per activity ("This activity uses your camera to check mouth shape. Turn on?") |
| **What is NOT stored** | Raw video, raw audio, facial features, voice biometrics |
| **Withdrawal effect** | Activity runs in fallback mode (no camera/mic); previously captured pose/transcription data deleted |

### Purpose E: Safety Processing (Anomaly Detection)

| Property | Value |
|---|---|
| **What it covers** | Sibling gaming detection, device sharing detection, prompt injection defence, off-curriculum request detection |
| **Data tier** | Tier 1 (anomaly_score field on session events) |
| **Lawful basis** | Legitimate interests (Art. 6(1)(f)) — documented LIA on file |
| **Required for service?** | Yes — cannot be disabled while service is active |
| **Default** | On (legitimate interests, not consent-gated) |
| **Parent visibility** | Full — flagged sessions shown in dashboard with explanation |
| **Why not consent?** | Safety processing must always be active; consent can be withdrawn, but safety cannot be optional |

---

## 2. Consent Lifecycle

### Obtaining Consent

```
Parent creates account
  → Email verified (Tier 0 identity created)
  → Adds child (first name + year group)
  → Presented with consent screen:
      - Plain-English explanation of what is collected and why
      - Separate toggles for each purpose (A-D)
      - "Learn more" links to detailed explanation per purpose
      - Clear statement of what is NEVER collected
  → Each toggle recorded as individual consent event with timestamp
```

### Recording Consent

Every consent event must record:

```json
{
  "consent_id": "UUID",
  "parent_id": "UUID",
  "child_id": "UUID",
  "purpose": "adaptive_learning | teacher_sharing | analytics | camera | microphone",
  "action": "granted | withdrawn",
  "timestamp": "ISO 8601",
  "version": "consent_text_version_hash",
  "method": "parent_dashboard_toggle"
}
```

**Retention**: Consent records retained for **6 years** after withdrawal (legal requirement: proof of valid consent).

### Withdrawing Consent

- Must be **as easy as giving consent** (same toggle, same screen)
- Effect must be **immediate** (within the current session)
- Must be **clearly communicated** to the parent (what will happen to existing data, what service changes)
- Child must be informed in age-appropriate language that the experience will change

### Age 13 Transition

When a child reaches the UK digital age of consent (13):

1. System prompts parent that child can now manage their own consent
2. Child is presented with age-appropriate consent screen
3. Child re-consents (or not) for each purpose independently
4. Parent retains dashboard access but child controls consent toggles
5. Consent records updated to reflect child-held consent

---

## 3. Parental Verification

### At Account Creation

| Step | Method | Strength |
|---|---|---|
| Email verification | Email loop with confirmation link | Low |
| Adult verification | Credit card micro-charge (1p, refunded) | Medium |

This is proportionate to our risk level (moderate — educational profiling, no health data, no financial data, no geolocation).

### When Verification Strengthens

If we add higher-risk processing in future (e.g., cloud-based speech recognition, video analysis), verification must be reassessed. Document the decision in the DPIA.

---

## 4. Third-Party Processor Requirements

Before any child data is sent to a third-party service, we must have:

| Requirement | Detail |
|---|---|
| **Data Processing Agreement** (Art. 28) | Signed agreement specifying processing purposes, data types, security measures, deletion obligations |
| **Sub-processor list** | Published list of all sub-processors with notification of changes |
| **PII audit** | Documented analysis of what PII enters the processor's systems |
| **Retention guarantee** | Processor must not retain data beyond what is needed for the specific request |
| **Training exclusion** | Processor must not use children's data for model training |

### Current Processors (To Be Completed)

| Processor | Data Sent | Agreement Status |
|---|---|---|
| Neo4j Aura (graph DB) | Curriculum data only (no learner data in graph) | TODO |
| LLM inference provider | Concept IDs, error patterns, scaffold types, possibly child first name | TODO — critical: must confirm training exclusion and data retention |
| Cloud hosting | Event store, identity store | TODO |

---

## 5. Parent Rights Implementation

| Right | How Parent Exercises It | Our Response Time |
|---|---|---|
| **Access** (Art. 15) | Dashboard (real-time) + formal export button | Instant (dashboard) / 30 days (formal SAR) |
| **Rectification** (Art. 16) | Flag incorrect data via dashboard | 30 days |
| **Erasure** (Art. 17) | One-click "Delete all data" in settings | 72 hours |
| **Restriction** (Art. 18) | Pause adaptive learning toggle | Immediate |
| **Portability** (Art. 20) | Export as JSON (xAPI format) | 30 days |
| **Object to profiling** (Art. 21) | Withdraw adaptive learning consent | Immediate (service enters static mode) |
| **Automated decision explanation** (Art. 22) | Dashboard shows reasoning for current difficulty, next concept | Instant |

---

## 6. Compliance Checklist for New Features

Before merging any PR that introduces or modifies data processing:

- [ ] Every data element classified in `DATA_CLASSIFICATION.md`
- [ ] Lawful basis confirmed for each processing purpose
- [ ] Consent is unbundled (not combined with other purposes)
- [ ] No PROHIBITED data is collected, even indirectly
- [ ] Tier 0/1 separation enforced (no PII in event log)
- [ ] Retention periods specified and implemented
- [ ] Parent can view, export, and delete the data via dashboard
- [ ] LLM prompts reviewed for PII content
- [ ] DPIA updated if processing has materially changed
- [ ] User story includes privacy boundary section

---

## Related documents

| Document | Relationship |
|---|---|
| [README](../../README.md) | Links here from the [privacy section](../../README.md#privacy-and-compliance) |
| [DATA_CLASSIFICATION.md](DATA_CLASSIFICATION.md) | [Data tier definitions](DATA_CLASSIFICATION.md#tier-0-identity) -- what data exists at each tier that consent governs |
| [CHILD_PROFILE_CONSENT.md](../../docs/design/CHILD_PROFILE_CONSENT.md) | Full legal analysis: [consent architecture](../../docs/design/CHILD_PROFILE_CONSENT.md#implementation-consent-flow), [consent granularity](../../docs/design/CHILD_PROFILE_CONSENT.md#consent-granularity), [verification methods](../../docs/design/CHILD_PROFILE_CONSENT.md#4-consent-verification-how-we-know-its-the-parent) |
| [DPIA.md](DPIA.md) | Data Protection Impact Assessment -- must be updated when consent purposes change |
| [OUTPUT_SCHEMAS.md](../../docs/design/OUTPUT_SCHEMAS.md) | [Schema B](../../docs/design/OUTPUT_SCHEMAS.md#output-contract-1) must respect consent state (camera/mic per-activity, teacher sharing opt-in) |
| [INTERACTION_MODES.md](../../docs/design/INTERACTION_MODES.md) | [Camera/microphone modes](../../docs/design/INTERACTION_MODES.md#mode-7-physical-movement-camera-pose-detection) that require Purpose D consent |
| [SOURCES.md](../../docs/research/SOURCES.md) | [Privacy and compliance sources](../../docs/research/SOURCES.md#8-privacy-compliance-and-consent-added-2026-02-20) -- ICO guidance, GDPR, Children's Code |

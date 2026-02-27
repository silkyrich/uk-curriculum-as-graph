# Child Profile, Consent & Compliance Analysis

**Status**: Working document (2026-02-20)
**Purpose**: Define what child data we can collect, what parents can consent to, and how we meet GDPR and ethical requirements.

---

## The Problem

You cannot personalise learning without knowing the learner. A teacher knows their pupil — their misconceptions, their pace, what scaffolding works, what trips them up. Our platform must build an equivalent model. But the learner is a child, and children's data attracts the highest level of legal and ethical protection in every jurisdiction we care about.

This document works through three questions:
1. **What can parents consent to?** (the legal ceiling)
2. **What should we collect?** (the ethical line)
3. **How do we operationalise both?** (the architecture)

---

## 1. Legal Framework

### 1.1 Which Laws Apply to Us?

We are a **commercial edtech provider** offering a service **directly to parents and children** (not through schools as a processor). This means:

| Regulation | Applies? | Why |
|---|---|---|
| **UK GDPR** | Yes | Processing personal data of UK residents |
| **ICO Children's Code** (Age Appropriate Design Code) | **Yes** | We are an Information Society Service likely to be accessed by under-18s |
| **Data Protection Act 2018 s.9** | Yes | Sets UK age of digital consent at 13 |
| **Online Safety Act 2023** (from July 2025) | Likely | Complementary safety duties for children's services |
| **COPPA** (if US users) | Yes | Under-13s require verifiable parental consent |
| **EU GDPR Art. 8** | If EU users | Age threshold varies by member state (13-16) |

**Critical distinction**: The Children's Code **exempts schools** processing data for educational purposes. It does **not** exempt edtech companies offering services directly to children or parents. We are in scope.

If we were to sell through schools as a pure processor (acting solely on the school's instructions, not determining purposes of processing), the Code would not apply. But that is not our model — we determine the processing purposes (adaptive learning, knowledge tracing, pedagogical decisions). We are a controller.

### 1.2 Lawful Basis: Consent vs Legitimate Interests

For an ISS processing children's data, there are two viable lawful bases:

**Option A: Consent (Art. 6(1)(a) + Art. 8)**
- Parent must consent for under-13s
- Child can consent from age 13 (UK threshold)
- Must be freely given, specific, informed, unambiguous
- Must be withdrawable at any time (and withdrawal must be as easy as giving it)
- Must use "reasonable efforts" to verify parental responsibility

**Option B: Legitimate Interests (Art. 6(1)(f))**
- Available to non-public-authority controllers
- Requires a three-part Legitimate Interests Assessment (LIA):
  1. Purpose test: is there a legitimate interest?
  2. Necessity test: is the processing necessary for that interest?
  3. Balancing test: do the individual's interests override?
- The UK GDPR explicitly states that the balancing test must give particular weight to children's rights
- Must still comply with data minimisation and all Children's Code standards

**Our position**: We should use **consent** as the primary lawful basis for the core adaptive learning processing, combined with **legitimate interests** for specific, narrowly-scoped operations like safety/anomaly detection. Reasons:

1. Parents expect to actively opt in to an AI system learning about their child
2. Consent gives parents a clear, unambiguous control mechanism
3. The ICO has indicated that legitimate interests is "unlikely to provide a valid lawful basis for profiling" in many children's contexts
4. Consent aligns with our transparency-first design philosophy
5. For safety processing (sibling gaming detection, prompt injection defence), legitimate interests is more appropriate because consent can be withdrawn, but safety processing must always be active

### 1.3 What Parents Can Legally Consent To

Under UK GDPR + Children's Code, parental consent can authorise processing that:

- Is **necessary for the service** the child is "actively and knowingly engaged" in
- Uses **minimal data** (only what is needed for the stated purpose)
- Has **high privacy by default** (profiling off unless compelling reason)
- Does **not use nudge techniques** to encourage providing unnecessary data
- Serves the **best interests of the child**
- Is **transparent** (parent and child can understand what is processed and why)

Parental consent **cannot** override:
- The data minimisation principle (parent cannot consent to unnecessary collection)
- The prohibition on detrimental use (Standard 5 of Children's Code)
- The requirement to act in the child's best interests (even if the parent disagrees)
- The child's own rights under GDPR (including the right to erasure)

**Key implication**: Consent is not a blank cheque. Even with parental consent, we can only process data that is genuinely necessary for the educational purpose and is in the child's best interests.

### 1.4 Children's Code: The 15 Standards (Our Obligations)

| # | Standard | Our Compliance Approach |
|---|---|---|
| 1 | **Best interests of the child** | Every design decision documented with child welfare rationale |
| 2 | **Data protection impact assessment** | DPIA required before launch and for significant changes |
| 3 | **Age appropriate application** | Learner profiles layer provides year-group constraints |
| 4 | **Transparency** | Parent dashboard with full data visibility; child-friendly explanations |
| 5 | **Detrimental use of data** | No engagement maximisation, no commercial profiling, no addictive patterns |
| 6 | **Policies and community standards** | Published, child-appropriate terms |
| 7 | **Default settings** | Highest privacy by default; profiling off until parent activates |
| 8 | **Data minimisation** | Minimal schema (see Section 2); no identity in event log |
| 9 | **Data sharing** | No sharing with third parties; parent controls teacher access |
| 10 | **Geolocation** | Not collected (not needed for adaptive learning) |
| 11 | **Parental controls** | Full dashboard; child notified of monitoring |
| 12 | **Profiling** | Off by default; compelling reason argument for adaptive learning (see Section 3) |
| 13 | **Nudge techniques** | No dark patterns; no gamification badges/leaderboards |
| 14 | **Connected toys and devices** | N/A unless AR/camera features enabled (separate consent per modality) |
| 15 | **Online tools** | Easy data deletion, account removal, consent withdrawal |

---

## 2. What We Need to Know About the Child (Data Tiers)

### Tier 0: Identity (Separate Store, Maximum Protection)

This is **account management data**, not learning data. Stored in a separate identity service, never in the learning event log.

| Data | Purpose | Retention | Legal Basis |
|---|---|---|---|
| Parent email | Account, notifications | Until account deletion | Contract |
| Child first name | Personalise UI ("Well done, Zara") | Until account deletion | Consent |
| Year group | Select age-appropriate constraints | Until account deletion | Consent |
| Subjects enabled | Scope the curriculum | Until account deletion | Consent |

**Not collected**: Surname, school, address, date of birth (year group is sufficient), photo, device fingerprint.

### Tier 1: Learning Events (Core Adaptive Engine)

This is what drives the adaptive learning. **Pseudonymous** — the event log uses UUIDs, not names.

| Data | Example | Purpose | Retention |
|---|---|---|---|
| Attempt result | correct/incorrect | Mastery estimation | 12 months rolling |
| Response time | 1200ms | Retrieval strength (fluent vs deriving) | 12 months rolling |
| Error pattern | /e/ confused with /i/ 58% | Misconception detection | Until mastery achieved |
| Hint requested | boolean | Scaffold effectiveness | 12 months rolling |
| Scaffold type used | visual, verbal, manipulative | Personalise intervention style | 12 months rolling |
| Concept ID | Neo4j GUID | Curriculum grounding | 12 months rolling |
| Session timestamps | start/end | Session length monitoring | 30 days |

**Compelling reason for profiling**: This data constitutes "profiling" under the Children's Code (automated processing to evaluate learning behaviour). Our compelling reason argument:

1. **Core to the service**: Adaptive learning cannot function without tracking what the child knows and doesn't know. Without this data, the service degrades to a static worksheet.
2. **Best interests**: Personalised instruction demonstrably outperforms one-size-fits-all (effect sizes 0.3-0.5 SD in meta-analyses). Not profiling would deliver a worse educational outcome.
3. **No harmful effects**: The profiling is used exclusively for curriculum-aligned pedagogical decisions. It cannot recommend harmful content because all content is grounded in the National Curriculum graph.
4. **Protective measures**: Parent can view all profile data, delete at any time, withdraw consent. Child is never shown their "profile" in a way that could label or stigmatise.

### Tier 2: Derived Learner Model (Computed, Not Stored Directly)

Derived from Tier 1 events. These are **projections**, not additional data collection.

| Derived State | Computed From | Purpose |
|---|---|---|
| Mastery probability per concept | Attempt results + BKT/PFA model | "What does the child know?" |
| Retrieval strength per fact | Response times over sessions | "Is this fluent or still being derived?" |
| Optimal spacing interval | Forgetting curve per concept | "When should we review this?" |
| Scaffold preference | Historical scaffold effectiveness | "Visual or verbal for this child?" |
| Outer fringe (next concepts) | Mastery + prerequisite graph | "What is the child ready to learn?" |
| Zone of Proximal Development | Mastery + difficulty calibration | "How hard should the next question be?" |

### Tier 3: Aggregated Analytics (Anonymised, Opt-Out)

Population-level insights for curriculum research. **Never individual-level**.

| Data | Aggregation | Purpose | Opt-Out? |
|---|---|---|---|
| Common misconceptions per concept | Across 1000+ children minimum | Improve item bank | Yes |
| Average sessions to mastery | Per concept, anonymised | Inform curriculum sequencing | Yes |
| Scaffold effectiveness rates | Per intervention type | Improve pedagogy | Yes |

### What Is Explicitly Excluded (Hard Boundaries)

| Data | Why Excluded |
|---|---|
| Emotional state inference | Not needed for curriculum adaptation; risk of parasocial relationship |
| Interest/preference profiling | "I like dinosaurs" is irrelevant to phonics mastery |
| Personal disclosures | Family situation, friendships — flagged and discarded by prompt classifier |
| Engagement/attention metrics | No eye tracking, no scroll behaviour, no time-on-page beyond session bounds |
| Cross-platform data | No importing from social media, other apps, browsing history |
| Biometric data | No face recognition, no fingerprint, no voice biometrics (even if camera/mic used for pedagogy, only anonymised pose/shape data processed locally) |
| Device fingerprinting | No purpose for curriculum adaptation |

---

## 3. The Profiling Problem (Our Hardest Compliance Question)

### The Tension

The Children's Code says: **profiling off by default**.
Our service **requires** profiling to function — adaptive learning is, by definition, profiling.

### The Resolution

The ICO explicitly allows profiling when there is a "compelling reason" and appropriate safeguards. The test:

**1. Is profiling core to the service?**
Yes. Without knowledge tracing, the service is a static question bank. The parent is signing up specifically for adaptive, personalised learning. Profiling is the service, not an add-on.

**2. Can you provide a core service without profiling?**
A residual service (practice questions without adaptation) could exist, but it would not deliver the educational benefit the parent is paying for. We should offer this as a fallback for parents who withdraw profiling consent, but it is not the core proposition.

**3. Is profiling in the child's best interests?**
Yes. Evidence from learning science (spaced retrieval practice, knowledge tracing, productive failure) shows personalised sequencing significantly outperforms fixed sequences. Not profiling would harm the child's educational outcomes relative to what is achievable.

**4. Are there safeguards against harmful effects?**
- All content is curriculum-grounded (no recommendation of harmful content)
- No engagement maximisation (session lengths are bounded by age-appropriate limits)
- No commercial use of profiles (no advertising, no data sales)
- Full parent transparency and deletion rights
- No labelling or stigmatising of the child based on their profile
- Profile data never shared without explicit parent consent per recipient

### Implementation: Consent Flow

```
SIGN-UP FLOW:

1. Parent creates account (email verification)
2. Parent adds child (first name + year group only)
3. Parent sees clear explanation:
   "To personalise [child's] learning, we track:
    - Which questions they get right and wrong
    - How quickly they answer (to tell fluency from guessing)
    - Which types of help work best for them

    We use this to:
    - Choose the right difficulty level
    - Review topics at the right time
    - Pick the teaching approach that works best

    We NEVER track:
    - Personal conversations or feelings
    - Interests or preferences outside learning
    - What they do on other apps or websites"

4. Parent gives SPECIFIC consent for:
   [ ] Core adaptive learning (required for service)
   [ ] Share progress with teacher (optional, per teacher)
   [ ] Anonymised research analytics (optional)
   [ ] Camera/microphone for specific activities (optional, per activity type)

5. Child sees age-appropriate version:
   "This app remembers what you're learning so it can
    help you practice the right things. Your [parent]
    can see how you're doing."
```

### Consent Granularity

Consent must be **specific** and **unbundled** (GDPR Art. 7; Children's Code Standard 12). We need separate consent toggles for:

| Consent Purpose | Required? | Default | Can Withdraw? |
|---|---|---|---|
| Core adaptive learning | Yes (for full service) | Off until consented | Yes (degrades to static mode) |
| Teacher sharing | No | Off | Yes |
| Anonymised analytics | No | Off | Yes |
| Camera (movement activities) | No | Off, per activity | Yes |
| Microphone (voice activities) | No | Off, per activity | Yes |
| Session transcripts in teacher reports | No | Off | Yes |

---

## 4. Consent Verification (How We Know It's the Parent)

UK GDPR Art. 8(2) requires "reasonable efforts" to verify that the person consenting holds parental responsibility. What counts as "reasonable" depends on the risk level.

### Our Risk Level

We process educational interaction data (not health data, not financial data, not location data). The profiling is for curriculum adaptation only. Risk level: **moderate** (profiling children, but in a controlled educational context with no harmful content exposure).

### Verification Methods (Proportionate to Risk)

| Method | Strength | Appropriate For |
|---|---|---|
| **Email loop** (parent email verification) | Low | Account creation |
| **Credit card micro-charge** (e.g., 1p refunded) | Medium | Confirming adult identity |
| **ID document upload** | High | Not proportionate for our risk level |
| **Knowledge-based verification** | Medium | Recovery/dispute scenarios |

**Our approach**: Email loop for account creation + credit card micro-charge for consent activation. This is proportionate to our risk level and aligns with ICO guidance that "in low-risk cases, verification of parental responsibility via email may be sufficient."

If we later add higher-risk processing (e.g., camera-based activities), we may need to strengthen verification for those specific consent toggles.

---

## 5. Data Subject Rights (Child and Parent)

### Parent Rights (as holder of parental responsibility for under-13)

| Right | Implementation |
|---|---|
| **Access** (Art. 15) | Dashboard shows all stored data in human-readable form |
| **Rectification** (Art. 16) | Parent can flag incorrect data; we correct within 30 days |
| **Erasure** (Art. 17) | One-click deletion of all child data; completed within 72 hours |
| **Restriction** (Art. 18) | Parent can pause processing (enters static mode) |
| **Portability** (Art. 20) | Export all data as structured JSON (xAPI format) |
| **Object to profiling** (Art. 21) | Withdraw adaptive learning consent; service degrades gracefully |
| **Not be subject to automated decisions** (Art. 22) | All pedagogical decisions are explainable via curriculum graph; parent can see reasoning |

### Child Rights (Developing Autonomy)

The Children's Code and UNCRC recognise that children have their own rights, which may sometimes differ from their parents' wishes. As children mature:

| Age | Rights Posture |
|---|---|
| **Under 10** | Parent exercises all rights on child's behalf |
| **10-12** | Parent exercises rights; child should be informed in age-appropriate language |
| **13+** | Child can exercise own rights (UK digital age of consent); parent retains oversight |

We should design the system so that at age 13, the child can independently:
- View their own data
- Request deletion
- Manage sharing settings
- Withdraw consent for optional processing

---

## 6. DPIA Requirements

The ICO requires a Data Protection Impact Assessment before launching any service likely to be accessed by children. Our DPIA must cover:

### Required DPIA Elements

1. **Systematic description of processing** — What data, what purposes, what flows
2. **Necessity and proportionality** — Why we need each data element; why less intrusive alternatives won't work
3. **Risk assessment** — Risks to children's rights and freedoms, including material, physical, psychological, and social harm
4. **Mitigation measures** — Technical and organisational measures to address each risk
5. **Children's Code compliance** — How we meet each of the 15 standards
6. **Consultation** — DPO review, user testing with parents and children, input from children's rights experts

### Key Risks to Assess

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Data breach exposing learning profiles | Low | High | Pseudonymised event log; identity separated; encryption at rest |
| Profiling creates stigmatising labels | Medium | High | No labels shown to child; profile expressed only as pedagogical actions |
| AI makes incorrect pedagogical decision | Medium | Medium | Curriculum graph grounds all decisions; human override via teacher sharing |
| Parent uses data to pressure child | Low | High | No competitive framing in parent dashboard; guidance on healthy engagement |
| Child feels surveilled | Medium | Medium | Age-appropriate transparency; warm, non-evaluative UI tone |
| Scope creep (data used for unintended purposes) | Low | High | Purpose limitation enforced in architecture; no third-party data access |
| Consent fatigue (parent clicks through without reading) | Medium | Medium | Layered consent; short plain-English summaries; specific per-purpose toggles |

---

## 7. Ethical Framework (Beyond Legal Compliance)

Legal compliance is the floor, not the ceiling. Our ethical obligations go further:

### 7.1 The Teacher Analogy (and Its Limits)

A teacher knows their pupil. But a teacher also:
- Forgets (data doesn't)
- Has limited bandwidth (can't optimise for each child simultaneously)
- Is bound by professional ethics and oversight
- Doesn't follow the child home

Our system has perfect memory and infinite attention. This creates **power asymmetries** that don't exist in a classroom:

| Teacher | Our System | Ethical Implication |
|---|---|---|
| Forgets minor incidents | Stores every error | Must implement meaningful data expiry |
| Sees ~30 children | Sees ~N children simultaneously | Must not enable competitive comparison |
| Professional oversight | Algorithmic decisions | Must be auditable and explainable |
| Bounded context (school hours) | Potentially unbounded | Must enforce session limits |
| Intuitive judgement | Statistical inference | Must acknowledge uncertainty; never present probability as certainty |

### 7.2 Principles Beyond Compliance

1. **No permanent record**: Learning struggles at age 7 must not follow a child to age 17. Data retention must be bounded and purposeful.

2. **No competitive framing**: The parent dashboard shows mastery progress against the curriculum, never against other children.

3. **No engagement maximisation**: We optimise for learning outcomes, not time-on-platform. Sessions have firm age-appropriate limits. There are no streaks, no badges, no "come back tomorrow" nudges.

4. **No emotional dependency**: The AI teaches, it doesn't befriend. Prompt classifiers discard personal disclosures. The system redirects emotional overtures gently.

5. **Productive failure is not punishment**: When the system presents deliberately challenging problems (productive failure pedagogy), the child must never feel they are failing. Framing, tone, and scaffolding must make struggle feel safe.

6. **Right to a fresh start**: If a parent deletes data, the child's experience should restart cleanly. No shadow profiles, no inferred state from metadata.

7. **Explainability to the parent**: Every pedagogical decision should be traceable. "Why is my child being asked this?" must always have a curriculum-grounded answer, visible in the parent dashboard.

### 7.3 What We Refuse to Build (Even If Legal)

| Capability | Legal? | We Build It? | Why Not |
|---|---|---|---|
| Emotional state detection from response patterns | Possibly | **No** | Unreliable; creates false intimacy; not needed for curriculum adaptation |
| Interest profiling for content theming | Yes with consent | **No** | Unnecessary for learning; creates engagement optimisation incentive |
| Predictive analytics ("will pass KS2 SATs") | Yes with consent | **No** | Stigmatising; uncertain; parents will over-index on predictions |
| Sharing anonymised profiles with researchers | Yes with consent | **Not yet** | Only when we have robust anonymisation and 1000+ user base |
| Cross-device tracking | Yes with consent | **No** | Not needed; no educational purpose |
| AI companion/friend persona | Yes with consent | **No** | Creates parasocial relationship; not in child's best interests |

---

## 8. Practical Architecture for Compliance

### 8.1 Data Separation

```
[Identity Service]          [Learning Event Store]         [Curriculum Graph]
  - Parent email              - learner_id (UUID)            - Neo4j (static)
  - Child first name          - concept_id                   - Concept nodes
  - Year group                - attempt result               - Prerequisite chains
  - Consent records           - response_time_ms             - Domain structure
  - Sharing permissions       - scaffold_type                - Learner profiles
                              - timestamp                       (age constraints)
         |                           |                              |
         |     [Identity boundary]   |                              |
         +----------+                |                              |
                    |                |                              |
              [Session Service]------+------------------------------+
              - Joins identity + events + curriculum
              - Generates pedagogical decisions
              - Enforces session limits
              - Runs prompt classifier
              - Writes to event store (pseudonymised)
```

The identity service and the learning event store are **architecturally separated**. The event store never contains names, emails, or any directly identifying information. The join happens in the session service at runtime and is never persisted in joined form.

### 8.2 Consent State Machine

```
ACCOUNT_CREATED (no child data processed yet)
    │
    ├─ Parent adds child → CHILD_REGISTERED (name + year group only)
    │
    ├─ Parent consents to adaptive learning → LEARNING_ACTIVE
    │   ├─ Parent withdraws → LEARNING_PAUSED (static mode)
    │   ├─ Parent deletes → DATA_DELETED (72hr completion)
    │   └─ Child turns 13 → CHILD_CONSENT_TRANSITION
    │       ├─ Child re-consents → LEARNING_ACTIVE (child-held consent)
    │       └─ Child does not consent → LEARNING_PAUSED
    │
    ├─ Parent consents to teacher sharing → SHARING_ACTIVE
    │   └─ Per-teacher, per-data-type granularity
    │
    └─ Parent consents to anonymised analytics → ANALYTICS_ACTIVE
        └─ Can withdraw without affecting learning
```

### 8.3 Retention Schedule

| Data Category | Retention | Deletion Trigger | Method |
|---|---|---|---|
| Learning events | 12 months rolling | Auto-expire | Hard delete from event store |
| Session transcripts | 30 days | Auto-expire | Hard delete |
| Derived learner model | Recomputed; no independent retention | Parent deletes events | Model becomes empty |
| Account/identity | Until account deletion | Parent request | Hard delete within 72 hours |
| Consent records | 6 years after consent withdrawn | Legal requirement (proof of consent) | Hard delete after 6 years |
| Anonymised aggregates | Indefinite | Cannot be attributed to individual | N/A (truly anonymised) |

---

## 9. Gap Analysis: Where We Are vs Where We Need to Be

### Already Designed (In This Codebase)

- [x] Minimal learner event schema (RESEARCH_BRIEFING.md Section 6)
- [x] Age-appropriate constraints per year group (learner-profiles layer)
- [x] Privacy enforcement layers (prompt classifier, data minimisation, parent control)
- [x] No-gamification policy (FeedbackProfile nodes, all gamification flags false)
- [x] Session data boundaries (what we store vs what we don't)
- [x] Anomaly detection (sibling gaming, prompt injection)
- [x] Parent dashboard specification (CHILD_EXPERIENCE.md)
- [x] Event-sourced architecture for auditability

### Still Needed

- [ ] **Formal DPIA document** — Following ICO Annex D template
- [ ] **Consent flow UX design** — Wireframes for parent sign-up, consent toggles, child notification
- [ ] **Consent state machine implementation** — Backend service managing consent lifecycle
- [ ] **Age-gate / parental verification** — Email loop + micro-charge implementation
- [ ] **Data retention automation** — 30-day and 12-month auto-deletion jobs
- [ ] **Identity/event store separation** — Infrastructure design for the two-store architecture
- [ ] **Consent withdrawal handler** — Graceful degradation to static mode
- [ ] **Age 13 transition flow** — Re-consent mechanism when child reaches digital age of consent
- [ ] **Privacy notice** — Child-friendly and parent versions
- [ ] **Records of Processing Activities (ROPA)** — Art. 30 requirement
- [ ] **DPO appointment or decision** — Document whether we need a DPO (likely yes, given systematic monitoring of children)
- [ ] **Third-party processor agreements** — For any cloud infrastructure (Neo4j Aura, LLM provider)
- [ ] **LLM provider DPIA** — Specific assessment of data sent to LLM inference (must not include PII)

---

## 10. Open Questions

1. **LLM inference and children's data**: When the LLM generates a hint or explanation, what data is sent in the prompt? The concept ID and error pattern are learning data. If we include the child's name for personalisation ("Well done, Zara"), we are sending PII to a third-party processor. Do we anonymise at the LLM boundary, or do we rely on processor agreements?

2. **Camera/microphone processing**: The INTERACTION_MODES.md specifies local-only processing (MediaPipe, TensorFlow Lite). If this changes (e.g., cloud-based speech recognition), the risk profile changes dramatically and requires fresh consent and DPIA.

3. **School channel**: If we later sell through schools (B2B), the lawful basis and consent model change entirely. Schools can rely on public task (Art. 6(1)(e)) and we might act as a processor. This is a different compliance architecture.

4. **International users**: COPPA (US) has different consent verification requirements ("verifiable parental consent" is a higher bar). EU member states set digital consent ages between 13-16. Each jurisdiction needs specific consideration.

5. **Data portability format**: xAPI is the interoperability standard. Should we commit to xAPI-formatted exports for Art. 20 portability requests? This would also support Learning Record Store integration.

6. **Anonymisation threshold**: We've said "1000+ children minimum" for anonymised aggregates. Is this sufficient? The ICO doesn't specify a number, but k-anonymity with k=1000 on a small concept graph may still allow re-identification. Needs formal analysis.

---

## References

### Legal

- [ICO Age Appropriate Design Code (Children's Code)](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-a-code-of-practice-for-online-services/)
- [ICO: The Children's Code and Education Technologies](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/the-children-s-code-and-education-technologies-edtech/)
- [ICO: Profiling for Automated Decision-Making (Best Interests Framework)](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/how-to-use-our-guidance-for-standard-one-best-interests-of-the-child/best-interests-framework/profiling-for-automated-decision-making/)
- [ICO: Profiling for Content Delivery and Personalisation](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/how-to-use-our-guidance-for-standard-one-best-interests-of-the-child/best-interests-framework/profiling-for-content-delivery/)
- [ICO: DPIA Requirements (Standard 2)](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-a-code-of-practice-for-online-services/2-data-protection-impact-assessments/)
- [ICO: DPIA Template (Annex D)](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-a-code-of-practice-for-online-services/annex-d-dpia-template/)
- [ICO: Lawful Basis for Children's Data](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/children-and-the-uk-gdpr/what-do-we-need-to-consider-when-choosing-a-basis-for-processing-children-s-personal-data/)
- [ICO: Profiling Standard (Standard 12)](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-a-code-of-practice-for-online-services/12-profiling/)
- [ICO: Children's Code Strategy Progress (March 2025)](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/protecting-childrens-privacy-online-our-childrens-code-strategy/children-s-code-strategy-progress-update-march-2025/)
- [Art. 8 UK GDPR: Conditions applicable to child's consent](https://gdpr-info.eu/art-8-gdpr/)
- [Sprintlaw: At What Age Can Children Consent?](https://sprintlaw.co.uk/articles/at-what-age-can-children-legally-consent-to-their-data-being-processed-a-guide-for-uk-businesses/)
- [EdTech and the ICO Children's Code (Bates Wells)](https://bateswells.co.uk/updates/edtech-and-the-application-of-the-ico-childrens-code/)
- [Stevens & Bolton: Children's Code and Education Technologies](https://www.stevens-bolton.com/insights/102ktzs/ico-the-childrens-code-and-education-technologies/)
- [Defend Digital Me: Code of Practice on Children's Data and Education](https://defenddigitalme.org/2025/03/03/a-code-of-practice-on-childrens-data-and-education-whats-next/)

### Internal

- `docs/design/RESEARCH_BRIEFING.md` Section 6: Learner Domain Architecture
- `docs/user-stories/README.md`: Privacy architecture and data boundaries
- `docs/user-stories/child-experience/CHILD_EXPERIENCE.md`: Parent dashboard and consent flows
- `layers/learner-profiles/README.md`: Age-appropriate design constraints

### Upcoming Legislation

- **Data (Use and Access) Act** (law from 19 June 2025) — ICO guidance under review
- **Online Safety Act 2023** — Protection of Children Codes (from July 2025)
- **Proposed education-specific code of practice** — Would address profiling and AI in education specifically

---

## Related documents

| Document | Relationship |
|---|---|
| [README](../../README.md) | Links here from the [privacy section](../../README.md#privacy-and-compliance) for legal framework, profiling problem, and ethical constraints |
| [DATA_CLASSIFICATION.md](../../core/compliance/DATA_CLASSIFICATION.md) | Implements [Tier 0-3 data classification](../../core/compliance/DATA_CLASSIFICATION.md#tier-0-identity) and [prohibited data rules](../../core/compliance/DATA_CLASSIFICATION.md#prohibited-never-collected-under-any-circumstances) defined in this analysis |
| [CONSENT_RULES.md](../../core/compliance/CONSENT_RULES.md) | Implements [unbundled consent purposes](../../core/compliance/CONSENT_RULES.md#1-consent-purposes-unbundled) and [consent lifecycle](../../core/compliance/CONSENT_RULES.md#2-consent-lifecycle) from this analysis |
| [DPIA.md](../../core/compliance/DPIA.md) | DPIA skeleton based on the [requirements defined here](#6-dpia-requirements) |
| [PROJECT_DIRECTION.md](PROJECT_DIRECTION.md) | [What's built vs planned](PROJECT_DIRECTION.md#whats-built-vs-whats-planned) -- compliance framework status |
| [OUTPUT_SCHEMAS.md](OUTPUT_SCHEMAS.md) | [Schema B hard constraints](OUTPUT_SCHEMAS.md#output-contract-1) implement the gamification ban, vocabulary limits, and feedback rules from this analysis |
| [RESEARCH_BRIEFING.md](RESEARCH_BRIEFING.md) | [Motivation science](RESEARCH_BRIEFING.md#4-motivation-and-engagement-what-the-evidence-actually-says) evidence base for the [ethical framework](#7-ethical-framework-beyond-legal-compliance) |
| [SOURCES.md](../research/SOURCES.md) | [Privacy and compliance sources](../research/SOURCES.md#8-privacy-compliance-and-consent-added-2026-02-20) -- ICO guidance, GDPR Article 8, profiling standards |
| [Learner profiles layer](../../layers/learner-profiles/README.md) | Implements [age-appropriate constraints](../../layers/learner-profiles/README.md#why-this-exists) grounded in this analysis |
| [Privacy research](../research/privacy-compliance/) | Source audit trail for all regulatory research |

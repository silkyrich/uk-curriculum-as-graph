# Privacy & Compliance Research Index
**Created:** 2026-02-20
**Purpose:** Audit trail for legal and regulatory research informing the child profile consent architecture.

## Summary

Research into the legal framework governing children's data in a commercial adaptive learning platform. Focus: UK GDPR, ICO Children's Code (Age Appropriate Design Code), and edtech-specific guidance.

| # | Source | Year | Type | Access | Relevance | Key contribution |
|---|---|---|---|---|---|---|
| 1 | ICO Children's Code (AADC) | 2021 | regulatory code | web search summaries | Critical | 15 standards framework; profiling-off-by-default; compelling reason test |
| 2 | ICO EdTech Guidance | 2023 | regulatory guidance | web search summary (403 on direct fetch) | Critical | Determines whether we are in scope; controller vs processor distinction |
| 3 | UK GDPR Art. 8 / DPA 2018 s.9 | 2018 | legislation | multiple secondary sources | Critical | Age 13 digital consent threshold; parental consent verification requirements |
| 4 | ICO Best Interests Framework: Profiling for ADM | 2023 | regulatory guidance | web search summary (403 on direct fetch) | High | Automated decision-making profiling rules; GDPR Recital 71 |
| 5 | ICO Best Interests Framework: Profiling for Content Delivery | 2023 | regulatory guidance | web search summary (403 on direct fetch) | High | Content personalisation profiling rules; compelling reason examples |
| 6 | ICO DPIA Requirements (Standard 2) | 2021 | regulatory guidance | web search summary | High | DPIA mandatory for children's services; Annex D template |
| 7 | ICO Lawful Basis for Children's Data | 2023 | regulatory guidance | web search summary | High | Consent vs legitimate interests analysis for children |
| 8 | ICO Profiling Standard (Standard 12) | 2021 | regulatory code | web search summary | High | Profiling off by default; exceptions for core service, accessibility, safeguarding |
| 9 | ICO Children's Code Strategy Progress (Mar 2025) | 2025 | regulatory update | web search summary | Medium | Recommender systems review; upcoming education code |
| 10 | ICO Children's Code Strategy Progress (Dec 2025) | 2025 | regulatory update | web search summary | Medium | Latest enforcement activity and guidance updates |
| 11 | Data (Use and Access) Act | 2025 | legislation | web search reference | Medium | All ICO guidance under review from June 2025 |
| 12 | Online Safety Act 2023 | 2023 | legislation | web search reference | Medium | Complementary Protection of Children Codes from July 2025 |
| 13 | Bates Wells: EdTech and the ICO Children's Code | 2023 | legal analysis | web search summary | Medium | Practical analysis of when edtech is in scope |
| 14 | Stevens & Bolton: Children's Code and EdTech | 2023 | legal analysis | web search summary | Medium | Controller/processor distinction worked examples |
| 15 | 5Rights Foundation: AADC Impact Assessment | 2024 | policy analysis | web search reference | Low | Broader impact of AADC on children's online services |

## Key findings

### 1. We are in scope of the Children's Code

As a commercial edtech provider offering a direct-to-parent/child service, we are an Information Society Service likely to be accessed by under-18s. We determine the purposes and means of processing (adaptive learning algorithm, knowledge tracing model). We are a **controller**, not a processor.

The Code would NOT apply only if all three conditions were met: (a) not accessed on a direct-to-consumer basis, (b) we only process to fulfil a school's public tasks, (c) we act solely on the school's instructions. None of these apply to our model.

### 2. Profiling requires a "compelling reason"

Standard 12 requires profiling off by default. The compelling reason test permits exceptions for:
- Core service functionality (adaptive learning cannot function without knowledge tracing)
- Accessibility (e.g., identifying need for TTS or subtitles)
- Safeguarding (e.g., anomaly detection for device sharing)
- Age assurance

Our argument: adaptive learning profiling is core to the service and in the child's best interests. This is documented in detail in `docs/design/CHILD_PROFILE_CONSENT.md` Section 3.

### 3. Consent is the appropriate lawful basis

For our direct-to-consumer model with under-13 users, parental consent (Art. 6(1)(a) + Art. 8) is the primary lawful basis. Legitimate interests (Art. 6(1)(f)) may supplement for safety processing only.

### 4. Upcoming legislative changes may affect us

- Data (Use and Access) Act (June 2025): ICO guidance under review
- Online Safety Act Protection of Children Codes (July 2025): complementary duties
- Proposed education-specific code of practice: would directly address AI profiling in education

### Access limitations

The ICO website returned 403 errors on direct page fetches during this research session. All ICO guidance summaries are derived from web search result snippets and secondary legal analysis sources, not from reading the full ICO pages. This should be noted when citing specific ICO positions — the summaries may miss nuance available in the full guidance text. A manual review of the full ICO pages is recommended.

## Files in this directory

- `ico_childrens_code_overview.md` — Summary of the 15 standards and their application
- `ico_edtech_guidance.md` — When the Code applies to education technology providers
- `uk_gdpr_art8_parental_consent.md` — Age thresholds, consent verification, lawful bases
- `ico_profiling_standards.md` — Standards 5 and 12: detrimental use and profiling rules
- `ico_dpia_requirements.md` — DPIA obligations for children's services
- `upcoming_legislation.md` — Data (Use and Access) Act, Online Safety Act, education code

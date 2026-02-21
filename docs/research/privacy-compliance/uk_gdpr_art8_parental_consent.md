# UK GDPR Article 8: Parental Consent for Children's Data
**Sources:**
- https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/children-and-the-uk-gdpr/what-are-the-rules-about-an-iss-and-consent/
- https://gdpr-info.eu/art-8-gdpr/
- https://ukgdpr.fieldfisher.com/chapter-2/article-8-gdpr/
- https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/children-and-the-uk-gdpr/what-do-we-need-to-consider-when-choosing-a-basis-for-processing-children-s-personal-data/
- https://sprintlaw.co.uk/articles/at-what-age-can-children-legally-consent-to-their-data-being-processed-a-guide-for-uk-businesses/
**Fetched:** 2026-02-20
**Type:** legislation + regulatory guidance
**Access:** web search summaries from multiple secondary sources

## What it is

Article 8 of the UK GDPR sets conditions for children's consent when an Information Society Service (ISS) relies on consent as the lawful basis for processing. The Data Protection Act 2018 s.9 sets the UK age threshold at 13.

## Key rules

### Age threshold

- **Under 13**: Only a parent or legal guardian can provide consent for personal data processing
- **13 and over**: Children can legally consent themselves, provided they understand what they are agreeing to
- This is specific to the UK. EU member states set thresholds between 13-16

### When Article 8 applies

Article 8 applies when:
1. You are offering an ISS directly to a child, AND
2. You are relying on **consent** as the lawful basis for processing

It does NOT require consent in all cases. If another lawful basis applies (legitimate interests, public task, contract), Article 8's specific parental consent rules do not trigger. However, the general principle that children deserve enhanced protection still applies regardless of lawful basis.

### Parental consent verification

Art. 8(2) requires "reasonable efforts" to verify that the person consenting holds parental responsibility. What is "reasonable" depends on:
- **Risk level**: Higher-risk processing requires stronger verification
- **Available technology**: Must use suitable age verification mechanisms available in the marketplace
- The ICO prefers "attribute" systems offering yes/no responses (e.g., "is this person over 13?" or "does this person hold parental responsibility?")

Examples of verification methods (escalating strength):
- Email loop (low risk)
- Credit card micro-charge (medium risk)
- ID document upload (high risk)
- Knowledge-based verification (medium risk, for disputes)

### Alternative lawful bases

Consent is not always the most appropriate basis for children's data:

- **Schools**: Can rely on Art. 6(1)(e) — public task. Article 8 parental consent rules do not apply.
- **EdTech direct-to-consumer**: Consent is typically appropriate.
- **Legitimate interests** (Art. 6(1)(f)): Available but must give "particular" weight to children's rights in the balancing test. ICO says this is "unlikely to provide a valid lawful basis for profiling" in many children's contexts.
- **Counselling/preventive services**: DPA 2018 s.9 exempts these from Art. 8 requirements.

### Consent requirements (when consent is used)

Standard UK GDPR consent requirements apply with enhanced obligations:
- Freely given (not bundled with other consents)
- Specific (separate consent per purpose)
- Informed (child-friendly language)
- Unambiguous (clear affirmative action)
- Withdrawable (as easy to withdraw as to give)
- Using consent does not remove the obligation to assess processing risks independently

## Application to our platform

We should use consent as the primary lawful basis because:
1. We are a direct-to-consumer ISS
2. Parents expect to opt in to AI-powered adaptive learning
3. Consent gives parents clear control
4. Our user base is primarily under-13 (KS1-KS2)

Verification approach: email loop for account creation + credit card micro-charge for consent activation (proportionate to our moderate risk level).

## Relevance to platform

This establishes the legal mechanism by which parents authorise our processing. The consent flow design in `docs/design/CHILD_PROFILE_CONSENT.md` Section 3 implements these requirements.

## Caveats

No full text of ICO guidance pages was fetched (403 on direct ICO URLs). Analysis synthesised from multiple secondary legal sources and web search summaries. The core legislation (Art. 8 text) is available from gdpr-info.eu. Manual review of full ICO guidance recommended.

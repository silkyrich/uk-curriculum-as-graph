# CASE Standards — Research Notes

Research notes on the five academic standards frameworks included in the
UK Curriculum as Graph CASE layer (v3.5).

## Files

| File | Framework | Key Research Question |
|---|---|---|
| [ngss.md](ngss.md) | Next Generation Science Standards | How does the US inquiry cycle compare to UK Working Scientifically? |
| [common_core_math.md](common_core_math.md) | Common Core State Standards — Mathematics | How do mathematical practices compare to UK mathematical reasoning skills? |
| [common_core_ela.md](common_core_ela.md) | Common Core State Standards — ELA | How do anchor standards map to UK English reading/writing objectives? |
| [texas_teks_science.md](texas_teks_science.md) | Texas TEKS Science | What happens when a state rejects NGSS but still covers evolution? |
| [wyoming_science.md](wyoming_science.md) | Wyoming Science Standards | Case study: political removal and reinstatement of climate change content |

## Key Themes

### Decentralised vs centralised curriculum control

The US has no federal curriculum mandate. Each of the ~50 states sets its own academic
standards. This contrasts starkly with England's DfE-mandated National Curriculum.
CASE (IMS Global) provides the common exchange format that makes US standards
machine-readable and comparable.

### The politics of science standards

The evolution and climate change controversies in US science standards illustrate how
curriculum content is a site of political contestation. Wyoming's 2016 removal of
climate change language and its 2020 reinstatement, or South Carolina's ongoing
resistance to NGSS, have no direct analogue in the UK system — but similar debates
about RSE, religion, and British values show the same underlying dynamic.

### The 3D learning model (NGSS) vs subject-domain model (UK)

NGSS organises science around three dimensions:
1. Science and Engineering Practices (SEPs) — what scientists *do*
2. Crosscutting Concepts (CCCs) — ideas that span all science
3. Disciplinary Core Ideas (DCIs) — the content knowledge

The UK National Curriculum organises science around:
1. Working Scientifically — procedural skills
2. Subject content domains — Biology, Chemistry, Physics

The graph alignment (`ALIGNS_TO` relationships) makes these structural differences
explicit and queryable.

### Grade bands vs key stages

NGSS uses grade bands: K–2, 3–5, 6–8, 9–12.
The UK uses key stages: KS1 (Y1–2), KS2 (Y3–6), KS3 (Y7–9), KS4 (Y10–11).

Approximate mapping:
| US Grade Band | UK Key Stage |
|---|---|
| K–2 | KS1 |
| 3–5 | Lower KS2 |
| 6–8 | KS3 |
| 9–12 | KS4 + post-16 |

## CASE API Notes

All frameworks are fetched from `https://casenetwork.imsglobal.org/ims/case/v1p0`
(IMS CASE Network) unless a framework-specific endpoint is configured in
`data/extractions/case/case_sources.json`.

Texas TEA publishes TEKS at their own CASE endpoint; Wyoming may be available via
the CASE Network or the Wyoming DOE directly.

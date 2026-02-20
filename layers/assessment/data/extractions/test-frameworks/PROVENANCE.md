# KS2 Test Framework Extractions — Provenance

## Source Documents

| Framework | Publication URL | PDF URL | STA Reference | Downloaded |
|---|---|---|---|---|
| KS2 Mathematics | https://www.gov.uk/government/publications/key-stage-2-mathematics-test-framework | https://assets.publishing.service.gov.uk/media/5a822bbded915d74e62362a2/2016_KS2_Mathematics_framework_PDFA_V5.pdf | STA/15/7342/e (ISBN 978-1-78315-827-0) | 2026-02-17 |
| KS2 English Reading | https://www.gov.uk/government/publications/key-stage-2-english-reading-test-framework | https://assets.publishing.service.gov.uk/media/5a82454eed915d74e3402a2a/2016_KS2_Englishreading_framework_PDFA_V3.pdf | STA/15/7341/e (ISBN 978-1-78315-826-3) | 2026-02-17 |
| KS2 English GPS | https://www.gov.uk/government/publications/key-stage-2-english-grammar-punctuation-and-spelling-test-framework | https://assets.publishing.service.gov.uk/media/5a82cc1ded915d74e34039f1/2016_KS2_EnglishGPS_framework_PDFA_V9.pdf | STA/15/7340/e (ISBN 978-1-78315-825-6) | 2026-02-17 |

## Local PDFs

Stored at: `data/curriculum-documents/test-frameworks/`

- `KS2_Mathematics_TestFramework_2016.pdf` — 45 pages, 1.11 MB
- `KS2_EnglishReading_TestFramework_2016.pdf` — 22 pages, 399 KB
- `KS2_EnglishGPS_TestFramework_2016.pdf` — 35 pages, 381 KB

## Extraction Method

1. PDFs were downloaded directly from GOV.UK assets via `curl -L`
2. Text extracted using `pdftotext` (poppler 26.02.0): `pdftotext <file> <output.txt>`
3. Raw text files cached at `data/extractions/test-frameworks/raw/`
4. Content domain tables parsed from raw text and structured into JSON extraction files

## Extraction Structure

Each JSON extraction file (`ks2_*_test_framework.json`) contains:
- `framework_metadata` — document identification, marks, timing
- `test_papers` — individual test papers within the framework
- `content_domain_codes` — every content domain code with:
  - code, code_id, year (for maths), strand, substrand, description
  - `programme_id` linking to the corresponding curriculum Programme node in Neo4j

## Content Domain Coding Systems

### Mathematics
Codes: `{year}{strand_letter}{substrand_number}` e.g. `3N1`, `4C7`, `6F4`
- Year prefix: 3, 4, 5, 6
- Strands: N (Number/Place Value), C (Calculations), F (Fractions/Decimals/%), R (Ratio/Proportion), A (Algebra), M (Measurement), G (Geometry-properties), P (Position/Direction), S (Statistics)

### English Reading
Codes: `2a` through `2h` (8 content domains covering comprehension skills)

### English GPS — Paper 1 (Grammar/Punctuation/Vocabulary)
Codes: `G1.1` through `G7.4` (hierarchical, e.g. G1 = Grammatical terms, G5 = Punctuation)

### English GPS — Paper 2 (Spelling)
Codes: `S37`, `S38`, etc. (drawn from the statutory spelling appendix)

## Notes

- These frameworks apply to the **2016 national curriculum tests** (based on 2014 curriculum)
- Assessment arrangements for 2025-2026 remain unchanged (confirmed on publication pages)
- The frameworks were designed **for test developers**, not to guide teaching
- Teacher assessment still covers curriculum elements not testable in paper format

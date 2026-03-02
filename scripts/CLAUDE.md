# Planner Compiler Notes

This folder is the canonical source for teacher planner generation.

The planner compiler has three main stages:

- `generate_all_planners.py` orchestrates batch generation and writes outputs under `generated/teacher-planners/`.
- `planner_queries.py` queries Neo4j and assembles a `StudyContext` object for each study.
- `render_markdown.py`, `render_docx.py`, and `render_pptx.py` turn that context into delivery artifacts.

## Current markdown compiler behavior

The markdown path is the most actively developed output target and is the reference implementation for semantic surfacing.

Recent changes:

- `planner_queries.py` now prefers exact `SourceDocument` matches linked through study domains/programmes, then concept-level links, before falling back to broad subject/key-stage matching.
- Source-document fallback intentionally deprioritizes `Test Framework` documents when a better curriculum source is available.
- The exact-source aggregation queries order by `hits DESC, props.name` so the generation query works cleanly against Neo4j aggregation rules.
- `render_markdown.py` now surfaces more graph data that was already present in the model, including:
  - study `pedagogical_rationale`
  - richer `VehicleTemplate` descriptions and `ks_agent_prompt` notes
  - structured science enquiry guidance, question stems, scaffold prompts, and misconception detail
  - richer geography place, contrast, and feature details
- Markdown planners now include a subject capability summary near the top of each file. This makes subject-specific coverage explicit instead of implying every subject should expose the same semantic payload.

## Design boundary

The graph is the instructional structure layer. These scripts are responsible for exposing that structure clearly in generated outputs.

If review feedback says "the model has this already," check both:

- whether `planner_queries.py` is fetching the field into `StudyContext`
- whether the renderer is actually surfacing it in the output format

Most recent quality work in this folder has been about closing that gap.

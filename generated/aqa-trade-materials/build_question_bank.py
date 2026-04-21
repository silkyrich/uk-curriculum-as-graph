"""
build_question_bank.py — Build question-bank.md from curriculum_unit.json

Questions are numbered sequentially across all sections (Q1, Q2...) in section
order. Cross-references use q_id which is stable regardless of order.
"""

import json
import sys
from pathlib import Path


MARK_TYPE_LABELS = {
    2:  "Knowledge Check",
    4:  "Data Response",
    9:  "Analysis",
    15: "Extended Analysis",
    25: "Evaluation Essay",
}


def build_question_bank(unit_path: str, output_path: str = None):
    with open(unit_path) as f:
        unit = json.load(f)

    meta = unit.get("meta", {})
    sections = unit.get("sections", [])
    concepts = unit.get("concepts", {})

    lines = []
    lines.append(f"# Question Bank: {meta.get('title', 'Unit')}")
    lines.append(f"\n**Subject:** {meta.get('subject', '')}  ")
    lines.append(f"**Spec reference:** {meta.get('spec_ref', '')}  ")
    lines.append(f"**Generated from:** `curriculum_unit.json`\n")
    lines.append("> Questions are numbered by section order. Reorder sections and rebuild to renumber.\n")
    lines.append("---\n")

    # Collect all questions with sequential numbering
    all_questions = []
    for i, section in enumerate(sections, 1):
        for q in section.get("questions", []):
            all_questions.append((i, section, q))

    # ── Questions section (all questions first, mark schemes after) ────────────

    lines.append("# QUESTIONS\n")
    lines.append("---\n")

    current_section_num = None
    q_counter = 0

    for section_num, section, q in all_questions:
        if section_num != current_section_num:
            current_section_num = section_num
            lines.append(f"## Section {section_num}: {section['title']}\n")

        q_counter += 1
        marks = q.get("marks", "?")
        ao_tags = q.get("ao_tags", [])
        q_type = q.get("type", "")
        type_label = MARK_TYPE_LABELS.get(marks, "")
        ao_str = "/".join(ao_tags)
        concept_names = [concepts.get(cid, {}).get("name", cid) for cid in q.get("concepts_tested", [])]

        lines.append(f"### Q{q_counter}. [{marks} marks] {type_label}")
        if ao_str:
            lines.append(f"*Assessment objectives: {ao_str}*  ")
        if concept_names:
            lines.append(f"*Concepts: {', '.join(concept_names)}*  ")
        slide_link = q.get("links_to_slide")
        if slide_link:
            lines.append(f"*See slide `{slide_link}`*  ")
        lines.append(f"*Question ID: `{q.get('q_id', '?')}`*\n")

        # Stimulus if present
        if q.get("stimulus"):
            lines.append(f"**Stimulus:**\n\n> {q['stimulus']}\n")

        lines.append(q.get("question_text", ""))
        lines.append("")

        # Time guidance
        time_guide = q.get("time_guidance")
        if time_guide:
            lines.append(f"*Suggested time: {time_guide}*\n")

        lines.append("")

    lines.append("---\n")
    lines.append("# MARK SCHEMES\n")
    lines.append("---\n")

    # ── Mark schemes ───────────────────────────────────────────────────────────

    current_section_num = None
    q_counter = 0

    for section_num, section, q in all_questions:
        if section_num != current_section_num:
            current_section_num = section_num
            lines.append(f"## Section {section_num}: {section['title']}\n")

        q_counter += 1
        marks = q.get("marks", "?")
        type_label = MARK_TYPE_LABELS.get(marks, "")

        lines.append(f"### Mark Scheme: Q{q_counter} [{marks} marks] {type_label}\n")
        lines.append(f"*Question ID: `{q.get('q_id', '?')}`*\n")

        ms = q.get("mark_scheme", "")
        if ms:
            lines.append(ms)
        else:
            lines.append("*Mark scheme pending*")
        lines.append("")

        trap = q.get("examiner_trap")
        if trap:
            lines.append(f"> **⚠ Examiner trap:** {trap}\n")

        hint = q.get("hint")
        if hint:
            lines.append(f"> **Hint (for formative use):** {hint}\n")

        model = q.get("model_answer_summary")
        if model:
            lines.append(f"**Model answer summary:**\n\n{model}\n")

        lines.append("")

    # ── Summary statistics ─────────────────────────────────────────────────────

    lines.append("---\n")
    lines.append("## Question Bank Summary\n")

    mark_totals = {}
    ao_totals = {}
    for _, _, q in all_questions:
        m = q.get("marks", 0)
        mark_totals[m] = mark_totals.get(m, 0) + 1
        for ao in q.get("ao_tags", []):
            ao_totals[ao] = ao_totals.get(ao, 0) + 1

    total_marks = sum(q.get("marks", 0) for _, _, q in all_questions)
    lines.append(f"**Total questions:** {len(all_questions)}  ")
    lines.append(f"**Total marks available:** {total_marks}\n")

    lines.append("| Mark type | Count |")
    lines.append("|-----------|-------|")
    for marks in sorted(mark_totals.keys()):
        lines.append(f"| {marks}-mark ({MARK_TYPE_LABELS.get(marks, 'other')}) | {mark_totals[marks]} |")
    lines.append("")

    lines.append("| Assessment Objective | Questions referencing |")
    lines.append("|----------------------|-----------------------|")
    for ao in sorted(ao_totals.keys()):
        lines.append(f"| {ao} | {ao_totals[ao]} |")
    lines.append("")

    # Concept coverage
    concept_question_map = {}
    for _, _, q in all_questions:
        for cid in q.get("concepts_tested", []):
            concept_question_map.setdefault(cid, []).append(q.get("q_id", "?"))

    lines.append("### Concept Coverage\n")
    lines.append("| Concept | Questions |")
    lines.append("|---------|-----------|")
    for cid, qids in sorted(concept_question_map.items()):
        name = concepts.get(cid, {}).get("name", cid)
        lines.append(f"| {name} | {', '.join(qids)} |")

    output = "\n".join(lines)

    if output_path is None:
        output_path = Path(unit_path).parent / "question-bank.md"

    with open(output_path, "w") as f:
        f.write(output)

    print(f"Question bank written: {output_path} ({len(all_questions)} questions, {total_marks} marks)")
    return str(output_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 build_question_bank.py <curriculum_unit.json> [output.md]")
        sys.exit(1)
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    build_question_bank(inp, out)

#!/usr/bin/env python3
"""
Markdown renderer for teacher planners.

Renders a StudyContext into a professional markdown document matching
the Roman Britain format. Universal sections + subject-specific blocks.
"""

import json
from planner_queries import StudyContext, RELATIONSHIP_FIELDS, DISPLAY_FIELDS


# ── Subject-specific section config ──────────────────────────────────

SUBJECT_SECTIONS = {
    'History':              'render_history_section',
    'Geography':            'render_geography_section',
    'Science':              'render_science_section',
    'English':              'render_english_section',
    'Art and Design':       'render_art_section',
    'Music':                'render_music_section',
    'Design and Technology': 'render_dt_section',
    'Computing':            'render_computing_section',
}


CAPABILITY_LABELS = {
    'curriculum_anchor': 'Curriculum anchor',
    'concept_model': 'Concept model',
    'differentiation': 'Differentiation data',
    'thinking_lens': 'Thinking lens',
    'lesson_structure': 'Lesson structure',
    'subject_references': 'Subject references',
    'cross_curricular': 'Cross-curricular links',
    'vocabulary_definitions': 'Vocabulary definitions',
    'success_criteria': 'Success criteria',
    'prerequisites': 'Prior knowledge links',
    'assessment_alignment': 'Assessment alignment',
    'learner_scaffolding': 'Learner scaffolding',
}


SUBJECT_CAPABILITY_TARGETS = {
    'History': [
        'curriculum_anchor', 'concept_model', 'differentiation', 'thinking_lens',
        'lesson_structure', 'subject_references', 'cross_curricular',
        'vocabulary_definitions', 'success_criteria', 'prerequisites',
        'learner_scaffolding',
    ],
    'Geography': [
        'curriculum_anchor', 'concept_model', 'differentiation', 'thinking_lens',
        'lesson_structure', 'subject_references', 'cross_curricular',
        'vocabulary_definitions', 'success_criteria', 'prerequisites',
        'assessment_alignment', 'learner_scaffolding',
    ],
    'Science': [
        'curriculum_anchor', 'concept_model', 'differentiation', 'thinking_lens',
        'lesson_structure', 'subject_references', 'cross_curricular',
        'vocabulary_definitions', 'success_criteria', 'prerequisites',
        'assessment_alignment', 'learner_scaffolding',
    ],
    'English': [
        'curriculum_anchor', 'concept_model', 'differentiation', 'thinking_lens',
        'lesson_structure', 'subject_references', 'cross_curricular',
        'vocabulary_definitions', 'success_criteria', 'prerequisites',
        'assessment_alignment', 'learner_scaffolding',
    ],
    'Art and Design': [
        'curriculum_anchor', 'concept_model', 'differentiation', 'thinking_lens',
        'lesson_structure', 'cross_curricular', 'vocabulary_definitions',
        'success_criteria', 'prerequisites', 'learner_scaffolding',
    ],
    'Music': [
        'curriculum_anchor', 'concept_model', 'differentiation', 'thinking_lens',
        'lesson_structure', 'cross_curricular', 'vocabulary_definitions',
        'success_criteria', 'prerequisites', 'learner_scaffolding',
    ],
    'Design and Technology': [
        'curriculum_anchor', 'concept_model', 'differentiation', 'thinking_lens',
        'lesson_structure', 'cross_curricular', 'vocabulary_definitions',
        'success_criteria', 'prerequisites', 'learner_scaffolding',
    ],
    'Computing': [
        'curriculum_anchor', 'concept_model', 'differentiation', 'thinking_lens',
        'lesson_structure', 'cross_curricular', 'vocabulary_definitions',
        'success_criteria', 'prerequisites', 'learner_scaffolding',
    ],
}


def render_markdown(ctx: StudyContext) -> str:
    """Render a complete teacher planner as markdown."""
    lines = []
    _add = lines.append
    capability_state = _capability_state(ctx)

    # ── Header ───────────────────────────────────────────────────────
    _add(f"# {ctx.subject} | Teacher Planner: {ctx.study.get('name', 'Untitled')}")
    _add(f"*[{ctx.study_id}]*")
    _add('')

    # Metadata line
    meta_parts = []
    meta_parts.append(f"**Subject:** {ctx.subject}")
    meta_parts.append(f"**Key Stage:** {ctx.key_stage}")
    yg = ctx.study.get('year_groups')
    if yg:
        if isinstance(yg, list):
            yg = ', '.join(yg)
        meta_parts.append(f"**Year group:** {yg}")
    _add(' | '.join(meta_parts))

    # Second metadata line
    meta2 = []
    cur_ref = ctx.study.get('curriculum_reference')
    if cur_ref:
        if isinstance(cur_ref, list):
            cur_ref = cur_ref[0] if cur_ref else ''
        meta2.append(f"**Statutory reference:** {cur_ref}")
    # Source document
    if ctx.source_documents:
        sd = ctx.source_documents[0]
        sd_name = sd.get('name', sd.get('document_name', ''))
        sd_ref = sd.get('reference', sd.get('document_reference', ''))
        if sd_name:
            meta2.append(f"**Source document:** {sd_name}" + (f" ({sd_ref})" if sd_ref else ''))
    if meta2:
        _add(' | '.join(meta2))

    # Third metadata line
    meta3 = []
    duration = ctx.study.get('duration_lessons')
    if duration:
        meta3.append(f"**Estimated duration:** {duration} lessons")
    study_type = ctx.study.get('study_type', ctx.study.get('unit_type', ctx.study.get('enquiry_type', '')))
    if study_type:
        meta3.append(f"**Study type:** {study_type.replace('_', ' ').title()}")
    status = ctx.study.get('curriculum_status', '')
    if status:
        meta3.append(f"**Status:** {status.title()}")
    if meta3:
        _add(' | '.join(meta3))

    _add('')

    # ── Capability coverage ───────────────────────────────────────────
    targets = SUBJECT_CAPABILITY_TARGETS.get(ctx.subject, [])
    if targets:
        available = [CAPABILITY_LABELS[c] for c in targets if capability_state.get(c)]
        missing = [CAPABILITY_LABELS[c] for c in targets if not capability_state.get(c)]
        _add(f"**Planner coverage:** {len(available)}/{len(targets)} expected capabilities surfaced")
        _add('')
        if available:
            _add(f"**Available now:** {', '.join(available)}")
        if missing:
            _add(f"**Still thin/missing:** {', '.join(missing)}")
        _add('')

    _add('---')
    _add('')

    # ── Enquiry questions ────────────────────────────────────────────
    eq = ctx.study.get('enquiry_questions', [])
    if isinstance(eq, str):
        try:
            eq = json.loads(eq)
        except (json.JSONDecodeError, TypeError):
            eq = [eq] if eq else []
    # Also check for single enquiry_question (Science, Geo)
    if not eq:
        single_eq = ctx.study.get('enquiry_question')
        if single_eq:
            eq = [single_eq]

    if eq:
        _add('## Enquiry questions')
        _add('')
        for i, q in enumerate(eq, 1):
            _add(f"{i}. {q}")
        _add('')
        _add('---')
        _add('')

    # ── Concepts ─────────────────────────────────────────────────────
    if ctx.concepts:
        primary = [c for c in ctx.concepts if c.get('is_primary')]
        secondary = [c for c in ctx.concepts if not c.get('is_primary')]

        _add('## Concepts')
        _add('')
        _add(f"This study delivers **{len(primary)} primary concept{'s' if len(primary) != 1 else ''}** "
             f"and **{len(secondary)} secondary concept{'s' if len(secondary) != 1 else ''}**.")
        _add('')

        # Primary concepts (full treatment)
        for c in primary:
            _render_concept_full(lines, c)

        # Secondary concepts (can be full or compact depending on count)
        for c in secondary:
            if len(secondary) <= 4:
                _render_concept_compact(lines, c, ctx.label)
            else:
                _render_concept_minimal(lines, c)

        _add('---')
        _add('')

    # ── Thinking lens ────────────────────────────────────────────────
    if ctx.thinking_lenses:
        _add('## Thinking lens' + (f": {ctx.thinking_lenses[0]['lens_name']} (primary)" if ctx.thinking_lenses else ''))
        _add('')
        primary_lens = ctx.thinking_lenses[0]
        _add(f"**Key question:** {primary_lens.get('key_question', '')}")
        _add('')
        if primary_lens.get('rationale'):
            _add(f"**Why this lens fits:** {primary_lens['rationale']}")
            _add('')
        stems = primary_lens.get('question_stems', [])
        if stems:
            _add(f"**Question stems for {ctx.key_stage}:**")
            for s in stems:
                _add(f"- {s}")
            _add('')

        # Secondary lenses
        if len(ctx.thinking_lenses) > 1:
            sec = ctx.thinking_lenses[1]
            rationale = sec.get('rationale', '')
            _add(f"**Secondary lens:** {sec['lens_name']}"
                 + (f" — {rationale}" if rationale else ''))
            _add('')

        _add('---')
        _add('')

    # ── Session structure (vehicle templates) ────────────────────────
    if ctx.templates:
        _add('## Session structure' + (f": {' + '.join(t.get('name', '') for t in ctx.templates)}" if ctx.templates else ''))
        _add('')
        if len(ctx.templates) > 1:
            _add(f"This study uses {len(ctx.templates)} vehicle templates:")
            _add('')

        for vt in ctx.templates:
            _add(f"### {vt.get('name', 'Template')}" +
                 (f" (main structure)" if vt == ctx.templates[0] and len(ctx.templates) > 1 else ''))
            template_desc = vt.get('description', '')
            if template_desc:
                _add(template_desc)
                _add('')
            phases = vt.get('session_structure', [])
            if phases:
                _add(f"`{'` → `'.join(phases)}`")
                _add('')
            assessment = vt.get('assessment_approach', '')
            if assessment:
                _add(f"**Assessment:** {assessment}")
                _add('')
            ks_prompt = vt.get('ks_agent_prompt', '')
            if ks_prompt:
                _add(f"**Teacher note:** {ks_prompt}")
                _add('')
            stems = vt.get('ks_question_stems', [])
            if stems:
                _add(f"**{ctx.key_stage} question stems:**")
                for s in stems:
                    _add(f"- {s}")
                _add('')

        _add('---')
        _add('')

    # ── Subject-specific section ─────────────────────────────────────
    renderer_name = SUBJECT_SECTIONS.get(ctx.subject)
    if renderer_name and renderer_name in globals():
        globals()[renderer_name](lines, ctx)

    # ── Pedagogical rationale ────────────────────────────────────────
    rationale = ctx.study.get('pedagogical_rationale', '')
    if rationale:
        _add('## Why this study matters')
        _add('')
        _add(rationale)
        _add('')
        _add('---')
        _add('')

    # ── Sequencing ───────────────────────────────────────────────────
    if ctx.follows or ctx.leads_to:
        _add('## Sequencing')
        _add('')
        if ctx.follows:
            _add(f"**Follows:** {ctx.follows}")
        if ctx.leads_to:
            _add(f"**Leads to:** {ctx.leads_to}")
        _add('')
        _add('---')
        _add('')

    # ── Pitfalls ─────────────────────────────────────────────────────
    pitfalls = ctx.study.get('common_pitfalls', [])
    if isinstance(pitfalls, str):
        try:
            pitfalls = json.loads(pitfalls)
        except (json.JSONDecodeError, TypeError):
            pitfalls = [pitfalls] if pitfalls else []
    if pitfalls:
        _add('## Pitfalls to avoid')
        _add('')
        for i, p in enumerate(pitfalls, 1):
            _add(f"{i}. {p}")
        _add('')

    # ── Sensitive content ────────────────────────────────────────────
    sensitive = ctx.study.get('sensitive_content_notes', [])
    if isinstance(sensitive, str):
        try:
            sensitive = json.loads(sensitive)
        except (json.JSONDecodeError, TypeError):
            sensitive = [sensitive] if sensitive else []
    if sensitive:
        _add('## Sensitive content')
        _add('')
        for s in sensitive:
            _add(f"- {s}")
        _add('')

    if pitfalls or sensitive:
        _add('---')
        _add('')

    # ── Success criteria ─────────────────────────────────────────────
    success = ctx.study.get('success_criteria', [])
    if isinstance(success, str):
        try:
            success = json.loads(success)
        except (json.JSONDecodeError, TypeError):
            success = [success] if success else []
    # Also pull from vehicle template
    if not success and ctx.templates:
        for vt in ctx.templates:
            sc = vt.get('success_criteria', [])
            if sc:
                success = sc
                break

    if success:
        _add('## Success criteria')
        _add('')
        _add('**Pupils can:**')
        for s in success:
            _add(f"- {s}")
        _add('')
        _add('---')
        _add('')

    # ── Cross-curricular opportunities ───────────────────────────────
    if ctx.cross_curricular:
        _add('## Cross-curricular opportunities')
        _add('')
        _add('| Link | Subject | Connection | Strength |')
        _add('|------|---------|------------|----------|')
        for cc in ctx.cross_curricular:
            name = cc.get('target_name', '')
            subj = cc.get('target_subject', '')
            hook = cc.get('hook', '')
            strength = cc.get('strength', '')
            _add(f"| {name} | {subj} | {hook} | {strength.title() if strength else ''} |")
        _add('')
        _add('---')
        _add('')

    # ── Epistemic skills ─────────────────────────────────────────────
    if ctx.epistemic_skills:
        _add(f'## {_skill_heading(ctx.subject)} ({ctx.key_stage})')
        _add('')
        _add('These disciplinary skills should be woven through teaching, not taught in isolation:')
        _add('')
        for skill in ctx.epistemic_skills:
            desc = skill.get('description', '')
            _add(f"- **{skill['name']}** — {desc}" if desc else f"- **{skill['name']}**")
        _add('')
        _add('---')
        _add('')

    # ── Vocabulary word mat ──────────────────────────────────────────
    definitions = ctx.study.get('definitions', [])
    if isinstance(definitions, str):
        try:
            definitions = json.loads(definitions)
        except (json.JSONDecodeError, TypeError):
            definitions = []

    # Also gather key_vocabulary from concepts
    all_vocab = set()
    for c in ctx.concepts:
        kv = c.get('key_vocabulary', '')
        if isinstance(kv, str) and kv:
            all_vocab.update(v.strip() for v in kv.split(','))
        elif isinstance(kv, list):
            all_vocab.update(kv)

    if definitions or all_vocab:
        _add('## Vocabulary word mat')
        _add('')
        # If definitions are dicts with term+meaning
        if definitions and isinstance(definitions[0], dict):
            _add('| Term | Meaning |')
            _add('|------|---------|')
            for d in definitions:
                _add(f"| {d.get('term', '')} | {d.get('meaning', '')} |")
        elif definitions and isinstance(definitions[0], str):
            _add('| Term | Meaning |')
            _add('|------|---------|')
            for d in definitions:
                _add(f"| {d} | |")
        # Supplement with concept key_vocabulary not already in definitions
        def_terms = set()
        for d in definitions:
            if isinstance(d, dict):
                def_terms.add(d.get('term', '').lower())
            elif isinstance(d, str):
                def_terms.add(d.lower())
        extra_vocab = sorted(v for v in all_vocab if v.lower() not in def_terms)
        # Limit concept vocab supplement to 10 terms max
        extra_vocab = extra_vocab[:10]
        if extra_vocab and not definitions:
            # No definitions at all — create table from concept vocab
            _add('| Term | Meaning |')
            _add('|------|---------|')
        for v in extra_vocab:
            _add(f"| {v} | *(from concept key vocabulary)* |")
        _add('')

    # ── Prior knowledge / retrieval plan ────────────────────────────
    if ctx.prerequisites:
        _add('## Prior knowledge (retrieval plan)')
        _add('')
        _add('Pupils should already know the following from earlier units:')
        _add('')
        _add('| Prior knowledge needed | For concept | Description |')
        _add('|----------------------|-------------|-------------|')
        seen = set()
        for p in ctx.prerequisites:
            key = p.get('prereq_id', '')
            if key in seen:
                continue
            seen.add(key)
            prereq_name = p.get('prereq_name', '')
            target = p.get('target_name', '')
            desc = p.get('prereq_description', '')
            if len(desc) > 100:
                desc = desc[:97] + '...'
            _add(f"| {prereq_name} | {target} | {desc} |")
        _add('')
        _add('---')
        _add('')

    # ── Assessment alignment (KS2) ───────────────────────────────
    if ctx.assessment_codes:
        _add('## Assessment alignment (KS2)')
        _add('')
        _add('KS2 test framework content domain codes assessed by this study:')
        _add('')
        _add('| Code | Description | Assesses concept |')
        _add('|------|-------------|-----------------|')
        for ac in ctx.assessment_codes:
            _add(f"| **{ac.get('code_id', '')}** | {ac.get('description', '')} | {ac.get('concept_name', '')} |")
        _add('')
        _add('---')
        _add('')

    # ── Scaffolding and inclusion ─────────────────────────────────
    if ctx.learner_profile:
        ped = ctx.learner_profile.get('pedagogy', {})
        content = ctx.learner_profile.get('content', {})
        feedback = ctx.learner_profile.get('feedback', {})
        year_id = ctx.learner_profile.get('year_id', '')

        if ped or content or feedback:
            _add(f'## Scaffolding and inclusion ({year_id})')
            _add('')
            _add('| Guideline | Detail |')
            _add('|-----------|--------|')
            if content.get('label'):
                lexile = ''
                if content.get('lexile_min') and content.get('lexile_max'):
                    lexile = f" (Lexile {content['lexile_min']}–{content['lexile_max']})"
                _add(f"| Reading level | {content['label']}{lexile} |")
            if content.get('tts_required') is not None:
                tts = 'Required' if content['tts_required'] else ('Available' if content.get('tts_available') else 'Not needed')
                _add(f"| Text-to-speech | {tts} |")
            if content.get('max_sentence_length_words'):
                _add(f"| Max sentence length | {content['max_sentence_length_words']} words |")
            if content.get('vocabulary_notes'):
                _add(f"| Vocabulary | {content['vocabulary_notes']} |")
            if ped.get('scaffolding_level'):
                _add(f"| Scaffolding level | {ped['scaffolding_level'].replace('_', ' ').title()} |")
            if ped.get('hint_tiers_max'):
                _add(f"| Hint tiers | {ped['hint_tiers_max']} tiers |")
            if ped.get('session_length_min_minutes') and ped.get('session_length_max_minutes'):
                _add(f"| Session length | {ped['session_length_min_minutes']}–{ped['session_length_max_minutes']} minutes |")
            if ped.get('worked_examples_required'):
                style = ped.get('worked_example_style', '')
                _add(f"| Worked examples | Required" + (f" — {style}" if style else '') + " |")
            if feedback.get('ai_tone'):
                _add(f"| Feedback tone | {feedback['ai_tone'].replace('_', ' ').title()} |")
            if feedback.get('normalize_struggle'):
                _add(f"| Normalize struggle | Yes |")
            if feedback.get('feedback_example_correct'):
                _add(f"| Example correct feedback | *{feedback['feedback_example_correct']}* |")
            if feedback.get('feedback_example_incorrect'):
                _add(f"| Example error feedback | *{feedback['feedback_example_incorrect']}* |")
            _add('')
            _add('---')
            _add('')

    # ── Knowledge organiser ───────────────────────────────────────
    ko_definitions = ctx.study.get('definitions', [])
    if isinstance(ko_definitions, str):
        try:
            ko_definitions = json.loads(ko_definitions)
        except (json.JSONDecodeError, TypeError):
            ko_definitions = []
    ko_events = ctx.study.get('key_events', [])
    if isinstance(ko_events, str):
        try:
            ko_events = json.loads(ko_events)
        except (json.JSONDecodeError, TypeError):
            ko_events = [ko_events] if ko_events else []
    ko_figures = ctx.study.get('key_figures', [])
    if isinstance(ko_figures, str):
        try:
            ko_figures = json.loads(ko_figures)
        except (json.JSONDecodeError, TypeError):
            ko_figures = [ko_figures] if ko_figures else []
    ko_period = ctx.study.get('period', '')
    # Core facts from expected/secure DL descriptions of primary concepts
    ko_core_facts = []
    for c in ctx.concepts:
        if not c.get('is_primary'):
            continue
        for dl in c.get('difficulty_levels', []):
            if dl.get('label') in ('expected', 'secure') and dl.get('description'):
                ko_core_facts.append({
                    'concept': c.get('name', c.get('concept_name', '')),
                    'description': dl['description']
                })
                break

    if ko_definitions or ko_events or ko_figures or ko_core_facts:
        _add('## Knowledge organiser')
        _add('')
        if ko_period:
            _add(f"**Period:** {ko_period}")
            _add('')
        if ko_definitions:
            _add('**Key terms:**')
            for d in ko_definitions:
                if isinstance(d, dict):
                    _add(f"- **{d.get('term', '')}**: {d.get('meaning', '')}")
                else:
                    _add(f"- {d}")
            _add('')
        if ko_events:
            _add('**Timeline / key events:**')
            for e in ko_events:
                _add(f"- {e}")
            _add('')
        if ko_figures:
            _add(f"**Key figures:** {', '.join(ko_figures)}")
            _add('')
        if ko_core_facts:
            _add('**Core facts (expected standard):**')
            for fact in ko_core_facts:
                _add(f"- **{fact['concept']}**: {fact['description']}")
            _add('')
        _add('---')
        _add('')

    # ── Graph context ─────────────────────────────────────────────────
    _add('## Graph context')
    _add('')
    _add(f"**Node type:** `{ctx.label}` | **Study ID:** `{ctx.study_id}`")
    _add('')

    id_field_map = {
        'HistoryStudy': 'study_id', 'GeoStudy': 'study_id',
        'ScienceEnquiry': 'enquiry_id', 'EnglishUnit': 'unit_id',
    }
    id_field = id_field_map.get(ctx.label, 'suggestion_id')

    domain_ids = ctx.study.get('domain_ids', [])
    if isinstance(domain_ids, str):
        try:
            domain_ids = json.loads(domain_ids)
        except (json.JSONDecodeError, TypeError):
            domain_ids = []
    if domain_ids:
        _add(f"**Domain IDs:** {', '.join(f'`{d}`' for d in domain_ids)}")
        _add('')

    if ctx.concepts:
        _add('**Concept IDs:**')
        for c in ctx.concepts:
            cid = c.get('concept_id', '')
            name = c.get('concept_name', c.get('name', ''))
            pri = ' (primary)' if c.get('is_primary') else ''
            _add(f"- `{cid}`: {name}{pri}")
        _add('')

    _add('**Cypher query:**')
    _add('```cypher')
    _add(f"MATCH (ts:{ctx.label} {{{id_field}: '{ctx.study_id}'}})")
    _add(f"  -[:DELIVERS_VIA]->(c:Concept)")
    _add(f"  -[:HAS_DIFFICULTY_LEVEL]->(dl)")
    _add(f"RETURN c.name, dl.label, dl.description")
    _add('```')
    _add('')

    # ── Footer ─────────────────────────────────────────────────────
    _add('---')
    _add('')
    _add('*Generated from the UK Curriculum Knowledge Graph — zero LLM generation.*')
    _add('')

    return '\n'.join(lines)


# ── Concept rendering helpers ────────────────────────────────────────

def _render_concept_full(lines, concept):
    """Full treatment for primary concepts — description, guidance, differentiation."""
    _add = lines.append
    cid = concept.get('concept_id', '')
    name = concept.get('concept_name', concept.get('name', ''))
    ctype = concept.get('concept_type', '')
    tw = concept.get('teaching_weight', '')

    _add(f"### Primary concept: {name} ({cid})")
    _add('')

    meta = []
    if ctype:
        meta.append(f"**Type:** {ctype.title()}")
    if tw:
        meta.append(f"**Teaching weight:** {tw}/6")
    if meta:
        _add(' | '.join(meta))
        _add('')

    desc = concept.get('description', '')
    if desc:
        _add(desc)
        _add('')

    guidance = concept.get('teaching_guidance', '')
    if guidance:
        _add(f"**Teaching guidance:** {guidance}")
        _add('')

    kv = concept.get('key_vocabulary', '')
    if kv:
        _add(f"**Key vocabulary:** {kv}")
        _add('')

    misconceptions = concept.get('common_misconceptions', '')
    if misconceptions:
        _add(f"**Common misconceptions:** {misconceptions}")
        _add('')

    # Differentiation table
    dls = concept.get('difficulty_levels', [])
    if dls:
        _add('#### Differentiation')
        _add('')
        # Check which columns have data
        has_task = any(dl.get('example_task') for dl in dls)
        has_errors = any(dl.get('common_errors') for dl in dls)
        has_response = any(dl.get('example_response') for dl in dls)

        if has_task and has_errors:
            _add('| Level | What success looks like | Example task | Common errors |')
            _add('|-------|------------------------|-------------|---------------|')
        elif has_task:
            _add('| Level | What success looks like | Example task |')
            _add('|-------|------------------------|-------------|')
        else:
            _add('| Level | What success looks like | Common errors |')
            _add('|-------|------------------------|---------------|')

        for dl in dls:
            label = dl.get('label', '').replace('_', ' ').title()
            desc = dl.get('description', '')
            task = dl.get('example_task', '')
            errors = dl.get('common_errors', '')
            if isinstance(errors, list):
                errors = '; '.join(errors)

            if has_task and has_errors:
                _add(f"| **{label}** | {desc} | {task} | {errors} |")
            elif has_task:
                _add(f"| **{label}** | {desc} | {task} |")
            else:
                _add(f"| **{label}** | {desc} | {errors} |")

        _add('')

        # Model responses (below table for readability)
        if has_response:
            for dl in dls:
                resp = dl.get('example_response', '')
                if resp:
                    label = dl.get('label', '').replace('_', ' ').title()
                    _add(f"> **Model response ({label}):** *{resp}*")
                    _add('')

    # CPA representation stages (primary maths)
    rss = concept.get('representation_stages', [])
    if rss:
        _add('#### Representation stages (CPA)')
        _add('')
        _add('| Stage | Description | Resources | Transition cue |')
        _add('|-------|-------------|-----------|----------------|')
        for rs in rss:
            stage = rs.get('stage', '').title()
            desc = rs.get('description', '')
            resources = rs.get('resources', [])
            if isinstance(resources, list):
                resources = ', '.join(resources)
            cue = rs.get('transition_cue', '')
            _add(f"| **{stage}** | {desc} | {resources} | {cue} |")
        _add('')


def _render_concept_compact(lines, concept, label):
    """Compact rendering for secondary concepts — name, ID, role in study."""
    _add = lines.append
    cid = concept.get('concept_id', '')
    name = concept.get('concept_name', concept.get('name', ''))
    ctype = concept.get('concept_type', '')
    tw = concept.get('teaching_weight', '')

    _add(f"### Secondary concept: {name} ({cid})")
    _add('')

    meta = []
    if ctype:
        meta.append(f"**Type:** {ctype.title()}")
    if tw:
        meta.append(f"**Teaching weight:** {tw}/6")
    if meta:
        _add(' | '.join(meta))
        _add('')

    desc = concept.get('description', '')
    if desc:
        _add(desc)
        _add('')

    # Compact differentiation (just levels + errors, no full table)
    dls = concept.get('difficulty_levels', [])
    if dls:
        _add('#### Differentiation')
        _add('')
        has_errors = any(dl.get('common_errors') for dl in dls)
        _add('| Level | What success looks like | Common errors |')
        _add('|-------|------------------------|---------------|')
        for dl in dls:
            label = dl.get('label', '').replace('_', ' ').title()
            desc = dl.get('description', '')
            errors = dl.get('common_errors', '')
            if isinstance(errors, list):
                errors = '; '.join(errors)
            _add(f"| **{label}** | {desc} | {errors} |")
        _add('')


def _render_concept_minimal(lines, concept):
    """Minimal rendering — just name and description, one line each."""
    _add = lines.append
    cid = concept.get('concept_id', '')
    name = concept.get('concept_name', concept.get('name', ''))
    desc = concept.get('description', '')
    _add(f"- **{name}** ({cid}): {desc[:120]}{'...' if len(desc) > 120 else ''}")


def _skill_heading(subject: str) -> str:
    """Return the appropriate heading for epistemic skills."""
    mapping = {
        'History': 'Historical thinking skills',
        'Geography': 'Geographical skills',
        'Science': 'Working scientifically skills',
        'English': 'Reading and writing skills',
        'Computing': 'Computational thinking skills',
        'Mathematics': 'Mathematical reasoning skills',
    }
    return mapping.get(subject, 'Disciplinary skills')


def _has_meaningful_vocab_definitions(ctx: StudyContext) -> bool:
    """True when at least one vocabulary term includes a non-empty meaning."""
    definitions = ctx.study.get('definitions', [])
    if isinstance(definitions, str):
        try:
            definitions = json.loads(definitions)
        except (json.JSONDecodeError, TypeError):
            return False
    if not definitions:
        return False
    return any(
        isinstance(d, dict) and bool(d.get('meaning', '').strip())
        for d in definitions
    )


def _has_subject_references(ctx: StudyContext) -> bool:
    """True when a subject-specific reference collection contains data."""
    if not ctx.references:
        return False
    return any(bool(value) for value in ctx.references.values())


def _capability_state(ctx: StudyContext) -> dict[str, bool]:
    """Compute which planner capabilities are actually surfaced for this study."""
    return {
        'curriculum_anchor': bool(ctx.study.get('curriculum_reference')) and bool(ctx.source_documents),
        'concept_model': bool(ctx.concepts),
        'differentiation': any(bool(c.get('difficulty_levels')) for c in ctx.concepts),
        'thinking_lens': bool(ctx.thinking_lenses),
        'lesson_structure': bool(ctx.templates),
        'subject_references': _has_subject_references(ctx),
        'cross_curricular': bool(ctx.cross_curricular),
        'vocabulary_definitions': _has_meaningful_vocab_definitions(ctx),
        'success_criteria': bool(ctx.study.get('success_criteria')) or any(
            bool(t.get('success_criteria')) for t in ctx.templates
        ),
        'prerequisites': bool(ctx.prerequisites),
        'assessment_alignment': bool(ctx.assessment_codes),
        'learner_scaffolding': bool(ctx.learner_profile),
    }


# ── Subject-specific section renderers ───────────────────────────────

def render_history_section(lines, ctx: StudyContext):
    """History-specific sections: sources, figures, disciplinary concepts."""
    _add = lines.append
    study = ctx.study

    # Primary sources
    sources = ctx.references.get('sources', [])
    if sources:
        _add('## Primary sources')
        _add('')
        _add(f"{'Three' if len(sources) == 3 else str(len(sources))} historically grounded source types are available for this study:")
        _add('')
        for i, src in enumerate(sources, 1):
            name = src.get('name', src.get('source_name', ''))
            stype = src.get('source_type', '').replace('_', ' ').title()
            date = src.get('date', src.get('date_range', ''))
            _add(f"### {i}. {name}" + (f" ({stype}, {date})" if stype else ''))

            provenance = src.get('provenance', src.get('description', ''))
            if provenance:
                _add(provenance)
                _add('')

            ped_use = src.get('pedagogical_use', '')
            if ped_use:
                _add(f"**How to use:** {ped_use}")
                _add('')

            location = src.get('location', '')
            if location:
                _add(f"**Location:** {location}")
            url = src.get('url', '')
            if url:
                _add(f"**URL:** {url}")
            _add('')
        _add('---')
        _add('')

    # Disciplinary concepts
    dc = ctx.references.get('disciplinary_concepts', [])
    if dc:
        _add('## Disciplinary concepts foregrounded')
        _add('')
        _add('| Concept | Key question | Role in this study |')
        _add('|---------|-------------|-------------------|')
        for d in dc:
            name = d.get('name', d.get('concept_name', ''))
            kq = d.get('key_question', '')
            guidance = d.get('ks_guidance', '')
            _add(f"| {name} | {kq} | {guidance} |")
        _add('')
        _add('---')
        _add('')

    # Key figures and events
    figures = study.get('key_figures')
    events = study.get('key_events')
    if figures or events:
        _add('## Key figures and events')
        _add('')
        if figures:
            if isinstance(figures, str):
                try:
                    figures = json.loads(figures)
                except (json.JSONDecodeError, TypeError):
                    figures = [figures]
            _add(f"**Key figures:** {', '.join(figures)}")
            _add('')
        if events:
            if isinstance(events, str):
                try:
                    events = json.loads(events)
                except (json.JSONDecodeError, TypeError):
                    events = [events]
            _add('**Key events:**')
            for e in events:
                _add(f"- {e}")
            _add('')

        period = study.get('period', '')
        if period:
            _add(f"**Period:** {period}")
            _add('')

        perspectives = study.get('perspectives')
        if perspectives:
            if isinstance(perspectives, str):
                try:
                    perspectives = json.loads(perspectives)
                except (json.JSONDecodeError, TypeError):
                    perspectives = [perspectives]
            _add(f"**Perspectives to include:** {', '.join(perspectives)}")
            _add('')

        sig = study.get('significance_claim', '')
        if sig:
            _add(f"**Significance claim:** {sig}")
            _add('')

        interps = study.get('interpretations')
        if interps:
            if isinstance(interps, str):
                try:
                    interps = json.loads(interps)
                except (json.JSONDecodeError, TypeError):
                    interps = [interps]
            _add('**Historiographical debate:**')
            for interp in interps:
                _add(f"- {interp}")
            _add('')

        _add('---')
        _add('')


def render_science_section(lines, ctx: StudyContext):
    """Science-specific sections: variables, equipment, safety, enquiry type."""
    _add = lines.append
    study = ctx.study

    # Variables
    variables = study.get('variables')
    if variables:
        if isinstance(variables, str):
            try:
                variables = json.loads(variables)
            except (json.JSONDecodeError, TypeError):
                variables = None
        if variables and isinstance(variables, dict):
            _add('## Variables')
            _add('')
            _add(f"**Independent:** {variables.get('independent', '')}")
            _add(f"**Dependent:** {variables.get('dependent', '')}")
            controlled = variables.get('controlled', [])
            if controlled:
                if isinstance(controlled, list):
                    _add(f"**Controlled:** {', '.join(controlled)}")
                else:
                    _add(f"**Controlled:** {controlled}")
            _add('')
            _add('---')
            _add('')

    # Equipment and safety
    equipment = study.get('equipment', [])
    safety = study.get('safety_notes', '')
    if equipment or safety:
        _add('## Equipment and safety')
        _add('')
        if equipment:
            if isinstance(equipment, str):
                try:
                    equipment = json.loads(equipment)
                except (json.JSONDecodeError, TypeError):
                    equipment = [equipment]
            _add('**Equipment:**')
            for e in equipment:
                _add(f"- {e}")
            _add('')
        if safety:
            hazard = study.get('hazard_level', '')
            _add(f"**Safety notes:** {safety}" + (f" (Hazard level: {hazard})" if hazard else ''))
            _add('')
        _add('---')
        _add('')

    # Expected outcome and recording
    outcome = study.get('expected_outcome', '')
    recording = study.get('recording_format', [])
    if outcome or recording:
        _add('## Expected outcome')
        _add('')
        if outcome:
            _add(outcome)
            _add('')
        if recording:
            if isinstance(recording, str):
                try:
                    recording = json.loads(recording)
                except (json.JSONDecodeError, TypeError):
                    recording = [recording]
            _add(f"**Recording format:** {', '.join(recording)}")
            _add('')
        _add('---')
        _add('')

    # Enquiry types
    ets = ctx.references.get('enquiry_types', [])
    if ets:
        _add('## Enquiry type')
        _add('')
        for et in ets:
            _add(f"### {et.get('name', '')}")
            desc = et.get('description', '')
            if desc:
                _add(desc)
                _add('')
            guidance = et.get(f"{ctx.key_stage.lower()}_guidance", '')
            if guidance:
                _add(f"**{ctx.key_stage} guidance:** {guidance}")
                _add('')
            stems = et.get('question_stems', [])
            if stems:
                _add('**Question stems:**')
                for stem in stems:
                    _add(f"- {stem}")
                _add('')
            scaffold = et.get('key_question_scaffold', [])
            if scaffold:
                _add('**Teacher scaffold:**')
                for step in scaffold:
                    _add(f"- {step}")
                _add('')
        _add('')
        _add('---')
        _add('')

    # Misconceptions (from reference nodes)
    misconceptions = ctx.references.get('misconceptions', [])
    if misconceptions:
        _add('## Known misconceptions')
        _add('')
        for m in misconceptions:
            _add(f"### {m.get('name', '')}")
            pupil_statement = m.get('pupil_statement', '')
            if pupil_statement:
                _add(f"**What pupils may say:** {pupil_statement}")
            explanation = m.get('correct_explanation', m.get('description', ''))
            if explanation:
                _add(f"**Correct explanation:** {explanation}")
            diagnostic = m.get('diagnostic_questions', [])
            if diagnostic:
                _add('**Diagnostic questions:**')
                for q in diagnostic[:3]:
                    _add(f"- {q}")
            _add('')
        _add('')
        _add('---')
        _add('')


def render_english_section(lines, ctx: StudyContext):
    """English-specific sections: text type, writing outcome, grammar, texts."""
    _add = lines.append
    study = ctx.study

    # Text type and features
    text_type = study.get('text_type', '')
    features = study.get('text_features_to_teach', [])
    if text_type or features:
        _add('## Text type and features')
        _add('')
        if text_type:
            _add(f"**Text type:** {text_type.replace('_', ' ').title()}")
        if features:
            if isinstance(features, str):
                try:
                    features = json.loads(features)
                except (json.JSONDecodeError, TypeError):
                    features = [features]
            _add(f"**Features to teach:** {', '.join(features)}")
        _add('')

    # Writing outcome
    outcome = study.get('writing_outcome', '')
    if outcome:
        _add(f"**Writing outcome:** {outcome}")
        _add('')

    # Grammar focus
    grammar = study.get('grammar_focus', [])
    if grammar:
        if isinstance(grammar, str):
            try:
                grammar = json.loads(grammar)
            except (json.JSONDecodeError, TypeError):
                grammar = [grammar]
        _add(f"**Grammar focus:** {', '.join(grammar)}")
        gram_src = study.get('grammar_year_source', '')
        if gram_src:
            _add(f"*(from {gram_src} Appendix 2)*")
        _add('')

    # Literary terms
    lit_terms = study.get('literary_terms', [])
    if lit_terms:
        if isinstance(lit_terms, str):
            try:
                lit_terms = json.loads(lit_terms)
            except (json.JSONDecodeError, TypeError):
                lit_terms = [lit_terms]
        _add(f"**Literary terms:** {', '.join(lit_terms)}")
        _add('')

    if text_type or features or outcome or grammar:
        _add('---')
        _add('')

    # Suggested texts
    texts = study.get('suggested_texts', [])
    if texts:
        if isinstance(texts, str):
            try:
                texts = json.loads(texts)
            except (json.JSONDecodeError, TypeError):
                texts = []
        if texts:
            _add('## Suggested texts')
            _add('')
            for t in texts:
                if isinstance(t, dict):
                    title = t.get('title', '')
                    author = t.get('author', '')
                    note = t.get('note', '')
                    _add(f"- **{title}** by {author}" + (f" — {note}" if note else ''))
                else:
                    _add(f"- {t}")
            _add('')
            _add('---')
            _add('')

    # Genres
    genres = ctx.references.get('genres', [])
    if genres:
        _add('## Genre')
        _add('')
        for g in genres:
            _add(f"- **{g.get('name', '')}:** {g.get('description', '')}")
        _add('')
        _add('---')
        _add('')

    # Set texts
    set_texts = ctx.references.get('set_texts', [])
    if set_texts:
        _add('## Set texts')
        _add('')
        for st in set_texts:
            _add(f"- **{st.get('title', st.get('name', ''))}** by {st.get('author', '')}")
        _add('')
        _add('---')
        _add('')


def render_geography_section(lines, ctx: StudyContext):
    """Geography-specific sections: locations, scale, fieldwork, maps."""
    _add = lines.append
    study = ctx.study

    # Locations and scale
    scale = study.get('scale', '')
    themes = study.get('themes', [])
    if scale or themes:
        _add('## Study scope')
        _add('')
        if scale:
            _add(f"**Scale:** {scale.replace('_', ' ').title()}")
        if themes:
            if isinstance(themes, str):
                try:
                    themes = json.loads(themes)
                except (json.JSONDecodeError, TypeError):
                    themes = [themes]
            _add(f"**Themes:** {', '.join(themes)}")
        _add('')

    # Map types and data sources
    maps = study.get('map_types', [])
    data_src = study.get('data_sources', [])
    if maps or data_src:
        if maps:
            if isinstance(maps, str):
                try:
                    maps = json.loads(maps)
                except (json.JSONDecodeError, TypeError):
                    maps = [maps]
            _add(f"**Map types:** {', '.join(m.replace('_', ' ') for m in maps)}")
        if data_src:
            if isinstance(data_src, str):
                try:
                    data_src = json.loads(data_src)
                except (json.JSONDecodeError, TypeError):
                    data_src = [data_src]
            _add(f"**Data sources:** {', '.join(data_src)}")
        _add('')

    # Fieldwork
    fieldwork = study.get('fieldwork_potential', '')
    if fieldwork:
        _add(f"**Fieldwork potential:** {fieldwork}")
        _add('')

    # Assessment guidance
    assess = study.get('assessment_guidance', '')
    if assess:
        _add(f"**Assessment guidance:** {assess}")
        _add('')

    if scale or themes or maps or fieldwork:
        _add('---')
        _add('')

    # Places
    places = ctx.references.get('places', [])
    if places:
        _add('## Locations')
        _add('')
        for p in places:
            place_name = p.get('formal_name', p.get('name', ''))
            details = []
            if p.get('country'):
                details.append(p['country'])
            if p.get('continent'):
                details.append(p['continent'])
            if p.get('place_type'):
                details.append(p['place_type'].replace('_', ' '))
            if p.get('scale'):
                details.append(p['scale'].replace('_', ' '))
            suffix = f" ({', '.join(details)})" if details else ''
            _add(f"### {place_name}{suffix}")
            description = p.get('description', '')
            if description:
                _add(description)
                _add('')
            if p.get('development_classification'):
                _add(f"**Development context:** {p['development_classification']}")
            exemplar_choices = p.get('exemplar_choices', [])
            if exemplar_choices:
                _add(f"**Suggested exemplars:** {', '.join(exemplar_choices)}")
            physical = p.get('key_physical_features', [])
            if physical:
                _add(f"**Key physical features:** {', '.join(physical)}")
            human = p.get('key_human_features', [])
            if human:
                _add(f"**Key human features:** {', '.join(human)}")
            _add('')
        _add('')
        _add('---')
        _add('')

    # Contrasting localities
    contrasts = ctx.references.get('contrasts', [])
    if contrasts:
        _add('## Contrasting localities')
        _add('')
        for c in contrasts:
            _add(f"### {c.get('name', '')}")
            rationale = c.get('pedagogical_rationale', c.get('description', ''))
            if rationale:
                _add(rationale)
                _add('')
            dimensions = c.get('dimensions', [])
            if dimensions:
                _add(f"**Compare through:** {', '.join(dimensions)}")
            prompts = c.get('stimulus_questions', [])
            if prompts:
                _add('**Stimulus questions:**')
                for prompt in prompts[:4]:
                    _add(f"- {prompt}")
            _add('')
        _add('')
        _add('---')
        _add('')


def render_art_section(lines, ctx: StudyContext):
    """Art-specific sections: artist, movement, medium, techniques."""
    _add = lines.append
    study = ctx.study

    _add('## Art focus')
    _add('')
    artist = study.get('artist', '')
    if artist:
        dates = study.get('artist_dates', '')
        _add(f"**Artist:** {artist}" + (f" ({dates})" if dates else ''))
    movement = study.get('art_movement', '')
    if movement:
        _add(f"**Art movement:** {movement}")
    medium = study.get('medium', [])
    if medium:
        if isinstance(medium, list):
            _add(f"**Medium:** {', '.join(medium)}")
        else:
            _add(f"**Medium:** {medium}")
    techniques = study.get('techniques', [])
    if techniques:
        if isinstance(techniques, list):
            _add(f"**Techniques:** {', '.join(techniques)}")
        else:
            _add(f"**Techniques:** {techniques}")
    elements = study.get('visual_elements', [])
    if elements:
        if isinstance(elements, list):
            _add(f"**Visual elements:** {', '.join(elements)}")
        else:
            _add(f"**Visual elements:** {elements}")
    context = study.get('cultural_context', '')
    if context:
        _add(f"**Cultural context:** {context}")
    _add('')
    _add('---')
    _add('')


def render_music_section(lines, ctx: StudyContext):
    """Music-specific sections: genre, composer, elements, instruments."""
    _add = lines.append
    study = ctx.study

    _add('## Music focus')
    _add('')
    genre = study.get('genre', '')
    if genre:
        _add(f"**Genre:** {genre.replace('_', ' ').title()}")
    composer = study.get('composer', '')
    piece = study.get('piece', '')
    if composer or piece:
        _add(f"**Composer/piece:** {composer}" + (f" — {piece}" if piece else ''))
    elements = study.get('musical_elements', [])
    if elements:
        if isinstance(elements, list):
            _add(f"**Musical elements:** {', '.join(elements)}")
    instruments = study.get('instrument', [])
    if instruments:
        if isinstance(instruments, list):
            _add(f"**Instruments:** {', '.join(instruments)}")
    notation = study.get('notation_level', '')
    if notation:
        _add(f"**Notation level:** {notation.replace('_', ' ')}")
    repertoire = study.get('listening_repertoire', [])
    if repertoire:
        if isinstance(repertoire, list):
            _add(f"**Listening repertoire:** {', '.join(repertoire)}")
    mmc = study.get('mmc_reference', '')
    if mmc:
        _add(f"**MMC reference:** {mmc}")
    _add('')
    _add('---')
    _add('')


def render_dt_section(lines, ctx: StudyContext):
    """DT-specific sections: design brief, materials, tools, safety."""
    _add = lines.append
    study = ctx.study

    strand = study.get('dt_strand', '')
    if strand:
        _add(f"## Design and Technology: {strand.replace('_', ' ').title()}")
    else:
        _add('## Design and Technology focus')
    _add('')

    brief = study.get('design_brief', '')
    if brief:
        _add(f"**Design brief:** {brief}")
        _add('')

    materials = study.get('materials', [])
    if materials:
        if isinstance(materials, list):
            _add(f"**Materials:** {', '.join(materials)}")
    tools = study.get('tools', [])
    if tools:
        if isinstance(tools, list):
            _add(f"**Tools:** {', '.join(tools)}")
    techniques = study.get('techniques', [])
    if techniques:
        if isinstance(techniques, list):
            _add(f"**Techniques:** {', '.join(techniques)}")
    safety = study.get('safety_notes', '')
    if safety:
        _add(f"**Safety notes:** {safety}")

    eval_criteria = study.get('evaluation_criteria', [])
    if eval_criteria:
        if isinstance(eval_criteria, list):
            _add('')
            _add('**Evaluation criteria:**')
            for e in eval_criteria:
                _add(f"- {e}")

    # Food-specific
    allergens = study.get('food_allergens', [])
    if allergens:
        if isinstance(allergens, list):
            _add(f"**Food allergens:** {', '.join(allergens)}")
    food_skills = study.get('food_skills', [])
    if food_skills:
        if isinstance(food_skills, list):
            _add(f"**Food skills:** {', '.join(food_skills)}")

    _add('')
    _add('---')
    _add('')


def render_computing_section(lines, ctx: StudyContext):
    """Computing-specific sections: language, concepts, tools."""
    _add = lines.append
    study = ctx.study

    _add('## Computing focus')
    _add('')

    paradigm = study.get('programming_paradigm', '')
    if paradigm:
        _add(f"**Programming paradigm:** {paradigm.replace('_', ' ').title()}")
    tool = study.get('software_tool', '')
    if tool:
        _add(f"**Software/tool:** {tool}")
    concepts = study.get('computational_concept', [])
    if concepts:
        if isinstance(concepts, list):
            _add(f"**Computational concepts:** {', '.join(c.replace('_', ' ') for c in concepts)}")
    abstraction = study.get('abstraction_level', '')
    if abstraction:
        _add(f"**Abstraction level:** {abstraction.replace('_', ' ').title()}")
    themes = study.get('themes', [])
    if themes:
        if isinstance(themes, list):
            _add(f"**Themes:** {', '.join(themes)}")
    _add('')
    _add('---')
    _add('')

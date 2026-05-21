#!/usr/bin/env python3
"""
Markdown renderers for the full curriculum graph site export.

Mirror of compile_site_data.py: the website compiles eight graph views into
JSON; these functions turn the *same* query results into a hierarchical set
of markdown pages so the markdown build is not missing data the site exposes.

Each renderer takes a plain data dict/list (identical in shape to what
compile_site_data.py writes as JSON) and returns a markdown string.
"""

import re


# ── Formatting helpers ───────────────────────────────────────────────

def slug(text: str) -> str:
    """URL/folder-safe slug (matches compile_site_data.slugify)."""
    text = (text or '').lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-') or 'untitled'


def cell(value) -> str:
    """Escape a value for use inside a markdown table cell."""
    if value is None:
        return ''
    if isinstance(value, (list, tuple)):
        value = '; '.join(str(v) for v in value if v not in (None, ''))
    text = str(value)
    return text.replace('|', '\\|').replace('\n', ' ').replace('\r', ' ').strip()


def listify(value) -> list:
    """Coerce a str/list/None into a clean list of strings."""
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return [str(v) for v in value if v not in (None, '')]
    return [str(value)]


def year_sort_key(year_id) -> int:
    """Sort EYFS first, then Y1..Y11."""
    if not year_id:
        return 99
    if year_id == 'EYFS':
        return 0
    m = re.match(r'Y(\d+)', str(year_id))
    return int(m.group(1)) if m else 98


def titleize(text) -> str:
    return str(text or '').replace('_', ' ').strip().title()


def _h(level: int, text: str) -> str:
    return f"{'#' * level} {text}"


# ── 1. Site index (overview) ─────────────────────────────────────────

def render_site_index(overview: dict, subjects: list, lenses: list,
                       profiles: list, planner_count: int) -> str:
    """Root README.md — global stats and navigation."""
    L = []
    L.append('# UK Curriculum Knowledge Graph — Markdown Export')
    L.append('')
    L.append('A complete markdown rendering of the curriculum knowledge graph. '
             'This export mirrors every data view served by the website.')
    L.append('')

    L.append('## Graph at a glance')
    L.append('')
    L.append('| Measure | Count |')
    L.append('|---------|-------|')
    rows = [
        ('Subjects', overview.get('subjects')),
        ('Key stages', overview.get('key_stages_count')),
        ('Domains', overview.get('domains')),
        ('Objectives', overview.get('objectives')),
        ('Concepts', overview.get('concepts')),
        ('Concept clusters', overview.get('clusters')),
        ('Difficulty levels', overview.get('difficulty_levels')),
        ('Thinking lenses', overview.get('thinking_lenses')),
        ('Prerequisite links', overview.get('prerequisites')),
        ('Teacher planners', planner_count),
    ]
    for label, value in rows:
        if value is not None:
            L.append(f"| {label} | {value:,} |" if isinstance(value, int)
                     else f"| {label} | {cell(value)} |")
    L.append('')

    key_stages = overview.get('key_stages', [])
    if key_stages:
        L.append('## Key stages')
        L.append('')
        L.append('| Key stage | Name | Years | Concepts |')
        L.append('|-----------|------|-------|----------|')
        for ks in key_stages:
            years = ', '.join(ks.get('year_ids', []))
            L.append(f"| {cell(ks.get('id'))} | {cell(ks.get('name'))} | "
                     f"{cell(years)} | {ks.get('concept_count', 0)} |")
        L.append('')

    L.append('## Sections')
    L.append('')
    L.append('- [Subjects](subjects/) — curriculum structure, domains and concepts')
    L.append('- [Thinking lenses](thinking-lenses/) — cross-subject cognitive framings')
    L.append('- [Learner profiles](learner-profiles/) — age-appropriate pedagogy by year')
    L.append('- [Delivery modes](delivery-modes/) — how each concept can be taught')
    L.append('- [Prerequisites](prerequisites/) — learning progression links')
    L.append('- [Teacher planners](planners/) — ready-to-use study planners')
    L.append('')

    if subjects:
        L.append('### Subjects index')
        L.append('')
        L.append('| Subject | Key stages | Domains | Concepts | Clusters |')
        L.append('|---------|-----------|---------|----------|----------|')
        for s in sorted(subjects, key=lambda x: x.get('name', '')):
            sslug = s.get('slug') or slug(s.get('name', ''))
            ks = ', '.join(s.get('key_stages', []))
            L.append(f"| [{cell(s.get('name'))}](subjects/{sslug}/) | {cell(ks)} | "
                     f"{s.get('total_domains', 0)} | {s.get('total_concepts', 0)} | "
                     f"{s.get('total_clusters', 0)} |")
        L.append('')

    L.append('---')
    L.append('')
    L.append('*Generated from the UK Curriculum Knowledge Graph — zero LLM generation.*')
    L.append('')
    return '\n'.join(L)


# ── 2. Subject index ─────────────────────────────────────────────────

def render_subject_index(subject: dict) -> str:
    """Per-subject README.md — years, domains and links to domain pages."""
    L = []
    name = subject.get('name', 'Subject')
    L.append(f"# {name}")
    L.append('')
    L.append('| Measure | Count |')
    L.append('|---------|-------|')
    L.append(f"| Key stages | {cell(', '.join(subject.get('key_stages', [])))} |")
    L.append(f"| Domains | {subject.get('total_domains', 0)} |")
    L.append(f"| Concepts | {subject.get('total_concepts', 0)} |")
    L.append(f"| Concept clusters | {subject.get('total_clusters', 0)} |")
    L.append('')

    years = sorted(subject.get('years', []),
                   key=lambda y: y.get('year_number') or year_sort_key(y.get('year_id')))
    for year in years:
        yid = year.get('year_id', '')
        ks = year.get('key_stage', '')
        heading = f"Year {year.get('year_number')}" if year.get('year_number') else yid
        L.append(f"## {heading}" + (f" ({ks})" if ks else ''))
        L.append('')
        domains = year.get('domains', [])
        if not domains:
            L.append('*No domains.*')
            L.append('')
            continue
        L.append('| Domain | Concepts | Clusters |')
        L.append('|--------|----------|----------|')
        for d in domains:
            did = d.get('domain_id', '')
            link = f"{yid}/{did}.md"
            L.append(f"| [{cell(d.get('name'))}]({link}) | "
                     f"{d.get('concept_count', 0)} | {d.get('cluster_count', 0)} |")
        L.append('')

    L.append('---')
    L.append('')
    L.append('[← Back to site index](../../README.md)')
    L.append('')
    return '\n'.join(L)


# ── 3. Domain detail page ────────────────────────────────────────────

def render_domain(domain: dict) -> str:
    """Full domain page — concepts, clusters, prerequisites, suggestions, SEND."""
    L = []
    _add = L.append

    _add(f"# {domain.get('name', 'Domain')}")
    _add(f"*[{domain.get('domain_id', '')}]*")
    _add('')

    meta = []
    if domain.get('subject'):
        meta.append(f"**Subject:** {domain['subject']}")
    if domain.get('year_id'):
        yn = domain.get('year_number')
        meta.append(f"**Year:** {'Year ' + str(yn) if yn else domain['year_id']}")
    if domain.get('key_stage'):
        meta.append(f"**Key stage:** {domain['key_stage']}")
    if meta:
        _add(' | '.join(meta))
        _add('')

    if domain.get('description'):
        _add(domain['description'])
        _add('')
    if domain.get('curriculum_context'):
        _add(f"**Curriculum context:** {domain['curriculum_context']}")
        _add('')

    _add('---')
    _add('')

    # ── Concepts ─────────────────────────────────────────────────────
    concepts = domain.get('concepts', [])
    _add(f"## Concepts ({len(concepts)})")
    _add('')
    for c in concepts:
        _render_domain_concept(L, c)

    # ── Concept clusters ─────────────────────────────────────────────
    clusters = domain.get('clusters', [])
    if clusters:
        _add(f"## Concept clusters ({len(clusters)})")
        _add('')
        for cl in clusters:
            _add(f"### {cl.get('name', 'Cluster')} "
                 f"`{cl.get('cluster_id', '')}`")
            _add('')
            cmeta = []
            if cl.get('cluster_type'):
                cmeta.append(f"**Type:** {titleize(cl['cluster_type'])}")
            if cl.get('teaching_weeks'):
                cmeta.append(f"**Teaching weeks:** {cl['teaching_weeks']}")
            if cl.get('lesson_count'):
                cmeta.append(f"**Lessons:** {cl['lesson_count']}")
            if cl.get('is_curated'):
                cmeta.append('**Curated**')
            if cmeta:
                _add(' | '.join(cmeta))
                _add('')
            if cl.get('rationale'):
                _add(cl['rationale'])
                _add('')
            cids = cl.get('concept_ids', [])
            if cids:
                _add(f"**Concepts grouped:** {', '.join(f'`{x}`' for x in cids)}")
                _add('')
            lenses = cl.get('thinking_lenses', [])
            if lenses:
                _add('**Thinking lenses:**')
                _add('')
                _add('| Rank | Lens | Key question | Why it fits |')
                _add('|------|------|--------------|-------------|')
                for tl in lenses:
                    _add(f"| {cell(tl.get('rank'))} | {cell(tl.get('name'))} | "
                         f"{cell(tl.get('key_question'))} | {cell(tl.get('rationale'))} |")
                _add('')
            after = cl.get('sequenced_after', [])
            if after:
                _add(f"**Sequenced after:** {', '.join(f'`{x}`' for x in after)}")
                _add('')
        _add('---')
        _add('')

    # ── Prerequisites ────────────────────────────────────────────────
    prereqs = domain.get('prerequisites', [])
    if prereqs:
        _add('## Prior knowledge (prerequisites from other domains)')
        _add('')
        _add('| Prior concept | From domain | Needed for |')
        _add('|---------------|-------------|-----------|')
        for p in prereqs:
            from_dom = p.get('from_domain_name') or p.get('from_domain_id') or ''
            _add(f"| {cell(p.get('prereq_name'))} `{p.get('prereq_id', '')}` | "
                 f"{cell(from_dom)} | {cell(p.get('target_name'))} |")
        _add('')
        _add('---')
        _add('')

    # ── Study suggestions ────────────────────────────────────────────
    suggestions = domain.get('suggestions', [])
    if suggestions:
        _add(f"## Study suggestions ({len(suggestions)})")
        _add('')
        for s in suggestions:
            _render_suggestion(L, s)
        _add('---')
        _add('')

    # ── Access and inclusion (SEND) ──────────────────────────────────
    _render_domain_send(L, domain)

    _add('[← Back to subject](../README.md)')
    _add('')
    return '\n'.join(L)


def _render_domain_concept(lines, c):
    _add = lines.append
    name = c.get('name', '')
    cid = c.get('concept_id', '')
    _add(f"### {name} `{cid}`")
    _add('')

    badges = []
    if c.get('concept_type'):
        badges.append(f"**Type:** {titleize(c['concept_type'])}")
    if c.get('teaching_weight'):
        badges.append(f"**Teaching weight:** {c['teaching_weight']}/6")
    if c.get('is_keystone'):
        badges.append('**Keystone concept**')
    dm = c.get('delivery_mode')
    if dm and dm.get('name'):
        badges.append(f"**Delivery:** {dm['name']}")
    if badges:
        _add(' | '.join(badges))
        _add('')

    if c.get('description'):
        _add(c['description'])
        _add('')
    if c.get('teaching_guidance'):
        _add(f"**Teaching guidance:** {c['teaching_guidance']}")
        _add('')
    if c.get('key_vocabulary'):
        kv = c['key_vocabulary']
        if isinstance(kv, list):
            kv = ', '.join(kv)
        _add(f"**Key vocabulary:** {kv}")
        _add('')
    if c.get('common_misconceptions'):
        _add(f"**Common misconceptions:** {c['common_misconceptions']}")
        _add('')

    if dm and (dm.get('confidence') or dm.get('rationale')):
        bits = []
        if dm.get('confidence'):
            bits.append(f"confidence: {dm['confidence']}")
        if dm.get('rationale'):
            bits.append(dm['rationale'])
        _add(f"**Delivery rationale:** {' — '.join(bits)}")
        _add('')

    # Difficulty levels
    dls = c.get('difficulty_levels', [])
    if dls:
        _add('**Difficulty levels:**')
        _add('')
        _add('| Level | What success looks like | Example task | Common errors |')
        _add('|-------|-------------------------|--------------|---------------|')
        for dl in dls:
            label = titleize(dl.get('label'))
            num = dl.get('level_number')
            label_disp = f"{num}. {label}" if num else label
            _add(f"| {cell(label_disp)} | {cell(dl.get('description'))} | "
                 f"{cell(dl.get('example_task'))} | {cell(dl.get('common_errors'))} |")
        _add('')
        for dl in dls:
            if dl.get('example_response'):
                _add(f"> **Model response ({titleize(dl.get('label'))}):** "
                     f"*{dl['example_response']}*")
                _add('')

    # Representation stages (CPA)
    rss = c.get('representation_stages', [])
    if rss:
        _add('**Representation stages (CPA):**')
        _add('')
        _add('| Stage | Description | Resources | Transition cue |')
        _add('|-------|-------------|-----------|----------------|')
        for rs in rss:
            _add(f"| {cell(titleize(rs.get('stage')))} | {cell(rs.get('description'))} | "
                 f"{cell(rs.get('resources'))} | {cell(rs.get('transition_cue'))} |")
        _add('')

    # Vocabulary terms
    vts = c.get('vocabulary_terms', [])
    if vts:
        _add('**Vocabulary terms:**')
        _add('')
        _add('| Term | Definition | Tier | Word class | Introduced here |')
        _add('|------|------------|------|------------|-----------------|')
        for vt in vts:
            intro = 'Yes' if vt.get('introduced') else ''
            _add(f"| {cell(vt.get('term'))} | {cell(vt.get('definition'))} | "
                 f"{cell(vt.get('tier'))} | {cell(vt.get('word_class'))} | {intro} |")
        _add('')


def _render_suggestion(lines, s):
    _add = lines.append
    _add(f"### {s.get('name', 'Study')}")
    _add('')
    if s.get('type'):
        _add(f"*{titleize(s['type'])}*")
        _add('')
    if s.get('description'):
        _add(s['description'])
        _add('')
    if s.get('pedagogical_rationale'):
        _add(f"**Why this study:** {s['pedagogical_rationale']}")
        _add('')

    # Subject-specific optional fields
    field_labels = [
        ('period', 'Period'),
        ('enquiry_question', 'Enquiry question'),
        ('enquiry_type', 'Enquiry type'),
        ('writing_outcome', 'Writing outcome'),
        ('genre', 'Genre'),
        ('place', 'Place'),
        ('contrast', 'Contrasting locality'),
        ('cpa_stage', 'CPA stage'),
        ('nc_aim_emphasis', 'NC aim emphasis'),
    ]
    for key, label in field_labels:
        if s.get(key):
            _add(f"**{label}:** {cell(s[key])}")
            _add('')

    list_labels = [
        ('key_figures', 'Key figures'),
        ('disciplinary_concepts', 'Disciplinary concepts'),
        ('sources', 'Sources'),
        ('misconceptions', 'Misconceptions addressed'),
        ('manipulatives', 'Manipulatives'),
        ('representations', 'Representations'),
        ('fluency_targets', 'Fluency targets'),
    ]
    for key, label in list_labels:
        vals = listify(s.get(key))
        if vals:
            _add(f"**{label}:** {', '.join(vals)}")
            _add('')

    if s.get('variables'):
        _add(f"**Variables:** {cell(s['variables'])}")
        _add('')
    if s.get('template_name'):
        _add(f"**Vehicle template:** {s['template_name']}")
        _add('')
    cids = s.get('concept_ids', [])
    if cids:
        _add(f"**Delivers concepts:** {', '.join(f'`{x}`' for x in cids)}")
        _add('')
    cc = s.get('cross_curricular', [])
    if cc:
        names = [x.get('target_name', '') for x in cc if x.get('target_name')]
        if names:
            _add(f"**Cross-curricular links:** {', '.join(names)}")
            _add('')


def _render_domain_send(lines, domain):
    _add = lines.append
    summary = domain.get('send_summary')
    barriers = domain.get('concept_barriers', [])
    if not summary and not barriers:
        return

    _add('## Access and inclusion (SEND)')
    _add('')
    if summary:
        _add(f"{summary.get('concepts_with_barriers', 0)} of "
             f"{summary.get('total_concepts', 0)} concepts have tagged access barriers.")
        _add('')
        counts = summary.get('barrier_counts', {})
        if counts:
            _add('**Barrier frequency:**')
            _add('')
            _add('| Barrier | Concepts affected |')
            _add('|---------|-------------------|')
            for name, n in sorted(counts.items(), key=lambda x: -x[1]):
                _add(f"| {cell(name)} | {n} |")
            _add('')
        top = summary.get('top_strategies', [])
        if top:
            _add('**Most relevant support strategies:**')
            _add('')
            _add('| Strategy | Tier | Construct risk | Mitigates |')
            _add('|----------|------|----------------|-----------|')
            for st in top:
                _add(f"| {cell(st.get('name'))} | {cell(st.get('tier'))} | "
                     f"{cell(st.get('construct_risk'))} | {st.get('mitigates_count', 0)} |")
            _add('')

    if barriers:
        _add('**Barriers per concept:**')
        _add('')
        _add('| Concept | Barrier | Level | Rationale |')
        _add('|---------|---------|-------|-----------|')
        for cb in barriers:
            cname = cb.get('concept_name', '')
            for b in cb.get('barriers', []):
                _add(f"| {cell(cname)} | {cell(b.get('name'))} | "
                     f"{cell(b.get('level'))} | {cell(b.get('rationale'))} |")
        _add('')
    _add('---')
    _add('')


# ── 4. Thinking lenses ───────────────────────────────────────────────

def render_lens_index(lenses: list) -> str:
    L = []
    L.append('# Thinking lenses')
    L.append('')
    L.append('Ten cross-subject cognitive lenses applied to concept clusters. '
             'Each lens reframes a topic around a recurring kind of question.')
    L.append('')
    L.append('| Lens | Key question | Clusters | Primary use |')
    L.append('|------|--------------|----------|-------------|')
    for tl in lenses:
        link = f"{slug(tl.get('name', ''))}.md"
        L.append(f"| [{cell(tl.get('name'))}]({link}) | {cell(tl.get('key_question'))} | "
                 f"{tl.get('cluster_count', 0)} | {tl.get('primary_count', 0)} |")
    L.append('')
    L.append('[← Back to site index](../README.md)')
    L.append('')
    return '\n'.join(L)


def render_lens(tl: dict) -> str:
    L = []
    L.append(f"# {tl.get('name', 'Thinking lens')}")
    L.append(f"*[{tl.get('id', '')}]*")
    L.append('')
    if tl.get('description'):
        L.append(tl['description'])
        L.append('')
    if tl.get('key_question'):
        L.append(f"**Key question:** {tl['key_question']}")
        L.append('')
    if tl.get('agent_prompt'):
        L.append(f"**Agent prompt:** {tl['agent_prompt']}")
        L.append('')

    L.append('| Measure | Count |')
    L.append('|---------|-------|')
    L.append(f"| Clusters applying this lens | {tl.get('cluster_count', 0)} |")
    L.append(f"| Clusters using it as primary | {tl.get('primary_count', 0)} |")
    L.append('')

    ks_prompts = [p for p in tl.get('ks_prompts', []) if p and p.get('key_stage')]
    if ks_prompts:
        L.append('## Age-banded prompts')
        L.append('')
        for p in sorted(ks_prompts, key=lambda x: x.get('key_stage', '')):
            L.append(f"### {p['key_stage']}")
            L.append('')
            if p.get('agent_prompt'):
                L.append(p['agent_prompt'])
                L.append('')
            stems = listify(p.get('question_stems'))
            if stems:
                L.append('**Question stems:**')
                for stem in stems:
                    L.append(f"- {stem}")
                L.append('')

    L.append('---')
    L.append('')
    L.append('[← Back to thinking lenses](README.md)')
    L.append('')
    return '\n'.join(L)


# ── 5. Learner profiles ──────────────────────────────────────────────

def render_profile_index(profiles: list) -> str:
    L = []
    L.append('# Learner profiles')
    L.append('')
    L.append('Age-appropriate pedagogy, content and feedback guidelines for each year group.')
    L.append('')
    L.append('| Year | Age range | Interaction types |')
    L.append('|------|-----------|-------------------|')
    for p in sorted(profiles, key=lambda x: x.get('year_number') or year_sort_key(x.get('year_id'))):
        yid = p.get('year_id', '')
        link = f"{slug(yid)}.md"
        name = p.get('year_name') or yid
        L.append(f"| [{cell(name)}]({link}) | {cell(p.get('age_range'))} | "
                 f"{len(p.get('interactions', []))} |")
    L.append('')
    L.append('[← Back to site index](../README.md)')
    L.append('')
    return '\n'.join(L)


def render_profile(p: dict) -> str:
    L = []
    name = p.get('year_name') or p.get('year_id', 'Year')
    L.append(f"# {name} — learner profile")
    L.append('')
    if p.get('age_range'):
        L.append(f"**Age range:** {p['age_range']}")
        L.append('')

    for section_key, heading in (('content', 'Content guideline'),
                                 ('pedagogy', 'Pedagogy profile'),
                                 ('feedback', 'Feedback profile')):
        data = p.get(section_key) or {}
        rows = [(k, v) for k, v in data.items()
                if v not in (None, '', [], {}) and not k.startswith('display')]
        if not rows:
            continue
        L.append(f"## {heading}")
        L.append('')
        L.append('| Property | Value |')
        L.append('|----------|-------|')
        for k, v in sorted(rows):
            L.append(f"| {cell(titleize(k))} | {cell(v)} |")
        L.append('')

    interactions = p.get('interactions', [])
    if interactions:
        L.append('## Supported interaction types')
        L.append('')
        L.append('| Interaction | Category | Input method | Visual complexity |')
        L.append('|-------------|----------|--------------|-------------------|')
        for it in interactions:
            L.append(f"| {cell(it.get('name'))} | {cell(it.get('category'))} | "
                     f"{cell(it.get('input_method'))} | {cell(it.get('visual_complexity'))} |")
        L.append('')

    L.append('---')
    L.append('')
    L.append('[← Back to learner profiles](README.md)')
    L.append('')
    return '\n'.join(L)


# ── 6. Delivery modes ────────────────────────────────────────────────

def render_delivery(delivery: dict) -> str:
    L = []
    L.append('# Delivery modes')
    L.append('')
    L.append('Every concept is classified by what combination of AI, human '
             'facilitation and specialist expertise it needs.')
    L.append('')

    modes = delivery.get('modes', [])
    if modes:
        L.append('## Modes')
        L.append('')
        L.append('| Mode | Description |')
        L.append('|------|-------------|')
        for m in modes:
            L.append(f"| **{cell(m.get('name'))}** | {cell(m.get('description'))} |")
        L.append('')

    summary = delivery.get('summary', [])
    if summary:
        total = sum(r.get('count', 0) for r in summary) or 1
        L.append('## Overall distribution')
        L.append('')
        L.append('| Mode | Concepts | Share |')
        L.append('|------|----------|-------|')
        for r in summary:
            pct = 100.0 * r.get('count', 0) / total
            L.append(f"| {cell(r.get('mode_name'))} | {r.get('count', 0)} | {pct:.1f}% |")
        L.append('')

    by_subject = delivery.get('by_subject', [])
    if by_subject:
        mode_ids = [m.get('id') for m in modes]
        mode_names = {m.get('id'): m.get('name') for m in modes}
        L.append('## By subject')
        L.append('')
        header = '| Subject | ' + ' | '.join(mode_names.get(mid, mid) for mid in mode_ids) + ' |'
        L.append(header)
        L.append('|' + '---|' * (len(mode_ids) + 1))
        for row in by_subject:
            cells = [cell(row.get('subject'))]
            for mid in mode_ids:
                cells.append(str(row.get('modes', {}).get(mid, {}).get('count', 0)))
            L.append('| ' + ' | '.join(cells) + ' |')
        L.append('')

    by_ks = delivery.get('by_key_stage', [])
    if by_ks:
        mode_ids = [m.get('id') for m in modes]
        mode_names = {m.get('id'): m.get('name') for m in modes}
        L.append('## By key stage')
        L.append('')
        header = '| Key stage | ' + ' | '.join(mode_names.get(mid, mid) for mid in mode_ids) + ' |'
        L.append(header)
        L.append('|' + '---|' * (len(mode_ids) + 1))
        for row in by_ks:
            cells = [cell(row.get('key_stage'))]
            for mid in mode_ids:
                cells.append(str(row.get('modes', {}).get(mid, {}).get('count', 0)))
            L.append('| ' + ' | '.join(cells) + ' |')
        L.append('')

    requirements = delivery.get('requirements', [])
    if requirements:
        L.append('## Teaching requirements')
        L.append('')
        L.append('| Requirement | Category | Implies minimum mode | Concepts | Description |')
        L.append('|-------------|----------|----------------------|----------|-------------|')
        for r in requirements:
            L.append(f"| {cell(r.get('name'))} | {cell(r.get('category'))} | "
                     f"{cell(r.get('implies_mode'))} | {r.get('concept_count', 0)} | "
                     f"{cell(r.get('description'))} |")
        L.append('')

    L.append('---')
    L.append('')
    L.append('[← Back to site index](../README.md)')
    L.append('')
    return '\n'.join(L)


# ── 7. Prerequisites ─────────────────────────────────────────────────

def render_prerequisites(prereq_graph: dict) -> str:
    nodes = {n['id']: n for n in prereq_graph.get('nodes', [])}
    edges = prereq_graph.get('edges', [])

    L = []
    L.append('# Prerequisite progression')
    L.append('')
    L.append(f"{len(edges):,} prerequisite links connect {len(nodes):,} concepts "
             'into learning progressions.')
    L.append('')

    # Per-subject counts
    subj_counts = {}
    cross_subject = []
    for e in edges:
        src = nodes.get(e.get('source'), {})
        tgt = nodes.get(e.get('target'), {})
        s_subj = src.get('subject') or 'Unknown'
        t_subj = tgt.get('subject') or 'Unknown'
        subj_counts[t_subj] = subj_counts.get(t_subj, 0) + 1
        if s_subj != t_subj:
            cross_subject.append((e, src, tgt))

    if subj_counts:
        L.append('## Links by subject')
        L.append('')
        L.append('| Subject | Incoming prerequisite links |')
        L.append('|---------|-----------------------------|')
        for subj, n in sorted(subj_counts.items(), key=lambda x: -x[1]):
            L.append(f"| {cell(subj)} | {n} |")
        L.append('')

    if cross_subject:
        L.append(f'## Cross-subject prerequisites ({len(cross_subject)})')
        L.append('')
        L.append('Concepts whose prerequisite sits in a different subject — useful '
                 'for cross-curricular sequencing.')
        L.append('')
        L.append('| Prerequisite | From subject | Enables | In subject |')
        L.append('|--------------|--------------|---------|------------|')
        for e, src, tgt in sorted(cross_subject,
                                  key=lambda x: (x[1].get('subject') or '',
                                                 x[2].get('subject') or '')):
            L.append(f"| {cell(e.get('source_name'))} | {cell(src.get('subject'))} | "
                     f"{cell(e.get('target_name'))} | {cell(tgt.get('subject'))} |")
        L.append('')

    L.append('---')
    L.append('')
    L.append('[← Back to site index](../README.md)')
    L.append('')
    return '\n'.join(L)


# ── 8. Planner index ─────────────────────────────────────────────────

def render_planner_index(planners: list) -> str:
    """planners/README.md — grouped by subject then key stage."""
    L = []
    L.append('# Teacher planners')
    L.append('')
    L.append(f"{len(planners)} ready-to-use study planners generated from the graph.")
    L.append('')

    by_subject = {}
    for p in planners:
        by_subject.setdefault(p.get('subject', 'Other'), []).append(p)

    for subject in sorted(by_subject):
        L.append(f"## {subject}")
        L.append('')
        items = by_subject[subject]
        by_ks = {}
        for p in items:
            by_ks.setdefault(p.get('key_stage', ''), []).append(p)
        for ks in sorted(by_ks):
            L.append(f"### {ks}" if ks else '### (unspecified key stage)')
            L.append('')
            for p in sorted(by_ks[ks], key=lambda x: x.get('title', '')):
                L.append(f"- [{cell(p.get('title'))}]({p['rel_path']})")
            L.append('')

    L.append('---')
    L.append('')
    L.append('[← Back to site index](../README.md)')
    L.append('')
    return '\n'.join(L)

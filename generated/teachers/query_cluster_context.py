#!/usr/bin/env python3
"""
Pull the complete teaching context for a ConceptCluster from Neo4j.

Queries:
  - Cluster metadata (name, type, rationale, inspired_by, is_curated)
  - All concepts in the cluster (description, guidance, vocabulary,
    misconceptions, keystone flag, concept_type, teaching_weight)
  - Domain context (name, curriculum_context, structure_type)
  - Subject and year group
  - Learner profile for that year:
      ContentGuideline  — reading level, TTS, Lexile, agent_content_prompt
      PedagogyProfile   — session structure, scaffolding, productive failure,
                          desirable_difficulties, agent_pedagogy_prompt
      FeedbackProfile   — tone, safety flags, avoid_phrases, agent_feedback_prompt
      InteractionTypes  — primary + secondary with agent_prompt for each
  - Prerequisite concepts (what pupils must already know)
  - All concepts in the containing domain (for sequencing context)
  - Previous cluster (SEQUENCED_AFTER back-link)
  - Next cluster(s)
  - PedagogyTechniques in use for this year group

Output: JSON to stdout or --output file, plus Markdown summary.

Usage:
  python3 query_cluster_context.py MA-Y3-D001-CL001
  python3 query_cluster_context.py MA-Y3-D001-CL001 --output year3-maths/context.json
  python3 query_cluster_context.py SC-KS2-D001-CL001 --year Y5 --output year5-science/context.json

The --year flag overrides the year group used for the learner profile (ContentGuideline,
PedagogyProfile, FeedbackProfile, InteractionTypes). Use it when a KS-level domain returns
the wrong anchor year (e.g. SC-KS2 anchors to Y3 but you're teaching the cluster in Y5).
"""

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / "core" / "scripts"))

from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


def query_context(session, cluster_id, year_override=None):
    ctx = {}

    # ── 1. Cluster node ───────────────────────────────────────────────────────
    r = session.run("""
        MATCH (cc:ConceptCluster {cluster_id: $cid})
        RETURN cc.cluster_id        AS cluster_id,
               cc.cluster_name      AS cluster_name,
               cc.cluster_type      AS cluster_type,
               cc.rationale         AS rationale,
               cc.inspired_by       AS inspired_by,
               cc.is_curated        AS is_curated,
               cc.teaching_weeks    AS teaching_weeks,
               cc.lesson_count      AS lesson_count,
               cc.is_keystone_cluster AS is_keystone_cluster
    """, cid=cluster_id)
    row = r.single()
    if not row:
        raise ValueError(f"ConceptCluster '{cluster_id}' not found in graph")
    ctx["cluster"] = dict(row)

    # ── 2. Concepts grouped by this cluster ───────────────────────────────────
    r = session.run("""
        MATCH (cc:ConceptCluster {cluster_id: $cid})-[:GROUPS]->(c:Concept)
        RETURN c.concept_id             AS concept_id,
               c.concept_name          AS concept_name,
               c.description           AS description,
               c.teaching_guidance     AS teaching_guidance,
               c.key_vocabulary        AS key_vocabulary,
               c.common_misconceptions AS common_misconceptions,
               coalesce(c.concept_type, 'knowledge')  AS concept_type,
               coalesce(c.teaching_weight, 1)          AS teaching_weight,
               coalesce(c.is_keystone, false)          AS is_keystone
        ORDER BY c.concept_id
    """, cid=cluster_id)
    ctx["concepts"] = [dict(r) for r in r]

    # ── 2b. Difficulty levels per concept ──────────────────────────────────────
    r = session.run("""
        MATCH (cc:ConceptCluster {cluster_id: $cid})-[:GROUPS]->(c:Concept)
              -[:HAS_DIFFICULTY_LEVEL]->(dl:DifficultyLevel)
        RETURN c.concept_id AS concept_id, dl.level_number AS level,
               dl.label AS label, dl.description AS description,
               dl.example_task AS example_task
        ORDER BY c.concept_id, dl.level_number
    """, cid=cluster_id)
    dl_by_concept = {}
    for row in r:
        dl_by_concept.setdefault(row["concept_id"], []).append(dict(row))
    ctx["difficulty_levels"] = dl_by_concept

    # ── 2c. Representation stages per concept ──────────────────────────────
    r = session.run("""
        MATCH (cc:ConceptCluster {cluster_id: $cid})-[:GROUPS]->(c:Concept)
              -[:HAS_REPRESENTATION_STAGE]->(rs:RepresentationStage)
        RETURN c.concept_id AS concept_id, rs.stage_number AS stage_number,
               rs.stage AS stage, rs.description AS description,
               rs.resources AS resources, rs.example_activity AS example_activity,
               rs.transition_cue AS transition_cue
        ORDER BY c.concept_id, rs.stage_number
    """, cid=cluster_id)
    rs_by_concept = {}
    for row in r:
        rs_by_concept.setdefault(row["concept_id"], []).append(dict(row))
    ctx["representation_stages"] = rs_by_concept

    # ── 3. Domain + subject + year group ─────────────────────────────────────
    r = session.run("""
        MATCH (d:Domain)-[:HAS_CLUSTER]->(cc:ConceptCluster {cluster_id: $cid})
        OPTIONAL MATCH (p:Programme)-[:HAS_DOMAIN]->(d)
        OPTIONAL MATCH (y:Year)-[:HAS_PROGRAMME]->(p)
        OPTIONAL MATCH (ks:KeyStage)-[:HAS_YEAR]->(y)
        RETURN d.domain_id           AS domain_id,
               d.domain_name         AS domain_name,
               d.description         AS domain_description,
               d.curriculum_context  AS curriculum_context,
               coalesce(d.structure_type, 'mixed') AS structure_type,
               p.subject_name        AS subject,
               p.key_stage           AS key_stage,
               y.year_id             AS year_id,
               y.name                AS year_label,
               ks.name              AS key_stage_name
    """, cid=cluster_id)
    row = r.single()
    ctx["domain"] = dict(row) if row else {}

    year_id = ctx["domain"].get("year_id")

    # --year flag overrides the domain anchor (use when cluster is KS-level but
    # you're teaching it in a specific year, e.g. SC-KS2 → Y5 not Y3)
    if year_override:
        ctx["domain"]["year_id"] = year_override
        ctx["domain"]["year_override"] = True
        year_id = year_override

    # ── 4. All clusters in this domain (for sequencing) ───────────────────────
    domain_id = ctx["domain"].get("domain_id")
    if domain_id:
        r = session.run("""
            MATCH (d:Domain {domain_id: $did})-[:HAS_CLUSTER]->(cc:ConceptCluster)
            OPTIONAL MATCH (cc)-[:SEQUENCED_AFTER]->(prev:ConceptCluster)
            RETURN cc.cluster_id    AS cluster_id,
                   cc.cluster_name  AS cluster_name,
                   cc.cluster_type  AS cluster_type,
                   prev.cluster_id  AS after_id
            ORDER BY cc.cluster_id
        """, did=domain_id)
        ctx["domain_clusters"] = [dict(r) for r in r]

    # ── 5. Previous cluster in sequence ──────────────────────────────────────
    r = session.run("""
        MATCH (cc:ConceptCluster {cluster_id: $cid})-[:SEQUENCED_AFTER]->(prev:ConceptCluster)
        RETURN prev.cluster_id    AS cluster_id,
               prev.cluster_name  AS cluster_name,
               prev.cluster_type  AS cluster_type
    """, cid=cluster_id)
    ctx["previous_cluster"] = dict(r.single()) if r.peek() else None

    # ── 6. Next cluster(s) in sequence ───────────────────────────────────────
    r = session.run("""
        MATCH (next:ConceptCluster)-[:SEQUENCED_AFTER]->(cc:ConceptCluster {cluster_id: $cid})
        RETURN next.cluster_id    AS cluster_id,
               next.cluster_name  AS cluster_name,
               next.cluster_type  AS cluster_type
        ORDER BY next.cluster_id
    """, cid=cluster_id)
    ctx["next_clusters"] = [dict(r) for r in r]

    # ── 7. Prerequisite concepts (what pupils must already know) ──────────────
    r = session.run("""
        MATCH (cc:ConceptCluster {cluster_id: $cid})-[:GROUPS]->(c:Concept)
              <-[rel:PREREQUISITE_OF]-(prereq:Concept)
        WHERE NOT (cc)-[:GROUPS]->(prereq)
        OPTIONAL MATCH (prereq_d:Domain)-[:HAS_CONCEPT]->(prereq)
        RETURN DISTINCT prereq.concept_id   AS concept_id,
               prereq.concept_name          AS concept_name,
               prereq_d.domain_name         AS from_domain,
               prereq_d.domain_id           AS from_domain_id,
               rel.relationship_type        AS rel_type,
               rel.strength                 AS strength,
               rel.rationale                AS rationale
        ORDER BY prereq.concept_id
    """, cid=cluster_id)
    ctx["prerequisite_concepts"] = [dict(r) for r in r]

    # ── 8. Learner profile — only if year_id is known ─────────────────────────
    if year_id:
        # ContentGuideline
        r = session.run("""
            MATCH (y:Year {year_id: $yid})-[:HAS_CONTENT_GUIDELINE]->(cg:ContentGuideline)
            RETURN cg.reading_level_description  AS reading_level_description,
                   cg.lexile_min                 AS lexile_min,
                   cg.lexile_max                 AS lexile_max,
                   cg.flesch_kincaid_grade_max   AS flesch_kincaid_grade_max,
                   cg.max_sentence_length_words  AS max_sentence_length_words,
                   cg.avg_sentence_length_words  AS avg_sentence_length_words,
                   cg.vocabulary_level           AS vocabulary_level,
                   cg.academic_vocabulary_ok     AS academic_vocabulary_ok,
                   cg.tts_required               AS tts_required,
                   cg.agent_content_prompt       AS agent_content_prompt
        """, yid=year_id)
        row = r.single()
        ctx["content_guideline"] = dict(row) if row else {}

        # PedagogyProfile
        r = session.run("""
            MATCH (y:Year {year_id: $yid})-[:HAS_PEDAGOGY_PROFILE]->(pp:PedagogyProfile)
            OPTIONAL MATCH (pp)-[:USES_TECHNIQUE]->(pt:PedagogyTechnique)
            OPTIONAL MATCH (pp)-[:INTRODUCES_TECHNIQUE]->(intro_pt:PedagogyTechnique)
            RETURN pp.session_length_min_minutes    AS session_length_min,
                   pp.session_length_max_minutes    AS session_length_max,
                   pp.hint_tiers_max                AS hint_tiers_max,
                   pp.productive_failure_appropriate AS productive_failure_appropriate,
                   pp.scaffolding_level             AS scaffolding_level,
                   pp.session_sequence              AS session_sequence,
                   pp.desirable_difficulties        AS desirable_difficulties,
                   pp.spacing_interval_days_min     AS spacing_interval_days_min,
                   pp.spacing_interval_days_max     AS spacing_interval_days_max,
                   pp.agent_pedagogy_prompt         AS agent_pedagogy_prompt,
                   collect(DISTINCT pt.name)       AS active_techniques,
                   collect(DISTINCT intro_pt.name) AS introduced_techniques
        """, yid=year_id)
        row = r.single()
        ctx["pedagogy_profile"] = dict(row) if row else {}

        # FeedbackProfile
        r = session.run("""
            MATCH (y:Year {year_id: $yid})-[:HAS_FEEDBACK_PROFILE]->(fp:FeedbackProfile)
            RETURN fp.feedback_style                AS feedback_style,
                   fp.ai_tone                       AS ai_tone,
                   fp.gamification_safe             AS gamification_safe,
                   fp.progress_bars_safe            AS progress_bars_safe,
                   fp.leaderboards_safe             AS leaderboards_safe,
                   fp.badge_systems_safe            AS badge_systems_safe,
                   fp.unexpected_delight_safe       AS unexpected_delight_safe,
                   fp.delight_frequency             AS delight_frequency,
                   fp.counter_misconceptions_explicit AS counter_misconceptions_explicit,
                   fp.metacognitive_reflection      AS metacognitive_reflection,
                   fp.feedback_example_correct      AS feedback_example_correct,
                   fp.feedback_example_incorrect    AS feedback_example_incorrect,
                   fp.avoid_phrases                 AS avoid_phrases,
                   fp.agent_feedback_prompt         AS agent_feedback_prompt
        """, yid=year_id)
        row = r.single()
        ctx["feedback_profile"] = dict(row) if row else {}

        # InteractionTypes (primary and secondary)
        r = session.run("""
            MATCH (y:Year {year_id: $yid})-[rel:SUPPORTS_INTERACTION]->(it:InteractionType)
            RETURN it.interaction_id     AS interaction_id,
                   it.name              AS name,
                   it.category          AS category,
                   it.agent_prompt      AS agent_prompt,
                   it.ui_notes          AS ui_notes,
                   it.requires_literacy AS requires_literacy,
                   it.requires_numeracy AS requires_numeracy,
                   it.subject_affinity  AS subject_affinity,
                   rel.primary          AS is_primary
            ORDER BY rel.primary DESC, it.category, it.name
        """, yid=year_id)
        ctx["interaction_types"] = [dict(r) for r in r]

    else:
        ctx["content_guideline"] = {}
        ctx["pedagogy_profile"] = {}
        ctx["feedback_profile"] = {}
        ctx["interaction_types"] = []

    # ── 9. ThinkingLens options for this cluster (ordered by rank) ───────────
    key_stage = ctx["domain"].get("key_stage")
    r = session.run("""
        MATCH (cc:ConceptCluster {cluster_id: $cid})-[rel:APPLIES_LENS]->(tl:ThinkingLens)
        OPTIONAL MATCH (tl)-[pf:PROMPT_FOR]->(ks:KeyStage {key_stage_id: $ks})
        RETURN tl.lens_id       AS lens_id,
               tl.lens_name     AS lens_name,
               tl.description   AS description,
               tl.key_question  AS key_question,
               coalesce(pf.agent_prompt, tl.agent_prompt) AS agent_prompt,
               pf.question_stems AS question_stems,
               rel.rank         AS rank,
               rel.rationale    AS mapping_rationale
        ORDER BY rel.rank
    """, cid=cluster_id, ks=key_stage)
    ctx["thinking_lenses"] = [dict(row) for row in r]

    # ── 10. Topic suggestions that deliver concepts in this cluster ──────────
    r = session.run("""
        MATCH (cc:ConceptCluster {cluster_id: $cid})-[:GROUPS]->(c:Concept)
              <-[:DELIVERS_VIA]-(ts)
        WITH ts, labels(ts)[0] AS label,
             collect(DISTINCT c.concept_id) AS concept_ids
        OPTIONAL MATCH (ts)-[:USES_TEMPLATE]->(vt:VehicleTemplate)
        WITH ts, label, concept_ids, collect(DISTINCT vt.template_type) AS templates
        RETURN label, ts.name AS name,
               coalesce(ts.study_id, ts.enquiry_id, ts.unit_id, ts.suggestion_id) AS id,
               ts.key_stage AS ks,
               ts.curriculum_status AS status,
               ts.pedagogical_rationale AS rationale,
               properties(ts) AS ts_props,
               concept_ids, templates
        ORDER BY label, ts.key_stage, ts.name
    """, cid=cluster_id)
    ctx["topic_suggestions"] = [dict(row) for row in r]

    # ── 11. Subject reference nodes linked from topic suggestions ────────────
    # Return all node AND relationship properties so nothing is lost
    r = session.run("""
        MATCH (cc:ConceptCluster {cluster_id: $cid})-[:GROUPS]->(c:Concept)
              <-[:DELIVERS_VIA]-(ts)-[rel]->(ref)
        WHERE ref.display_category = 'Subject Reference'
        RETURN DISTINCT labels(ts)[0] AS source_label,
               coalesce(ts.study_id, ts.enquiry_id, ts.unit_id, ts.suggestion_id) AS source_id,
               ts.name AS source_name,
               type(rel) AS rel_type,
               properties(rel) AS rel_props,
               labels(ref)[0] AS ref_label,
               ref.name AS ref_name,
               properties(ref) AS ref_props
        ORDER BY source_id, type(rel), ref.name
    """, cid=cluster_id)
    ctx["subject_references"] = [dict(row) for row in r]

    # ── 12. Cross-curricular links from topic suggestions ────────────────────
    r = session.run("""
        MATCH (cc:ConceptCluster {cluster_id: $cid})-[:GROUPS]->(c:Concept)
              <-[:DELIVERS_VIA]-(ts)-[r:CROSS_CURRICULAR]->(ts2)
        RETURN DISTINCT
               coalesce(ts.study_id, ts.enquiry_id, ts.unit_id, ts.suggestion_id) AS source_id,
               ts.name AS source_name, labels(ts)[0] AS source_label,
               r.hook AS hook, r.strength AS strength,
               coalesce(ts2.study_id, ts2.enquiry_id, ts2.unit_id, ts2.suggestion_id) AS target_id,
               ts2.name AS target_name, labels(ts2)[0] AS target_label
        ORDER BY source_id
    """, cid=cluster_id)
    ctx["cross_curricular_links"] = [dict(row) for row in r]

    # ── 13. VehicleTemplate details (with age-banded prompts) ────────────────
    r = session.run("""
        MATCH (cc:ConceptCluster {cluster_id: $cid})-[:GROUPS]->(c:Concept)
              <-[:DELIVERS_VIA]-(ts)-[:USES_TEMPLATE]->(vt:VehicleTemplate)
        OPTIONAL MATCH (vt)-[tf:TEMPLATE_FOR]->(ks:KeyStage {key_stage_id: $ks})
        RETURN DISTINCT vt.template_id AS template_id, vt.template_type AS template_type,
               vt.name AS name, vt.description AS description,
               properties(vt) AS vt_props,
               tf.agent_prompt AS agent_prompt,
               tf.question_stems AS question_stems
        ORDER BY vt.template_type
    """, cid=cluster_id, ks=key_stage)
    ctx["vehicle_templates"] = [dict(row) for row in r]

    # ── 14. Source documents (provenance / curriculum authority) ────────────
    r = session.run("""
        MATCH (cc:ConceptCluster {cluster_id: $cid})-[:GROUPS]->(c:Concept)
              -[:SOURCED_FROM]->(sd:SourceDocument)
        RETURN DISTINCT sd.document_id AS doc_id, sd.title AS title,
               sd.dfe_reference AS dfe_ref, sd.url AS url
        ORDER BY sd.document_id
    """, cid=cluster_id)
    ctx["source_documents"] = [dict(row) for row in r]

    return ctx


def render_markdown(ctx):
    """Render a comprehensive Markdown briefing from the context dict."""
    c = ctx["cluster"]
    d = ctx["domain"]
    cg = ctx.get("content_guideline", {})
    pp = ctx.get("pedagogy_profile", {})
    fp = ctx.get("feedback_profile", {})
    concepts = ctx.get("concepts", [])
    difficulty_levels = ctx.get("difficulty_levels", {})
    representation_stages = ctx.get("representation_stages", {})
    prereqs = ctx.get("prerequisite_concepts", [])
    interactions = ctx.get("interaction_types", [])
    domain_clusters = ctx.get("domain_clusters", [])
    thinking_lenses = ctx.get("thinking_lenses", [])

    lines = []

    lines.append(f"# Lesson Context: {c['cluster_name']}")
    lines.append("")
    lines.append(f"> **Cluster**: `{c['cluster_id']}` | Type: {c['cluster_type']} | "
                 f"{'⭐ Keystone cluster' if c['is_keystone_cluster'] else ''} "
                 f"{'✓ Curated' if c.get('is_curated') else '⚙ Algorithmic'}")
    lines.append("")

    # ── Overview ──
    lines.append("## Overview")
    lines.append("")
    lines.append(f"- **Subject**: {d.get('subject', '—')}")
    year_display = d.get('year_id', d.get('key_stage', '—'))
    if d.get('year_override'):
        year_display += " *(year override — learner profile reflects this year, not domain anchor)*"
    lines.append(f"- **Year group**: {year_display} ({d.get('year_label', '')})")
    lines.append(f"- **Domain**: {d.get('domain_name', '—')} (`{d.get('domain_id', '—')}`)")
    lines.append(f"- **Estimated teaching time**: {c.get('lesson_count', '—')} lessons "
                 f"(~{c.get('teaching_weeks', '—')} weeks)")
    if c.get("inspired_by"):
        lines.append(f"- **Modelled on**: {c['inspired_by']}")
    lines.append("")
    if c.get("rationale"):
        lines.append("### Pedagogical rationale")
        lines.append("")
        lines.append(c["rationale"])
        lines.append("")

    # ── Curriculum context ──
    if d.get("curriculum_context"):
        lines.append("## Curriculum context")
        lines.append("")
        lines.append(d["curriculum_context"])
        lines.append("")

    # ── Domain progression ──
    if domain_clusters:
        lines.append("## Domain progression")
        lines.append("")
        lines.append("All clusters in this domain (in sequence):")
        lines.append("")
        for cl in domain_clusters:
            marker = "**→ THIS CLUSTER**" if cl["cluster_id"] == c["cluster_id"] else ""
            lines.append(f"- `{cl['cluster_id']}` [{cl['cluster_type']}] {cl['cluster_name']} {marker}")
        lines.append("")
    prev = ctx.get("previous_cluster")
    nexts = ctx.get("next_clusters", [])
    if prev:
        lines.append(f"**Comes after**: `{prev['cluster_id']}` — {prev['cluster_name']}")
        lines.append("")
    if nexts:
        for n in nexts:
            lines.append(f"**Leads to**: `{n['cluster_id']}` — {n['cluster_name']}")
        lines.append("")

    # ── ThinkingLens options ──
    if thinking_lenses:
        lines.append("## Thinking lenses")
        lines.append("")
        lines.append("*The following lenses apply to this cluster. Each is a valid framing — "
                     "choose the one that fits your lesson angle.*")
        lines.append("")
        for tl in thinking_lenses:
            primary = " *(recommended)*" if tl["rank"] == 1 else ""
            lines.append(f"### {tl['lens_name']}{primary}")
            lines.append("")
            lines.append(f"*{tl.get('description', '')}*")
            lines.append("")
            if tl.get("mapping_rationale"):
                lines.append(f"**Why this lens fits:** {tl['mapping_rationale']}")
                lines.append("")
            if tl.get("key_question"):
                lines.append(f"> **Key question for pupils:** _{tl['key_question']}_")
                lines.append("")
            if tl.get("agent_prompt"):
                lines.append(f"> **AI instruction:** {tl['agent_prompt']}")
                lines.append("")
            stems = tl.get("question_stems")
            if stems:
                lines.append("**Question stems:**")
                for stem in stems:
                    lines.append(f"- {stem}")
            lines.append("")

    # ── Prerequisites ──
    if prereqs:
        lines.append("## Prerequisite knowledge")
        lines.append("")
        lines.append("Pupils should already be able to:")
        lines.append("")
        for p in prereqs:
            extras = []
            if p.get('rel_type'):
                extras.append(p['rel_type'])
            if p.get('strength'):
                extras.append(f"strength: {p['strength']}")
            extra_str = f" [{', '.join(extras)}]" if extras else ""
            lines.append(f"- **{p['concept_name']}** "
                         f"(from `{p.get('from_domain_id', '')}` — {p.get('from_domain', '')}){extra_str}")
            if p.get('rationale'):
                lines.append(f"  Rationale: {p['rationale']}")
        lines.append("")

    # ── Concepts ──
    lines.append(f"## Concepts in this cluster ({len(concepts)})")
    lines.append("")
    for c_node in concepts:
        keystone = " ⭐ **keystone**" if c_node["is_keystone"] else ""
        lines.append(f"### {c_node['concept_name']}{keystone}")
        lines.append(f"*`{c_node['concept_id']}` · {c_node['concept_type']} · "
                     f"weight {c_node['teaching_weight']}*")
        lines.append("")
        if c_node.get("description"):
            lines.append(c_node["description"])
            lines.append("")
        if c_node.get("teaching_guidance"):
            lines.append(f"**Teaching guidance:** {c_node['teaching_guidance']}")
            lines.append("")
        if c_node.get("key_vocabulary"):
            lines.append(f"**Key vocabulary:** {c_node['key_vocabulary']}")
            lines.append("")
        if c_node.get("common_misconceptions"):
            lines.append(f"**Common misconceptions:** {c_node['common_misconceptions']}")
            lines.append("")
        # Difficulty levels (if present for this concept)
        dl_list = difficulty_levels.get(c_node["concept_id"], [])
        if dl_list:
            lines.append("**Difficulty levels:**")
            for dl in dl_list:
                label_display = dl["label"].replace("_", " ").title()
                lines.append(f"{dl['level']}. **{label_display}**: {dl['description']}"
                             f" — *\"{dl['example_task']}\"*")
            lines.append("")
        # Representation stages (CPA — if present for this concept)
        rs_list = representation_stages.get(c_node["concept_id"], [])
        if rs_list:
            lines.append("**CPA stages (Concrete → Pictorial → Abstract):**")
            for rs in rs_list:
                lines.append(f"{rs['stage_number']}. **{rs['stage'].title()}**: {rs['description']}")
                if rs.get("resources"):
                    lines.append(f"   Resources: {', '.join(rs['resources'])}")
                if rs.get("transition_cue"):
                    lines.append(f"   *Transition cue:* {rs['transition_cue']}")
            lines.append("")

    # ── Topic Suggestions ──
    SKIP_TS_PROPS = {"display_category", "display_color", "display_icon", "display_size",
                     "name", "key_stage", "curriculum_status", "pedagogical_rationale",
                     "study_id", "enquiry_id", "unit_id", "suggestion_id", "suggestion_type",
                     "domain_ids", "source_concept_ids"}
    topic_suggestions = ctx.get("topic_suggestions", [])
    if topic_suggestions:
        lines.append(f"## Topic suggestions ({len(topic_suggestions)})")
        lines.append("")
        lines.append("Studies, enquiries, and units that deliver concepts in this cluster:")
        lines.append("")
        for ts in topic_suggestions:
            status_flag = f" [{ts['status']}]" if ts.get('status') else ""
            lines.append(f"### {ts['id']} — {ts['name']}{status_flag}")
            lines.append(f"*{ts['label']} · KS: {ts['ks']} · Templates: {', '.join(ts['templates'])}*")
            lines.append("")
            if ts.get('concept_ids'):
                lines.append(f"Delivers concepts: {', '.join(ts['concept_ids'])}")
            if ts.get('rationale'):
                lines.append(f"\n**Rationale:** {ts['rationale']}")
            # Dump all remaining subject-specific properties
            props = ts.get('ts_props') or {}
            for k, v in sorted(props.items()):
                if k in SKIP_TS_PROPS or v is None or v == "" or v == []:
                    continue
                if isinstance(v, list):
                    v = ", ".join(str(x) for x in v)
                lines.append(f"- **{k}**: {v}")
            lines.append("")

    # ── Subject References ──
    SKIP_PROPS = {"display_category", "display_color", "display_icon", "display_size", "name"}
    subject_refs = ctx.get("subject_references", [])
    if subject_refs:
        lines.append(f"## Subject reference nodes ({len(subject_refs)})")
        lines.append("")
        by_source = {}
        for sr in subject_refs:
            by_source.setdefault(sr['source_id'], []).append(sr)
        for source_id, refs in by_source.items():
            source_name = refs[0]['source_name']
            lines.append(f"**{source_id}** ({source_name}):")
            for rn in refs:
                lines.append(f"\n  **[{rn['rel_type']}] {rn['ref_label']}: {rn['ref_name']}**")
                # Relationship properties (e.g. FOREGROUNDS.ks_guidance, IN_GENRE.role)
                rel_props = rn.get('rel_props') or {}
                for k, v in sorted(rel_props.items()):
                    if v is None or v == "" or v == []:
                        continue
                    if isinstance(v, list):
                        v = ", ".join(str(x) for x in v)
                    lines.append(f"  - _{k}_: {v}")
                # Node properties
                props = rn.get('ref_props') or {}
                for k, v in sorted(props.items()):
                    if k in SKIP_PROPS or v is None or v == "" or v == []:
                        continue
                    if isinstance(v, list):
                        v = ", ".join(str(x) for x in v)
                    lines.append(f"  - {k}: {v}")
            lines.append("")

    # ── Cross-curricular links ──
    cross_links = ctx.get("cross_curricular_links", [])
    if cross_links:
        lines.append(f"## Cross-curricular links ({len(cross_links)})")
        lines.append("")
        for cl in cross_links:
            strength_flag = f" [{cl['strength']}]" if cl.get('strength') else ""
            lines.append(f"- **{cl['source_name']}** ({cl['source_label']}) → "
                         f"**{cl['target_name']}** ({cl['target_label']}){strength_flag}")
            if cl.get('hook'):
                lines.append(f"  Hook: {cl['hook']}")
        lines.append("")

    # ── Vehicle Templates ──
    SKIP_VT_PROPS = {"display_category", "display_color", "display_icon", "display_size",
                     "name", "template_id", "template_type", "description"}
    vehicle_templates = ctx.get("vehicle_templates", [])
    if vehicle_templates:
        lines.append(f"## Vehicle templates ({len(vehicle_templates)})")
        lines.append("")
        for vt in vehicle_templates:
            lines.append(f"### {vt['template_type']} — {vt['name']}")
            if vt.get('description'):
                lines.append(f"{vt['description']}")
            if vt.get('agent_prompt'):
                lines.append(f"\n> **Agent prompt:** {vt['agent_prompt']}")
            stems = vt.get('question_stems')
            if stems:
                if isinstance(stems, list):
                    lines.append(f"**Question stems:** {', '.join(stems)}")
                else:
                    lines.append(f"**Question stems:** {stems}")
            # Dump remaining VT node properties
            props = vt.get('vt_props') or {}
            for k, v in sorted(props.items()):
                if k in SKIP_VT_PROPS or v is None or v == "" or v == []:
                    continue
                if isinstance(v, list):
                    v = ", ".join(str(x) for x in v)
                lines.append(f"- {k}: {v}")
            lines.append("")

    # ── Source Documents ──
    source_docs = ctx.get("source_documents", [])
    if source_docs:
        lines.append("## Source documents")
        lines.append("")
        for sd in source_docs:
            lines.append(f"- **{sd['title']}**")
            if sd.get('dfe_ref'):
                lines.append(f"  DfE reference: {sd['dfe_ref']}")
            if sd.get('url'):
                lines.append(f"  URL: {sd['url']}")
        lines.append("")

    # ── Learner profile ──
    lines.append("---")
    lines.append("")
    lines.append("## Learner profile")
    lines.append("")

    if cg:
        lines.append("### Content & language guidelines")
        lines.append("")
        lines.append(f"- **Reading level**: {cg.get('reading_level_description', '—')}")
        if cg.get("lexile_min") or cg.get("lexile_max"):
            lines.append(f"- **Lexile range**: {cg.get('lexile_min', '?')}–{cg.get('lexile_max', '?')}L")
        if cg.get("flesch_kincaid_grade_max"):
            lines.append(f"- **FK grade max**: {cg['flesch_kincaid_grade_max']}")
        lines.append(f"- **Max sentence length**: {cg.get('max_sentence_length_words', '—')} words")
        lines.append(f"- **TTS required**: {'Yes' if cg.get('tts_required') else 'No'}")
        lines.append(f"- **Academic vocabulary**: {'OK' if cg.get('academic_vocabulary_ok') else 'Avoid'}")
        if cg.get("agent_content_prompt"):
            lines.append("")
            lines.append(f"> **AI content instruction**: {cg['agent_content_prompt']}")
        lines.append("")

    if pp:
        lines.append("### Pedagogy profile")
        lines.append("")
        lines.append(f"- **Session length**: {pp.get('session_length_min', '—')}–"
                     f"{pp.get('session_length_max', '—')} minutes")
        lines.append(f"- **Scaffolding**: {pp.get('scaffolding_level', '—')}")
        lines.append(f"- **Productive failure**: "
                     f"{'Appropriate ✓' if pp.get('productive_failure_appropriate') else 'Not yet — worked examples first'}")
        lines.append(f"- **Hint tiers**: max {pp.get('hint_tiers_max', '—')}")
        lines.append(f"- **Spacing interval**: {pp.get('spacing_interval_days_min', '—')}–"
                     f"{pp.get('spacing_interval_days_max', '—')} days")

        session_seq = pp.get("session_sequence")
        if session_seq:
            if isinstance(session_seq, str):
                try:
                    session_seq = json.loads(session_seq)
                except Exception:
                    pass
            if isinstance(session_seq, list):
                lines.append(f"- **Session sequence**: {' → '.join(session_seq)}")

        difficulties = pp.get("desirable_difficulties")
        if difficulties:
            if isinstance(difficulties, str):
                try:
                    difficulties = json.loads(difficulties)
                except Exception:
                    pass
            if isinstance(difficulties, list):
                lines.append(f"- **Active desirable difficulties**: {', '.join(difficulties)}")

        if pp.get("active_techniques"):
            lines.append(f"- **Pedagogy techniques in use**: "
                         f"{', '.join(t for t in pp['active_techniques'] if t)}")
        if pp.get("introduced_techniques"):
            lines.append(f"- **Techniques introduced this year**: "
                         f"{', '.join(t for t in pp['introduced_techniques'] if t)}")
        if pp.get("agent_pedagogy_prompt"):
            lines.append("")
            lines.append(f"> **AI pedagogy instruction**: {pp['agent_pedagogy_prompt']}")
        lines.append("")

    if fp:
        lines.append("### Feedback profile")
        lines.append("")
        lines.append(f"- **Style**: {fp.get('feedback_style', '—')}")
        lines.append(f"- **AI tone**: {fp.get('ai_tone', '—')}")
        lines.append(f"- **Gamification**: {'Safe' if fp.get('gamification_safe') else '⚠ Not safe — avoid'}")
        lines.append(f"- **Unexpected delight**: {'Safe ✓' if fp.get('unexpected_delight_safe') else 'Not safe'} "
                     f"({fp.get('delight_frequency', '—')})")
        lines.append(f"- **Explicit misconception correction**: "
                     f"{'Yes ✓' if fp.get('counter_misconceptions_explicit') else 'Keep implicit'}")
        lines.append(f"- **Metacognitive reflection**: "
                     f"{'Yes ✓' if fp.get('metacognitive_reflection') else 'Not yet'}")
        if fp.get("feedback_example_correct"):
            lines.append(f"- **Example (correct)**: \"{fp['feedback_example_correct']}\"")
        if fp.get("feedback_example_incorrect"):
            lines.append(f"- **Example (incorrect)**: \"{fp['feedback_example_incorrect']}\"")
        avoid = fp.get("avoid_phrases")
        if avoid:
            if isinstance(avoid, str):
                try:
                    avoid = json.loads(avoid)
                except Exception:
                    pass
            if isinstance(avoid, list):
                lines.append(f"- **Avoid phrases**: {', '.join(f'\"{p}\"' for p in avoid[:5])}")
        if fp.get("agent_feedback_prompt"):
            lines.append("")
            lines.append(f"> **AI feedback instruction**: {fp['agent_feedback_prompt']}")
        lines.append("")

    if interactions:
        lines.append("### Interaction types available")
        lines.append("")
        primary = [i for i in interactions if i.get("is_primary")]
        secondary = [i for i in interactions if not i.get("is_primary")]

        if primary:
            lines.append("**Primary (preferred):**")
            for i in primary:
                lines.append(f"- **{i['name']}** (`{i['interaction_id']}`, {i['category']})")
                if i.get("agent_prompt"):
                    lines.append(f"  > {i['agent_prompt']}")
            lines.append("")
        if secondary:
            lines.append("**Secondary (available):**")
            for i in secondary:
                lines.append(f"- {i['name']} (`{i['interaction_id']}`, {i['category']})")
            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Query lesson context from Neo4j")
    parser.add_argument("cluster_id", help="ConceptCluster ID e.g. MA-Y3-D001-CL001")
    parser.add_argument("--output", help="Directory to write context.json and context.md")
    parser.add_argument("--year", help="Override year group for learner profile (e.g. Y5). "
                                       "Use when a KS-level domain anchors to the wrong year.")
    args = parser.parse_args()

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    try:
        with driver.session() as session:
            ctx = query_context(session, args.cluster_id, year_override=args.year)
    finally:
        driver.close()

    md = render_markdown(ctx)

    if args.output:
        out_dir = Path(args.output)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "context.json").write_text(json.dumps(ctx, indent=2))
        (out_dir / "context.md").write_text(md)
        print(f"Written to {out_dir}/context.json and context.md")
    else:
        print(md)


if __name__ == "__main__":
    main()

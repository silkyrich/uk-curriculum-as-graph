# Neo4j Bloom Perspectives

**Hybrid styling approach**: Display properties stored **in the graph** + Bloom perspectives for exploration.

## Why This Approach?

✅ **Styling is version controlled** (committed to git)
✅ **Portable across Neo4j instances** (travels with data)
✅ **Works with Bloom AND custom visualizations** (D3.js, Cytoscape, exports)
✅ **No lock-in to Bloom** (properties work anywhere)

## Display Properties (In Graph)

Every node has these properties:
- `display_color`: Hex color (e.g., `#3B82F6`)
- `display_icon`: Material Design icon name (e.g., `lightbulb_outline`)
- `display_category`: High-level category (e.g., `UK Curriculum`, `CASE Standards`)
- `name`: Standard caption property (all 3,252 nodes)

**Added by**: `scripts/add_display_properties.py`
**Version controlled**: `migrations/add_display_properties.cypher`

---

## Color Scheme

### UK Curriculum (Blues & Purples)
- **Concept**: #3B82F6 (Blue-500) — 💡 lightbulb_outline
- **Domain**: #8B5CF6 (Violet-500) — 📁 folder
- **Objective**: #10B981 (Emerald-500) — 🚩 flag
- **Programme**: #1E3A8A (Blue-900) — 📋 assignment
- **Subject**: #DC2626 (Red-600) — 📖 menu_book
- **Topic**: #7C3AED (Violet-600) — 🗺️ map

### Epistemic Skills (Teals & Greens)
- **WorkingScientifically**: #14B8A6 (Teal-500) — 🔬 science
- **ReadingSkill**: #EC4899 (Pink-500) — 📖 menu_book
- **MathematicalReasoning**: #F59E0B (Amber-500) — 🔢 calculate
- **GeographicalSkill**: #059669 (Emerald-600) — 🌍 public
- **HistoricalThinking**: #92400E (Amber-900) — 📜 history_edu
- **ComputationalThinking**: #4F46E5 (Indigo-600) — 💻 computer

### CASE Standards (Oranges & Browns)
- **Framework**: #EA580C (Orange-600) — 🏛️ account_balance
- **Dimension**: #C2410C (Orange-700) — 📐 view_in_ar
- **Practice**: #0284C7 (Sky-600) — ⚙️ engineering
- **CoreIdea**: #B45309 (Amber-700) — 🎓 school
- **CrosscuttingConcept**: #15803D (Green-700) — 🌐 hub
- **PerformanceExpectation**: #6B7280 (Gray-500) — 📊 assessment

### Assessment (Grays)
- **ContentDomainCode**: #6B7280 (Gray-500) — 🔖 bookmark
- **TestFramework**: #374151 (Gray-700) — 📝 quiz
- **TestPaper**: #4B5563 (Gray-600) — 📄 description

---

## Bloom Perspectives (External)

### 1. `main_perspective.json`
**Complete view** of UK curriculum with CASE comparison layer.

**Features**:
- All node types styled with graph properties
- Relationship coloring by semantic type
- Size nodes by connectivity (`degree * 2`)
- Search phrases for common queries
- Rules for highlighting cross-cutting concepts

**Use for**: General exploration, teaching, presentations

### 2. `comparison_perspective.json`
**Specialized view** for NGSS vs UK curriculum comparison.

**Features**:
- Emphasizes CASE Standards nodes (larger sizes)
- Highlights ALIGNS_TO relationships (dashed, thick)
- Search phrases for 3D model exploration
- Badge for aligned nodes (⟷)

**Use for**: Research, curriculum comparison, policy analysis

---

## How to Import to Bloom

### Option A: Via Bloom UI (Easiest)

1. Go to https://console.neo4j.io
2. Open your database → **"Open with Bloom"**
3. Click **⚙️ Settings** (top right)
4. **Perspectives** → **Import**
5. Upload `main_perspective.json`
6. Click **"Use this perspective"**

### Option B: Via Cypher (Properties Already There!)

The display properties are **already in the graph**, so Bloom will automatically pick them up:

1. Open Bloom
2. Create **New Perspective**
3. Bloom will detect all node labels
4. For each label, set:
   - **Color**: `{display_color}` (references the property)
   - **Icon**: `{display_icon}`
   - **Caption**: `{name}`

### Option C: Manual Configuration

If you prefer to configure manually:

1. Open Bloom → **Create Perspective**
2. **Node Categories**:
   - Add each label (Concept, Domain, Practice, etc.)
   - Set color from table above
   - Set icon from table above
   - Set caption to `{name}`
3. **Relationship Types**:
   - `PREREQUISITE_OF`: Red (#EF4444), thickness 2
   - `ALIGNS_TO`: Orange (#F59E0B), dashed
   - `TEACHES`: Blue (#3B82F6)

---

## Search Phrases

### General Exploration
```
Show me Science for KS2
Prerequisites for fractions
Show UK Curriculum layer
```

### CASE Comparison
```
NGSS 3 dimensions
Show NGSS practices aligned to UK
Performance Expectations using Asking Questions
Compare NGSS to UK science
```

### Custom Cypher
```cypher
// Find most foundational concepts
MATCH (c:Concept)<-[:PREREQUISITE_OF]-(dependent)
RETURN c.name, count(dependent) AS dependents
ORDER BY dependents DESC
LIMIT 10

// NGSS Performance Expectations using all 3 dimensions
MATCH (pe:PerformanceExpectation)-[:USES_PRACTICE]->(p:Practice)
MATCH (pe)-[:USES_CORE_IDEA]->(ci:CoreIdea)
MATCH (pe)-[:USES_CONCEPT]->(ccc:CrosscuttingConcept)
RETURN pe, p, ci, ccc
LIMIT 10
```

---

## Exporting Styled Data

Since display properties are **in the graph**, they export with your data:

```bash
# Neo4j dump (includes display properties)
neo4j-admin dump --database=neo4j --to=curriculum-graph-styled.dump

# CSV export (includes display_color, display_icon columns)
MATCH (n:Concept)
RETURN n.concept_id, n.name, n.display_color, n.display_icon, n.display_category
```

---

## Updating Styles

### Option 1: Modify the migration script
```bash
# Edit scripts/add_display_properties.py
# Change colors/icons in NODE_STYLES dictionary
# Re-run migration
python3 scripts/add_display_properties.py
```

### Option 2: Direct Cypher updates
```cypher
// Change all Concept nodes to a different blue
MATCH (c:Concept)
SET c.display_color = '#60A5FA'  // Blue-400
```

### Option 3: Per-node customization
```cypher
// Highlight a specific important concept
MATCH (c:Concept {concept_id: 'MA-Y3-FRAC-001'})
SET c.display_color = '#FBBF24',  // Amber-400 (highlight)
    c.display_size = 60
```

---

## Next Steps

1. ✅ Display properties added to all 3,252 nodes
2. ✅ Bloom perspectives created and version controlled
3. 🔜 Import perspective to Aura Bloom
4. 🔜 Create custom search phrases for your research questions
5. 🔜 Export styled visualizations for papers/presentations

**Questions?** Check the main README or open an issue.

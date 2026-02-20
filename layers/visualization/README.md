# Visualization Layer

Applies formatting and styling to all nodes in the knowledge graph. This layer runs **last** — after all data layers have been imported.

## What It Does

| Script | Purpose |
|---|---|
| `add_name_properties.py` | Adds `name` property to every node (Neo4j Browser needs this) |
| `add_display_properties.py` | Applies `display_color`, `display_icon`, `display_category`, `display_size` |
| `upload_bloom_perspective.py` | Writes Bloom perspective directly into the database |
| `apply_formatting.py` | Orchestrates all three steps in order |

## Usage

```bash
# Run everything (recommended)
python3 layers/visualization/scripts/apply_formatting.py

# Individual steps
python3 layers/visualization/scripts/add_name_properties.py
python3 layers/visualization/scripts/add_display_properties.py
python3 layers/visualization/scripts/upload_bloom_perspective.py

# Skip Bloom upload (if not using Bloom)
python3 layers/visualization/scripts/apply_formatting.py --skip-perspective
```

## Directory Structure

```
layers/visualization/
├── README.md
├── scripts/
│   ├── apply_formatting.py        ← entry point
│   ├── add_name_properties.py
│   ├── add_display_properties.py
│   └── upload_bloom_perspective.py
└── data/
    ├── perspectives/
    │   └── main_perspective.json  ← Bloom perspective definition
    └── cypher/
        └── add_display_properties.cypher  ← generated, gitignored
```

## Node Styling

All 26 node types have assigned:
- **Color** — Tailwind CSS palette; warm = CASE, cool = UK, teal = Epistemic, gray = Assessment
- **Icon** — Material Design icon name
- **Category** — `"UK Curriculum"`, `"CASE Standards"`, `"Epistemic Skills"`, `"Assessment"`, `"Structure"`
- **Size** — 1–5 scale: 5=root structural, 4=mid, 3=grouping, 2=content, 1=leaf

## Bloom Perspective

The perspective (`data/perspectives/main_perspective.json`) is stored in git and uploaded to the database programmatically. Opening Bloom against this database will automatically show the "UK Curriculum Knowledge Graph" perspective.

To update the perspective: edit the JSON, then run `upload_bloom_perspective.py`.

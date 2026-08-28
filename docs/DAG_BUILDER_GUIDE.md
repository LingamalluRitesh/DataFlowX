# DataFlowX Visual DAG Builder Guide

## 1. Interactive Canvas Overview
The DataFlowX Visual DAG Builder is powered by React Flow with custom node renderers, dynamic input/output ports, drag-and-drop node placement, and real-time topological cycle validation.

## 2. Canvas Node Palette
| Node Type | Icon | Color Accent | Purpose |
| :--- | :--- | :--- | :--- |
| **Extract / Source** | Database | Blue | Ingest data from Postgres, MySQL, Mongo, REST, CSV, Kafka |
| **Quality Check** | ShieldCheck | Emerald | Apply validation suites, quality scoring, row quarantining |
| **Transform** | Layers | Violet | Vectorized transformations (Select, Rename, Filter, Deduplicate) |
| **Aggregate** | BarChart3 | Amber | Group by rollups, sums, counts, averages |
| **Custom SQL** | Code2 | Cyan | ANSI DuckDB / SQLite SQL queries on in-flight DataFrames |
| **Warehouse Load** | HardDrive | Yellow | Load transformed datasets into analytical tables |
| **Alert / Notify** | Bell | Red | Dispatch Slack/Email/Webhook notifications on task events |

## 3. Keyboard Shortcuts & Workflow
- **Add Node**: Click any node template in the left sidebar palette.
- **Connect Ports**: Drag from a source node's right port to a target node's left port.
- **Configure**: Click any node to open the configuration drawer.
- **Run Pipeline**: Click "Save & Execute" to trigger an instant execution with live streaming terminal logs.

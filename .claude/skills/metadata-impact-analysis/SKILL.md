---
name: metadata-impact-analysis
description: Analyze downstream impact before making schema changes. Traces lineage through dbt models and dashboards to identify what breaks if a column is renamed, dropped, or its type changes. Triggers include "impact analysis", "what breaks if", "can I rename", "can I drop", "downstream impact".
---

# Impact Analysis

Analyze the downstream impact of a schema change (rename, drop, type change) on a dbt model column. Traces lineage through OpenMetadata to identify affected models, dashboards, and column references.

## How It Works

Execute steps **sequentially** — complete each step before starting the next. Do NOT fire multiple MCP calls or file reads in parallel.

### Step 1: Parse input
Extract model and column from `$ARGUMENTS`. Accepts:
- `campaign_performance.total_conversions` → specific column
- `campaign_performance` → full table (all columns)
- Natural language like "rename total_conversions from campaign_performance" → extract both

### Step 2: Confirm entity exists
Call `search_metadata` to find the table by name. This returns columns inline so you can confirm the column exists and get the correct FQN. Do NOT call `get_entity_details` at this stage.

### Step 3: Trace downstream lineage
Call `get_entity_lineage` on the confirmed FQN. Collect all downstream nodes (tables, views, dashboards). Present a brief summary to the user before continuing:
> "Found N downstream entities: [list]. Checking column references..."

### Step 4: Check SQL references
Use `Grep` to search for the column name across `dbt/models/` SQL and YAML files. This is a single local search — no MCP calls needed.

### Step 5: Check dashboard impact
If lineage returned dashboard nodes, call `search_metadata` for dashboards. If no dashboards in lineage, skip this step.

### Step 6: Compile report
Combine lineage, SQL grep results, and dashboard data into the output format below. Include ownership from any entity that had it set.

## MCP Tools

- **`get_entity_details`** — Entity by FQN + `entity_type: "table"` or `"dashboard"` (read-only)
- **`get_entity_lineage`** — Downstream dependencies from a given entity (read-only)
- **`search_metadata`** — Fallback search if FQN lookup fails (read-only)

## Reference

**FQN pattern**: `marketing_postgres.postgres.marketing.{model}`
**Mart models**: `campaign_performance`, `daily_summary`, `user_journey`, `channel_attribution`
**dbt SQL**: `dbt/models/marts/{model}.sql`, `dbt/models/intermediate/{model}.sql`

## Output Format

```
## Impact Analysis: {model}.{column}

Change type: rename | drop | type change

### Direct downstream
| Entity | Type | Column references | Owner |
|--------|------|-------------------|-------|
| daily_summary | table | total_conversions (3 refs in SQL) | — |

### Dashboard impact
| Dashboard | Service | Granularity |
|-----------|---------|-------------|
| Agentic Data Modeling Demo | Metabase | dashboard-level only |

### Risk: HIGH | MEDIUM | LOW
- HIGH: dashboard or 2+ downstream models affected
- MEDIUM: 1 downstream model affected
- LOW: no downstream references found

### Recommended actions
1. Rename column in {model}.sql
2. Update references in: daily_summary.sql (lines X, Y, Z)
3. Update _marts.yml descriptions
4. Re-run dbt + ingestion
5. Notify: {owner} (owner of downstream assets)
```

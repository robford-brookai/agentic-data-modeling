---
name: metadata-impact-analysis
description: Analyze downstream impact before making schema changes. Traces lineage through dbt models and dashboards to identify what breaks if a column is renamed, dropped, or its type changes. Triggers include "impact analysis", "what breaks if", "can I rename", "can I drop", "downstream impact".
---

# Impact Analysis

Analyze the downstream impact of a schema change (rename, drop, type change) on a dbt model column. Traces lineage through OpenMetadata to identify affected models, dashboards, and column references.

## How It Works

1. **Parse `$ARGUMENTS`** — Extract model and column from input. Accepts:
   - `campaign_performance.total_conversions` → specific column
   - `campaign_performance` → full table (all columns)
2. **Find the entity** — `get_entity_details` with FQN `marketing_postgres.marketing.public.{model}`, `entity_type: "table"`. Confirm the column exists.
3. **Trace downstream lineage** — `get_entity_lineage` on the same FQN. Collect all downstream nodes: tables, views, dashboards.
4. **Check column references** — For each downstream table, call `get_entity_details` and scan column descriptions and names for references to the target column. Also read the dbt SQL (`dbt/models/**/{downstream_model}.sql`) to find direct SQL references.
5. **Check dashboard impact** — For downstream dashboards/charts, report name + service (Metabase, etc.). Note: Metabase integration links at dashboard level only, not chart-level.
6. **Identify ownership** — For each impacted entity, report the owner (if set) so the user knows who to notify.
7. **Report** — Structured impact report with risk assessment.

## MCP Tools

- **`get_entity_details`** — Entity by FQN + `entity_type: "table"` or `"dashboard"` (read-only)
- **`get_entity_lineage`** — Downstream dependencies from a given entity (read-only)
- **`search_metadata`** — Fallback search if FQN lookup fails (read-only)

## Reference

**FQN pattern**: `marketing_postgres.marketing.public.{model}`
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

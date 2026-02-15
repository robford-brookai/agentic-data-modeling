---
name: enrich-metadata
description: Enrich OpenMetadata entity descriptions with context from your dbt project. Use when adding new models, discovering column nuances, or documenting business logic during development. Triggers include "enrich", "add context to", "document this column", "update metadata for".
---

# Enrich Metadata

Push semantic context from your dbt project into OpenMetadata without leaving your IDE.

## How It Works

1. **Parse the request** — Extract the target (model or model.column) and any explicit context from `$ARGUMENTS`. If no context is provided, default to reading dbt files.
2. **Read dbt context** — Find and read the dbt model SQL file under `dbt/models/` and its corresponding YAML schema file (`_marts.yml`, `_intermediate.yml`, or `_sources.yml`). Extract transformation logic, column definitions, joins, filters, and business rules relevant to the target.
3. **Look up in OpenMetadata** — Call `search_metadata` with the model or table name to find the entity. Then call `get_entity_details` with `entity_type: "table"` and the discovered FQN to get the current description, column list, and tags.
4. **Diff and propose** — Compare what dbt knows vs what OpenMetadata has. For each gap, draft an enriched description. Present the before/after to the user and ask for confirmation before writing.
5. **Patch** — Call `patch_entity` to update. Use JSONPatch format:
   - Table description: `[{"op": "add", "path": "/description", "value": "..."}]`
   - Column description: `[{"op": "add", "path": "/columns/{index}/description", "value": "..."}]`

## Argument Parsing

Three usage patterns:

- `$ARGUMENTS` = `campaign_performance.total_conversions — only counts digital conversions, excludes TV and Radio`
  → Enrich a specific column with explicit context.

- `$ARGUMENTS` = `user_journey`
  → Enrich a full model. Read `dbt/models/**/user_journey.sql` and its schema YAML to auto-generate descriptions for columns that are missing or vague.

- `$ARGUMENTS` = `campaign_performance.total_conversions`
  → Enrich a specific column by deriving context from the SQL and YAML (no explicit context provided).

Parse `$ARGUMENTS` by splitting on ` — ` (space-dash-dash-space). Left side is the target, right side (if present) is explicit context.

Split the target on `.` — first part is the model name, second part (if present) is the column name.

## Finding dbt Files

Use this search order for the model SQL file:
1. `dbt/models/marts/{model_name}.sql`
2. `dbt/models/intermediate/{model_name}.sql`
3. `dbt/models/staging/{model_name}.sql`

For the YAML schema, check the corresponding `_{folder}.yml` file in the same directory (e.g., `_marts.yml`, `_intermediate.yml`, `_sources.yml`).

Also trace upstream: read the SQL to find `{{ ref('...') }}` calls and read those models too, to understand where the data comes from.

## Enrichment Guidelines

When writing descriptions for OpenMetadata, make them AI-readable:

- **State what it is** — "Total count of conversion events attributed to digital marketing channels."
- **State what it includes** — "Includes paid search, social, display, and email channels."
- **State what it excludes** — "Excludes TV, Radio, and organic/direct conversions."
- **State the grain** — "One row per campaign per day."
- **State the source** — "Aggregated from stg_conversions via int_conversion_metrics_by_campaign."
- **Flag edge cases** — "Returns 0 (not NULL) when no conversions exist, via COALESCE."

Keep descriptions under 3 sentences for columns, under 5 sentences for tables. Use plain text — no markdown formatting (OpenMetadata renders plain text in descriptions).

## Output

After patching, confirm:
- Entity name and FQN
- What changed (before → after for each field)
- Remind the user that downstream AI queries now have richer context

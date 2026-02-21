---
name: metadata-ai-readiness
description: Audit and enrich dbt mart models for AI consumption. Checks schema quality, queries the database to discover edge cases, validates OpenMetadata catalog presence, and writes fixes back to dbt YAML. Triggers include "ai readiness", "is this model ready", "checklist for", "enrich", "pre-merge check".
---

# AI Readiness

## How It Works

1. **Parse `$ARGUMENTS`** — Model name (e.g. `user_journey`), `model.column` for single column, or `all`/empty for all 4 marts.
2. **dbt schema checks** — Read `dbt/models/marts/{model}.sql` + `_marts.yml`. Check: model has description, all SQL columns in YAML with descriptions, grain columns have `not_null` + `unique` tests.
3. **Query the database** — Postgres MCP against `localhost:5432`:
   - Shape & grain: `SELECT COUNT(*), COUNT(DISTINCT {grain}) FROM {model}`
   - Column profiling: NULLs, min/max, distinct counts on metrics
   - Edge case discovery: zeros vs NULLs, skewed distributions, date gaps → become `[Known Issues / Caveats]`
   - Build 2-3 example queries for AI agent consumption
4. **OpenMetadata checks** (read-only) — `get_entity_details` with FQN `marketing_postgres.marketing.public.{model}`, `entity_type: "table"`. Check: description, column descriptions, ownership, tags. If entity missing, flag ingestion needed.
5. **Report** — Pass/fail checklist + query guidance. Summarize: passed, auto-fixable, manual-action.
6. **Offer fixes** — Propose changes, confirm with user, edit `_marts.yml`:
   - **Can fix**: missing/thin descriptions (model + columns), missing column YAML entries
   - **Cannot fix** (flag only): missing dbt tests (print snippet), OpenMetadata gaps (ownership, tags → UI action), entity not in catalog → suggest `docker compose --profile ingestion up ingest-postgres ingest-dbt`

## After Fix

- Report what changed in `_marts.yml` (before → after)
- Re-ingest: `docker compose --profile ingestion up ingest-postgres ingest-dbt`
- Validate: `get_entity_details` on the model FQN, confirm updated descriptions on columns, report final state

## MCP Tools

- **Postgres MCP** — Query grain, profile distributions, discover edge cases, build example queries
- **`get_entity_details`** — Entity by FQN + `entity_type: "table"` (read-only)
- **`get_entity_lineage`** — Upstream/downstream dependencies for context (read-only)

## Reference

**Mart models**: `campaign_performance`, `daily_summary`, `user_journey`, `channel_attribution`
**Files**: SQL at `dbt/models/marts/{model}.sql`, YAML at `dbt/models/marts/_marts.yml`
**Upstream**: trace `{{ ref('...') }}` calls in SQL

**Grain map**:
- `campaign_performance` → composite: `campaign_id` + `date`
- `daily_summary` → single: `date`
- `user_journey` → single: `user_id`
- `channel_attribution` → single: `channel`

## Description Format

Plain text with bracketed headers (no markdown — OpenMetadata and dbt YAML render plain text).

**Tables**: `[Business Purpose]` what it answers + why it exists. `[How It's Used]` consumers + decisions. `[Data Grain]` one row = what, source lineage. `[Known Issues / Caveats]` exclusions, NULLs, edge cases.

**Columns**: `[Business Purpose]` what it represents. `[Known Issues / Caveats]` only when real caveats exist — skip otherwise.

## Output Format

Checklist per model with 3 sections: **dbt Schema** (description, columns in YAML, descriptions, grain tests), **OpenMetadata Catalog** (entity exists, descriptions, ownership), **Query Guidance** (grain check, edge cases, example queries). End with `PASS: X/Y | Auto-fixable: N | Manual: N`.

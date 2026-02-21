---
name: metadata-glossary
description: Manage an OpenMetadata glossary derived from dbt models. Parses dbt YAML for column names and descriptions, groups them into business categories, and creates/syncs glossary terms via OpenMetadata MCP. Triggers include "metadata glossary", "create glossary", "business terms", "sync glossary".
---

# Glossary

Manage an OpenMetadata glossary derived from dbt models. Scans dbt YAML files for columns and descriptions, groups terms into business categories, and creates or syncs them via OpenMetadata MCP write tools.

## How It Works

1. **Parse `$ARGUMENTS`** — Determine mode:
   - `audit` (default) — dry-run: scan dbt YAML, show what would be created, no writes
   - `create` — full create: glossary + all category terms + individual terms
   - `sync` — add only missing terms to an existing glossary
2. **Scan dbt YAML** — Read `dbt/models/marts/_marts.yml`, `dbt/models/intermediate/_intermediate.yml`, `dbt/models/staging/_sources.yml`. Extract column names + descriptions from all models.
3. **Group into categories** — Map extracted terms to parent categories:
   - **KPIs**: roas, cpa, ctr, cpc, conversion_rate, budget_utilization
   - **Attribution**: first_touch, last_touch, linear, attributed_conversions
   - **User Journey**: touchpoints, journey_length, user_type, channel_behavior
   - **Campaign Metrics**: spend, impressions, clicks, daily_budget
   - **Conversion Metrics**: conversions, revenue, order_value, converting_users
   - **Session Metrics**: sessions, session_duration, pages_per_session, engaged_sessions
4. **Check existing** — `search_metadata` with `entity_type: "glossary"` to find existing glossary and terms. Also search for each category term to detect what already exists.
5. **Create or sync** — In `create`/`sync` mode:
   - `create_glossary` for the parent glossary ("Marketing Analytics")
   - `create_glossary_term` for each category (as parent terms under the glossary)
   - `create_glossary_term` for each individual term under its category
   - Skip any term that already exists

## Argument Parsing

- `$ARGUMENTS` = `audit` or empty → dry-run, no writes
- `$ARGUMENTS` = `create` → full create from scratch
- `$ARGUMENTS` = `sync` → add missing terms only

## MCP Tools

- **`search_metadata`** (read) — Check for existing glossary and terms before creating
- **`create_glossary`** (write) — Create the parent glossary
- **`create_glossary_term`** (write) — Create category parent terms and individual terms

## MCP Constraints

- **No update/delete via MCP** — Flag outdated terms for manual action in OpenMetadata UI
- **Check before create** — `search_metadata` before each `create_glossary_term` to avoid duplicates
- **`create_glossary` will fail if glossary already exists** — Handle gracefully: catch the error, log it, continue with term sync

## Term Description Format

`{Business definition from dbt column description}. Found in: {model_name(s)}.`

If a term appears in multiple models, list all of them.

## Glossary Structure

```
Marketing Analytics (glossary)
├── KPIs (parent term)
│   ├── ROAS, CPA, CTR, CPC, Conversion Rate, Budget Utilization
├── Attribution
│   ├── First-Touch, Last-Touch, Linear, Attributed Conversions
├── User Journey
│   ├── Touchpoints, Journey Length, User Type, Channel Behavior
├── Campaign Metrics
│   ├── Spend, Impressions, Clicks, Daily Budget
├── Conversion Metrics
│   ├── Conversions, Revenue, Average Order Value, Converting Users
└── Session Metrics
    ├── Sessions, Session Duration, Pages Per Session, Engaged Sessions
```

## Output Format

```
## Marketing Analytics — Glossary Sync

Mode: audit | create | sync

### Summary
- Categories: 6
- Terms to create: 24
- Terms already exist: 0
- Terms needing update: 2 (manual action in OpenMetadata UI)

### Detail
KPIs (parent term)
  ✓ ROAS — created
  ✓ CPA — created
  - CTR — already exists
  ...

### Needs Manual Update
- CPC: dbt description changed since last sync (update in OpenMetadata UI)
```

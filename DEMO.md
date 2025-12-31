# Demo: Agentic Data Modeling with OpenMetadata MCP

This demo showcases how AI agents can interact with your data catalog through the OpenMetadata MCP (Model Context Protocol) server to answer complex data questions, perform impact analysis, and explore data lineage.

## Overview

By connecting Claude Code to OpenMetadata, you can ask natural language questions about your data warehouse and get instant, accurate answers powered by your metadata catalog. This enables:

- **Impact Analysis**: Understand downstream effects before making schema changes
- **Data Discovery**: Find and validate data sources for analysis
- **Lineage Exploration**: Trace data flows from source to dashboard
- **Governance**: Identify data owners and compliance requirements

---

## Use Case 1: Impact Analysis on Schema Changes

Prerequisite: Configure Lineage in OpenMetadata

![Lineage Config](images/demo_openmetadata_lineage.mp4)

**Question:** *"Can you do an impact analysis on changing the column `total_conversions` name of `campaign_performance` model?"*

### The Challenge
Before renaming a column in your data model, you need to understand what will break downstream. Manually tracing dependencies across dbt models, dashboards, and reports is time-consuming and error-prone.

### The Solution
Claude Code uses the OpenMetadata MCP to:
1. Find the `campaign_performance` model
2. Trace its downstream lineage
3. Identify which models and dashboards use the `total_conversions` column
4. Provide a comprehensive impact report

![Impact Analysis](images/demo_claude_code_impact_analysis.png)

### Result
The agent identifies that renaming `total_conversions` will break:
- **1 downstream table**: `daily_summary` (with 3 column references)
- **1 dashboard**: "Agentic Data Modeling Demo" on Metabase

This saves hours of manual investigation and prevents production incidents.

---

## Use Case 2: Data Discovery & Validation

Prerequisite: Update the description on OpenMetadata

![Target Revenue Description](images/demo_metabase_dashboard_target_revenue_description.png)

**Question:** *"Is target revenue chart on Metabase considering TV and Radio?"*

### The Challenge
Business users often ask: "What data is included in this dashboard?" Answering requires understanding chart definitions, SQL queries, and upstream data sources.

### The Solution
Claude Code queries OpenMetadata to:
1. Search for the "Target Revenue" chart in Metabase
2. Read the chart's description and metadata
3. Check upstream lineage to see source tables
4. Validate what data is actually included

![Target Revenue Chart Discovery](images/demo_claude_code_target_revenue.png)

### Result
**Answer: No**, the Target Revenue chart does **NOT** include TV and Radio data. The chart explicitly documents:
> "Note: we don't have information on traditional media (TV, Radio) so breaking down revenue by those channels is not supported."

The chart only uses data from the `campaigns_daily` table, which tracks digital advertising channels.

---

## Use Case 3: Lineage Exploration

**Question:** *"What tables feed into `user_journey` model?"*

### The Challenge
Understanding data lineage is critical for debugging, impact analysis, and data quality investigations. Manually tracing dependencies through dbt DAGs and SQL is tedious.

### The Solution
Claude Code leverages OpenMetadata's lineage tracking to:
1. Find the `user_journey` model
2. Trace upstream dependencies through intermediate models
3. Identify source tables
4. Visualize the complete data flow

![dbt Lineage](images/demo_dbt_lineage.png)

### Result
The `user_journey` model is built from **2 direct upstream tables**:
- `int_user_touchpoint_summary` - User interaction metrics
- `int_user_conversions` - Conversion metrics

Which ultimately trace back to **2 source tables**:
- `attribution_touchpoints` - Multi-touch attribution data
- `conversions` - Purchase events

The agent provides both the immediate dependencies and the full lineage tree, making it easy to understand data provenance.

---

## Use Case 4: Ownership & Governance

Prerequisite: Create a Team and update ownership of the Metabase Dashboard on OpenMetadata

![Dashboard Owner Classification](images/demo_metabase_dashboard_owner_classification.png)

**Question:** *"Who owns the Agentic Data Modeling Demo dashboard?"*

### The Challenge
In large organizations, knowing who owns specific data assets is essential for:
- Getting approval for changes
- Reporting data quality issues
- Understanding compliance requirements

### The Solution
Claude Code queries OpenMetadata for ownership information:

![Owner Query](images/demo_claude_code_owner.png)


### Result
The agent can quickly identify the dashboard owner and any associated teams or governance classifications, streamlining collaboration and accountability.

---

## Lineage Visualization

OpenMetadata provides visual lineage graphs that show the complete data flow from source tables through transformations to final dashboards:

![OpenMetadata Lineage](images/demo_openmetadata_lineage.mp4)

This visualization helps data teams:
- Understand data dependencies
- Debug data quality issues
- Plan schema migrations
- Document data flows for compliance

---

## Key Benefits

### For Data Engineers
- **Instant impact analysis** before making schema changes
- **Automated lineage tracing** without manual SQL parsing
- **Faster debugging** by understanding data flows

### For Analytics Engineers
- **Quick validation** of what data is included in models
- **Easy discovery** of existing assets to avoid duplication
- **Better documentation** through automated metadata queries

### For Data Analysts
- **Self-service data discovery** without asking engineers
- **Confidence in data sources** with full lineage visibility
- **Clear ownership** for data governance questions

### For Data Leaders
- **Reduced production incidents** through impact analysis
- **Faster time-to-insight** with AI-powered metadata search
- **Better data governance** through ownership tracking

---

## Getting Started

Follow the [Quick Start Guide](QUICKSTART.md) to:
1. Set up the demo environment with Docker
2. Ingest metadata into OpenMetadata
3. Connect Claude Code to the OpenMetadata MCP server
4. Start asking questions about your data!

## Example Questions to Try

Once connected, try asking Claude:

- "Show me all tables tagged with PII"
- "What's the grain of the campaign_performance model?"
- "Which dashboards will break if I delete the conversions table?"
- "List all dbt models owned by the marketing team"
- "What columns in the user_journey table come from attribution_touchpoints?"
- "How many BigQuery services are connected?"
- "Find all Tier 1 tables in the marketing database"
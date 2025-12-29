# Agentic Data Modeling with OpenMetadata

A complete, self-contained data analytics stack that automatically:
- Seeds marketing data from S3 into local PostgreSQL
- Runs dbt transformations to create analytics models
- Configures Metabase with pre-loaded database connections and metadata
- Provides unified metadata management via OpenMetadata
- Enables AI-powered data exploration through Claude
### Unified Metadata with OpenMetadata

**OpenMetadata** serves as a unified metadata platform that easily connects different parts of the data engineering cycle. It acts as a central hub to:
- Ingest metadata from data sources, transformation tools (dbt), and visualization layers
- Build end-to-end lineage showing data flow from source tables → dbt models → dashboards
- Centralize documentation, schemas, column descriptions, and relationships
- Track dependencies and understand the downstream impact of changes

This provides a complete view of our data ecosystem, enabling you to explore metadata, view lineage, and understand dependencies across all your data assets.

### AI-Powered Metadata Exploration with Claude MCP Server

Once your data engineering components are connected to OpenMetadata, you can leverage the **Claude MCP (Model Context Protocol) Server** to interact with your metadata using natural language. This enables:

- **Natural Language Queries**: Ask questions about your data architecture in plain English, such as "What tables feed into the campaign_performance model?" or "Show me all dashboards that use user data"
- **Intelligent Exploration**: Discover relationships and dependencies without manually navigating through the UI
- **Documentation Assistance**: Get instant answers about column meanings, data types, and business context
- **Lineage Visualization**: Understand data flows through conversational queries rather than complex graph navigation
- **Impact Analysis**: Quickly identify what would be affected by changes to specific tables or models

The MCP server bridges the gap between your metadata and AI, making it accessible and queryable through natural language, dramatically reducing the time needed to understand and explore your data architecture.

### Architecture

- **Data Source**: PostgreSQL database
- **Transformation**: [dbt](https://www.getdbt.com/) for data modeling and transformation.
- **Visualisation**: [Metabase](https://www.metabase.com/) dashboards for business intelligence
- **Metadata Management**: [OpenMetadata](https://open-metadata.org/) to unify all metadata in one platform (hosted locally)
- **AI Integration**: Claude MCP Server to connect with metadata and enable natural language queries
![Architecture](images/architecture.png)
This setup enables a complete data analytics workflow where:
1. Raw data flows from PostgreSQL
2. dbt transforms and models the data locally
3. Metabase provides interactive dashboards
4. OpenMetadata centralizes metadata from all components via **YAML-based ingestion** (not UI), providing unified lineage and metadata views
5. Claude MCP Server allows AI-powered exploration and querying of the metadata through natural language

**Key Feature:** All OpenMetadata ingestion is configured through YAML files, enabling Infrastructure as Code (IaC) practices. Ingestion runs on-demand using Docker Compose profiles, giving you control over when metadata is synchronized. While OpenMetadata provides a UI for configuration, this project uses YAML files for version control, automation, and reproducibility.

## Quick Start

**Requirements:** Docker and Docker Compose

```bash
cd openmetadata
docker compose up -d
```

This starts:
- PostgreSQL with 148K rows from S3
- dbt (17 analytics models)
- Metabase (http://localhost:3000) (your credentials)
- OpenMetadata (http://localhost:8585) (admin@open-metadata.org/admin)
- Airflow (http://localhost:8080) (admin/admin)

**Total:** 23 tables/views ready to query!

### Metabase Setup

1. Complete setup wizard to create your user at http://localhost:3000
2. Save your email and password on the `.env` variables `METABASE_USERNAME` and `METABASE_PASSWORD`
3. Load pre-configured dashboard: `docker compose up seed-metabase`
4. Visit http://localhost:3000/dashboard/2-agentic-modeling-demo

### OpenMetadata Ingestion

**1. Get JWT Token:**
- Login at http://localhost:8585 (admin/admin)
- Follow this [link](http://localhost:8585/users/admin/access-token) to create your Access Token
- Create token and save to on the `.env` variable `OPENMETADATA_JWT_TOKEN`:

**2. Run ingestion:**
```bash
docker compose --profile ingestion up ingest-postgres ingest-dbt ingest-metabase
```

**What gets ingested on `openmetadata/ingestion-configs/`:**
- **PostgreSQL**: Tables and schemas from `marketing` schema → creates `marketing_postgres` service
- **dbt**: Models and lineage → links to PostgreSQL service (run after PostgreSQL ingestion)
- **Metabase**: Dashboards and charts → completes full lineage: tables → dbt → dashboards


## AI Integration with OpenMetadata MCP with Claude Code

Connect Claude to your metadata using the OpenMetadata MCP Server:

```bash
claude mcp add-json "openmetadata" '{
  "command": "npx",
  "args": [
    "-y", "mcp-remote",
    "http://localhost:8585/mcp",
    "--auth-server-url=http://localhost:8585/mcp",
    "--client-id=openmetadata",
    "--header", "Authorization:${AUTH_HEADER}"
  ],
  "env": {
    "AUTH_HEADER": "Bearer <OPENMETADATA_JWT_TOKEN>"
  }
}'
```

Pass the value of `OPENMETADATA_JWT_TOKEN` you got on OpenMetadata settings. 

Then ask Claude questions like:

- "Can you do an impact on analysis on changing the column `total_conversions` name?"
- "What tables feed into campaign_performance?"
- "Show me the schema for user_journey"
- "Explain the data lineage from sessions to conversions"

## Project Structure

```text
.
├── dbt/                           # dbt project
│   ├── models/
│   │   ├── staging/               
│   │   ├── intermediate/          
│   │   └── marts/                 
│   ├── dbt_project.yml
│   └── profiles.yml               # Postgres connection
├── images/                         # Architecture diagrams
│   └── architecture.png
├── openmetadata/
│   ├── docker-compose.yml         # Main orchestration file
│   └── ingestion-configs/         # YAML-based ingestion configs
│       ├── postgres_ingestion.yaml
│       ├── dbt_ingestion.yaml
│       └── metabase_ingestion.yaml
├── seed/                           # Data seeding scripts
│   ├── Dockerfile
│   ├── config.py                   # Shared configuration
│   ├── requirements.txt
│   ├── s3.py                       # S3 → PostgreSQL seeder
│   ├── metabase.py                 # Metabase pre-configuration
│   └── metabase.sql                # Metabase seed data
└── README.md
```

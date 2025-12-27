# Agentic Data Modeling with OpenMetadata

A complete, self-contained data analytics stack that automatically:
- Seeds marketing data from S3 into local PostgreSQL
- Runs dbt transformations to create analytics models
- Provides unified metadata management via OpenMetadata
- Enables AI-powered data exploration through Claude

### Unified Metadata with OpenMetadata

**OpenMetadata** serves as a unified metadata platform that easily connects different parts of the data engineering cycle. It acts as a central hub to:
- Ingest metadata from data sources, transformation tools (dbt), and visualization layers
- Build end-to-end lineage showing data flow from source tables → dbt models → dashboards
- Centralize documentation, schemas, column descriptions, and relationships
- Track dependencies and understand the downstream impact of changes

This provides a complete view of your data ecosystem, enabling you to explore metadata, view lineage, and understand dependencies across all your data assets.

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

This setup enables a complete data analytics workflow where:
1. Raw data flows from PostgreSQL
2. dbt transforms and models the data locally
3. Metabase provides interactive dashboards
4. OpenMetadata centralizes metadata from all components, providing unified lineage and metadata views
5. Claude MCP Server allows AI-powered exploration and querying of the metadata through natural language

## Quick Start

**Requirements:** Docker & Docker Compose

```bash
cd openmetadata
docker compose -f docker-compose-postgres.yml up -d
```

This  command will:
1. Start PostgreSQL and load 148K rows from public S3 bucket
2. Run dbt to create 17 analytics models (staging, intermediate, marts)
3. Start OpenMetadata at http://localhost:8585

**Total:** 23 tables/views ready for metadata ingestion

## Accessing Services

- **OpenMetadata**: http://localhost:8585 (admin/admin)
- **Metabase**: http://localhost:3000
- **Airflow**: http://localhost:8080 (admin/admin)
- **PostgreSQL**: localhost:5432

### Connecting Metabase to PostgreSQL

When setting up a database connection in Metabase:

1. Go to http://localhost:3000 and complete initial setup
2. Ignore `Sample Database` option and add a PostgreSQL database with these settings:

```
Host: host.docker.internal
Port: 5432
Database name: postgres
Username: postgres
Password: password
```

Select `marketing` as the schema to connect to.

**Important**: Use `host.docker.internal` as the host (not `localhost` or `postgresql`) because Metabase runs inside Docker and needs to access the PostgreSQL container.


## What You Get

**23 ready-to-query tables** in your local PostgreSQL database:

- 6 raw marketing tables (148K rows from S3)
- 17 analytics models (automatically transformed)
- All indexed in OpenMetadata with full lineage

## AI Integration with Claude

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
    "AUTH_HEADER": "Bearer <YOUR-OPENMETADATA-PAT>"
  }
}'
```

Get your Personal Access Token from: **Settings > Users > Access Tokens**

Then ask Claude questions like:
- "What tables feed into campaign_performance?"
- "Show me the schema for user_journey"
- "Explain the data lineage from sessions to conversions"


## Project Structure

```
.
├── dbt/                           # dbt project
│   ├── models/
│   │   ├── staging/               
│   │   ├── intermediate/          
│   │   └── marts/                 
│   ├── dbt_project.yml
│   └── profiles.yml               # Postgres connection
├── openmetadata/
│   ├── docker-compose-postgres.yml 
│   └── seed/                       # S3 → Postgres seeding
│       ├── Dockerfile              
│       ├── requirements.txt        
│       └── seed_data.py            
└── README.md
```

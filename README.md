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
docker compose up -d
```

This command will automatically:
1. Start PostgreSQL and load 148K rows from public S3 bucket
2. Run dbt to create 17 analytics models (staging, intermediate, marts)
3. Start Metabase at http://localhost:3000
4. Start OpenMetadata at http://localhost:8585

**Total:** 23 tables/views ready to query - no manual database setup required!

## Accessing Services

- **OpenMetadata**: http://localhost:8585 (admin/admin)
- **Metabase**: http://localhost:3000
- **Airflow**: http://localhost:8080 (admin/admin)
- **PostgreSQL**: localhost:5432

### Setting up Metabase

1. Complete the setup wizard at <http://localhost:3000> (create admin user)
2. Load pre-configured database connection and dashboard:

   ```bash
   docker compose up seed-metabase
   ```

3. Visit the [Agentic Modeling Demo Dashboard](http://localhost:3000/dashboard/2-agentic-modeling-demo)

The seeder automatically triggers schema sync via Metabase API to populate table metadata immediately.

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

```text
.
├── dbt/                           # dbt project
│   ├── models/
│   │   ├── staging/               
│   │   ├── intermediate/          
│   │   └── marts/                 
│   ├── dbt_project.yml
│   └── profiles.yml               # Postgres connection
├── openmetadata/
│   └── docker-compose.yml
├── seed/                           # Data seeding scripts
│   ├── Dockerfile
│   ├── config.py                   # Shared configuration
│   ├── requirements.txt
│   ├── s3.py                       # S3 → PostgreSQL seeder
│   ├── metabase.py                 # Metabase pre-configuration
│   └── metabase.sql                # Metabase seed data
└── README.md
```

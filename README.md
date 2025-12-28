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
4. OpenMetadata centralizes metadata from all components via **YAML-based ingestion** (not UI), providing unified lineage and metadata views
5. Claude MCP Server allows AI-powered exploration and querying of the metadata through natural language

**Key Feature:** All OpenMetadata ingestion is configured through YAML files, enabling Infrastructure as Code (IaC) practices. Ingestion runs on-demand using Docker Compose profiles, giving you control over when metadata is synchronized. While OpenMetadata provides a UI for configuration, this project uses YAML files for version control, automation, and reproducibility.

## Quick Start

**Requirements:** Docker & Docker Compose

### Step 1: Start the Main Stack

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

### Step 2: Configure Environment Variables

Before running ingestion, set up your environment variables. Create `openmetadata/.env`:

```bash
OPENMETADATA_JWT_TOKEN=your_jwt_token_here
METABASE_USERNAME=your_metabase_username
METABASE_PASSWORD=your_metabase_password
```

**Getting your JWT Token:**
1. Wait for OpenMetadata to start (check http://localhost:8585)
2. Login with admin/admin
3. Go to **Settings → Users → Access Tokens**
4. Create a new token and copy it to your `.env` file

### Step 3: Run Metadata Ingestion

Once the main stack is running and you've set your environment variables, run the ingestion services:

```bash
# Run all ingestion services
docker compose --profile ingestion up ingest-postgres ingest-dbt ingest-metabase

# Or run them individually
docker compose --profile ingestion up ingest-postgres
docker compose --profile ingestion up ingest-dbt
docker compose --profile ingestion up ingest-metabase
```

The ingestion services will:
1. **PostgreSQL ingestion**: Ingest database tables and schemas into OpenMetadata
2. **dbt ingestion**: Ingest dbt models, lineage, and transformations (runs after PostgreSQL ingestion)
3. **Metabase ingestion**: Ingest Metabase dashboards and charts (runs after Metabase is configured)


## Accessing Services

- **OpenMetadata**: http://localhost:8585 (admin@open-metadata.org/admin)
- **Metabase**: http://localhost:3000 (username/password that you created)
- **Airflow**: http://localhost:8080 (admin/admin)
- **PostgreSQL**: localhost:5432

## Ingestion Configuration

All metadata ingestion is configured using **YAML files** instead of the OpenMetadata UI. This approach provides:

- **Version Control**: All configurations are stored in Git
- **Reproducibility**: Easy to recreate the same setup anywhere
- **Infrastructure as Code**: Manage metadata ingestion like any other infrastructure
- **Selective Execution**: Use Docker Compose profiles to run ingestion on-demand

While you can configure ingestion through the OpenMetadata UI, this project uses YAML-based configuration for better DevOps practices.

### Running Ingestion

Ingestion services use Docker Compose profiles and are **not** started automatically. This allows you to:
- Control when ingestion runs
- Re-run ingestion after making changes
- Run specific ingestion services independently

**Run all ingestion services:**
```bash
docker compose --profile ingestion up ingest-postgres ingest-dbt ingest-metabase
```

**Run services individually:**
```bash
# 1. PostgreSQL ingestion (must run first)
docker compose --profile ingestion up ingest-postgres

# 2. dbt ingestion (depends on PostgreSQL ingestion)
docker compose --profile ingestion up ingest-dbt

# 3. Metabase ingestion (depends on Metabase being configured)
docker compose --profile ingestion up ingest-metabase
```

The ingestion services automatically:
- Wait for OpenMetadata server to be ready
- Substitute environment variables in YAML configs
- Execute in the correct dependency order

### Ingestion Configurations

The project includes three YAML-based ingestion configurations:

1. **PostgreSQL Ingestion** (`openmetadata/ingestion-configs/postgres_ingestion.yaml`)
   - Ingests database tables and schemas from PostgreSQL
   - Creates `marketing_postgres` service in OpenMetadata
   - Filters to `marketing` schema using regex pattern

2. **dbt Ingestion** (`openmetadata/ingestion-configs/dbt_ingestion.yaml`)
   - Ingests dbt models, lineage, and transformations
   - Links dbt models to the PostgreSQL database service
   - Creates data lineage from source tables → dbt models
   - Requires PostgreSQL ingestion to complete first

3. **Metabase Ingestion** (`openmetadata/ingestion-configs/metabase_ingestion.yaml`)
   - Ingests Metabase dashboards and charts
   - Links dashboards to underlying database tables
   - Completes end-to-end lineage: tables → dbt → dashboards
   - Requires Metabase to be configured and running

### Environment Variables

The ingestion YAML files use environment variable substitution. Set these in `openmetadata/.env`:

```bash
OPENMETADATA_JWT_TOKEN=your_jwt_token_here
METABASE_USERNAME=your_metabase_username
METABASE_PASSWORD=your_metabase_password
```

The ingestion services automatically substitute these values into the YAML configs before running.

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
│   ├── docker-compose.yml         # Main orchestration file
│   └── ingestion-configs/         # YAML-based ingestion configs
│       ├── postgres_ingestion.yaml
│       ├── dbt_ingestion.yaml
│       ├── metabase_ingestion.yaml
docs
├── seed/                           # Data seeding scripts
│   ├── Dockerfile
│   ├── config.py                   # Shared configuration
│   ├── requirements.txt
│   ├── s3.py                       # S3 → PostgreSQL seeder
│   ├── metabase.py                 # Metabase pre-configuration
│   └── metabase.sql                # Metabase seed data
└── README.md
```

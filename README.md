# Agentic Data Modeling Project

## Overview

This project demonstrates a modern data analytics stack with unified metadata management and AI-powered querying capabilities. The architecture integrates multiple tools to create a seamless data pipeline from source to insights.

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

## Prerequisites

- Python 3.11+ (for dbt)
- Node.js (for Claude MCP server)
- Docker and Docker Compose (for OpenMetadata)
- [Claude Code CLI](https://claude.ai/code)

## Setup

### 1. OpenMetadata Setup

OpenMetadata is hosted locally and provides a unified metadata platform. The docker-compose configuration file (`docker-compose-postgres.yml`) was obtained from the [official OpenMetadata website](https://docs.open-metadata.org/latest/quick-start/local-docker-deployment/).

To get started:
1. Download the docker-compose file from the [OpenMetadata documentation](https://docs.open-metadata.org/deployment/docker)
2. Place it in the `openmetadata/` directory
3. Start OpenMetadata using Docker Compose:

```bash
cd openmetadata
docker-compose -f docker-compose-postgres.yml up -d
```

Ensure OpenMetadata is running on `http://localhost:8585` before proceeding with other setup steps.

### 2. dbt Setup

dbt is used for data transformation and is configured to work with PostgreSQL database:

```bash
python3 -m venv venv
source venv/bin/activate
cd dbt
pip install -r requirements.txt
```

Then run your dbt models:

```bash
dbt run
dbt docs generate
```
### 3. Integrate with Claude Code 

The Claude MCP (Model Context Protocol) server enables AI-powered interaction with your metadata. You can ask questions about your data models, schemas, and relationships using natural language.

#### Steps to Connect:

1. **Generate a Personal Access Token (PAT) in OpenMetadata:**
   - Navigate to **Settings > Users > [Your User] > Access Tokens**
   - Create a new token and copy it

2. **Add the MCP server to Claude Code:**

```bash
claude mcp add-json "openmetadata" '{
  "command": "npx",
  "args": [
    "-y",
    "mcp-remote",
    "http://localhost:8585/mcp",
    "--auth-server-url=http://localhost:8585/mcp",
    "--client-id=openmetadata",
    "--verbose",
    "--clean",
    "--header",
    "Authorization:${AUTH_HEADER}"
  ],
  "env": {
    "AUTH_HEADER": "Bearer <YOUR-OPENMETADATA-PAT>"
  }
}'
```

   Replace `<YOUR-OPENMETADATA-PAT>` with your actual Personal Access Token.

3. **Restart Claude Code** and verify the connection with `/mcp`

4. **Start Querying**: Once connected, you can ask Claude questions like:
   - "What tables are in my database?"
   - "Show me the relationships between my dbt models"
   - "What are the column descriptions for the user_journey table?"
   - "Explain the data lineage for campaign_performance"

## Project Structure

```
.
├── dbt/                    # dbt project for data transformation
│   ├── models/
│   │   ├── staging/       # Staging models (raw data)
│   │   ├── intermediate/  # Intermediate transformations
│   │   └── marts/         # Final business-ready models
│   └── dbt_project.yml
├── openmetadata/          # OpenMetadata configuration
│   └── docker-compose-postgres.yml
└── README.md
```


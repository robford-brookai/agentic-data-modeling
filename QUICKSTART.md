# ⚡ Quick Start

A step by step guide on how to get started with this project.

**Requirements:** Docker and Docker Compose

1. Run `cd openmetadata && cp .env.example .env` to get your credentials file ready, you will need it later:

```bash
# .env
OPENMETADATA_JWT_TOKEN=your_jwt_token_here
METABASE_USERNAME=your_metabase_username
METABASE_PASSWORD=your_metabase_password
```

2. Run the docker container:
```bash
docker compose up -d
```

This starts:
- PostgreSQL with 148K rows from S3
- dbt (17 analytics models)
- Metabase (http://localhost:3000)
- OpenMetadata (http://localhost:8585)

**Total:** 23 tables/views ready to query!

## 📊 Metabase Setup

1. Complete setup wizard to create your user at http://localhost:3000
2. Save your email and password on the `.env` variables `METABASE_USERNAME` and `METABASE_PASSWORD`
3. Load pre-configured dashboard: `docker compose up seed-metabase`
4. Visit the [Agentic Data Modeling Demo Dashboard](http://localhost:3000/dashboard/2-agentic-modeling-demo) to verify everything works correctly

## 📥 OpenMetadata Ingestion

**1. Get JWT Token:**
- Login at http://localhost:8585 using `admin@open-metadata.org` & `admin` as credentials
- Follow this [link](http://localhost:8585/users/admin/access-token) to create your Access Token
- Create token and save to on the `.env` variable `OPENMETADATA_JWT_TOKEN`:

**2. Run ingestion:**
```bash
docker compose --profile ingestion up ingest-postgres ingest-dbt ingest-metabase
```

**What gets ingested on `openmetadata/ingestion-configs/`:**
- **PostgreSQL**: Tables and schemas from `marketing` schema → creates `marketing_postgres` service
- **dbt**: Models and lineage → links to PostgreSQL service
- **Metabase**: Dashboards and charts → completes full lineage: tables → dbt → dashboards

## 🧠 AI Integration with OpenMetadata MCP with Claude Code

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

> You can do this with Cursor by adding it to `mcp.json` file.

Then ask questions like:

- "Can you do an impact on analysis on changing the column `total_conversions` name?"
- "What tables feed into campaign_performance?"
- "Show me the schema for user_journey"
- "Explain the data lineage from sessions to conversions"
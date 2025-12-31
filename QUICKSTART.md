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
- Metabase
- OpenMetadata

**Total:** 23 tables/views ready to query!

## 📊 Metabase Setup

1. Complete setup wizard to create your dummy user at `http://localhost:3000` (Continue with Sample Data)
2. Save your email and password on the `.env` variables `METABASE_USERNAME` and `METABASE_PASSWORD`

## 📥 OpenMetadata Ingestion

**1. Get JWT Token:**
- Login at `http://localhost:8585` using `admin@open-metadata.org` & `admin` as credentials
- Follow this `http://localhost:8585/users/admin/access-token` to create your Access Token
- Create token and save to on the `.env` variable `OPENMETADATA_JWT_TOKEN`:

![OpenMetadata Token](images/openmetadata_token.png)

**2. Run ingestion:**
```bash
docker compose --profile ingestion up ingest-postgres ingest-dbt ingest-metabase
```

**What gets ingested on `openmetadata/ingestion-configs/`:**
- **PostgreSQL**: Tables and schemas from `marketing` schema → creates `marketing_postgres` service
- **dbt**: Models and lineage → links to PostgreSQL service
- **Metabase**: Dashboards and charts → completes full lineage: tables → dbt → dashboards

You will see the PostgreSQL (dbt included) and Metabase assets available to explore:

![OpenMetadata UI](images/openmetadata_ui.png)

To double check, visit the Metabase Dashboard [Agentic Data Modeling Demo Dashboard](http://localhost:3000/dashboard/2-agentic-data-modeling-demo) to verify everything works correctly:

![Metabase Dashboard](images/metabase_dashboard.png)

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

Then use OpenMetadata MCP Server to ask questions such as:

- "Can you do an impact on analysis on changing the column `total_conversions` name of `campaign_performance` model?"
- "Is target revenue chart on Metabase considering TV and Radio?"
- "What tables feed into `user_journey` model?"
- "Who owns the Agentic Data Modeling Demo dahsboard?"
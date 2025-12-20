# Open Metadata Project

## Integrate with Claude Code 

### Prerequisites

- [OpenMetadata](https://open-metadata.org/) running locally on `http://localhost:8585`
- Node.js (for `npx`)
- [Claude Code CLI](https://claude.ai/code)

To connect Claude Code to your OpenMetadata instance:

1. Generate a Personal Access Token (PAT) in OpenMetadata:
   - Go to **Settings > Users > [Your User] > Access Tokens**
   - Create a new token

2. Add the MCP server to Claude Code:

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

3. Restart Claude Code and verify with `/mcp`

## Get dbt models ready for ingestion into OpenMetadata

```bash
python3 -m venv venv
source venv/bin/activate
cd dbt
pip install -r requirements.txt
```

Then run:
```bash
dbt run
dbt docs generate
```
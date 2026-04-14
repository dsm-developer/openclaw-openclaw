Name: SmartSuite Connector
Description: Fetches SmartSuite records using environment-secured API credentials. The AI should use this skill to read data from SmartSuite workspaces and return structured JSON results.

Security:
- No hardcoded secrets.
- Required environment variables: `SMARTSUITE_API_KEY`, `SMARTSUITE_WORKSPACE_ID`.

Usage:
- Run `python logic.py` to validate connectivity.
- The connector prints retrieved records and can be called by an AI agent.

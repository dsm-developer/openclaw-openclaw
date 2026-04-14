# SmartSuite Connector

This skill provides a SmartSuite connector that reads API credentials from environment variables and fetches records from a SmartSuite workspace.

## Environment

Required:
- `SMARTSUITE_API_KEY`
- `SMARTSUITE_WORKSPACE_ID`

## Install

```bash
python -m pip install requests
```

## Run

```bash
python logic.py
```

## Notes

- The connector is intentionally credential-free in source control.
- Store secrets in your local environment before running.
- Update the API base URL and request payload as needed for your SmartSuite account.

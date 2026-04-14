import os
import sys
import json

try:
    import requests
except ImportError:
    raise ImportError("Install requests with: pip install requests")

SMARTSUITE_API_KEY = os.getenv("SMARTSUITE_API_KEY")
SMARTSUITE_WORKSPACE_ID = os.getenv("SMARTSUITE_WORKSPACE_ID")
SMARTSUITE_API_BASE = "https://api.smartsuite.com/v1"


def fetch_records(limit=5):
    if not SMARTSUITE_API_KEY or not SMARTSUITE_WORKSPACE_ID:
        raise EnvironmentError("SMARTSUITE_API_KEY and SMARTSUITE_WORKSPACE_ID must be set in the environment.")

    url = f"{SMARTSUITE_API_BASE}/workspaces/{SMARTSUITE_WORKSPACE_ID}/records"
    headers = {
        "Authorization": f"Bearer {SMARTSUITE_API_KEY}",
        "Accept": "application/json",
    }
    params = {"limit": limit}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def main():
    try:
        records = fetch_records(limit=5)
        print(json.dumps(records, indent=2))
    except Exception as exc:
        print(f"Error fetching SmartSuite records: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

import os

"""Example skill template entrypoint.

This script demonstrates how an AI tool should read secrets from environment variables
and avoid hardcoded credentials.
"""


def main():
    api_key = os.getenv("MY_TOOL_API_KEY")
    if not api_key:
        raise EnvironmentError("Set MY_TOOL_API_KEY in the environment before running this tool.")

    print("Template logic is ready to run.")
    print("This example tool would use environment-based secrets and execute its core behavior here.")


if __name__ == "__main__":
    main()

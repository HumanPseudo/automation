#!/usr/bin/env python3
import sys
import argparse
import json
from automation_hub.services.workspace.client import WorkspaceService

def main():
    parser = argparse.ArgumentParser(description="Manage Google Calendar events.")
    parser.add_argument("--action", required=True, help="Action to perform: list, create, update.")
    parser.add_argument("--details", type=str, required=True, help="JSON string with event details.")

    args = parser.parse_args()

    try:
        details = json.loads(args.details)
        client = WorkspaceService()
        if client.connect():
            # Llamada al manager específico de calendario
            result = client.calendar.manage_calendar(args.action, details)
            print(json.dumps(result))
            client.disconnect()
        else:
            print(json.dumps({"status": "error", "message": "Connection failed"}))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))

if __name__ == "__main__":
    main()

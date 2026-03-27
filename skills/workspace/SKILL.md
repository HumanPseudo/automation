---
name: workspace
description: Automate Google Workspace tasks like Calendar, Sheets, and Docs.
triggers:
  - "calendar"
  - "sheets"
  - "spreadsheet"
  - "docs"
---

# Workspace Skill

This skill allows the agent to interact with Google Workspace services through the `automation_hub` package.

## Scripts

The following scripts are available to perform Workspace operations:

- `manage_calendar.py`: Create, list, or update calendar events.
- `read_sheet.py`: Fetch data from specific ranges in Google Sheets.

## Usage Example

> "Schedule a meeting with the team tomorrow at 10 AM regarding project X."

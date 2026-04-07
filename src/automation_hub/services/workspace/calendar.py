from datetime import datetime, time, timezone
from typing import Any, Dict, List

from googleapiclient.discovery import Resource


class CalendarManager:
    """Handles Google Calendar operations."""

    def __init__(self, service: Resource):
        self.service = service

    def get_today_bounds(self):
        """Helper to get ISO timestamps for today."""
        now = datetime.now(timezone.utc)
        start = (
            datetime.combine(now.date(), time.min)
            .replace(tzinfo=timezone.utc)
            .isoformat()
        )
        end = (
            datetime.combine(now.date(), time.max)
            .replace(tzinfo=timezone.utc)
            .isoformat()
        )
        return start, end

    def list_today_events(self, calendar_id: str = "primary") -> List[Dict[str, Any]]:
        start, end = self.get_today_bounds()
        events_result = (
            self.service.events()
            .list(
                calendarId=calendar_id,
                timeMin=start,
                timeMax=end,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        return events_result.get("items", [])

    def create_event(
        self,
        summary: str,
        start_time: str,
        end_time: str,
        description: str = "",
        calendar_id: str = "primary",
    ):
        event_body = {
            "summary": summary,
            "description": description,
            "start": {"dateTime": start_time, "timeZone": "UTC"},
            "end": {"dateTime": end_time, "timeZone": "UTC"},
        }
        return (
            self.service.events()
            .insert(calendarId=calendar_id, body=event_body)
            .execute()
        )

    def manage_calendar(self, action: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """Orchestrates calendar actions."""
        calendar_id = details.get("calendar_id", "primary")
        if action == "list":
            return {"status": "success", "data": self.list_today_events(calendar_id)}

        if action == "create":
            try:
                result = self.create_event(
                    summary=details.get("summary"),
                    start_time=details.get("start_time"),
                    end_time=details.get("end_time"),
                    description=details.get("description", ""),
                    calendar_id=calendar_id,
                )
                return {"status": "success", "data": result}
            except Exception as e:
                return {"status": "error", "message": str(e)}

        return {"status": "error", "message": f"Action {action} not implemented"}

    def get_today_summary(
        self,
        tasks_manager=None,
        sheets_manager=None,
        spreadsheet_id: str = None,
        log_range: str = "A1:Z100",
        calendar_id: str = "primary",
    ):
        """Aggregates information for a daily summary."""
        summary = {
            "events": self.list_today_events(calendar_id),
            "tasks": [],
            "logs": [],
        }

        if tasks_manager:
            summary["tasks"] = tasks_manager.list_tasks()

        if sheets_manager and spreadsheet_id:
            summary["logs"] = sheets_manager.read_range(spreadsheet_id, log_range)

        return summary

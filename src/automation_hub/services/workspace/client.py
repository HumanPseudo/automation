import os
import logging
from typing import Any, Dict
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from automation_hub.core.service import BaseService
from automation_hub.services.workspace.calendar import CalendarManager
from automation_hub.services.workspace.sheets import SheetsManager
from automation_hub.services.workspace.tasks import TasksManager

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/tasks.readonly",
]


class WorkspaceService(BaseService):
    """Orchestrator for Google Workspace services."""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.creds = None
        self.calendar: CalendarManager = None
        self.sheets: SheetsManager = None
        self.tasks: TasksManager = None

    def connect(self) -> bool:
        """Handles Auth and initializes specialized managers."""
        self.logger.info("Connecting to Google Workspace...")
        logging.getLogger("googleapiclient.discovery_cache").setLevel(logging.ERROR)

        token_path = "token.json"
        creds_path = "credentials.json"

        if os.path.exists(token_path):
            self.creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        if not self.creds or not self.creds.valid:
            try:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.logger.info("Refreshing token...")
                    self.creds.refresh(Request())
                else:
                    if not os.path.exists(creds_path):
                        self.logger.error(f"Falta {creds_path}")
                        return False
                    flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                    self.creds = flow.run_local_server(
                        port=0, access_type="offline", prompt="consent"
                    )

                # Ensure token.json is created with 600 permissions (owner read/write only)
                fd = os.open(token_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
                with os.fdopen(fd, "w") as token:
                    token.write(self.creds.to_json())
            except Exception as e:
                self.logger.error(f"Auth error: {e}")
                return False

        try:
            self.calendar = CalendarManager(
                build("calendar", "v3", credentials=self.creds, static_discovery=False)
            )
            self.sheets = SheetsManager(
                build("sheets", "v4", credentials=self.creds, static_discovery=False)
            )
            self.tasks = TasksManager(
                build("tasks", "v1", credentials=self.creds, static_discovery=False)
            )

            self.logger.info("Workspace connected and managers initialized.")
            return True
        except Exception as e:
            self.logger.error(f"Build error: {e}")
            return False

    def disconnect(self):
        self.calendar = None
        self.sheets = None
        self.tasks = None

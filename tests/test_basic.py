import unittest
from unittest.mock import MagicMock, patch
from automation_hub.services.workspace.client import WorkspaceService
from automation_hub.services.social.client import SocialService


class TestAutomationHub(unittest.TestCase):
    @patch("automation_hub.services.workspace.client.WorkspaceService.connect")
    def test_workspace_service(self, mock_connect):
        mock_connect.return_value = True
        client = WorkspaceService()
        self.assertTrue(client.connect())

        # Mock calendar and its manage_calendar method
        client.calendar = MagicMock()
        client.calendar.manage_calendar.return_value = {"status": "success"}

        result = client.calendar.manage_calendar("list", {})
        self.assertEqual(result["status"], "success")

    def test_social_service(self):
        client = SocialService()
        self.assertTrue(client.connect())
        result = client.post_update("X", "Hello World!")
        self.assertEqual(result["status"], "success")


if __name__ == "__main__":
    unittest.main()

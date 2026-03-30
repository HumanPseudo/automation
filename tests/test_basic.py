import unittest
from automation_hub.services.workspace.client import WorkspaceService
from automation_hub.services.social.client import SocialService


class TestAutomationHub(unittest.TestCase):
    def test_workspace_service(self):
        client = WorkspaceService()
        self.assertTrue(client.connect())
        result = client.manage_calendar("list", {})
        self.assertEqual(result["status"], "success")

    def test_social_service(self):
        client = SocialService()
        self.assertTrue(client.connect())
        result = client.post_update("X", "Hello World!")
        self.assertEqual(result["status"], "success")


if __name__ == "__main__":
    unittest.main()

from typing import List, Dict, Any
from googleapiclient.discovery import Resource

class TasksManager:
    """Handles Google Tasks operations."""
    
    def __init__(self, service: Resource):
        self.service = service

    def list_tasks(self, tasklist: str = '@default') -> List[Dict[str, Any]]:
        results = self.service.tasks().list(tasklist=tasklist).execute()
        return results.get('items', [])

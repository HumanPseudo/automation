from typing import List, Any
from googleapiclient.discovery import Resource

class SheetsManager:
    """Handles Google Sheets operations."""
    
    def __init__(self, service: Resource):
        self.service = service

    def read_range(self, spreadsheet_id: str, range_name: str) -> List[List[Any]]:
        result = self.service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        return result.get('values', [])

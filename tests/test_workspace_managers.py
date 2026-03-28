import unittest
from unittest.mock import MagicMock
from automation_hub.services.workspace.calendar import CalendarManager

class TestCalendarManager(unittest.TestCase):
    def test_list_today_events_calls_api(self):
        # 1. Crear un mock del servicio de Google
        mock_service = MagicMock()
        
        # 2. Simular la respuesta de la API: service.events().list().execute()
        mock_events = [{'summary': 'Meeting 1'}, {'summary': 'Meeting 2'}]
        mock_service.events.return_value.list.return_value.execute.return_value = {
            'items': mock_events
        }
        
        # 3. Inicializar el manager con el mock
        manager = CalendarManager(mock_service)
        
        # 4. Ejecutar el método
        results = manager.list_today_events()
        
        # 5. Verificar resultados sin tocar internet
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['summary'], 'Meeting 1')
        
        # Verificar que se llamó a la API correctamente
        self.assertTrue(mock_service.events.return_value.list.called)

if __name__ == "__main__":
    unittest.main()

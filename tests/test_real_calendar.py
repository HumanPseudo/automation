import logging
import sys
from datetime import datetime, timedelta, timezone

from automation_hub.services.workspace.client import WorkspaceService

# Configuración de logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def test_integration(user_email: str = "primary"):
    """
    Prueba de integración real con sincronización a base de datos local.
    """
    logger.info(f"--- 🧪 Probando Google Calendar + DB Local: {user_email} ---")
    
    ws = WorkspaceService()
    
    if not ws.connect():
        logger.error("No se pudo conectar a Google Workspace.")
        return

    try:
        # 1. Obtener eventos de Google
        logger.info(f"Obteniendo eventos de {user_email}...")
        events = ws.calendar.list_today_events(calendar_id=user_email)
        logger.info(f"✅ Eventos obtenidos de Google: {len(events)}")

        # 2. Guardar en la base de datos local
        if events:
            logger.info("Sincronizando con base de datos local...")
            ws.db.save_calendar_events(user_email, events)
            logger.info("✅ Sincronización completada.")

        # 3. Verificar lo que hay en la DB local
        logger.info("Consultando datos de la DB local...")
        local_events = ws.db.get_local_events(limit=5)
        logger.info(f"Últimos {len(local_events)} eventos en DB local:")
        for le in local_events:
            # Ahora le es un objeto CalendarEventModel, usamos .atributo
            logger.info(f"  - [{le.start_time}] {le.summary} (ID: {le.event_id[:8]}...)")

    except Exception as e:
        logger.error(f"❌ Error: {e}")
    finally:
        ws.disconnect()
        logger.info("--- 🏁 Fin de la Prueba ---")


if __name__ == "__main__":
    target_email = sys.argv[1] if len(sys.argv) > 1 else "primary"
    test_integration(target_email)

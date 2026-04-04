import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from automation_hub.services.workspace.client import WorkspaceService

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """
    Script de demostración para el uso del servicio de Google Workspace.
    Muestra cómo conectar, obtener un resumen del día y crear un evento.
    """
    logger.info("--- 🚀 Iniciando Demo de Google Workspace ---")

    ws: Optional[WorkspaceService] = None
    try:
        # 1. Instanciar el servicio (buscará credentials.json y token.json)
        ws = WorkspaceService()

        # 2. Conectar (Aquí se abrirá el navegador si no hay token válido)
        if not ws.connect():
            logger.error("No se pudo conectar a Google Workspace.")
            return

        # 3. Obtener el resumen de hoy (Eventos + Tareas)
        logger.info("--- 📅 Resumen de Hoy ---")
        summary: Dict[str, Any] = ws.calendar.get_today_summary(
            tasks_manager=ws.tasks, sheets_manager=ws.sheets
        )

        # Mostrar Eventos
        events: List[Dict[str, Any]] = summary.get("events", [])
        logger.info("📆 Eventos del Calendario (%d):", len(events))
        for event in events:
            start: str = event.get("start", {}).get(
                "dateTime", event.get("start", {}).get("date", "N/A")
            )
            logger.info("  - [%s] %s", start, event.get("summary", "Sin título"))

        # Mostrar Tareas
        tasks: List[Dict[str, Any]] = summary.get("tasks", [])
        logger.info("✅ Tareas Pendientes (%d):", len(tasks))
        for task in tasks:
            status = " [x]" if task.get("status") == "completed" else " [ ]"
            logger.info("  %s %s", status, task.get("title", "Sin título"))

        # 4. Probar creación de un evento de prueba
        logger.info("--- ➕ Creando Evento de Prueba ---")

        # Hora de ejemplo: Mañana a las 10 AM
        now = datetime.now(timezone.utc)
        tomorrow_10am = (now + timedelta(days=1)).replace(
            hour=10, minute=0, second=0, microsecond=0
        )
        tomorrow_11am = tomorrow_10am + timedelta(hours=1)

        result: Dict[str, Any] = ws.calendar.create_event(
            summary="🚀 Test Automation Hub",
            start_time=tomorrow_10am.isoformat(),
            end_time=tomorrow_11am.isoformat(),
            description="Evento creado automáticamente desde el bot de demostración.",
        )

        if result and "id" in result:
            logger.info("✅ Evento creado con éxito! ID: %s", result["id"])
        else:
            logger.warning("No se pudo confirmar la creación del evento: %s", result)

    except Exception:
        logger.exception("Se produjo un error inesperado durante la ejecución:")
    finally:
        if ws:
            ws.disconnect()
            logger.info("--- 👋 Fin de la Demo ---")


if __name__ == "__main__":
    main()

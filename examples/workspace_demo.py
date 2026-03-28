import json
from automation_hub.services.workspace.client import WorkspaceService

def main():
    print("--- 🚀 Iniciando Demo de Google Workspace ---")
    
    # 1. Instanciar el servicio (Se encargará de buscar credentials.json y token.json)
    ws = WorkspaceService()
    
    # 2. Conectar (Aquí se abrirá el navegador si no hay token válido)
    if not ws.connect():
        print("❌ Error: No se pudo conectar a Google Workspace.")
        return

    # 3. Obtener el resumen de hoy (Eventos + Tareas)
    print("\n--- 📅 Resumen de Hoy ---")
    summary = ws.calendar.get_today_summary(tasks_manager=ws.tasks, sheets_manager=ws.sheets)
    
    # Mostrar Eventos
    events = summary.get('events', [])
    print(f"\n📆 Eventos del Calendario ({len(events)}):")
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"  - [{start}] {event['summary']}")

    # Mostrar Tareas
    tasks = summary.get('tasks', [])
    print(f"\n✅ Tareas Pendientes ({len(tasks)}):")
    for task in tasks:
        status = " [x]" if task['status'] == 'completed' else " [ ]"
        print(f"  {status} {task['title']}")

    # 4. Probar creación de un evento de prueba
    print("\n--- ➕ Creando Evento de Prueba ---")
    # Hora de ejemplo: Mañana a las 10 AM
    from datetime import datetime, timedelta, timezone
    start = (datetime.now(timezone.utc) + timedelta(days=1)).replace(hour=10, minute=0, second=0).isoformat()
    end = (datetime.now(timezone.utc) + timedelta(days=1)).replace(hour=11, minute=0, second=0).isoformat()
    
    result = ws.calendar.create_event(
        summary="🚀 Test Automation Hub",
        start_time=start,
        end_time=end,
        description="Evento creado automáticamente desde el bot."
    )
    
    if 'id' in result:
        print(f"✅ Evento creado con éxito! ID: {result['id']}")
    else:
        print(f"❌ Error al crear el evento: {result}")

    ws.disconnect()
    print("\n--- 👋 Fin de la Demo ---")

if __name__ == "__main__":
    main()

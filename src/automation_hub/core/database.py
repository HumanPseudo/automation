import logging
import os
from typing import Any, Dict, List, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

from automation_hub.core.models import CalendarEventDB, CalendarEventSchema

# Cargar variables de entorno
load_dotenv()

class DatabaseManager:
    """Manages PostgreSQL database using SQLAlchemy ORM."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Construir URL de conexión
        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        dbname = os.getenv("POSTGRES_DB", "app_db")
        
        self.db_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        
        # Configurar Engine y SessionMaker
        self.engine = create_engine(self.db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        self.logger.info(f"SQLAlchemy Engine initialized for {host}:{port}")

    def get_session(self) -> Session:
        """Returns a new database session."""
        return self.SessionLocal()

    def save_calendar_events(self, calendar_id: str, raw_events: List[Dict[str, Any]]):
        """Validates with Pydantic and saves using SQLAlchemy ORM."""
        if not raw_events:
            return

        session = self.get_session()
        try:
            for raw_event in raw_events:
                # 1. Validar con Pydantic
                schema = CalendarEventSchema.from_google_api(calendar_id, raw_event)
                
                # 2. Convertir a Modelo de DB (ORM)
                event_db = session.get(CalendarEventDB, schema.event_id)
                
                if event_db:
                    # Actualizar existente
                    event_db.summary = schema.summary
                    event_db.description = schema.description
                    event_db.start_time = schema.start_time
                    event_db.end_time = schema.end_time
                else:
                    # Crear nuevo
                    new_event = CalendarEventDB(**schema.model_dump())
                    session.add(new_event)
            
            session.commit()
            self.logger.info(f"Successfully synced {len(raw_events)} events to database.")
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error syncing events: {e}")
        finally:
            session.close()

    def get_local_events(self, limit: int = 50) -> List[CalendarEventDB]:
        """Retrieves events using ORM."""
        session = self.get_session()
        try:
            return session.query(CalendarEventDB).order_by(CalendarEventDB.start_time.desc()).limit(limit).all()
        finally:
            session.close()

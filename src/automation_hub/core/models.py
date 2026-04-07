from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.orm import DeclarativeBase


# --- SQLAlchemy Models (Database Schema) ---

class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass


class CalendarEventDB(Base):
    """Database table for Google Calendar events."""
    __tablename__ = "calendar_events"

    event_id = Column(String, primary_key=True)
    calendar_id = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    description = Column(Text)
    start_time = Column(String)
    end_time = Column(String)
    synced_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TaskDB(Base):
    """Database table for Google Tasks."""
    __tablename__ = "tasks"

    task_id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    notes = Column(Text)
    status = Column(String)
    due = Column(String)
    synced_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# --- Pydantic Models (Validation & API DTOs) ---

class CalendarEventSchema(BaseModel):
    """Schema for data validation."""
    event_id: str
    calendar_id: str
    summary: str
    description: Optional[str] = None
    start_time: str
    end_time: str

    @classmethod
    def from_google_api(cls, calendar_id: str, event_data: dict):
        """Helper to create a schema from Google API response."""
        start = event_data.get("start", {}).get("dateTime", event_data.get("start", {}).get("date"))
        end = event_data.get("end", {}).get("dateTime", event_data.get("end", {}).get("date"))
        
        return cls(
            event_id=event_data.get("id"),
            calendar_id=calendar_id,
            summary=event_data.get("summary", "No Title"),
            description=event_data.get("description"),
            start_time=start,
            end_time=end
        )

    class Config:
        from_attributes = True

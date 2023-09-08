import enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.configs.base import Base


class NotificationTypeAlert(enum.Enum):
    waiting_register = 0
    error_in_consult_register = 1
    register_finished = 2
    task_to_do = 3


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    is_read = Column(Boolean, default=False)
    text = Column(String)
    type_alert = Column(Enum(NotificationTypeAlert), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    client_id = Column(Integer, ForeignKey("clients.id"))
    client = relationship("Client", back_populates="notifications")

import enum

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.configs.base import Base


class NotificationTypeAlert(enum.Enum):
    WAITING_REGISTER = 0
    ERROR_IN_CONSULT_REGISTER = 1
    REGISTER_FINISHED = 2
    TASK_TO_DO = 3


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

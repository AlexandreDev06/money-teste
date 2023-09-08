import enum

from sqlalchemy import (
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


class TaskTypeTask(enum.Enum):
    note = 0
    task = 1


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    will_send_at = Column(DateTime(timezone=True))
    type_task = Column(Enum(TaskTypeTask), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    client_id = Column(Integer, ForeignKey("clients.id"))
    client = relationship("Client", back_populates="tasks")

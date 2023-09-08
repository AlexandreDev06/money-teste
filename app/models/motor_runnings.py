from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    ForeignKey,
    Enum,
)
from sqlalchemy.sql import func
import enum
from sqlalchemy.orm import relationship

from app.configs.base import Base


class MotorRunningStatus(enum.Enum):
    in_progress = 0
    paused = 1
    finished = 2


class MotorType(enum.Enum):
    enrichment = 1
    eligibility = 2


class MotorRunning(Base):
    __tablename__ = "motor_runnings"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(MotorRunningStatus))
    motor_type = Column(Enum(MotorType))

    operation_id = Column(Integer, ForeignKey("operations.id"))
    operation = relationship("Operation", back_populates="motor_runnings")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

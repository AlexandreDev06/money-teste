import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.configs.base import Base


class MotorRunningStatus(enum.Enum):
    """Motor running status"""

    IN_PROGRESS = 0
    PAUSED = 1
    FINISHED = 2


class MotorType(int, enum.Enum):
    """Motor type"""

    ENTRY = 0
    ENRICHMENT = 1
    ELIGIBILITY = 2


class MotorRunning(Base):
    """Motor running model"""

    __tablename__ = "motor_runnings"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(MotorRunningStatus))
    motor_type = Column(Enum(MotorType))

    operation_id = Column(Integer, ForeignKey("operations.id"))
    operation = relationship("Operation", back_populates="motor_runnings")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

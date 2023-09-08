from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.configs.base import Base


class Operation(Base):
    """Operation model"""

    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    clients = relationship("Client", back_populates="operation")
    motor_runnings = relationship("MotorRunning", back_populates="operation")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

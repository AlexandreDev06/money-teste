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


class TimelinePipelineStatus(enum.Enum):
    entry = 0
    enrichment = 1
    eligibility = 2
    contact = 3
    waiting_fill = 4
    contract = 5
    general_verification = 6
    waiting_for_analyzes = 7
    in_queue = 8
    waiting_payment = 9
    completed_with_success = 10
    completed_with_failure = 11
    pending_docs = 12


class TimelineSource(enum.Enum):
    spreadsheet = 0
    landing_page = 1
    pending_registration = 2


class Timeline(Base):
    __tablename__ = "timelines"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    answer = Column(String)
    pipeline_status = Column(Enum(TimelinePipelineStatus))
    sended_at = Column(DateTime(timezone=True))
    source = Column(Enum(TimelineSource))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    client_id = Column(Integer, ForeignKey("clients.id"))
    client = relationship("Client", back_populates="timelines")

import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.configs.base import Base


class TimelinePipelineStatus(enum.Enum):
    ENTRY = 0
    ENRICHMENT = 1
    ELIGIBILITY = 2
    CONTACT = 3
    WAITING_FILL = 4
    CONTRACT = 5
    GENERAL_VERIFICATION = 6
    WAITING_FOR_ANALYZES = 7
    IN_QUEUE = 8
    WAITING_PAYMENT = 9
    COMPLETED_WITH_SUCCESS = 10
    COMPLETED_WITH_FAILURE = 11
    PENDING_DOCS = 12


class TimelineSource(enum.Enum):
    SPREADSHEET = 0
    LANDING_PAGE = 1
    PENDING_REGISTRATION = 2


class Timeline(Base):
    __tablename__ = "timelines"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    pipeline_status = Column(Enum(TimelinePipelineStatus))
    sended_at = Column(DateTime(timezone=True))
    source = Column(Enum(TimelineSource))

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    client_id = Column(Integer, ForeignKey("clients.id"))
    client = relationship("Client", back_populates="timelines")

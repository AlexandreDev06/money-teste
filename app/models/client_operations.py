import enum

from sqlalchemy import (
    ARRAY,
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.configs.base import Base


class ClientOperationPipelineStatus(enum.Enum):
    ENTRY = 13
    ENRICHMENT = 14
    ELIGIBILITY = 15
    CONTACT = 16
    WAITING_FILL = 17
    CONTRACT = 18
    GENERAL_VERIFICATION = 19
    WAITING_FOR_ANALYZES = 20
    IN_QUEUE = 21
    WAITING_PAYMENT = 22
    COMPLETED_WITH_SUCCESS = 23
    COMPLETED_WITH_FAILURE = 24
    PENDING_DOCS = 25


class ClientOperationSearchIrpfStatus(enum.Enum):
    NOT_SEARCHED = 0
    SEARCHING = 1
    SUCCESS = 2
    ERROR = 3


class ClientOperation(Base):
    __tablename__ = "client_operations"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer)
    salaries = Column(ARRAY(Float))
    is_elegible = Column(Boolean)
    refound_amount = Column(Float)
    is_active = Column(Boolean, default=True)
    irpf_situation = Column(String)
    pipeline_status = Column(Enum(ClientOperationPipelineStatus), default="ELIGIBILITY")
    cnpj_payer = Column(String)
    name_payer = Column(String)
    previd_official = Column(Integer)
    tax_received = Column(Float)
    search_irpf_status = Column(Enum(ClientOperationSearchIrpfStatus))
    sended_fill_ir_at = Column(DateTime(timezone=True))
    filled_ir_at = Column(DateTime(timezone=True))
    irpf_image = Column(String)

    client_id = Column(Integer, ForeignKey("clients.id"))
    client = relationship("Client", back_populates="client_operations")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

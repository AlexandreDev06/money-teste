import enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    ARRAY,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.configs.base import Base


class ClientSource(enum.Enum):
    SPREADSHEET = 0
    LANDING_PAGE = 1
    DIRF = 2


class ClientPipelineStatus(enum.Enum):
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


class ClientDocumentType(enum.Enum):
    RG = 0
    CNH = 1
    PEP = 2


class ClientSearchIrpfStatus(enum.Enum):
    NOT_SEARCHED = 0
    SEARCHING = 1
    SUCCESS = 2
    ERROR = 3


class ClientRegistrationStatus(enum.Enum):
    PENDING_DOCUMENTS = 0
    FINISHED = 1


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cpf = Column(String, nullable=False, unique=True)
    birth_date = Column(String, nullable=False)
    is_enriched = Column(Boolean, default=False)
    source = Column(Enum(ClientSource), nullable=False)
    mother_name = Column(String)
    document_type = Column(Enum(ClientDocumentType))
    document_file = Column(String)
    contract_token = Column(String)
    phone = Column(ARRAY(String))
    email = Column(ARRAY(String))
    cep = Column(ARRAY(String))
    house_number = Column(ARRAY(String))
    street = Column(ARRAY(String))
    district = Column(ARRAY(String))
    city = Column(ARRAY(String))
    state = Column(ARRAY(String))
    name_bank = Column(String)
    number_bank = Column(String)
    agency = Column(String)
    number_account = Column(String)
    code_pix = Column(String)
    search_irpf_status = Column(Enum(ClientSearchIrpfStatus), default=0)
    document_address = Column(String)
    is_active = Column(Boolean, default=True)
    email_sended_at = Column(DateTime(timezone=True))
    registration_status = Column(Enum(ClientRegistrationStatus))

    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    operation_id = Column(Integer, ForeignKey("operations.id"))
    operation = relationship("Operation", back_populates="clients")
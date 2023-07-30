from sqlalchemy import Column, Integer, String, Date, Double, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.config.db import Base


class BankSlip(Base):
    __tablename__ = "bank_slip"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    government_id = Column(String(11), nullable=False)
    debt_amount = Column(Double(10), nullable=False)
    debt_due_date = Column(Date(), nullable=False)
    debt_id = Column(Integer(), nullable=False)
    paid_at = Column(DateTime(), nullable=True)
    paid_by = Column(String(255), nullable=True)
    paid_amount = Column(Double(10), nullable=True)
    inserted_at = Column(DateTime(), nullable=True, default=datetime.now())
    updated_at = Column(DateTime(), nullable=True, default=datetime.now())

    def __init__(self, name, email, government_id, debt_amount, debt_due_date, debt_id):
        self.name = name
        self.email = email
        self.government_id = government_id
        self.debt_amount = debt_amount
        self.debt_due_date = debt_due_date
        self.debt_id = debt_id

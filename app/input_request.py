from pydantic import BaseModel, Field, EmailStr, validator
from decimal import Decimal
from datetime import datetime, date

class BankSlipPaid(BaseModel):
    debtId: str
    paidAt: str
    paidAmount: Decimal
    paidBy: str


class BankSlip(BaseModel):
    name: str
    governmentId: str = Field(min_length=11)
    email: EmailStr
    debtAmount: Decimal
    debtDueDate: date
    debtId: int

    @validator('debtDueDate', pre=True)
    def validate_date_format(cls, value):
        return datetime.strptime(value, '%Y-%m-%d').date()

    @validator('debtAmount', pre=True)
    def validate_debt_amount(cls, value):
        return Decimal(value)

    @validator('debtId', pre=True)
    def validate_debt_id(cls, value):
        return int(value)
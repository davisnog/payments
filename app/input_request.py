from fastapi.exceptions import HTTPException

from pydantic import BaseModel, Field, EmailStr, validator, ValidationError, field_validator
from decimal import Decimal
from datetime import datetime, date

class BankSlipPaid(BaseModel):
    debtId: int
    paidAt: datetime
    paidAmount: Decimal
    paidBy: str

    @validator('paidAt', pre=True)
    def validate_date_format(cls, value):
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

    @validator('debtId', pre=True)
    def validate_debt_id(cls, value):
        return int(value)

    @validator('paidAmount', pre=True)
    def validate_paid_amount(cls, value):
        return Decimal(value)


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


async def validate_file_upload(file):
    file.file.seek(0, 2)
    file_size = file.file.tell()

    await file.seek(0)
    content_type = file.content_type

    if content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Invalid file type, required csv file")

    if file_size > 1 * 1024:
        raise HTTPException(status_code=400, detail="File too large, greater than 1MB")

def validate_file_content(row):
    try:
        BankSlip.model_validate(row, strict=True)
        return [], BankSlip(**row).model_dump()
    except ValidationError as exc:
        errors = [{"type": e["type"], "field": " ".join(e["loc"]), "msg": e["msg"]} for e in exc.errors()]
        return errors, None

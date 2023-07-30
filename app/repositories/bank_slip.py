from app.config.db import SessionLocal
from app.models.bank_slip import BankSlip
from datetime import datetime

def save(bank_slip):
    session = SessionLocal()
    bank = BankSlip(name=bank_slip["name"], 
        email=bank_slip["email"], 
        government_id=bank_slip["governmentId"], 
        debt_amount=bank_slip["debtAmount"], 
        debt_due_date=bank_slip["debtDueDate"], 
        debt_id=bank_slip["debtId"])

    session.add(bank)
    session.commit()


def mark_as_paid(bank_slip):
    session = SessionLocal()
    session.query(BankSlip).filter_by(debt_id=bank_slip["debtId"]).update({
        "paid_at": bank_slip["paidAt"],
        "paid_by": bank_slip["paidBy"],
        "paid_amount": bank_slip["paidAmount"],
        "updated_at": datetime.now()
    })

    session.commit()


from app.config.celery import celery
from app.repositories.bank_slip import save, mark_as_paid

@celery.task(name="save_bank_slip_db")
def save_bank_slip_db(bank_slip):
    save(bank_slip)
    return bank_slip

@celery.task(name="process_bank_slip")
def process_bank_slip(bank_slip):
    print("process_bank_slip")
    print(bank_slip)

    return bank_slip

@celery.task(name="send_email_notification")
def send_email_notification(bank_slip):
    print("send_email_notification")
    print(bank_slip)
    return {}

@celery.task(name="mark_bank_slip_as_paid")
def mark_bank_slip_as_paid(bank_slip):
    mark_as_paid(bank_slip)
    return bank_slip

@celery.task(name="settle_current_account")
def settle_current_account(bank_slip):
    print("settle_current_account")
    return {}
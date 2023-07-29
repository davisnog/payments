import os
from celery import Celery

redis_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")

celery = Celery(__name__, broker=redis_url, backend=redis_url)

@celery.task(name="process_bank_slip")
def process_bank_slip(bank_slip):
    print('process_bank_slip')
    print(bank_slip)

@celery.task(name="send_email_notification")
def send_email_notification(bank_slip):
    print('send_email_notification')
    print(bank_slip)
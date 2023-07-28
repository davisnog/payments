import os
from celery import Celery

redis_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")

celery = Celery(__name__, broker=redis_url, backend=redis_url)

@celery.task(name="send_to_generate_bank_slip")
def send_to_generate_bank_slip(bank_slip):
    print('send_to_generate_bank_slip')
    print(bank_slip)
    return True
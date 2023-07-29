# from app.background_tasks import send_to_generate_bank_slip

def process(bank_slip):
    print('processing')
    # send_to_generate_bank_slip.delay(bank_slip)


def notify(bank_slip):
    print('notifying')
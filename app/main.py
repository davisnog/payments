from fastapi import FastAPI, UploadFile, File
from fastapi.exceptions import HTTPException
from celery import chain

from io import StringIO
import csv

from app import create_app

from app.input_request import (
    BankSlipPaid,
    BankSlip,
    validate_file_upload,
    validate_file_content,
)
from app.background_tasks import (
    process_bank_slip,
    send_email_notification,
    save_bank_slip_db,
    mark_bank_slip_as_paid,
    settle_current_account,
)

app = create_app()


@app.post("/v1/uploadfile")
async def create_upload_file(file: UploadFile):
    await validate_file_upload(file)

    contents = await file.read()

    f = StringIO(contents.decode("utf-8"))
    errors = []

    reader = csv.DictReader(f, delimiter=",")
    for index, row in enumerate(reader):
        error, bank_slip = validate_file_content(row)

        if error:
            errors.append({"line": index + 1, "fields": error})
        else:
            chain(
                save_bank_slip_db.s(bank_slip),
                process_bank_slip.s(),
                send_email_notification.s(),
            ).apply_async()

    if errors:
        raise HTTPException(status_code=422, detail=errors)

    return {"filename": file.filename}


@app.post("/v1/webhook")
async def webhook(bank_slip: BankSlipPaid):
    chain(
        mark_bank_slip_as_paid.s(bank_slip.model_dump()),
        settle_current_account.s(),
    ).apply_async()

    return {"message": "Ok"}

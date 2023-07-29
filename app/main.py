from fastapi import FastAPI, UploadFile, File
from fastapi.exceptions import HTTPException
from celery import chain

from io import StringIO
import csv

from app.input_request import BankSlipPaid, BankSlip, validate_file_upload, validate_file_content
from app.background_tasks import process_bank_slip, send_email_notification

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    await validate_file_upload(file)

    contents = await file.read()

    f = StringIO(contents.decode("utf-8"))
    errors = []

    reader = csv.DictReader(f, delimiter=',')
    for index, row in enumerate(reader):
        error, bank_slip = validate_file_content(row)

        if error:
            errors.append({"line": index+1, "fields": error})
        else:
            chain(process_bank_slip.s(bank_slip), send_email_notification.s(bank_slip))

    if errors:
        raise HTTPException(status_code=422, detail=errors)

    return {"filename": file.filename}

@app.post("/webhook")
async def webhook(bank_slip: BankSlipPaid):
    print(bank_slip)
    return {"message": "Ok"}

from fastapi import FastAPI, UploadFile
from io import StringIO
import csv

from input_request import BankSlipPaid, BankSlip
from process_bank_slip import notify, process

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    contents = await file.read()

    f = StringIO(contents.decode('utf-8'))

    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        BankSlip.model_validate(row, strict=True)
        process(row)
        notify(row)

    return {"filename": file.filename}

@app.post("/webhook")
async def webhook(bank_slip: BankSlipPaid):
    print(bank_slip)
    return {"message": "Ok"}

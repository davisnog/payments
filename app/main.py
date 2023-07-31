from fastapi import FastAPI, UploadFile, File, Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from celery import chain


from io import StringIO
import csv


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

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = exc.errors()
    modified_details = []
    for error in details:
        modified_details.append(
            {
                "loc": error["loc"],
                "message": error["msg"],
                "type": error["type"],
            }
        )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": modified_details}),
    )


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

    return {"message": "Uploaded with success {0}".format(file.filename)}


@app.post("/v1/webhook")
async def webhook(bank_slip: BankSlipPaid):
    chain(
        mark_bank_slip_as_paid.s(bank_slip.model_dump()),
        settle_current_account.s(),
    ).apply_async()

    return {"message": "Ok"}

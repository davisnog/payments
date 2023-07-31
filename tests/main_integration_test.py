import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.bank_slip import BankSlip
from datetime import datetime

client = TestClient(app)


def test_upload_with_success(db_session, celery_app):
    files = {"file": ("upload_ok.csv", open("tests/fixtures/upload_ok.csv", "rb"))}

    response = client.post("/v1/uploadfile", files=files)

    assert response.status_code == 200
    assert response.json() == {"message": "Uploaded with success upload_ok.csv"}

    result = db_session.query(BankSlip).count()

    assert result == 3


def test_webhook_with_success(db_session, celery_app):
    payload = {
        "debtId": "3012",
        "paidAt": "2022-06-09 10:00:00",
        "paidAmount": 100000.00,
        "paidBy": "John Doe",
    }

    response = client.post("/v1/webhook", json=payload)

    assert response.status_code == 200
    assert response.json() == {"message": "Ok"}

    result = db_session.query(BankSlip).filter_by(debt_id=3012).one()

    assert result.paid_at == datetime(2022, 6, 9, 10, 00, 00)

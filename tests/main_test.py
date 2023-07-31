from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_webhook_with_success(mocker):
    payload = {
        "debtId": "3012",
        "paidAt": "2022-06-09 10:00:00",
        "paidAmount": 100000.00,
        "paidBy": "John Doe",
    }

    mocker.patch("app.main.chain")
    mocker.patch("app.background_tasks.mark_bank_slip_as_paid")
    mocker.patch("app.background_tasks.settle_current_account")

    response = client.post("/v1/webhook", json=payload)

    assert response.status_code == 200
    assert response.json() == {"message": "Ok"}


def test_webhook_with_invalid_request(mocker):
    payload = {
        "debtId": "3012",
        "paidAt": "25-12-2022 10:00:00",
        "paidAmount": 100000.00,
        "paidBy": "John Doe",
    }

    mocker.patch("app.main.chain")
    mocker.patch("app.background_tasks.mark_bank_slip_as_paid")
    mocker.patch("app.background_tasks.settle_current_account")

    response = client.post("/v1/webhook", json=payload)

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "paidAt"],
                "message": "Value error, time data '25-12-2022 10:00:00' does not match format '%Y-%m-%d %H:%M:%S'",
                "type": "value_error",
            }
        ],
    }


def test_upload_with_success(mocker):
    files = {"file": ("upload_ok.csv", open("tests/fixtures/upload_ok.csv", "rb"))}

    mocker.patch("app.main.chain")
    mocker.patch("app.background_tasks.mark_bank_slip_as_paid")
    mocker.patch("app.background_tasks.settle_current_account")

    response = client.post("/v1/uploadfile", files=files)

    assert response.status_code == 200
    assert response.json() == {"message": "Uploaded with success upload_ok.csv"}


def test_upload_fail_content_type(mocker):
    files = {
        "file": (
            "upload_content_type.txt",
            open("tests/fixtures/upload_content_type.txt", "rb"),
        )
    }

    mocker.patch("app.main.chain")
    mocker.patch("app.background_tasks.mark_bank_slip_as_paid")
    mocker.patch("app.background_tasks.settle_current_account")

    response = client.post("/v1/uploadfile", files=files)

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid file type, required csv file"}


def test_upload_fail_large_file(mocker):
    files = {
        "file": ("upload_large.csv", open("tests/fixtures/upload_large.csv", "rb"))
    }

    mocker.patch("app.main.chain")
    mocker.patch("app.background_tasks.mark_bank_slip_as_paid")
    mocker.patch("app.background_tasks.settle_current_account")

    response = client.post("/v1/uploadfile", files=files)

    assert response.status_code == 400
    assert response.json() == {"detail": "File too large, greater than 1MB"}


def test_upload_fail_invalid_content(mocker):
    files = {
        "file": (
            "upload_invalid_content.csv",
            open("tests/fixtures/upload_invalid_content.csv", "rb"),
        )
    }

    mocker.patch("app.main.chain")
    mocker.patch("app.background_tasks.mark_bank_slip_as_paid")
    mocker.patch("app.background_tasks.settle_current_account")

    response = client.post("/v1/uploadfile", files=files)

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "fields": [
                    {
                        "field": "debtDueDate",
                        "msg": "Value error, time data '25-12-2014' does not match format '%Y-%m-%d'",
                        "type": "value_error",
                    }
                ],
                "line": 2,
            }
        ],
    }

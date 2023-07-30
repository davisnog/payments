run:
	uvicorn app.main:app --reload

upload:
	curl -i -X POST -H "Content-Type: multipart/form-data" \
		-F "file=@upload_large.csv;type=text/csv" http://localhost:8000/v1/uploadfile

upload_small:
	curl -i -X POST -H "Content-Type: multipart/form-data" \
		-F "file=@upload_small.csv;type=text/csv" http://localhost:8000/v1/uploadfile

upload_invalid_file:
	curl -i -X POST -H "Content-Type: multipart/form-data" \
		-F "file=@README.md;type=text/csv" http://localhost:8000/v1/uploadfile

upload_invalid_file_type:
	curl -i -X POST -H "Content-Type: multipart/form-data" \
		-F "file=@README.md;type=text/markdown" http://localhost:8000/v1/uploadfile


webhook:
	curl -X POST http://localhost:8000/v1/webhook \
   		-H 'Content-Type: application/json' \
   		-d '{"debtId": "3012", "paidAt": "2022-06-09 10:00:00", "paidAmount": 100000.00, "paidBy": "John Doe"}'


docker_run:
	docker compose up --build
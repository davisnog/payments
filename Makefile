run:
	uvicorn app.main:app --reload

upload:
	curl -i -X POST -H "Content-Type: multipart/form-data" \
		-F "file=@upload_large.csv;type=text/csv" http://localhost:8000/uploadfile

upload_invalid_file:
	curl -i -X POST -H "Content-Type: multipart/form-data" \
		-F "file=@README.md;type=text/csv" http://localhost:8000/uploadfile

upload_invalid_file_type:
	curl -i -X POST -H "Content-Type: multipart/form-data" \
		-F "file=@README.md;type=text/markdown" http://localhost:8000/uploadfile


webhook:
	curl -X POST http://localhost:8000/webhook \
   		-H 'Content-Type: application/json' \
   		-d '{"debtId": "8291", "paidAt": "2022-06-09 10:00:00", "paidAmount": 100000.00, "paidBy": "John Doe"}'


docker_run:
	docker compose up --build
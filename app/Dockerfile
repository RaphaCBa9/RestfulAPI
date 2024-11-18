
FROM python:3.9-slim


WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

# uvicorn app:app --host "localhost" --port 8000 --reload
CMD ["uvicorn", "app:app", "--host", "localhost", "--port", "8000", "--reload"]
FROM python:latest
LABEL authors="Sahmaya"

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN pip install "fastapi[standard]"

CMD ["fastapi", "run", "main.py", "--port", "8000", "--host", "0.0.0.0"]
FROM python:3.10-slim

RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir fastapi uvicorn httpx symspellpy jinja2 requests python-multipart aiofiles itsdangerous markupsafe

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

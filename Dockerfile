FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY data_master_app ./data_master_app
COPY mapping_studio ./mapping_studio
COPY docs ./docs
COPY README.md .

RUN mkdir -p /app/outputs

EXPOSE 8010

CMD ["uvicorn", "data_master_app.main:app", "--host", "0.0.0.0", "--port", "8010"]

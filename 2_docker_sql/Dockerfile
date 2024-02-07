FROM python:3.9.1

RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app

COPY ingest.py ingest.py

ENTRYPOINT ["python", "ingest.py"]


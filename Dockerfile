FROM python:3.12-slim

RUN pip install --no-cache-dir requests

COPY run-smoketest.py /app/run-smoketest.py
WORKDIR /app

ENTRYPOINT ["python", "-u", "run-smoketest.py"]

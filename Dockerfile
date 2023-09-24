FROM python:alpine3.18
ENV PYTHONPATH=/app

WORKDIR /app
COPY requirements.txt ./src/requirements.txt
RUN pip install --no-cache-dir -r ./src/requirements.txt

COPY ./src ./src

ENTRYPOINT ["python", "/app/src/main.py"]
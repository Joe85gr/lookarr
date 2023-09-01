FROM python:3.9.18-slim as build

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && pip install --no-cache-dir --target=/app/src -r requirements.txt

FROM python:alpine3.18
ENV PYTHONPATH=/app

COPY --from=build /app/src ./app/src
COPY --from=build /app/user_config ./app/user_config
COPY --from=build /app/user_config/config-sample.yml ./app/user_config/config.yml

ENTRYPOINT ["python", "/app/src/main.py"]
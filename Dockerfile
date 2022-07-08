# Dockerfile for production

FROM python:3.9-slim
COPY src/ .

RUN pip install poetry==1.1.13
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi


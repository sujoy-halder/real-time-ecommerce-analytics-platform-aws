FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN addgroup -S app && adduser -S app -G app

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY --chown=app:app app ./app

USER app

CMD ["python", "-m", "app.main"]

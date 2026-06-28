FROM python:3.12-slim
WORKDIR /app
RUN pip install --upgrade --no-cache-dir pip && pip install celery==5.3.6
COPY ./app .
CMD ["celery", "-A", \
    "app.infrastructure.message_brokers.celery_app", "worker", \
    "--loglevel=${CELERY_LOG_LEVEL}", \
    "--concurrency=${CELERY_WORKER_CONCURRENCY}", \
    "-Q ${DEFAULT_QUEUE}"]

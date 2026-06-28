from app.infrastructure.message_brokers.celery_app import celery_app

@celery_app.task(queue='default', routing_key='default.key')
def add(x, y):
    return x + y
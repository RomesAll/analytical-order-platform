from celery import Celery
from kombu import Queue, Exchange

celery_app = Celery(
    'app',
    broker='amqp://guest:guest@rabbitmq:5672//',
    backend='rpc://'
)

celery_app.conf.task_queues = (
    Queue(
        'default',
        Exchange('default', type='direct'),
        routing_key='default.key'),
)
celery_app.conf.task_default_queue = 'default'
celery_app.conf.task_default_exchange = 'default.key'

celery_app.conf.task_serializer = 'json'
celery_app.conf.accept_content = ['json']
celery_app.conf.enable_utc = True

celery_app.autodiscover_tasks(['app.infrastructure.message_brokers'])
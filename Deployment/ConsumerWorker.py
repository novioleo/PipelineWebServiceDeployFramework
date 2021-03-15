from concurrent.futures.thread import ThreadPoolExecutor

from celery import Celery
from kombu import Queue

from Deployment.server_config import WORKER_RABBITMQ_USERNAME, WORKER_RABBITMQ_PASSWORD, WORKER_RABBITMQ_HOST, \
    WORKER_RABBITMQ_PORT, WORKER_RABBITMQ_VHOST

celery_worker_app = Celery(
    "algorithm_worker",
    backend="rpc://",
    broker=f"amqp://{WORKER_RABBITMQ_USERNAME}:{WORKER_RABBITMQ_PASSWORD}@"
           f"{WORKER_RABBITMQ_HOST}:{WORKER_RABBITMQ_PORT}/{WORKER_RABBITMQ_VHOST}",
)

celery_worker_app.conf.update(
    task_track_started=True,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
)

celery_worker_app.conf.task_queues = (
    Queue('operate_request_queue', routing_key='ConsumerServices.#'),
)

# 用于放置一些非计算密集型任务
background_thread_pool_executor = ThreadPoolExecutor()

celery_worker_app.autodiscover_tasks(['Deployment.ConsumerServices'])
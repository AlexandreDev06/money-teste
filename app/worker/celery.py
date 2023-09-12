from celery import Celery
from app.configs.settings import settings


app = Celery(
    "tasks",
    broker=settings.redis_url,
    backend=settings.redis_url,
    broker_transport_options={"visibility_timeout": float("inf")},
    broker_connection_retry_on_startup=True,
)
from celery import Celery
from setup import settings

# Initialize Celery application
celery_app = Celery(
    "truecopy",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

# Celery Configuration
celery_app.conf.update(
    # Serilization Settng - For data format consistency
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",

    # Timezone Settings
    timezone="UTC",
    enable_utc=True,

    # Task Tracking - Tracks if task is started
    task_track_started=True,
    
    # Results expire after 1 hour
    result_expires=3600,  
    
    # One task at a time
    worker_concurrency=1,  
    
    # Manages worker workload
    worker_prefetch_multiplier=1,
)

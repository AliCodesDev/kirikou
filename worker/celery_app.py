from celery import Celery
from config import Config

celery_app = Celery(
    'kirikou',
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer="json",              # How to serialize task arguments
    result_serializer="json",            # How to serialize results
    accept_content=["json"],             # Only accept JSON
    timezone="UTC",                      # Consistent timestamps
    enable_utc=True,
    include=["worker.tasks"],
)

# Optional: Define periodic tasks (e.g., for regular RSS fetching)
celery_app.conf.beat_schedule = {
    'scrape-every-hour': {
        'task': 'scrape_all_sources',  # This should match the actual task name
        'schedule': 3600,  # Every hour
    },
}

if __name__ == "__main__":
    Config.validate()  # Ensure all required config is set
    Config.setup_logging()  # Set up logging before starting the worker
    celery_app.start()




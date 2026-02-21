from worker.celery_app import celery_app
from ingestion.feed_parser import scrape_all_sources, scrape_source_by_id


@celery_app.task(name="scrape_all_sources")
def scrape_all_sources_task():
    """Celery task to scrape all sources."""
    return scrape_all_sources()

@celery_app.task(name="scrape_source_by_id")
def scrape_source_by_id_task(source_id):
    """Celery task to scrape a specific source by ID."""
    return scrape_source_by_id(source_id)


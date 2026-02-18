from fastapi import APIRouter, HTTPException, BackgroundTasks
from ingestion import feed_parser as fp


router = APIRouter(prefix="/ingestion", tags=["Ingestion"])

@router.post("/scrape", status_code=202)
def trigger_scraping(background_tasks: BackgroundTasks):
    """Endpoint to trigger the scraping process."""
    background_tasks.add_task(fp.scrape_all_sources)
    return {"message": "Scraping started", "status": "accepted"}


@router.post("/scrape/{source_id}", status_code=202)
def trigger_scraping_source(source_id: int, background_tasks: BackgroundTasks):
    """Endpoint to trigger scraping for a specific source."""
    background_tasks.add_task(fp.scrape_source_by_id, source_id)
    return {"message": f"Scraping for source {source_id} started", "status": "accepted"}





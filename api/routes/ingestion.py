from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from ingestion import feed_parser as fp, validate_feeds as vf
from database.schemas import SourceResponse, SourceCreate, SourceUpdate, ScrapeResponse
from database import utils as db_utils
from sqlalchemy.orm import Session
from database.db import get_db
from worker.tasks import scrape_all_sources_task, scrape_source_by_id_task


router = APIRouter(prefix="/ingestion", tags=["Ingestion"])

@router.post("/scrape", status_code=202, response_model=ScrapeResponse)
def scrape_all_sources():
    """Endpoint to trigger scraping for all sources."""
    result = scrape_all_sources_task.delay()  # Trigger the Celery task asynchronously
    return {"message": "Scraping for all sources started", "status": "accepted", "task_id": result.id}


@router.post("/scrape/{source_id}", status_code=202, response_model=ScrapeResponse)
def trigger_scraping_source(source_id: int, db: Session = Depends(get_db)):
    """Endpoint to trigger scraping for a specific source."""
    source = db_utils.get_source_by_id(db, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    result = scrape_source_by_id_task.delay(source_id)  # Trigger the Celery task asynchronously
    return {"message": f"Scraping for source {source_id} started", "status": "accepted", "task_id": result.id}


@router.post("/sources", status_code=201, response_model=ScrapeResponse)
def create_source(source_data: SourceCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Endpoint to create a new news source."""
    new_source = db_utils.create_source(db, source_data.model_dump())

    if not new_source:
        raise HTTPException(status_code=400, detail="Failed to create source")
    
    db.commit()  # Commit immediately to get the new source ID for background tasks
    
    background_tasks.add_task(vf.validate_feed_url, source_data.url)
    background_tasks.add_task(vf.log_source_creation, new_source)
    
    return {"message": f"Source {new_source['name']} added successfully", "status": "created"}











from fastapi import APIRouter, HTTPException, BackgroundTasks
from ingestion import feed_parser as fp, validate_feeds as vf
from database.schemas import SourceResponse, SourceCreate, SourceUpdate, ScrapeResponse
from database import utils as db_utils


router = APIRouter(prefix="/ingestion", tags=["Ingestion"])

@router.post("/scrape", status_code=202, response_model=ScrapeResponse)
def trigger_scraping(background_tasks: BackgroundTasks):
    """Endpoint to trigger the scraping process."""
    background_tasks.add_task(fp.scrape_all_sources)
    return {"message": "Scraping started", "status": "accepted"}


@router.post("/scrape/{source_id}", status_code=202, response_model=ScrapeResponse)
def trigger_scraping_source(source_id: int, background_tasks: BackgroundTasks):
    """Endpoint to trigger scraping for a specific source."""
    source = db_utils.get_source_by_id(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    background_tasks.add_task(fp.scrape_source_by_id, source_id)
    return {"message": f"Scraping for source {source_id} started", "status": "accepted"}


@router.post("/sources", status_code=201, response_model=ScrapeResponse)
def create_source(source_data: SourceCreate, background_tasks: BackgroundTasks):
    """Endpoint to create a new news source."""
    new_source = db_utils.create_source(source_data.model_dump())
    if not new_source:
        raise HTTPException(status_code=400, detail="Failed to create source")
    
    background_tasks.add_task(vf.validate_feed_url, source_data.url)
    background_tasks.add_task(vf.log_source_creation, new_source)
    
    return {"message": f"Source {new_source['name']} added successfully", "status": "created"}











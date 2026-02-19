from fastapi import APIRouter, HTTPException, BackgroundTasks
from database import utils as db_utils
from database.schemas import SourceResponse, SourceCreate, SourceUpdate

router = APIRouter(prefix="/sources", tags=["Sources"])

@router.get("/", response_model=list[SourceResponse], status_code=200)
def get_sources():
    """Endpoint to retrieve all news sources."""
    sources = db_utils.get_all_sources()
    if not sources:
        raise HTTPException(status_code=404, detail="No sources found")
    return sources

@router.get("/{source_id}", response_model=SourceResponse, status_code=200)
def get_source(source_id: int):
    """Endpoint to retrieve a specific news source by ID."""
    source = db_utils.get_source_by_id(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


# @router.put("/{source_id}")
# def update_source(source_id: int, source_data: dict):
#     """Endpoint to update an existing news source."""
#     # Placeholder implementation
#     updated_source = db_utils.update_source(source_id, source_data)
#     if not updated_source:
#         raise HTTPException(status_code=404, detail="Source not found")
#     return {"source": updated_source}

# @router.delete("/{source_id}")
# def delete_source(source_id: int):
#     """Endpoint to delete a news source."""
#     # Placeholder implementation
#     if not db_utils.delete_source(source_id):
#         raise HTTPException(status_code=404, detail="Source not found")
#     return {"message": "Source deleted successfully"}




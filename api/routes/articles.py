from fastapi import APIRouter, HTTPException
from database import utils as db_utils
from typing import Optional

router = APIRouter(prefix="/articles", tags=["Articles"])

@router.get("/")
def get_articles(limit: int = 20, days: int = 7, source_name: str | None = None):
    """Endpoint to retrieve all articles."""
    if days < 1 or days > 30:
        raise HTTPException(status_code=400, detail="Days must be between 1 and 30")
    elif limit < 1 or limit > 500:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 500")
    elif not source_name:
        return db_utils.get_recent_articles(limit)
    else:
        return db_utils.get_articles_by_source(source_name, days, limit)
    
    
@router.get("/stats")
def get_article_stats():
    """Endpoint to retrieve article statistics."""
    return db_utils.get_source_stats()


@router.get("/{article_id}")
def get_article(article_id: int):
    """Endpoint to retrieve a specific article by ID."""
    article = db_utils.get_article_by_id(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article



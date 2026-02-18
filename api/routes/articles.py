from fastapi import APIRouter, HTTPException
from database import utils as db_utils
from fastapi import Query
from typing import Optional
from database.schemas import ArticleResponse, ArticleDetail, SourceStats

router = APIRouter(prefix="/articles", tags=["Articles"])

@router.get("/", response_model=list[ArticleResponse], status_code=200)
def get_articles(limit: int =  Query(default=20, ge=1, le=500), days: int = Query(default=7, ge=1, le=30), source_name: str | None = None):
    """Endpoint to retrieve all articles."""
    if not source_name:
        return db_utils.get_recent_articles(limit)
    else:
        return db_utils.get_articles_by_source(source_name, days, limit)
    
    
@router.get("/stats", response_model=list[SourceStats])
def get_article_stats():
    """Endpoint to retrieve article statistics."""
    return db_utils.get_source_stats()


@router.get("/{article_id}", response_model=ArticleDetail, status_code=200)
def get_article(article_id: int):
    """Endpoint to retrieve a specific article by ID."""
    article = db_utils.get_article_by_id(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article



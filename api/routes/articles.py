from fastapi import APIRouter, HTTPException, Depends, Query
from database import utils as db_utils
from typing import Optional
from database.schemas import ArticleResponse, ArticleDetail, SourceStats
from sqlalchemy.orm import Session
from database.db import get_db

router = APIRouter(prefix="/articles", tags=["Articles"])

@router.get("/", response_model=list[ArticleResponse], status_code=200)
def get_articles(limit: int =  Query(default=20, ge=1, le=500), 
                 days: int = Query(default=7, ge=1, le=30), 
                 source_name: str | None = None, 
                 db: Session = Depends(get_db)):
    
    """Endpoint to retrieve all articles."""
    if not source_name:
        return db_utils.get_recent_articles(db, limit)
    else:
        return db_utils.get_articles_by_source(db, source_name, days, limit)
    
    
@router.get("/stats", response_model=list[SourceStats])
def get_article_stats(db: Session = Depends(get_db)):
    """Endpoint to retrieve article statistics."""
    return db_utils.get_source_stats(db)


@router.get("/{article_id}", response_model=ArticleDetail, status_code=200)
def get_article(article_id: int, db: Session = Depends(get_db)):
    """Endpoint to retrieve a specific article by ID."""
    article = db_utils.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article



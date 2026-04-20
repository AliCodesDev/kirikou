from fastapi import APIRouter, HTTPException, Depends, Query, Request, Response
from database import utils as db_utils
from typing import Optional
from database.schemas import ArticleResponse, ArticleDetail, SourceStats
from sqlalchemy.orm import Session
from database.db import get_db
from api.rate_limiter import limiter
from config import get_settings

settings = get_settings()

router = APIRouter(prefix="/articles", tags=["Articles"])

@router.get("/", response_model=list[ArticleResponse], status_code=200)
@limiter.limit(settings.rate_limit_default)
def get_articles(request: Request,
                 response: Response,
                 limit: int =  Query(default=20, ge=1, le=500),
                 offset: int = Query(default=0, ge=0),
                 days: int = Query(default=7, ge=1, le=30),
                 source_name: str | None = None,
                 db: Session = Depends(get_db)):

    """Endpoint to retrieve all articles."""
    if not source_name:
        return db_utils.get_recent_articles(db, limit, offset)
    else:
        return db_utils.get_articles_by_source(db, source_name, days, limit, offset)


@router.get("/stats", response_model=list[SourceStats])
@limiter.limit(settings.rate_limit_default)
def get_article_stats(request: Request, response: Response, db: Session = Depends(get_db)):
    """Endpoint to retrieve article statistics."""
    return db_utils.get_source_stats(db)


@router.get("/{article_id}", response_model=ArticleDetail, status_code=200)
@limiter.limit(settings.rate_limit_default)
def get_article(request: Request, response: Response, article_id: int, db: Session = Depends(get_db)):
    """Endpoint to retrieve a specific article by ID."""
    article = db_utils.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article





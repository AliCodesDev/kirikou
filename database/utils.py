"""Database utility functions using SQLAlchemy ORM."""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy import func, text, case
from sqlalchemy.orm import joinedload
import logging

from database.models import Source, Article
from database.db import get_session, get_session_no_commit
from config import Config

logger = logging.getLogger(__name__)


def get_all_sources() -> List[Dict]:
    """
    Get all sources from database using ORM.
    
    Returns:
        List of source dictionaries
    """
    session = get_session_no_commit()
    try:
        sources = session.query(Source).order_by(Source.name).all()
        
        # Convert to dicts
        return [
            {
                'id': s.id,
                'name': s.name,
                'url': s.url,
                'country': s.country,
                'political_leaning': s.political_leaning
            }
            for s in sources
        ]
    finally:
        session.close()


def get_recent_articles(limit: int = 20) -> List[Dict]:
    """
    Get recent articles with source information using ORM.
    
    Args:
        limit: Maximum number of articles
        
    Returns:
        List of article dictionaries
    """
    session = get_session_no_commit()
    try:
        # Eager load source to avoid N+1 queries
        articles = session.query(Article)\
            .options(joinedload(Article.source))\
            .order_by(Article.published_at.desc())\
            .limit(limit)\
            .all()
        
        return [
            {
                'title': a.title,
                'url': a.url,
                'published_at': a.published_at,
                'source_name': a.source.name,
                'country': a.source.country,
                'political_leaning': a.source.political_leaning
            }
            for a in articles
        ]
    finally:
        session.close()


def get_source_stats() -> List[Dict]:
    """
    Get article count statistics for all sources.
    
    Returns:
        List of source statistics
    """ 
    
    session = get_session_no_commit()
    try:
        seven_days_ago = datetime.now() - timedelta(days=7)
        
        # Query with aggregation
        stats = session.query(
            Source.name.label('source_name'),
            func.count(Article.id).label('total_articles'),
            func.sum(
                case(
                    (Article.published_at > seven_days_ago, 1),
                    else_=0
                )
            ).label('articles_last_7d')
        )\
            .outerjoin(Article)\
            .group_by(Source.id, Source.name)\
            .order_by(func.count(Article.id).desc())\
            .all()
        
        return [
            {
                'source_name': stat.source_name,
                'total_articles': stat.total_articles,
                'articles_last_7d': int(stat.articles_last_7d or 0)
            }
            for stat in stats
        ]
    finally:
        session.close()


def get_inactive_sources(hours: int = 24) -> List[Dict]:
    """
    Find sources with no articles in the last N hours.
    
    Args:
        hours: Time window to check
        
    Returns:
        List of inactive sources
    """
    session = get_session_no_commit()
    try:
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # Subquery for last article date
        stats = session.query(
            Source.name.label('source_name'),
            Source.url,
            func.max(Article.published_at).label('last_article_date')
        )\
            .outerjoin(Article)\
            .group_by(Source.id, Source.name, Source.url)\
            .having(
                (func.max(Article.published_at) == None) |
                (func.max(Article.published_at) < cutoff_time)
            )\
            .order_by(func.max(Article.published_at).asc())\
            .all()
        
        return [
            {
                'source_name': stat.source_name,
                'url': stat.url,
                'last_article_date': stat.last_article_date
            }
            for stat in stats
        ]
    finally:
        session.close()


def get_duplicate_stories() -> List[Dict]:
    """
    Find articles with identical titles from different sources.
    
    Returns:
        List of duplicate pairs
    """
    session = get_session_no_commit()
    try:
        # Self-join to find duplicates
        a1 = session.query(Article).subquery('a1')
        a2 = session.query(Article).subquery('a2')
        s1 = session.query(Source).subquery('s1')
        s2 = session.query(Source).subquery('s2')
        
        duplicates = session.query(
            a1.c.title,
            s1.c.name.label('source1'),
            s2.c.name.label('source2'),
            a1.c.url.label('url1'),
            a2.c.url.label('url2'),
            a1.c.published_at.label('published1'),
            a2.c.published_at.label('published2')
        )\
            .join(a2, (a1.c.title == a2.c.title) & (a1.c.id < a2.c.id))\
            .join(s1, a1.c.source_id == s1.c.id)\
            .join(s2, a2.c.source_id == s2.c.id)\
            .order_by(a1.c.title)\
            .all()
        
        return [
            {
                'title': dup.title,
                'source1': dup.source1,
                'source2': dup.source2,
                'url1': dup.url1,
                'url2': dup.url2,
                'published1': dup.published1,
                'published2': dup.published2
            }
            for dup in duplicates
        ]
    finally:
        session.close()


def get_articles_by_source(source_name: str, days: int = 7) -> List[Dict]:
    """
    Get articles from a specific source within the last N days.
    
    Args:
        source_name: Name of the source
        days: Number of days to look back
        
    Returns:
        List of articles
    """
    session = get_session_no_commit()
    try:
        cutoff_date = datetime.now() - timedelta(days=days)
        
        articles = session.query(Article)\
            .join(Source)\
            .filter(
                Source.name == source_name,
                Article.published_at >= cutoff_date
            )\
            .order_by(Article.published_at.desc())\
            .all()
        
        return [
            {
                'title': a.title,
                'url': a.url,
                'published_at': a.published_at,
                'source_name': source_name,
                'country': a.source.country,
                'political_leaning': a.source.political_leaning
            }
            for a in articles
        ]
    finally:
        session.close()


def save_articles_batch(articles: List[Dict], source_id: int) -> int:
    """
    Save multiple articles to database.
    
    Uses raw SQL for bulk insert with ON CONFLICT (most efficient).
    
    Args:
        articles: List of article dicts
        source_id: ID of the source
        
    Returns:
        Number of articles inserted
    """
    if not articles:
        return 0
    
    # For bulk inserts with deduplication, raw SQL is still best
    with get_session() as session:
        # Prepare data
        data = [
            {
                'source_id': source_id,
                'title': article['title'],
                'description': article.get('description'),
                'content': article.get('content'),
                'author': article.get('author'),
                'published_at': article['published_at'],
                'url': article['url']
            }
            for article in articles
        ]
        
        # Use raw SQL with ON CONFLICT for efficiency
        result = session.execute(text("""
            INSERT INTO articles 
                (source_id, title, description, content, author, published_at, url)
            VALUES 
                (:source_id, :title, :description, :content, :author, :published_at, :url)
            ON CONFLICT (url) DO NOTHING
        """), data)
        
        # Get count of inserted rows
        inserted_count = result.rowcount
        
        logger.info(f"Saved {inserted_count} new articles (source_id={source_id})")
        return inserted_count
"""
Database package for Kirikou.

Provides:
- Models: Source, Article
- Session management: get_session, engine
- Utility functions: get_all_sources, save_articles_batch, etc.
"""
from database.models import Base, Source, Article
from database.db import engine, get_session, get_session_no_commit
from database.utils import (
    get_all_sources,
    get_recent_articles,
    get_source_stats,
    get_inactive_sources,
    get_duplicate_stories,
    get_articles_by_source,
    save_articles_batch
)

__all__ = [
    # Models
    'Base',
    'Source',
    'Article',
    
    # Session management
    'engine',
    'get_session',
    'get_session_no_commit',
    
    # Utilities
    'get_all_sources',
    'get_recent_articles',
    'get_source_stats',
    'get_inactive_sources',
    'get_duplicate_stories',
    'get_articles_by_source',
    'save_articles_batch',
]
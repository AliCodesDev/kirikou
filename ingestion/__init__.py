"""
Ingestion package for Kirikou.

Provides RSS feed scraping functionality.
"""
from ingestion.feed_parser import scrape_all_sources, fetch_feed, extract_articles

__all__ = [
    'scrape_all_sources',
    'fetch_feed',
    'extract_articles',
]
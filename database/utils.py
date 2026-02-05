"""Database utility functions for common queries."""
import psycopg2
from typing import List, Dict, Optional, Tuple
from config import Config
import logging

logger = logging.getLogger(__name__)


def execute_query(query: str, params: Tuple = None, fetch_one: bool = False) -> List[Dict]:
    """
    Execute a SQL query and return results as list of dictionaries.
    
    Args:
        query: SQL query string (use %s for parameters)
        params: Tuple of parameters to substitute
        fetch_one: If True, return single dict instead of list
        
    Returns:
        List of dictionaries (or single dict if fetch_one=True)
        
    Example:
        results = execute_query(
            "SELECT * FROM sources WHERE country = %s",
            ('UK',)
        )
    """
    conn = None
    cursor = None
    
    try:
        # TODO: Connect to database
        conn = psycopg2.connect(Config.DATABASE_URL)

        # TODO: Create cursor
        cursor = conn.cursor()

        # TODO: Execute query with params
        cursor.execute(query, params or ())

        # TODO: Get column names from cursor.description
        columns = [desc[0] for desc in cursor.description]

        # TODO: Fetch results (fetchone() or fetchall())
        if fetch_one:
            row = cursor.fetchone()
            if row:
                return dict(zip(columns, row))
            else:
                return None
        else:
            # TODO: Convert to list of dictionaries
            # TODO: Return results
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
        
    except psycopg2.Error as e:
        logger.error(f"Database query error: {e}")
        logger.error(f"Query: {query}")
        logger.error(f"Params: {params}")
        raise
        
    finally:
        # TODO: Close cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        pass


def get_recent_articles(limit: int = 20) -> List[Dict]:
    """
    Get recent articles with source information.
    
    Args:
        limit: Maximum number of articles to return (default: 20)
        
    Returns:
        List of article dictionaries with keys:
        - title
        - url
        - published_at
        - source_name
        - country
        - political_leaning
        
    Example:
        articles = get_recent_articles(5)
        for article in articles:
            print(f"{article['title']} from {article['source_name']}")
    """
    query = """
        SELECT
            a.title,
            a.url,
            a.published_at,
            s.name AS source_name,
            s.country,
            s.political_leaning
        FROM articles a
        JOIN sources s ON a.source_id = s.id
        ORDER BY a.published_at DESC
        LIMIT %s
    """
    
    # TODO: Call execute_query with the query and (limit,) as params
    # TODO: Return the results
    return execute_query(query, (limit,))


def get_source_stats() -> List[Dict]:
    """
    Get article count statistics for all sources.
    
    Returns:
        List of source statistics with keys:
        - source_name
        - total_articles
        - articles_last_7d
        
    Example:
        stats = get_source_stats()
        for stat in stats:
            print(f"{stat['source_name']}: {stat['total_articles']} total, "
                  f"{stat['articles_last_7d']} in last 7 days")
    """
    query = """
        SELECT
            s.name AS source_name,
            COUNT(a.id) AS total_articles,
            COUNT(CASE WHEN a.published_at > NOW() - INTERVAL '7 days' THEN 1 END) AS articles_last_7d
        FROM sources s
        LEFT JOIN articles a ON s.id = a.source_id
        GROUP BY s.id, s.name
        ORDER BY total_articles DESC
    """
    
    # TODO: Call execute_query
    return execute_query(query)


def get_inactive_sources(hours: int = 24) -> List[Dict]:
    """
    Find sources with no articles in the last N hours.
    
    Args:
        hours: Time window to check (default: 24)
        
    Returns:
        List of inactive sources with keys:
        - source_name
        - url
        - last_article_date (may be None)
        
    Example:
        inactive = get_inactive_sources(hours=48)
        for source in inactive:
            print(f"{source['source_name']} - last article: {source['last_article_date']}")
    """
    query = """
        SELECT
            s.name AS source_name,
            s.url,
            MAX(a.published_at) AS last_article_date
        FROM sources s
        LEFT JOIN articles a ON s.id = a.source_id
        GROUP BY s.id, s.name, s.url
        HAVING MAX(a.published_at) IS NULL OR MAX(a.published_at) < NOW() - INTERVAL '1 hour' * %s
        ORDER BY last_article_date ASC NULLS FIRST
    """
    
    # TODO: Call execute_query with (hours,) as params
    return execute_query(query, (hours,))


def get_duplicate_stories() -> List[Dict]:
    """
    Find articles with identical titles from different sources.
    
    Returns:
        List of duplicate pairs with keys:
        - title
        - source1
        - source2
        - url1
        - url2
        - published1
        - published2
        
    Example:
        duplicates = get_duplicate_stories()
        for dup in duplicates:
            print(f"'{dup['title']}' covered by {dup['source1']} and {dup['source2']}")
    """
    query = """
        SELECT
            a1.title,
            s1.name AS source1,
            s2.name AS source2,
            a1.url AS url1,
            a2.url AS url2,
            a1.published_at AS published1,
            a2.published_at AS published2
        FROM articles a1
        JOIN articles a2 ON a1.title = a2.title AND a1.id < a2.id
        JOIN sources s1 ON a1.source_id = s1.id
        JOIN sources s2 ON a2.source_id = s2.id
        ORDER BY a1.title
    """
    
    # TODO: Call execute_query
    return execute_query(query)


def get_articles_by_source(source_name: str, days: int = 7) -> List[Dict]:
    """
    Get articles from a specific source within the last N days.
    
    Args:
        source_name: Name of the source (e.g., "BBC News")
        days: Number of days to look back (default: 7)
        
    Returns:
        List of articles from that source
        
    Example:
        bbc_articles = get_articles_by_source("BBC News", days=30)
    """
    query = """
        SELECT
            a.title,
            a.url,
            a.published_at,
            s.name AS source_name,
            s.country,
            s.political_leaning
        FROM articles a
        JOIN sources s ON a.source_id = s.id
        WHERE s.name = %s 
          AND a.published_at >= NOW() - INTERVAL '1 day' * %s
        ORDER BY a.published_at DESC
    """
    
    # TODO: Call execute_query with (source_name, days) as params
    return execute_query(query, (source_name, days))
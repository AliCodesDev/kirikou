import requests, feedparser, logging
from config import Config
from datetime import datetime
from dateutil import parser as date_parser
from database.utils import get_all_sources_standalone, save_articles_batch, get_source_by_id_standalone


# Setup logging
Config.setup_logging()
logger = logging.getLogger(__name__)



def fetch_feed(url: str) -> feedparser.FeedParserDict | None:
    """
    Fetch URL
    
    Args:
        url: URL to fetch
    
    Returns:
        Parsed XML response or None
    """

    logger.info(f"Fetching RSS feed: {url}")
    try:
        response = requests.get(url, timeout=Config.REQUEST_TIMEOUT)
        response.raise_for_status()
        logger.info(f"Fetching RSS feed {url} successful !")
        parsed_xml = feedparser.parse(response.content)
        return parsed_xml

    except requests.HTTPError as e:
        logger.error(f"HTTP error: {e}")
        return None
    except requests.ConnectionError:
        logger.error(f"Network error - couldn't connect.\nURL: {url}")
        return None
    except requests.Timeout:
        logger.error(f"Request timed out.\nURL: {url}")
        return None
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        return None


def extract_articles(feed: feedparser.FeedParserDict) -> list[dict]:
    """
    Extract article metadata from parsed feed.
    
    Args:
        feed: Parsed feed from feedparser
        
    Returns:
        List of article dicts with:
        - title (str)
        - url (str)
        - description (str or None)
        - author (str or None)
        - published_at (datetime object)
    """
    articles = []
    
    if not feed.entries:
        logger.warning("Feed has zero entries")
        return articles
    
    for entry in feed.entries:
        try:
            # Extract title (required)
            title = entry.get('title', 'No Title')
            
            # Extract URL (required)
            url = entry.get('link')
            if not url:
                logger.warning("Entry missing URL, skipping")
                continue  # Skip entries without URL
            
            # Extract description (optional - None if missing)
            description = entry.get('summary') or entry.get('description')
            
            # Extract author (optional - None if missing)
            author = entry.get('author')
            
            # Extract and parse published date
            published_str = entry.get('published') or entry.get('updated')
            if published_str:
                try:
                    published_at = date_parser.parse(published_str)
                except Exception as e:
                    logger.warning(f"Failed to parse date '{published_str}': {e}")
                    published_at = datetime.now()
            else:
                # No date provided, use current time
                published_at = datetime.now()
            
            articles.append({
                'title': title,
                'url': url,
                'description': description,
                'author': author,
                'published_at': published_at  # datetime object, not string!
            })
            
        except Exception as e:
            logger.warning(f"Failed to parse entry: {e}")
            continue
    
    logger.info(f"Extracted {len(articles)} articles from feed")
    return articles


def scrape_all_sources():
    """
    Scrape articles from all sources in database.
    
    This is the main entry point for the scraper.
    Reads sources from database, fetches their feeds, and saves articles.
    """
    logger.info("=" * 70)
    logger.info("Starting RSS scraper...")
    logger.info("=" * 70)
    
    # Get sources from database
    sources = get_all_sources_standalone()
    logger.info(f"Found {len(sources)} sources to scrape\n")
    
    total_inserted = 0
    total_fetched = 0
    failed_sources = []
    
    for i, source in enumerate(sources, 1):
        try:
            logger.info(f"[{i}/{len(sources)}] Scraping {source['name']}...")
            
            # Fetch RSS feed
            feed = fetch_feed(source['url'])
            
            if not feed:
                logger.error(f"Failed to fetch feed for {source['name']}")
                failed_sources.append(source['name'])
                continue
            
            # Extract articles
            articles = extract_articles(feed)
            total_fetched += len(articles)
            
            if articles:
                # Save to database
                inserted = save_articles_batch(articles, source['id'])
                total_inserted += inserted
                
                duplicates = len(articles) - inserted
                logger.info(
                    f"✅ {source['name']}: "
                    f"{inserted} new, {duplicates} duplicates\n"
                )
            else:
                logger.warning(f"No articles found for {source['name']}\n")
                
        except Exception as e:
            logger.error(f"Failed to scrape {source['name']}: {e}\n")
            failed_sources.append(source['name'])
            continue
    
    # Final summary
    logger.info("=" * 70)
    logger.info("Scraping complete!")
    logger.info("=" * 70)
    logger.info(f"Sources processed: {len(sources)}")
    logger.info(f"Articles fetched:  {total_fetched}")
    logger.info(f"Articles inserted: {total_inserted}")
    logger.info(f"Duplicates skip:   {total_fetched - total_inserted}")
    if failed_sources:
        logger.warning(f"Failed sources:    {', '.join(failed_sources)}")
    logger.info("=" * 70)
    
    return total_inserted


def scrape_source_by_id(source_id: int):
    """
    Scrape articles from a single source by ID.
    
    Args:
        source_id: ID of the source to scrape
    """
    logger.info(f"Starting scrape for source ID {source_id}...")

    
    
    # Get source from database
    source = get_source_by_id_standalone(source_id)
    
    if not source:
        logger.error(f"Source with ID {source_id} not found")
        return 0
    
    try:
        # Fetch RSS feed
        feed = fetch_feed(source['url'])
        
        if not feed:
            logger.error(f"Failed to fetch feed for {source['name']}")
            return 0
        
        # Extract articles
        articles = extract_articles(feed)
        
        if articles:
            # Save to database
            inserted = save_articles_batch(articles, source['id'])
            duplicates = len(articles) - inserted
            
            logger.info(
                f"✅ {source['name']}: "
                f"{inserted} new, {duplicates} duplicates\n"
            )
            return inserted
        else:
            logger.warning(f"No articles found for {source['name']}\n")
            return 0
            
    except Exception as e:
        logger.error(f"Failed to scrape {source['name']}: {e}\n")
        return 0


if __name__ == "__main__":
    scrape_all_sources()

    








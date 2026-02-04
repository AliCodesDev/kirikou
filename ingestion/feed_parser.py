import requests, feedparser, logging
from config import Config

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
    Extract article data from a parsed RSS feed into a list of dictionaries.

    Args:
        feed: A parsed RSS feed object returned by feedparser.parse(),
              containing feed metadata and a list of entry items.

    Returns:
        A list of dictionaries, where each dictionary represents an article
        with keys: 'title', 'url', 'description', 'published_date', 'source_name'.
        Returns an empty list if the feed has no entries.
    """
    articles = []
    if not feed.entries:
        logger.warning("Feed has zero entries")
        return articles
    
    source_name = getattr(feed.feed, 'title', 'Unknown')
    for article in feed.entries:
        article_dict = {
            'title': article.get('title', 'Unknown'),
            'url': article.get('link', 'Unknown'),
            'description': article.get('summary', 'Unknown'),
            'published_date': article.get('published', 'Unknown'),
            'source_name': source_name
        }
        articles.append(article_dict)
    
    logger.info(f"Extracted {len(articles)} articles from feed")
    return articles

def scrape_feeds(feed_urls: list[str]) -> list[dict]:
    """
    Fetch and extract articles from multiple RSS feeds.
    
    Args:
        feed_urls: List of RSS feed URLs to scrape
        
    Returns:
        Combined list of all articles from all feeds
    """

    logger.info("\nInitiating feed scraping...\n")
    articles_collection = []
    success_count = 0

    for url in feed_urls:
        feed = fetch_feed(url)
        if feed:
            articles = extract_articles(feed)
            articles_collection.extend(articles)
            success_count += 1
        else:
            logger.warning(f"Failed to extract feed from URL: {url}")
    
    logger.info("\nScraping process finished:")
    logger.info(f"Total feeds attempted: {len(feed_urls)}")
    logger.info(f"Total feeds succeeded: {success_count}")
    logger.info(f"Total articles collected: {len(articles_collection)}\n")
    return articles_collection






if __name__ == "__main__":

    Config.setup_logging()
    logger = logging.getLogger(__name__)
    feed_urls = [
    "https://feeds.bbci.co.uk/news/rss.xml",           # BBC News
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",  # NY Times World
    "https://feeds.reuters.com/reuters/topNews",       # Reuters
    "https://www.aljazeera.com/xml/rss/all.xml"]        # Al Jazeera
    
    articles = scrape_feeds(feed_urls)
    logger.info(f"Final Summary: Attempted {len(feed_urls)} feeds, Collected {len(articles)} articles.")

    








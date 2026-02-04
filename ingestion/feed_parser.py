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


# Part 3: The Orchestrator
# Write a function that ties Parts 1 and 2 together, and handles multiple feeds.
# Requirements:

# Function signature: def scrape_feeds(feed_urls: list[str]) -> list[dict]
# Takes a list of RSS feed URLs
# Calls fetch_feed() for each URL
# If a feed fails (returns None), skip it and continue — don't crash
# Calls extract_articles() on each successful fetch
# Collects all articles from all feeds into one list and returns it
# Log the total number of articles collected at the end

# Think about:

# How do you skip a failed feed without stopping the loop?
# How do you combine articles from multiple feeds into one list?


# Part 4: A main Block
# Add an if __name__ == "__main__": block at the bottom that:

# Sets up logging using Config.setup_logging()
# Defines a list of 3-4 real RSS feed URLs to test with (BBC, Reuters, CNN, Al Jazeera — search for their RSS URLs)
# Calls scrape_feeds() with those URLs
# Prints a summary: how many feeds were attempted, how many succeeded, total articles collected


# Acceptance Criteria
# When you run:
# bashpython -m ingestion.feed_parser
# You should see:

# Timestamped log messages showing each feed being fetched
# INFO logs for successful fetches with article counts
# ERROR logs for any feeds that fail (if any)
# A final summary of total articles collected
# A log file updated in logs/kirikou.log


# Hints If You Get Stuck

# feedparser entries live in feed.entries — each entry is like a dictionary
# A feed's name is usually in feed.feed.title
# Each entry's link is usually in entry.link
# Each entry's publish date is usually in entry.published
# Remember: requests.get() can raise exceptions — that's what try/except is for



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

    








"""Validate RSS feed URLs and filter out broken ones."""
import requests
import feedparser
import logging
from typing import Dict

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)


KNOWN_FEEDS = {
    # UK Sources
    'bbc.com': {
        'name': 'BBC News',
        'url': 'http://feeds.bbci.co.uk/news/rss.xml',
        'country': 'UK',
        'political_leaning': 'center',
    },
    'theguardian.com': {
        'name': 'The Guardian',
        'url': 'https://www.theguardian.com/world/rss',
        'country': 'UK',
        'political_leaning': 'center-left',
    },
    'reuters.com': {
        'name': 'Reuters',
        'url': 'https://www.reutersagency.com/feed/',
        'country': 'UK',
        'political_leaning': 'center',
    },
    # US Sources
    'cnn.com': {
        'name': 'CNN',
        'url': 'http://rss.cnn.com/rss/edition.rss',
        'country': 'US',
        'political_leaning': 'center-left',
    },
    'foxnews.com': {
        'name': 'Fox News',
        'url': 'https://moxie.foxnews.com/google-publisher/latest.xml',
        'country': 'US',
        'political_leaning': 'right',
    },
    'npr.org': {
        'name': 'NPR',
        'url': 'https://feeds.npr.org/1001/rss.xml',
        'country': 'US',
        'political_leaning': 'center-left',
    },
    'nytimes.com': {
        'name': 'The New York Times',
        'url': 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
        'country': 'US',
        'political_leaning': 'center-left',
    },
    'washingtonpost.com': {
        'name': 'Washington Post',
        'url': 'https://feeds.washingtonpost.com/rss/world',
        'country': 'US',
        'political_leaning': 'center-left',
    },
    # International
    'aljazeera.com': {
        'name': 'Al Jazeera',
        'url': 'https://www.aljazeera.com/xml/rss/all.xml',
        'country': 'Qatar',
        'political_leaning': 'center',
    },
    'dw.com': {
        'name': 'Deutsche Welle',
        'url': 'https://rss.dw.com/xml/rss-en-all',
        'country': 'Germany',
        'political_leaning': 'center',
    },
    'france24.com': {
        'name': 'France 24',
        'url': 'https://www.france24.com/en/rss',
        'country': 'France',
        'political_leaning': 'center',
    },
    # Tech News
    'techcrunch.com': {
        'name': 'TechCrunch',
        'url': 'https://techcrunch.com/feed/',
        'country': 'US',
        'political_leaning': 'tech-focus',
    },
    'theverge.com': {
        'name': 'The Verge',
        'url': 'https://www.theverge.com/rss/index.xml',
        'country': 'US',
        'political_leaning': 'tech-focus',
    },
    'arstechnica.com': {
        'name': 'Ars Technica',
        'url': 'http://feeds.arstechnica.com/arstechnica/index',
        'country': 'US',
        'political_leaning': 'tech-focus',
    },
}


def validate_feed_url(url: str, timeout: int = 10) -> tuple[bool, str, int]:
    """
    Validate if a URL is a working RSS/Atom feed.
    
    Args:
        url: Feed URL to validate
        timeout: Request timeout in seconds
        
    Returns:
        Tuple of (is_valid, reason, item_count)
        - is_valid: True if feed is valid
        - reason: Error message if invalid, success message if valid
        - item_count: Number of items in feed (0 if invalid)
    """
    try:
        # Fetch with requests (with User-Agent to avoid blocks)
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; KirikouBot/1.0)'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        
        # Check HTTP status
        if response.status_code != 200:
            return False, f"HTTP {response.status_code}", 0
        
        # Check if it's XML
        content_type = response.headers.get('Content-Type', '').lower()
        if 'xml' not in content_type and 'rss' not in content_type:
            # Some feeds don't set proper content-type, check content
            if not response.text.strip().startswith('<?xml'):
                return False, "Not XML content", 0
        
        # Parse with feedparser
        feed = feedparser.parse(response.content)
        
        # Check if it's a valid feed format
        if not feed.version:
            return False, "Invalid feed format", 0
        
        # Check if it has entries
        item_count = len(feed.entries)
        if item_count == 0:
            return False, "No articles found", 0
        
        # Success!
        feed_type = "RSS" if "rss" in feed.version.lower() else "Atom"
        return True, f"{feed_type} feed with {item_count} items", item_count
        
    except requests.Timeout:
        return False, "Timeout", 0
    except requests.RequestException as e:
        return False, f"Request failed: {str(e)[:50]}", 0
    except Exception as e:
        return False, f"Error: {str(e)[:50]}", 0


def validate_all_feeds(feeds_dict: Dict) -> Dict:
    """
    Validate all feeds in dictionary and return only valid ones.
    
    Args:
        feeds_dict: Dictionary of feeds to validate
        
    Returns:
        Dictionary containing only valid feeds
    """
    valid_feeds = {}
    total = len(feeds_dict)
    
    logger.info(f"\n{'='*70}")
    logger.info(f"🔍 Validating {total} RSS Feeds")
    logger.info(f"{'='*70}\n")
    
    for i, (domain, feed_info) in enumerate(feeds_dict.items(), 1):
        name = feed_info['name']
        url = feed_info['url']
        
        logger.info(f"[{i}/{total}] Testing {name}...")
        logger.info(f"       URL: {url}")
        
        is_valid, reason, item_count = validate_feed_url(url)
        
        if is_valid:
            logger.info(f"       ✅ VALID - {reason}\n")
            valid_feeds[domain] = feed_info
            valid_feeds[domain]['validated_item_count'] = item_count
        else:
            logger.info(f"       ❌ INVALID - {reason}\n")
    
    return valid_feeds


def print_summary(original_count: int, valid_feeds: Dict):
    """Print validation summary."""
    valid_count = len(valid_feeds)
    invalid_count = original_count - valid_count
    
    logger.info(f"\n{'='*70}")
    logger.info("📊 VALIDATION SUMMARY")
    logger.info(f"{'='*70}\n")
    
    logger.info(f"Total Feeds:   {original_count}")
    logger.info(f"✅ Valid:      {valid_count}")
    logger.info(f"❌ Invalid:    {invalid_count}")
    logger.info(f"Success Rate:  {(valid_count/original_count)*100:.1f}%\n")
    
    if valid_feeds:
        logger.info("Valid Feeds:")
        logger.info("-" * 70)
        for domain, info in valid_feeds.items():
            item_count = info.get('validated_item_count', '?')
            logger.info(f"  • {info['name']} ({domain})")
            logger.info(f"    {info['url']}")
            logger.info(f"    Articles: {item_count} | Country: {info['country']} | "
                       f"Leaning: {info['political_leaning']}\n")
            

def log_source_creation(source: dict):
    """Log the creation of a new source."""
    source_id = source.get('id', 'unknown')
    logger.info(f"New source created with ID: {source_id}")
    

if __name__ == "__main__":
    # Validate all feeds
    valid_feeds = validate_all_feeds(KNOWN_FEEDS)
    
    # Print summary
    print_summary(len(KNOWN_FEEDS), valid_feeds)
    
    # Print Python dict format for easy copy-paste
    if valid_feeds:
        logger.info(f"\n{'='*70}")
        logger.info("📋 VALID FEEDS DICTIONARY (Copy-paste ready)")
        logger.info(f"{'='*70}\n")
        
        print("VALID_FEEDS = {")
        for domain, info in valid_feeds.items():
            # Remove the validated_item_count field for clean output
            clean_info = {k: v for k, v in info.items() if k != 'validated_item_count'}
            
            print(f"    '{domain}': {{")
            for key, value in clean_info.items():
                print(f"        '{key}': '{value}',")
            print("    },")
        print("}")
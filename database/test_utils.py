"""Test database utility functions."""
from database.utils import (
    get_recent_articles,
    get_source_stats,
    get_inactive_sources,
    get_duplicate_stories,
    get_articles_by_source
)

def test_recent_articles():
    print("\n" + "="*60)
    print("TEST: Get Recent Articles")
    print("="*60)
    
    articles = get_recent_articles(limit=5)
    
    print(f"Found {len(articles)} articles:")
    for article in articles:
        print(f"  - {article['title']} from {article['source_name']}")
        print(f"    Published: {article['published_at']}")
        print(f"    URL: {article['url']}")


def test_source_stats():
    print("\n" + "="*60)
    print("TEST: Source Activity Stats")
    print("="*60)
    
    stats = get_source_stats()
    
    for stat in stats:
        print(f"{stat['source_name']:15} - Total: {stat['total_articles']:3} | Last 7d: {stat['articles_last_7d']:3}")


def test_inactive_sources():
    print("\n" + "="*60)
    print("TEST: Find Inactive Sources (24h)")
    print("="*60)
    
    inactive = get_inactive_sources(hours=24)
    
    if inactive:
        for source in inactive:
            last = source['last_article_date'] or 'Never'
            print(f"  ⚠️  {source['source_name']} - Last article: {last}")
    else:
        print("  ✅ All sources are active!")


def test_duplicate_stories():
    print("\n" + "="*60)
    print("TEST: Find Duplicate Stories")
    print("="*60)
    
    duplicates = get_duplicate_stories()
    
    if duplicates:
        for dup in duplicates:
            print(f"\n  📰 '{dup['title']}'")
            print(f"     {dup['source1']}: {dup['url1']}")
            print(f"     {dup['source2']}: {dup['url2']}")
    else:
        print("  No duplicate stories found")


def test_articles_by_source():
    print("\n" + "="*60)
    print("TEST: Get Articles by Source (BBC News, last 7 days)")
    print("="*60)
    
    articles = get_articles_by_source("BBC News", days=7)
    
    print(f"Found {len(articles)} BBC articles:")
    for article in articles:
        print(f"  - {article['title']}")


if __name__ == "__main__":
    # Make sure you have test data loaded first!
    # psql kirikou_db < database/seed_data.sql
    
    test_recent_articles()
    test_source_stats()
    test_inactive_sources()
    test_duplicate_stories()
    test_articles_by_source()
    
    print("\n" + "="*60)
    print("✅ All tests complete!")
    print("="*60)
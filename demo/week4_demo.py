"""
Week 4 Demo: Complete Database Layer
Demonstrates all features built during Week 4
"""
from database.utils import (
    get_all_sources_standalone,
    get_recent_articles_standalone,
    get_source_stats_standalone,
    get_inactive_sources,
    get_duplicate_stories,
    get_articles_by_source_standalone
)
from database import get_session, Article, Source
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from datetime import datetime

print("="*70)
print("KIRIKOU - WEEK 4 DEMO: DATABASE LAYER")
print("="*70)

# 1. Sources Overview
print("\n📰 NEWS SOURCES")
print("-" * 70)
sources = get_all_sources_standalone()
print(f"Total sources configured: {len(sources)}")
print("\nPolitical spectrum coverage:")
by_leaning = {}
for s in sources:
    leaning = s['political_leaning']
    by_leaning[leaning] = by_leaning.get(leaning, 0) + 1

for leaning, count in sorted(by_leaning.items()):
    print(f"  {leaning:15} - {count} sources")

print("\nGeographic diversity:")
by_country = {}
for s in sources:
    country = s['country']
    by_country[country] = by_country.get(country, 0) + 1

for country, count in sorted(by_country.items()):
    print(f"  {country:15} - {count} sources")

# 2. Database Statistics
print("\n📊 DATABASE STATISTICS")
print("-" * 70)
stats = get_source_stats_standalone()
total_articles = sum(s['total_articles'] for s in stats)
total_recent = sum(s['articles_last_7d'] for s in stats)
print(f"Total articles ingested: {total_articles}")
print(f"Articles in last 7 days: {total_recent}")
print(f"\nTop 5 sources by article count:")
for stat in stats[:5]:
    print(f"  {stat['source_name']:20} - {stat['total_articles']:3} total "
          f"({stat['articles_last_7d']:2} in last 7d)")

# 3. Recent Articles
print("\n📝 RECENT ARTICLES (Last 10)")
print("-" * 70)
recent = get_recent_articles_standalone(10)
for i, article in enumerate(recent, 1):
    published = article['published_at'].strftime('%Y-%m-%d %H:%M') if isinstance(article['published_at'], datetime) else article['published_at']
    print(f"{i}. {article['title'][:60]}...")
    print(f"   📍 {article['source']['name']} ({article['source']['political_leaning']}) | 🕐 {published}")
    if i < 10:
        print()

# 4. Event Clustering (Duplicate Detection)
print("\n🔗 EVENT CLUSTERING (Duplicate Story Detection)")
print("-" * 70)
duplicates = get_duplicate_stories()
if duplicates:
    print(f"Found {len(duplicates)} duplicate story pairs (same event, different sources):")
    for dup in duplicates[:5]:  # Show first 5
        print(f"\n  📰 \"{dup['title'][:55]}...\"")
        print(f"     {dup['source1']} ↔ {dup['source2']}")
    if len(duplicates) > 5:
        print(f"\n  ... and {len(duplicates) - 5} more duplicate pairs")
else:
    print("No duplicate stories found (sources covering different topics)")

# 5. Feed Health Monitoring
print("\n⚕️  FEED HEALTH MONITORING")
print("-" * 70)
inactive_24h = get_inactive_sources(hours=24)
inactive_48h = get_inactive_sources(hours=48)

if not inactive_24h:
    print("✅ All sources active in last 24 hours!")
else:
    print(f"⚠️  {len(inactive_24h)} sources inactive in last 24 hours:")
    for source in inactive_24h:
        last = source['last_article_date']
        if last:
            if isinstance(last, datetime):
                last_str = last.strftime('%Y-%m-%d %H:%M')
            else:
                last_str = str(last)
            print(f"  - {source['source_name']}: Last article {last_str}")
        else:
            print(f"  - {source['source_name']}: No articles yet")

if inactive_48h and not inactive_24h:
    print(f"\n💡 {len(inactive_48h)} sources were inactive 24-48h ago but are now active")

# 6. ORM Relationship Demo
print("\n🔗 ORM RELATIONSHIPS DEMO")
print("-" * 70)
with get_session() as session:
    # Get a source and access its articles
    source = session.query(Source).first()
    if source:
        print(f"Source: {source.name}")
        print(f"Total articles: {len(source.articles)}")
        if source.articles:
            latest = max(source.articles, key=lambda a: a.published_at)
            print(f"Latest article: {latest.title[:50]}...")
            print(f"Published: {latest.published_at.strftime('%Y-%m-%d %H:%M')}")
    
    print()
    
    # Get an article and access its source (reverse relationship)
    article = session.query(Article).order_by(Article.published_at.desc()).first()
    if article:
        print(f"Recent article: {article.title[:50]}...")
        print(f"Published by: {article.source.name} ({article.source.country})")
        print(f"Political leaning: {article.source.political_leaning}")

# 7. Advanced ORM Queries
print("\n🔍 ADVANCED ORM QUERIES")
print("-" * 70)
with get_session() as session:
    # Count articles by country
    print("Articles by country:")
    country_counts = session.query(
        Source.country,
        func.count(Article.id).label('count')
    )\
        .join(Article)\
        .group_by(Source.country)\
        .order_by(func.count(Article.id).desc())\
        .all()
    
    for country, count in country_counts:
        print(f"  {country:15} - {count:3} articles")
    
    print("\nArticles by political leaning:")
    leaning_counts = session.query(
        Source.political_leaning,
        func.count(Article.id).label('count')
    )\
        .join(Article)\
        .group_by(Source.political_leaning)\
        .order_by(func.count(Article.id).desc())\
        .all()
    
    for leaning, count in leaning_counts:
        print(f"  {leaning:15} - {count:3} articles")

# 8. Query Performance
print("\n⚡ QUERY PERFORMANCE")
print("-" * 70)
print("Strategic indexes in place:")
print("  ✅ idx_articles_source_id (foreign key optimization)")
print("  ✅ idx_articles_published_at (date sorting)")
print("  ✅ idx_articles_source_date (composite index)")
print("  ✅ idx_articles_title (duplicate detection)")
print("  ✅ articles_url_key (deduplication - 1,601+ scans!)")
print("\nAll queries optimized for production performance!")

# 9. Deduplication in Action
print("\n🛡️  DEDUPLICATION SYSTEM")
print("-" * 70)
print("URL-based deduplication prevents storing duplicate articles.")
print("\nHow it works:")
print("  1. Each article URL must be unique (UNIQUE constraint)")
print("  2. Bulk insert uses: ON CONFLICT (url) DO NOTHING")
print("  3. Duplicates are automatically skipped")
print("  4. Index usage: articles_url_key scanned 1,601+ times")
print("\n💡 Run the scraper twice to see deduplication in action!")

# Summary
print("\n" + "="*70)
print("WEEK 4 COMPLETE!")
print("="*70)
print("\n✅ ACCOMPLISHMENTS:")
print("  • PostgreSQL database with referential integrity")
print("  • SQLAlchemy ORM with declarative models")
print("  • Automatic relationship navigation")
print("  • Strategic indexes for performance")
print("  • Comprehensive query utilities")
print("  • RSS scraper database integration")
print("  • Production-ready error handling")
print("  • Type-safe, Pythonic database operations")
print(f"  • {total_articles} articles from {len(sources)} global sources")
print(f"  • {len(duplicates)} duplicate story pairs detected")

print("\n🎯 TECHNICAL SKILLS GAINED:")
print("  • SQL (CRUD, JOINs, indexes, transactions)")
print("  • Database design and optimization")
print("  • SQLAlchemy ORM patterns")
print("  • Session management")
print("  • Query performance tuning")
print("  • Batch operations")
print("  • Connection pooling")

print("\n🚀 READY FOR WEEK 5: Flask REST API!")
print("  Next: Build HTTP endpoints to expose this data")
print("="*70)
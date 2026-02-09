"""Test SQLAlchemy ORM features."""
from database import get_session_no_commit, Source, Article
from sqlalchemy.orm import joinedload

print("="*70)
print("Testing SQLAlchemy ORM")
print("="*70)

session = get_session_no_commit()

try:
    # Test 1: Get a source and access its articles (relationship)
    print("\n1. Testing Relationships:")
    bbc = session.query(Source).filter_by(name='BBC News').first()
    print(f"   BBC has {len(bbc.articles)} articles")
    print(f"   Latest: {bbc.articles[0].title if bbc.articles else 'None'}")
    
    # Test 2: Get an article and access its source (reverse relationship)
    print("\n2. Testing Reverse Relationship:")
    article = session.query(Article).first()
    print(f"   Article: {article.title[:50]}...")
    print(f"   Source: {article.source.name}")
    
    # Test 3: Eager loading (no N+1 queries)
    print("\n3. Testing Eager Loading:")
    articles = session.query(Article)\
        .options(joinedload(Article.source))\
        .limit(5)\
        .all()
    
    for a in articles:
        print(f"   - {a.title[:40]}... from {a.source.name}")
    
    # Test 4: Filtering and counting
    print("\n4. Testing Filters:")
    us_sources = session.query(Source)\
        .filter_by(country='US')\
        .count()
    print(f"   US sources: {us_sources}")
    
    tech_articles = session.query(Article)\
        .join(Source)\
        .filter(Source.political_leaning == 'tech-focus')\
        .count()
    print(f"   Tech articles: {tech_articles}")
    
    print("\n" + "="*70)
    print("✅ All ORM features working!")
    print("="*70)

finally:
    session.close()
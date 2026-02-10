# Kirikou Database Documentation

## Overview

Kirikou uses PostgreSQL 16 as its primary database, with SQLAlchemy ORM for Python interactions.

**Current Stats:**

- Database Size: ~9 MB
- Articles: 842
- Sources: 10 active news outlets
- Indexes: 8 strategic indexes

## Schema

### Sources Table

Stores news outlet metadata with political classification.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-incrementing ID |
| name | TEXT | UNIQUE, NOT NULL | Source name (e.g., "BBC News") |
| url | TEXT | NOT NULL | RSS feed URL |
| country | TEXT | - | Country of origin |
| political_leaning | TEXT | - | Political classification |

### Articles Table

Stores scraped news articles with automatic deduplication.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-incrementing ID |
| source_id | INTEGER | FOREIGN KEY, NOT NULL | References sources(id) |
| title | TEXT | NOT NULL | Article headline |
| description | TEXT | - | Article summary |
| content | TEXT | - | Full article text (rarely available) |
| author | TEXT | - | Article author |
| published_at | TIMESTAMP | NOT NULL | Publication timestamp |
| scraped_at | TIMESTAMP | DEFAULT NOW() | When article was scraped |
| url | TEXT | UNIQUE, NOT NULL | Article URL (deduplication key) |

**Relationship:** One source has many articles (one-to-many).

## Indexes

Strategic indexes for query performance:

```sql
-- Foreign key optimization
CREATE INDEX idx_articles_source_id ON articles(source_id);

-- Date sorting/filtering (descending for recent-first queries)
CREATE INDEX idx_articles_published_at ON articles(published_at DESC);

-- Composite index for source + date queries
CREATE INDEX idx_articles_source_date ON articles(source_id, published_at DESC);

-- Duplicate detection
CREATE INDEX idx_articles_title ON articles(title);
```

**Automatic Indexes (created by constraints):**

- `articles_pkey` - Primary key on articles(id)
- `sources_pkey` - Primary key on sources(id)
- `articles_url_key` - UNIQUE constraint on articles(url) - **Most used index (1,601 scans)**
- `sources_name_key` - UNIQUE constraint on sources(name)

## SQLAlchemy Models

### Source Model

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Source(Base):
    __tablename__ = 'sources'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    url = Column(String, nullable=False)
    country = Column(String)
    political_leaning = Column(String)
    
    # Relationship: One source has many articles
    articles = relationship('Article', back_populates='source')
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'country': self.country,
            'political_leaning': self.political_leaning
        }
```

### Article Model

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Article(Base):
    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey('sources.id'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    content = Column(Text)
    author = Column(String)
    published_at = Column(DateTime, nullable=False)
    scraped_at = Column(DateTime, default=datetime.now)
    url = Column(String, unique=True, nullable=False)
    
    # Relationship: Many articles belong to one source
    source = relationship('Source', back_populates='articles')
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'source_id': self.source_id,
            'title': self.title,
            'description': self.description,
            'content': self.content,
            'author': self.author,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'scraped_at': self.scraped_at.isoformat() if self.scraped_at else None,
            'url': self.url,
            'source_name': self.source.name if self.source else None
        }
```

## Query Utilities

### Available Functions

All functions in `database/utils.py`:

#### `get_all_sources() -> List[Dict]`

Retrieve all news sources.

```python
sources = get_all_sources()
# Returns: [{'id': 1, 'name': 'BBC News', 'url': '...', ...}, ...]
```

#### `get_recent_articles(limit: int = 20) -> List[Dict]`

Get recent articles with source information (uses JOIN with eager loading).

```python
articles = get_recent_articles(limit=10)
# Returns articles with source_name, country, political_leaning
```

#### `get_source_stats() -> List[Dict]`

Source activity statistics with 7-day article counts.

```python
stats = get_source_stats()
# Returns: [{'source_name': 'BBC', 'total_articles': 83, 'articles_last_7d': 12}, ...]
```

#### `get_inactive_sources(hours: int = 24) -> List[Dict]`

Find sources with no recent articles (feed health monitoring).

```python
inactive = get_inactive_sources(hours=48)
# Returns sources with no articles in last 48 hours
```

#### `get_duplicate_stories() -> List[Dict]`

Event clustering - find articles with identical titles from different sources.

```python
duplicates = get_duplicate_stories()
# Returns: [{'title': '...', 'source1': 'BBC', 'source2': 'CNN'}, ...]
```

#### `get_articles_by_source(source_name: str, days: int = 7) -> List[Dict]`

Filter articles by source within specified timeframe.

```python
bbc_articles = get_articles_by_source('BBC News', days=30)
# Returns all BBC articles from last 30 days
```

#### `save_articles_batch(articles: List[Dict], source_id: int) -> int`

Bulk insert articles with automatic deduplication.

```python
article_data = [
    {'title': '...', 'url': '...', 'published_at': datetime(...), ...},
    # ... more articles
]
inserted = save_articles_batch(article_data, source_id=1)
# Returns count of new articles inserted (duplicates skipped)
```

### Direct ORM Usage Examples

```python
from database import get_session, Article, Source
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta

# Query with automatic relationship loading (avoids N+1 queries)
with get_session() as session:
    articles = session.query(Article)\
        .options(joinedload(Article.source))\
        .filter(Article.published_at >= datetime.now() - timedelta(days=7))\
        .order_by(Article.published_at.desc())\
        .limit(20)\
        .all()
    
    for article in articles:
        # Access related source without additional query
        print(f"{article.title} from {article.source.name}")

# Filter by source country
with get_session() as session:
    us_articles = session.query(Article)\
        .join(Source)\
        .filter(Source.country == 'US')\
        .order_by(Article.published_at.desc())\
        .all()

# Aggregate queries
from sqlalchemy import func

with get_session() as session:
    # Count articles per source
    counts = session.query(
        Source.name,
        func.count(Article.id).label('article_count')
    )\
        .join(Article)\
        .group_by(Source.name)\
        .order_by(func.count(Article.id).desc())\
        .all()
```

## Performance Considerations

### Deduplication Strategy

Articles with duplicate URLs are automatically rejected via:

```sql
INSERT INTO articles (...) VALUES (...)
ON CONFLICT (url) DO NOTHING;
```

**Performance:** The `articles_url_key` index has been scanned **1,601 times**, making deduplication checks extremely fast (<1ms per check).

### Batch Operations

Use `executemany()` for inserting multiple articles:

- **Single inserts:** ~10ms per article (slow for 50 articles)
- **Batch insert:** ~50ms for 50 articles (50x faster!)

```python
# Efficient batch insert
cursor.executemany(
    "INSERT INTO articles (...) VALUES (%s, %s, ...) ON CONFLICT (url) DO NOTHING",
    articles_data
)
```

### Connection Pooling

SQLAlchemy engine configured with connection pool:

```python
engine = create_engine(
    DATABASE_URL,
    pool_size=5,          # 5 persistent connections
    max_overflow=10,      # +10 overflow connections if needed
    pool_pre_ping=True    # Verify connection before use
)
```

### Query Optimization with Eager Loading

Avoid N+1 query problem using `joinedload()`:

```python
# BAD: N+1 queries (1 for articles + N for each source)
articles = session.query(Article).all()
for article in articles:
    print(article.source.name)  # Triggers separate query each time!

# GOOD: Single query with JOIN
articles = session.query(Article)\
    .options(joinedload(Article.source))\
    .all()
for article in articles:
    print(article.source.name)  # No additional query!
```

## Maintenance

### Vacuum and Analyze

PostgreSQL automatically maintains tables, but you can manually trigger:

```bash
# Reclaim space and update statistics
psql kirikou_db -c "VACUUM ANALYZE articles;"
psql kirikou_db -c "VACUUM ANALYZE sources;"
```

### Check Dead Rows

Monitor table health:

```sql
SELECT relname, n_live_tup, n_dead_tup 
FROM pg_stat_user_tables 
WHERE schemaname = 'public';
```

**Current status:** 0 dead rows in articles (excellent!)

### Backup

```bash
# Full database backup
pg_dump kirikou_db > backup_$(date +%Y%m%d).sql

# Compressed backup
pg_dump kirikou_db | gzip > backup_$(date +%Y%m%d).sql.gz
```

### Restore

```bash
# Restore from backup
psql kirikou_db < backup_20260210.sql
```

## Database Statistics

Current production stats (as of Week 4 completion):

- **Total articles:** 842
- **Total sources:** 10
- **Database size:** 9 MB
- **Most used index:** articles_url_key (1,601 scans) - deduplication
- **Average article size:** ~10 KB

## Future Enhancements

Planned improvements for later weeks:

- [ ] Full-text search on article content (PostgreSQL `tsvector`)
- [ ] Materialized views for analytics dashboards
- [ ] Partitioning articles table by date (when >100K articles)
- [ ] Archive old articles (>6 months) to separate table
- [ ] Add article sentiment scores (float column)
- [ ] Event clustering with similarity matching (not just exact title)
- [ ] Source reliability scores based on update frequency

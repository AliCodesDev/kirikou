# Changelog

All notable changes to Kirikou will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Week 4] - 2026-02-10

### Added

**Database Layer (Days 22-25):**

- PostgreSQL 16 database schema with referential integrity
- SQLAlchemy ORM models (Source, Article) with declarative Base
- Automatic relationship navigation (source.articles, article.source)
- Session management with context managers (`get_session()`, `get_session_no_commit()`)
- Database utility functions:
  - `get_all_sources()` - List all news sources
  - `get_recent_articles(limit)` - Recent articles with JOIN
  - `get_source_stats()` - Source activity statistics
  - `get_inactive_sources(hours)` - Feed health monitoring
  - `get_duplicate_stories()` - Event clustering
  - `get_articles_by_source(name, days)` - Filter by source
  - `save_articles_batch(articles, source_id)` - Bulk insert with deduplication
- Strategic indexes for query performance:
  - `idx_articles_source_id` - Foreign key optimization
  - `idx_articles_published_at` - Date sorting
  - `idx_articles_source_date` - Composite index
  - `idx_articles_title` - Duplicate detection
- Automatic deduplication via UNIQUE constraint on article URLs
- Batch insert operations for performance (50x faster than individual inserts)
- Connection pooling configuration (5 persistent + 10 overflow connections)
- RSS scraper database integration
- Feed validation system (13 sources validated, 92.9% success rate)
- Comprehensive database documentation (`docs/DATABASE.md`)

**RSS Scraper Enhancements:**

- Database-driven source management (reads from `sources` table)
- Enhanced date parsing with `python-dateutil`
- Improved error handling per feed
- Progress indicators during scraping
- Summary statistics (fetched, inserted, duplicates)
- Graceful handling of failed feeds

### Changed

- Migrated from raw psycopg2 queries to SQLAlchemy ORM
- Refactored all query utilities to use ORM patterns
- Updated README with Week 4 accomplishments
- Improved logging throughout database operations
- Enhanced article extraction to handle missing fields gracefully

### Technical Details

**Database Statistics:**

- 842 articles ingested
- 10 active news sources
- 9 MB database size
- 1,601 deduplication checks performed (articles_url_key index)
- 0 dead rows (excellent table health)

**Index Performance:**

- `articles_url_key`: 1,601 scans (deduplication workhorse)
- `sources_pkey`: 881 scans (joins working well)
- `idx_articles_title`: 12 scans (duplicate story detection)
- All strategic indexes operational

**Political Spectrum Coverage:**

- Center: BBC, Al Jazeera, Deutsche Welle
- Center-Left: CNN, Guardian, NYT, NPR
- Right: Fox News
- Tech-Focus: Ars Technica, TechCrunch

## [Week 3] - 2026-01-30 to 2026-02-05

### Added

**Data Ingestion (Days 15-21):**

- RSS feed parser using `feedparser` library
- Multi-source support with configurable feeds
- Error handling and retry logic for failed requests
- Automatic date parsing with `python-dateutil`
- Configuration management with environment variables
- Comprehensive logging system
- Feed validation script to test RSS sources
- Request timeout handling (10 seconds default)

**Infrastructure:**

- Project structure with modular packages
- Virtual environment setup
- Git version control
- `.env` configuration management
- Requirements tracking (`requirements.txt`)

### Technical Details

- 13 news sources configured
- HTTP timeout: 10 seconds
- Retry logic for transient failures
- Structured logging to console and file

## [Week 1-2] - 2026-01-16 to 2026-01-29

### Added

**Foundation (Days 1-14):**

- Project initialization
- Python fundamentals (variables, functions, data structures)
- Object-oriented programming (classes, methods, inheritance)
- File handling and exception management
- Module and package organization
- Development environment setup (Python 3.10+, VS Code)
- macOS development tools (Homebrew, PostgreSQL)

**Learning Exercises:**

- CLI tools for text analysis
- Class-based task manager prototype
- RSS feed parser prototype (learning exercise)

### Technical Skills Acquired

- Python syntax and idioms
- OOP design patterns
- Error handling best practices
- Code organization and modularity
- Git workflow (commits, branches, merging)

---

## Progress Summary

**Days Completed:** 25 of 84 (30%)

**Current Phase:** Database Layer Complete ✅

**Next Phase:** Week 5 - Flask REST API

**Technical Milestones:**

- ✅ Python and OOP fundamentals
- ✅ RSS scraping and data ingestion
- ✅ PostgreSQL database design
- ✅ SQLAlchemy ORM implementation
- ✅ Production-ready error handling
- ✅ Comprehensive documentation

**Portfolio Highlights:**

- 842 articles from 10 global news sources
- Production-grade database design with strategic indexes
- Type-safe ORM with automatic relationships
- 9 MB efficient database
- Clean, documented codebase
- Professional Git workflow with tagged milestones

---

## Coming Next

**Week 5 (Days 29-35):** Flask REST API

- RESTful endpoints for articles and sources
- Request validation and error handling
- JSON serialization of database models
- API documentation with Swagger
- Integration with existing database layer

**Week 6 (Days 36-42):** FastAPI Migration

- Async endpoints and background tasks
- Celery integration for scheduled scraping
- Redis caching for performance
- Migration from Flask to FastAPI

**Week 11 (Days 71-77):** LLM Integration

- OpenAI/Anthropic/Google API integration
- RAG (Retrieval-Augmented Generation) pattern
- Comparative bias analysis across sources
- Narrative difference detection

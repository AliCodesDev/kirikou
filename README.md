# Kirikou

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-in_development-yellow.svg)

A Media Intelligence Platform for RSS feed aggregation and analysis.

## Overview

Kirikou is a Python-based backend service designed to collect, process, and analyze media content from RSS feeds.

## Requirements

- Python 3.13+
- PostgreSQL

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd kirikou
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your configuration values.

## Configuration

The following environment variables can be configured:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://localhost/kirikou_db` |
| `SECRET_KEY` | API authentication key | None (optional) |
| `DEBUG` | Enable debug mode | `False` |
| `APP_NAME` | Application name | `Kirikou Media Intelligence` |
| `LOG_LEVEL` | Logging verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL) | `INFO` |
| `LOG_FILE` | Log output file path | `logs/kirikou.log` |
| `FETCH_INTERVAL` | RSS fetch interval in seconds | `3600` |
| `REQUEST_TIMEOUT` | HTTP request timeout in seconds | `10` |

## Project Structure

```
kirikou/
├── config.py              # Configuration management
├── database/              # Database layer (NEW!)
│   ├── __init__.py
│   ├── schema.sql         # PostgreSQL schema
│   └── init_db.py         # Database initialization
├── ingestion/             # Data ingestion module
│   └── feed_parser.py     # RSS feed fetching and parsing
├── logs/                  # Application logs
├── requirements.txt       # Python dependencies
└── .env.example           # Environment template
```

## Database Schema

**Sources Table:**

- Stores news outlet information (BBC, CNN, Reuters, etc.)
- Enforces unique source names
- Tracks country and political leaning for bias analysis

**Articles Table:**

- Stores news articles with title, URL, content, publication date
- **Deduplication:** UNIQUE constraint on URL prevents duplicate articles
- Foreign key links each article to its source
- Flexible content fields (description/content can be NULL for incomplete RSS feeds)

## Database Queries & Utilities

Kirikou provides reusable query functions for common operations:

```python
from database.utils import (
    get_recent_articles,
    get_source_stats,
    get_inactive_sources,
    get_duplicate_stories,
    get_articles_by_source
)

# Get latest 20 articles with source info
articles = get_recent_articles(limit=20)

# Get source activity statistics
stats = get_source_stats()

# Find inactive sources (potential broken feeds)
inactive = get_inactive_sources(hours=24)

# Detect duplicate stories (event clustering)
duplicates = get_duplicate_stories()

# Get articles from specific source
bbc_articles = get_articles_by_source("BBC News", days=7)
```

**Query Features:**

- All queries return dictionaries for easy access
- Proper error handling and logging
- Parameterized queries prevent SQL injection
- Connection pooling and cleanup

**Performance Optimizations:**

- Strategic indexes on frequently queried columns
- Composite indexes for common query patterns
- Transactions ensure data consistency

## Usage

**Initialize the database:**

```bash
python -m database.init_db
```

**Run the RSS feed scraper:**

```bash
python -m ingestion.feed_parser
```

## Status

🚧 **In Development** - Week 4, Day 23 of 12-week build

**Completed:**

- ✅ Configuration and logging system
- ✅ RSS feed scraper (Week 3)
- ✅ PostgreSQL database schema (Day 22)
  - Sources and Articles tables
  - Deduplication via UNIQUE constraints
  - Referential integrity via foreign keys
  - Automated timestamps
- ✅ Advanced SQL operations (Day 23)
  - JOINs (INNER, LEFT, self-join)
  - Strategic indexes for query performance
  - Transaction handling
  - Reusable database utilities
  
**Next up:**

- Day 24: Connect RSS scraper to database (articles persist!)
- Day 25: SQLAlchemy ORM

## License

MIT

# 🌍 Kirikou: Media Intelligence Agent

> **An autonomous AI-powered media intelligence platform that analyzes narrative bias across global news sources.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow)](https://github.com/AliCodesDev/kirikou)

Kirikou is not a news aggregator—it's an intelligence agent that *analyzes* how different media outlets cover the same events. By ingesting news from diverse sources across the political spectrum, Kirikou enables comparative analysis of narrative differences, bias, and tone.

**The Vision:** *"Don't just read the news. Understand the narrative."*

---

## 📊 Project Status

🚧 **Week 4, Day 24 of 12-Week Build** | Phase: Database Integration Complete

### ✅ Completed Features

**The Memory Layer (Database)**

- ✅ PostgreSQL schema with referential integrity
- ✅ Automatic deduplication (UNIQUE constraint on article URLs)
- ✅ Strategic indexes for query performance optimization
- ✅ Transaction-based operations with proper error handling
- ✅ Advanced SQL queries (JOINs, aggregations, analytics)
- ✅ Reusable database utilities with dictionary-based results

**The Senses (Data Ingestion)**

- ✅ RSS feed scraper with error handling and retry logic
- ✅ Multi-source support (10 active news sources)
- ✅ Automatic date parsing and standardization
- ✅ Batch insert operations for performance
- ✅ Connection to database with duplicate detection

**Infrastructure**

- ✅ Configuration management with environment variables
- ✅ Comprehensive logging system
- ✅ Modular architecture (separation of concerns)
- ✅ Production-ready error handling

### 📈 Current Data

- **406 articles** ingested from 10 global news sources
- **Political spectrum coverage:** Center, Center-Left, Right, Tech-Focus
- **Geographic diversity:** UK, US, Germany, Qatar
- **Deduplication:** Automatically skips duplicate URLs

### 🎯 Next Up

- **Day 25:** SQLAlchemy ORM implementation
- **Week 5:** Flask REST API for data access
- **Week 6:** FastAPI migration with async workers (Celery)
- **Week 11:** LLM integration for RAG-based bias analysis

---

## 🏗️ Architecture

Kirikou is built as a modular system following clean architecture principles:

### System Components

```
┌──────────────────────────────────────────────┐
│              KIRIKOU SYSTEM                  │
├──────────────────────────────────────────────┤
│                                              │
│  ┌──────────────┐      ┌──────────────┐      │
│  │  The Senses  │ ───> │  The Memory  │      │
│  │              │      │              │      │
│  │ RSS Scraper  │      │  PostgreSQL  │      │
│  │ Multi-source │      │  Dedup Logic │      │
│  │ Error Handle │      │  Indexes     │      │
│  └──────────────┘      └──────────────┘      │
│         │                      │             │
│         └──────────┬───────────┘             │
│                    │                         │
│         ┌──────────▼──────────┐              │
│         │   Query Utilities   │              │
│         │                     │              │
│         │ • Recent Articles   │              │
│         │ • Source Stats      │              │
│         │ • Duplicate Stories │              │
│         │ • Event Clustering  │              │
│         └─────────────────────┘              │
│                                              │
│  Coming Soon:                                │
│  ┌──────────────┐      ┌──────────────┐      │
│  │ The Nervous  │      │  The Brain   │      │
│  │   System     │      │              │      │
│  │              │      │  LLM + RAG   │      │
│  │ FastAPI      │      │  Bias Analyze│      │
│  │ Async Workers│      │  Compare     │      │
│  └──────────────┘      └──────────────┘      │
│                                              │
└──────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Core Technologies

- **Python 3.10+** - Modern Python with type hints
- **PostgreSQL 16** - Production-grade relational database
- **psycopg2** - PostgreSQL adapter for Python

### Python Libraries

- **feedparser** - RSS/Atom feed parsing
- **requests** - HTTP client for fetching feeds
- **python-dateutil** - Robust date parsing
- **logging** - Comprehensive application logging

### Planned Technologies

- **Flask → FastAPI** (Week 5-6) - RESTful API development
- **Celery + Redis** (Week 6) - Async task queue for background scraping
- **Docker** (Week 9) - Containerization for deployment
- **pytest** (Week 8) - Comprehensive test suite
- **LLM API** (Week 11) - OpenAI/Anthropic/Google for bias analysis

---

## 📚 Database Schema

### Sources Table

Stores news outlet metadata with political leaning classification.

```sql
CREATE TABLE sources (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    url TEXT NOT NULL,
    country TEXT,
    political_leaning TEXT
);
```

### Articles Table

Stores scraped articles with automatic deduplication via URL uniqueness.

```sql
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    source_id INTEGER NOT NULL REFERENCES sources(id),
    title TEXT NOT NULL,
    description TEXT,
    content TEXT,
    author TEXT,
    published_at TIMESTAMP NOT NULL,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    url TEXT NOT NULL UNIQUE  -- Deduplication constraint
);
```

### Strategic Indexes

Optimized for common query patterns:

```sql
-- Foreign key optimization
CREATE INDEX idx_articles_source_id ON articles(source_id);

-- Date sorting and filtering
CREATE INDEX idx_articles_published_at ON articles(published_at DESC);

-- Composite index for source + date queries
CREATE INDEX idx_articles_source_date ON articles(source_id, published_at DESC);

-- Duplicate detection optimization
CREATE INDEX idx_articles_title ON articles(title);
```

---

## 🚀 Getting Started

### Prerequisites

- **macOS** (Apple Silicon M4 tested)
- **Python 3.10+**
- **PostgreSQL 16**
- **Homebrew** (for macOS package management)

### Installation

#### 1. Install PostgreSQL

```bash
brew install postgresql@16
brew services start postgresql@16
```

#### 2. Create Database

```bash
createdb kirikou_db
```

#### 3. Clone Repository

```bash
git clone https://github.com/AliCodesDev/kirikou.git
cd kirikou
```

#### 4. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 6. Configure Environment

```bash
cp .env.example .env
# Edit .env with your database credentials
```

Example `.env`:

```env
DATABASE_URL=postgresql://localhost/kirikou_db
REQUEST_TIMEOUT=10
LOG_LEVEL=INFO
SECRET_KEY=your-secret-key-here
```

#### 7. Initialize Database

```bash
# Create tables and indexes
python -m database.init_db

# Load news sources
psql kirikou_db < database/add_sources.sql
```

---

## 💻 Usage

### Running the RSS Scraper

Fetch articles from all configured news sources:

```bash
python -m ingestion.feed_parser
```

**Output:**

```
======================================================================
Starting RSS scraper...
======================================================================
Found 13 sources to scrape

[1/13] Scraping Al Jazeera...
✅ Al Jazeera: 25 new, 0 duplicates

[2/13] Scraping BBC News...
✅ BBC News: 38 new, 0 duplicates

...

======================================================================
Scraping complete!
======================================================================
Sources processed: 13
Articles fetched:  406
Articles inserted: 406
Duplicates skip:   0
======================================================================
```

### Querying Data with Utilities

The project includes powerful query utilities that return clean dictionary results:

```python
from database.utils import (
    get_recent_articles,
    get_source_stats,
    get_duplicate_stories,
    get_inactive_sources
)

# Get latest articles with source information
articles = get_recent_articles(limit=20)
for article in articles:
    print(f"{article['title']} - {article['source_name']}")

# Get source activity statistics
stats = get_source_stats()
for stat in stats:
    print(f"{stat['source_name']}: {stat['total_articles']} articles")

# Find duplicate stories (event clustering)
duplicates = get_duplicate_stories()
for dup in duplicates:
    print(f"'{dup['title']}' covered by {dup['source1']} and {dup['source2']}")

# Monitor feed health
inactive = get_inactive_sources(hours=24)
for source in inactive:
    print(f"⚠️ {source['source_name']} - Last article: {source['last_article_date']}")
```

### Direct Database Queries

```bash
# Count total articles
psql kirikou_db -c "SELECT COUNT(*) FROM articles;"

# Recent articles with source info
psql kirikou_db -c "
    SELECT a.title, s.name as source, a.published_at 
    FROM articles a 
    JOIN sources s ON a.source_id = s.id 
    ORDER BY a.published_at DESC 
    LIMIT 10;
"

# Articles by source
psql kirikou_db -c "
    SELECT s.name, COUNT(a.id) as article_count
    FROM sources s
    LEFT JOIN articles a ON s.id = a.source_id
    GROUP BY s.name
    ORDER BY article_count DESC;
"
```

---

## 📁 Project Structure

```
kirikou/
├── config.py                 # Configuration management
├── database/                 # Database layer
│   ├── __init__.py
│   ├── init_db.py           # Database initialization
│   ├── schema.sql           # PostgreSQL schema with indexes
│   ├── add_sources.sql      # Validated news sources
│   ├── queries.sql          # Production SQL queries
│   ├── seed_data.sql        # Test data
│   └── utils.py             # Reusable query functions
├── ingestion/               # Data ingestion module
│   ├── __init__.py
│   ├── feed_parser.py       # RSS scraper
│   └── validate_feeds.py    # Feed validation utility
├── logs/                    # Application logs
├── venv/                    # Virtual environment
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (gitignored)
├── .env.example            # Environment template
└── README.md               # This file
```

---

## 🌐 News Sources

Kirikou currently ingests from **10 validated sources** across the political spectrum:

### Political Balance

- **Center:** BBC News, Al Jazeera, Deutsche Welle
- **Center-Left:** CNN, The Guardian, NPR, The New York Times
- **Right:** Fox News
- **Tech-Focus:** TechCrunch, Ars Technica

### Geographic Diversity

- **UK:** BBC News, The Guardian
- **US:** CNN, Fox News, NPR, NYT, TechCrunch, Ars Technica
- **International:** Al Jazeera (Qatar), Deutsche Welle (Germany)

### Feed Statistics (Current Snapshot)

- **Deutsche Welle:** 137 articles (largest feed)
- **CNN:** 50 articles
- **The Guardian:** 45 articles
- **BBC News:** 38 articles
- **The New York Times:** 36 articles
- **Al Jazeera:** 25 articles
- **Fox News:** 25 articles
- **Ars Technica:** 20 articles
- **TechCrunch:** 20 articles
- **NPR:** 10 articles

---

## 🎯 Key Features

### Automatic Deduplication

Articles with duplicate URLs are automatically skipped using PostgreSQL's `UNIQUE` constraint and `ON CONFLICT DO NOTHING` strategy. This ensures the same story isn't stored multiple times even if multiple sources link to it.

### Event Clustering

The duplicate detection query identifies when multiple sources cover the same story (same title), enabling future bias analysis:

```sql
-- Find articles with identical titles from different sources
SELECT a1.title, s1.name AS source1, s2.name AS source2
FROM articles a1
JOIN articles a2 ON a1.title = a2.title AND a1.id < a2.id
JOIN sources s1 ON a1.source_id = s1.id
JOIN sources s2 ON a2.source_id = s2.id;
```

Example output:

```
"Breaking: Election Results" - BBC News vs Fox News
"Breaking: Election Results" - BBC News vs CNN
"Breaking: Election Results" - CNN vs Fox News
```

**This is the foundation for Week 11's LLM-powered bias analysis!**

### Performance Optimization

- **Batch inserts** using `executemany()` for 50x speed improvement over individual inserts
- **Strategic indexes** on foreign keys, dates, and frequently queried columns
- **Transaction handling** ensures all-or-nothing batch operations
- **Connection pooling** ready for high-traffic API deployment (Week 5)

### Robust Error Handling

- Graceful handling of failed feeds (continues scraping other sources)
- Automatic date parsing with fallback to current time
- Connection cleanup in all scenarios (try/except/finally)
- Comprehensive logging at every step

---

## 🔮 Roadmap

### Phase 1: The Foundation (✅ Complete - Week 4)

- [x] RSS feed scraper with error handling
- [x] PostgreSQL database with deduplication
- [x] Strategic indexes for performance
- [x] Reusable database utilities
- [x] Transaction-based operations

### Phase 2: The Interface (🚧 Week 5)

- [ ] Flask REST API for data access
- [ ] CRUD endpoints for articles and sources
- [ ] Request validation and error handling
- [ ] API documentation (Swagger)

### Phase 3: Modern Stack (📅 Week 6)

- [ ] Migrate to FastAPI with async support
- [ ] Celery workers for background scraping
- [ ] Redis for caching and task queue
- [ ] Scheduled periodic scraping (every hour)

### Phase 4: Security (📅 Week 7)

- [ ] JWT authentication
- [ ] Rate limiting
- [ ] CORS configuration
- [ ] Input sanitization

### Phase 5: Testing (📅 Week 8)

- [ ] Comprehensive pytest suite
- [ ] Unit tests for all modules
- [ ] Integration tests for database operations
- [ ] 80%+ code coverage

### Phase 6: Deployment (📅 Week 9)

- [ ] Docker containerization
- [ ] Docker Compose for multi-container setup
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Cloud deployment (Render/AWS)

### Phase 7: Intelligence (📅 Week 11)

- [ ] LLM API integration (OpenAI/Anthropic/Google)
- [ ] RAG (Retrieval-Augmented Generation) pattern
- [ ] Comparative bias analysis across sources
- [ ] Narrative difference detection

### Phase 8: Production Polish (📅 Week 12)

- [ ] Monitoring and alerting
- [ ] Performance optimization
- [ ] Comprehensive documentation
- [ ] Portfolio-ready presentation

---

## 🧪 Testing Deduplication

Run the scraper twice to verify deduplication works:

**First run:**

```bash
python -m ingestion.feed_parser
# Output: Articles inserted: 406
```

**Second run (immediately after):**

```bash
python -m ingestion.feed_parser
# Output: Articles inserted: 8, Duplicates skip: 398
```

Only **new** articles since the last run are inserted. Existing URLs are automatically skipped!

---

## 📊 Analytics Queries

The project includes pre-built SQL queries for common analytics:

### Recent Articles Dashboard

```sql
SELECT a.title, a.url, a.published_at, 
       s.name AS source_name, s.country, s.political_leaning
FROM articles a
INNER JOIN sources s ON a.source_id = s.id
ORDER BY a.published_at DESC
LIMIT 20;
```

### Source Activity Report

```sql
SELECT s.name AS source_name,
       COUNT(a.id) AS total_articles,
       COUNT(CASE WHEN a.published_at > NOW() - INTERVAL '7 days' THEN 1 END) AS articles_last_7d
FROM sources s
LEFT JOIN articles a ON s.id = a.source_id
GROUP BY s.id, s.name
ORDER BY total_articles DESC;
```

### Inactive Sources Detection

```sql
SELECT s.name AS source_name, s.url,
       MAX(a.published_at) AS last_article_date
FROM sources s
LEFT JOIN articles a ON s.id = a.source_id
GROUP BY s.id, s.name, s.url
HAVING MAX(a.published_at) IS NULL 
    OR MAX(a.published_at) < NOW() - INTERVAL '24 hours'
ORDER BY last_article_date ASC NULLS FIRST;
```

---

## 🤝 Contributing

This is a learning project following a structured 12-week curriculum. Contributions, suggestions, and feedback are welcome!

### Development Workflow

1. Create a feature branch
2. Make changes with clear commit messages
3. Test thoroughly
4. Submit pull request with description

### Commit Message Format

```
type(scope): brief description

Types:
- feat: new feature
- fix: bug fix
- refactor: code restructuring
- test: adding tests
- docs: documentation
- chore: maintenance
```

Example:

```
feat(day24): connect RSS scraper to PostgreSQL database

- Enhanced extract_articles() to parse dates with dateutil
- Created save_articles_batch() for efficient batch inserts
- Implemented scrape_all_sources() reading from database
- Added get_all_sources() to query sources dynamically
```

---

## 📖 Learning Journey

This project is part of a **12-week Python Backend Development Journey** building a production-grade application from scratch. Each week focuses on specific backend engineering concepts:

- **Week 1-2:** Python fundamentals and OOP
- **Week 3:** Networking, HTTP, and API consumption
- **Week 4:** SQL, PostgreSQL, and database design ✅ (Current)
- **Week 5:** Flask web framework and REST APIs
- **Week 6:** FastAPI and async programming
- **Week 7:** Authentication, authorization, and security
- **Week 8:** Testing and quality assurance
- **Week 9:** Docker and CI/CD
- **Week 10:** Microservices architecture
- **Week 11:** Cloud deployment and LLM integration
- **Week 12:** Final polish and production deployment

**Progress:** Currently on Day 24 of 84 (29% complete)

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👤 Author

**Ali Ezzeddine**  
M.Sc. Cognitive Systems  
Backend Development Journey 2026

- GitHub: [@AliCodesDev](https://github.com/AliCodesDev)
- LinkedIn: [Connect with me](https://www.linkedin.com/in/aliezzeddinee/)
- Portfolio: Building in public! 🚀

---

## 🙏 Acknowledgments

- **Anthropic Claude** - AI development mentor
- **PostgreSQL Community** - Excellent database documentation
- **Python Community** - Rich ecosystem of libraries
- News organizations providing RSS feeds for educational purposes

---

## 📝 Notes

### Why "Kirikou"?

Named after the West African folk hero known for his intelligence and problem-solving abilities. Like the character, this agent navigates complex information landscapes to uncover truth.

### Educational Purpose

This project is built for **educational and portfolio purposes**. News content is fetched via publicly available RSS feeds and used for demonstrating backend engineering skills, not for commercial redistribution.

### Future Features (Post-Week 12)

- Email digest subscriptions
- Topic-based article clustering (NLP)
- Sentiment analysis across sources
- Frontend dashboard (React/Vue)
- Mobile app integration
- Multi-language support
- Historical trend analysis

---

<div align="center">

**⭐ Star this repo if you find it useful!**

Built with ❤️ and ☕ during a 12-week backend engineering journey

</div>

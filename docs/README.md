# 🌍 Kirikou: Media Intelligence Agent

> **An autonomous AI-powered media intelligence platform that analyzes narrative bias across global news sources.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)](https://www.postgresql.org/)
[![Celery](https://img.shields.io/badge/Celery-5.x-37814A)](https://docs.celeryq.dev/)
[![Redis](https://img.shields.io/badge/Redis-7.x-DC382D)](https://redis.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow)](https://github.com/AliCodesDev/kirikou)

Kirikou is not a news aggregator—it's an intelligence agent that *analyzes* how different media outlets cover the same events. By ingesting news from diverse sources across the political spectrum, Kirikou enables comparative analysis of narrative differences, bias, and tone.

**The Vision:** *"Don't just read the news. Understand the narrative."*

---

## 📊 Project Status

🚧 **Week 6, Day 42 of 12-Week Build** | Phase: Async Architecture ✅

### ✅ Completed Features

**Async Workers (Celery + Redis)** — *NEW in Week 6*

- ✅ Celery workers with Redis message broker for distributed task processing
- ✅ Celery Beat scheduler — autonomous hourly RSS scraping
- ✅ Task ID tracking in API responses for async job monitoring
- ✅ Process isolation — scraping runs in separate worker, API stays fast
- ✅ FastAPI dependency injection for database session management
- ✅ One session per request with route-controlled transactions

**Production Configuration** — *NEW in Week 6*

- ✅ Pydantic Settings for type-safe configuration management
- ✅ Automatic `.env` loading with type casting and validation
- ✅ `SecretStr` for sensitive values — secrets never leak in logs
- ✅ `@lru_cache` singleton — one shared settings instance app-wide
- ✅ Fail-fast validation — missing `DATABASE_URL` or `SECRET_KEY` crashes immediately with clear error
- ✅ `.env.example` template for easy project setup

**The Nervous System (API Layer)**

- ✅ FastAPI REST API with modular route organization
- ✅ Pydantic schemas with custom validators for request/response contracts
- ✅ Auto-generated Swagger documentation at `/docs`
- ✅ Background tasks for lightweight operations (feed validation, logging)
- ✅ Query parameter validation with constraints
- ✅ Nested JSON responses with proper REST structure
- ✅ Proper HTTP status codes (200, 201, 202, 400, 404, 422)

**The Memory Layer (Database)**

- ✅ PostgreSQL schema with referential integrity
- ✅ SQLAlchemy ORM with declarative models
- ✅ Type-safe database operations with Python classes
- ✅ Automatic relationship navigation (source.articles, article.source)
- ✅ Automatic deduplication (UNIQUE constraint on article URLs)
- ✅ Strategic indexes for query performance optimization
- ✅ Transaction-based operations with proper error handling
- ✅ Advanced SQL queries (JOINs, aggregations, analytics)
- ✅ Reusable database utilities with injected session support
- ✅ Session management with context managers and FastAPI dependency injection

**The Senses (Data Ingestion)**

- ✅ RSS feed scraper with error handling and retry logic
- ✅ Multi-source support (10+ active news sources)
- ✅ Automatic date parsing and standardization
- ✅ Batch insert operations for performance
- ✅ Connection to database with duplicate detection
- ✅ Celery-based async scraping via API triggers
- ✅ Autonomous hourly scraping via Celery Beat
- ✅ Single-source scraping support

**Infrastructure**

- ✅ Configuration management with environment variables
- ✅ Comprehensive logging system
- ✅ Modular architecture (separation of concerns)
- ✅ Production-ready error handling
- ✅ Redis for message brokering and result storage

### 📈 Current Data

- **1610+ articles** ingested from 10+ global news sources
- **9 API endpoints** with auto-generated documentation
- **8 Pydantic schemas** with validation and custom validators
- **2 Celery tasks** with hourly Beat schedule
- **10+ config settings** with type-safe Pydantic validation

- **Political spectrum coverage:** Center, Center-Left, Right, Tech-Focus
- **Geographic diversity:** UK, US, Germany, Qatar
- **Deduplication:** Automatically skips duplicate URLs

### 🎯 Next Up

- **Week 7:** JWT authentication, rate limiting, CORS, input sanitization
- **Week 8:** Comprehensive pytest test suite
- **Week 11:** LLM integration for RAG-based bias analysis

---

## 🏗️ Architecture

Kirikou is built as a modular system following clean architecture principles:

### System Components

```
┌──────────────────────────────────────────────────────┐
│                   KIRIKOU SYSTEM                     │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐      ┌──────────────┐              │
│  │  The Senses  │ ───> │  The Memory  │              │
│  │              │      │              │              │
│  │ RSS Scraper  │      │  PostgreSQL  │              │
│  │ Multi-source │      │  Dedup Logic │              │
│  │ Error Handle │      │  Indexes     │              │
│  └──────────────┘      └──────────────┘              │
│         │                      │                     │
│         └──────────┬───────────┘                     │
│                    │                                 │
│         ┌──────────▼──────────┐                      │
│         │  The Nervous System │                      │
│         │                     │                      │
│         │ FastAPI REST API    │                      │
│         │ Pydantic Schemas    │                      │
│         │ Dependency Inject.  │                      │
│         │ Auto Swagger Docs   │                      │
│         └─────────────────────┘                      │
│                    │                                 │
│         ┌──────────▼──────────┐                      │
│         │   Async Workers     │                      │
│         │                     │                      │
│         │ Celery + Redis      │                      │
│         │ Hourly Beat Sched.  │                      │
│         │ Task ID Tracking    │                      │
│         └─────────────────────┘                      │
│                                                      │
│  Coming Soon:                                        │
│  ┌──────────────┐      ┌──────────────┐              │
│  │  Security    │      │  The Brain   │              │
│  │              │      │              │              │
│  │ JWT Auth     │      │  LLM + RAG   │              │
│  │ Rate Limit   │      │  Bias Analyze│              │
│  │ CORS         │      │  Compare     │              │
│  └──────────────┘      └──────────────┘              │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### Process Architecture

```
┌──────────────────┐
│    FastAPI API    │       ┌─────────────┐       ┌──────────────┐
│    (uvicorn)     │──────►│    Redis     │──────►│ Celery Worker│
│                  │       │   (Broker)   │       │              │
│  POST /scrape    │       └─────────────┘       │ scrape_all   │
│  GET /articles   │              ▲               │ scrape_one   │
│  GET /sources    │              │               └──────────────┘
└──────────────────┘       ┌──────┴──────┐
                           │ Celery Beat │
        PostgreSQL ◄───    │             │
        (Database)         │ Every hour: │
                           │ scrape all  │
                           └─────────────┘

Running Processes:
1. uvicorn api.main:app              ← API server
2. redis-server                       ← Message broker
3. celery -A worker.celery_app worker ← Task executor
4. celery -A worker.celery_app beat   ← Scheduler
```

---

## 🛠️ Tech Stack

### Core Technologies

- **Python 3.10+** — Modern Python with type hints
- **FastAPI** — High-performance async-capable web framework
- **PostgreSQL 16** — Production-grade relational database
- **SQLAlchemy** — Modern ORM for database operations
- **Pydantic** — Data validation and serialization
- **Celery** — Distributed task queue for background jobs
- **Redis** — Message broker and result backend
- **Uvicorn** — ASGI server for running FastAPI

### Python Libraries

- **fastapi** — REST API framework with auto-docs
- **uvicorn** — ASGI server
- **pydantic** — Request/response validation
- **sqlalchemy** — Modern ORM for database operations
- **celery** — Distributed task queue
- **redis** — Redis client for Python
- **feedparser** — RSS/Atom feed parsing
- **requests** — HTTP client for fetching feeds
- **python-dateutil** — Robust date parsing
- **psycopg2-binary** — PostgreSQL driver for SQLAlchemy
- **python-dotenv** — Environment variable management
- **logging** — Comprehensive application logging

### Planned Technologies

- **JWT Auth** (Week 7) — Authentication and authorization
- **Docker** (Week 9) — Containerization for deployment
- **pytest** (Week 8) — Comprehensive test suite
- **LLM API** (Week 11) — OpenAI/Anthropic/Google for bias analysis

---

## 🚀 API Endpoints

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check — returns system status |

### Sources

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/sources` | List all news sources |
| `GET` | `/sources/{id}` | Get a single source by ID |

### Articles

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/articles` | List articles (supports `limit`, `days`, `source_name` filters) |
| `GET` | `/articles/stats` | Source activity statistics |
| `GET` | `/articles/{id}` | Get a single article with full detail |

### Ingestion

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/ingestion/scrape` | Trigger full RSS scraping (Celery task, returns `task_id`) |
| `POST` | `/ingestion/scrape/{source_id}` | Scrape a single source (Celery task, returns `task_id`) |
| `POST` | `/ingestion/sources` | Create a new source (with background feed validation) |

### Interactive Documentation

Once the server is running, visit:

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

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
    url TEXT NOT NULL UNIQUE
);
```

### Strategic Indexes

```sql
CREATE INDEX idx_articles_source_id ON articles(source_id);
CREATE INDEX idx_articles_published_at ON articles(published_at DESC);
CREATE INDEX idx_articles_source_date ON articles(source_id, published_at DESC);
CREATE INDEX idx_articles_title ON articles(title);
```

---

## 🐍 Pydantic Schemas

Kirikou uses Pydantic models for strict API contracts:

### Source Schemas

- **`SourceResponse`** — Full source data for API responses
- **`SourceCreate`** — Validated input for creating sources (URL format, political leaning validation)
- **`SourceUpdate`** — Partial update with optional fields
- **`SourceBrief`** — Minimal source info embedded in article responses

### Article Schemas

- **`ArticleResponse`** — Article with nested `SourceBrief`
- **`ArticleDetail`** — Extended article with description, author, scraped_at

### Utility Schemas

- **`SourceStats`** — Source activity statistics
- **`ScrapeResponse`** — Task trigger confirmation with optional `task_id`

### Example Response

```json
{
    "id": 42,
    "title": "Oil prices surge amid Red Sea tensions",
    "url": "https://bbc.com/news/oil-prices",
    "published_at": "2026-02-17T10:30:00",
    "source": {
        "id": 1,
        "name": "BBC News",
        "political_leaning": "center"
    }
}
```

### Example Scrape Response

```json
{
    "message": "Scraping for all sources started",
    "status": "accepted",
    "task_id": "a1b2c3d4-5678-90ab-cdef-1234567890ab"
}
```

---

## 🚀 Getting Started

### Prerequisites

- **macOS** (Apple Silicon M4 tested)
- **Python 3.10+**
- **PostgreSQL 16**
- **Redis**
- **Homebrew** (for macOS package management)

### Installation

#### 1. Install PostgreSQL and Redis

```bash
brew install postgresql@16 redis
brew services start postgresql@16
brew services start redis
```

Verify Redis is running:

```bash
redis-cli ping
# Should return: PONG
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
# Edit .env — generate a secret key:
python -c "import secrets; print(secrets.token_hex(32))"
# Paste the output as your SECRET_KEY value
```

#### 7. Initialize Database

```bash
python -m database.init_db
psql kirikou_db < database/add_sources.sql
```

#### 8. Start Kirikou (3 processes)

```bash
# Terminal 1: API Server
uvicorn api.main:app --reload

# Terminal 2: Celery Worker (executes scraping tasks)
celery -A worker.celery_app worker --loglevel=info

# Terminal 3: Celery Beat (triggers hourly scraping)
celery -A worker.celery_app beat --loglevel=info
```

Visit `http://127.0.0.1:8000/docs` to explore the API.

---

## 💻 Usage

### Running the Full System

Kirikou runs as 3 coordinated processes:

```bash
# Terminal 1: API Server
uvicorn api.main:app --reload

# Terminal 2: Celery Worker
celery -A worker.celery_app worker --loglevel=info

# Terminal 3: Celery Beat (optional — for autonomous hourly scraping)
celery -A worker.celery_app beat --loglevel=info
```

### Triggering RSS Scraping via API

```bash
# Scrape all sources (dispatched to Celery worker)
curl -X POST http://127.0.0.1:8000/ingestion/scrape
# Returns: {"message": "Scraping for all sources started", "status": "accepted", "task_id": "..."}

# Scrape a single source
curl -X POST http://127.0.0.1:8000/ingestion/scrape/1
# Returns: {"message": "Scraping for source 1 started", "status": "accepted", "task_id": "..."}
```

### Querying Articles

```bash
# Get latest 20 articles
curl http://127.0.0.1:8000/articles

# Get 5 articles from the last 3 days
curl "http://127.0.0.1:8000/articles?limit=5&days=3"

# Get BBC News articles
curl "http://127.0.0.1:8000/articles?source_name=BBC%20News"

# Get source statistics
curl http://127.0.0.1:8000/articles/stats
```

### Adding a New Source

```bash
curl -X POST http://127.0.0.1:8000/ingestion/sources \
  -H "Content-Type: application/json" \
  -d '{"name": "Reuters", "url": "https://www.reutersagency.com/feed/", "country": "UK", "political_leaning": "center"}'
```

### Running the RSS Scraper Directly (without Celery)

```bash
python -m ingestion.feed_parser
```

### Direct Database Queries

```bash
psql kirikou_db -c "SELECT COUNT(*) FROM articles;"
psql kirikou_db -c "
    SELECT a.title, s.name as source, a.published_at 
    FROM articles a 
    JOIN sources s ON a.source_id = s.id 
    ORDER BY a.published_at DESC 
    LIMIT 10;
"
```

---

## 📁 Project Structure

```
kirikou/
├── api/                          # API layer (Week 6)
│   ├── __init__.py
│   ├── main.py                  # FastAPI app creation & config
│   └── routes/
│       ├── __init__.py
│       ├── articles.py          # Article endpoints
│       ├── sources.py           # Source endpoints
│       └── ingestion.py         # Scraping & source creation endpoints
├── worker/                       # Celery workers (Week 6)
│   ├── __init__.py
│   ├── celery_app.py            # Celery app, config, Beat schedule
│   └── tasks.py                 # Task definitions (scrape wrappers)
├── config.py                    # Configuration management
├── database/                    # Database layer (Week 4)
│   ├── __init__.py
│   ├── db.py                   # Engine, session management, get_db dependency
│   ├── init_db.py              # Database initialization
│   ├── models.py               # SQLAlchemy ORM models
│   ├── schemas.py              # Pydantic validation schemas
│   ├── schema.sql              # PostgreSQL schema with indexes
│   ├── add_sources.sql         # Validated news sources
│   ├── queries.sql             # Production SQL queries
│   ├── seed_data.sql           # Test data
│   └── utils.py                # Reusable query functions (DI + standalone)
├── ingestion/                   # Data ingestion module (Week 3)
│   ├── __init__.py
│   ├── feed_parser.py          # RSS scraper
│   └── validate_feeds.py       # Feed validation utility
├── docs/                        # Documentation
│   ├── DATABASE.md             # Database documentation
│   ├── CHANGELOG.md            # Detailed change history
│   ├── LICENSE                  # MIT License
│   └── README.md               # This file
├── logs/                        # Application logs
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (gitignored)
└── .env.example                # Environment template
```

---

## 🌐 News Sources

Kirikou currently ingests from **10+ validated sources** across the political spectrum:

### Political Balance

- **Center:** BBC News, Al Jazeera, Deutsche Welle
- **Center-Left:** CNN, The Guardian, NPR, The New York Times
- **Right:** Fox News
- **Tech-Focus:** TechCrunch, Ars Technica

### Geographic Diversity

- **UK:** BBC News, The Guardian
- **US:** CNN, Fox News, NPR, NYT, TechCrunch, Ars Technica
- **International:** Al Jazeera (Qatar), Deutsche Welle (Germany)

---

## 🎯 Key Features

### Autonomous Scraping with Celery Beat

Celery Beat triggers RSS scraping every hour automatically. No manual intervention needed — Kirikou runs 24/7 as an autonomous agent. Scraping executes in a separate Celery worker process, keeping the API fast and responsive.

### RESTful API with Auto-Documentation

FastAPI provides interactive Swagger documentation at `/docs`, showing all endpoints, request/response schemas, and allowing direct testing from the browser.

### Dependency Injection

FastAPI's dependency injection manages database sessions — one session per request, centralized lifecycle, route-controlled transactions. This pattern enables easy testing and clean separation of concerns.

### Pydantic Validation

All API inputs are validated through Pydantic schemas with custom validators:

- URL format validation (must start with `http://` or `https://`)
- Political leaning restricted to known values
- Query parameter constraints (e.g., `limit` between 1-500, `days` between 1-30)

### Automatic Deduplication

Articles with duplicate URLs are automatically skipped using PostgreSQL's `UNIQUE` constraint and `ON CONFLICT DO NOTHING` strategy.

### Event Clustering

Duplicate detection identifies when multiple sources cover the same story, enabling future bias analysis:

```sql
SELECT a1.title, s1.name AS source1, s2.name AS source2
FROM articles a1
JOIN articles a2 ON a1.title = a2.title AND a1.id < a2.id
JOIN sources s1 ON a1.source_id = s1.id
JOIN sources s2 ON a2.source_id = s2.id;
```

**This is the foundation for Week 11's LLM-powered bias analysis!**

### Performance Optimization

- **Batch inserts** for 50x speed improvement over individual inserts
- **Strategic indexes** on foreign keys, dates, and frequently queried columns
- **Eager loading** with `joinedload()` to avoid N+1 query problems
- **Connection pooling** for high-traffic API deployment

---

## 🔮 Roadmap

### Phase 1: The Foundation (✅ Complete - Week 4)

- [x] RSS feed scraper with error handling
- [x] PostgreSQL database with deduplication
- [x] Strategic indexes for performance
- [x] SQLAlchemy ORM with declarative models
- [x] Type-safe database operations
- [x] Reusable database utilities
- [x] Transaction-based operations with session management

### Phase 2: The Interface (✅ Complete - Week 6)

- [x] FastAPI REST API with modular routes
- [x] Pydantic schemas with custom validators
- [x] CRUD endpoints for articles and sources
- [x] Query parameter validation and filtering
- [x] Auto-generated API documentation (Swagger)
- [x] Background tasks for lightweight operations

### Phase 3: Async Architecture (✅ Complete - Week 6)

- [x] Celery workers for distributed task execution
- [x] Redis as message broker and result backend
- [x] FastAPI dependency injection for database sessions
- [x] Celery Beat for autonomous hourly scraping
- [x] Task ID tracking in API responses

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

---

## 📖 Learning Journey

This project is part of a **12-week Python Backend Development Journey** building a production-grade application from scratch. Each week focuses on specific backend engineering concepts:

- **Week 1-2:** Python fundamentals and OOP ✅
- **Week 3:** Networking, HTTP, and API consumption ✅
- **Week 4:** SQL, PostgreSQL, and database design ✅
- **Week 5:** ~~Flask~~ (Skipped — jumped directly to FastAPI)
- **Week 6:** FastAPI, Pydantic, Celery, Redis, DI, Pydantic Settings ✅ (Complete — Day 42)
- **Week 7:** Authentication, authorization, and security
- **Week 8:** Testing and quality assurance
- **Week 9:** Docker and CI/CD
- **Week 10:** Microservices architecture
- **Week 11:** Cloud deployment and LLM integration
- **Week 12:** Final polish and production deployment

**Progress:** Day 42 of 84 (50% complete) 🎉

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

- **Anthropic Claude** — AI development mentor
- **FastAPI** — Excellent framework and documentation
- **PostgreSQL Community** — Excellent database documentation
- **Celery Project** — Robust distributed task queue
- **Python Community** — Rich ecosystem of libraries
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

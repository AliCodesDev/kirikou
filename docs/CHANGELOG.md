# Changelog

All notable changes to Kirikou will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Week 7] - 2026-03-21

### Added

**JWT Authentication (Days 43-44):**

- User registration endpoint (`POST /auth/register`) with unique username/email validation
- User login endpoint (`POST /auth/login`) with JWT token response
- JWT token creation and verification with HS256 algorithm
- `get_current_user` dependency — extracts and verifies Bearer token from Authorization header
- `User` SQLAlchemy model with hashed password, role, and is_active fields
- User query utilities: `get_user_by_id`, `get_user_by_username`, `get_user_by_email`, `create_user`
- Pydantic schemas: `UserCreate`, `UserResponse`, `TokenResponse`

**Role-Based Access Control (Day 44):**

- `UserRole` enum with `ADMIN` and `READER` roles
- `require_role()` dependency factory for protecting endpoints
- Ingestion endpoints (`POST /ingestion/*`) restricted to admin role
- Inactive user detection — returns 403 for deactivated accounts

**Security Hardening (Day 45):**

- Hardened `CryptContext` — explicit `bcrypt__rounds=12` + `deprecated="auto"` for future-proof rehashing
- Password max length (128 chars) added to `UserCreate` schema — bcrypt truncates at 72 bytes
- Updated `.env.example` with all settings: `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_EXPIRE_MINUTES`
- Generation instructions for secret keys as comments in `.env.example`

### Security Audit

- ✅ Generic login error message — no username/password enumeration
- ✅ `UserResponse` excludes `hashed_password` — never exposed in API responses
- ✅ `get_user_by_id` (used by `get_current_user`) excludes `hashed_password`
- ✅ Both `SECRET_KEY` and `JWT_SECRET_KEY` use `SecretStr` — never leak in logs
- ✅ `.env` is gitignored (`.env`, `.env.*`, `.env.local`)
- ✅ No hardcoded secrets found in codebase

### Technical Details

**API Endpoints:** 11 total (5 GET, 4 POST, 1 health check, 1 login)

**Auth Schemas:** 3 (UserCreate, UserResponse, TokenResponse)

**Dependencies Added:** PyJWT, passlib[bcrypt], bcrypt

---

## [Week 6] - 2026-02-21

### Added

**FastAPI REST API (Days 36-38):**

- FastAPI application with modular route organization
- RESTful API endpoints:
  - `GET /` — Health check
  - `GET /sources` — List all news sources
  - `GET /sources/{id}` — Get a single source
  - `GET /articles` — List articles with `limit`, `days`, and `source_name` query params
  - `GET /articles/stats` — Source activity statistics
  - `GET /articles/{id}` — Get a single article with full detail
  - `POST /sources` — Create a new source with background feed validation
  - `POST /scrape` — Trigger full RSS scraping (Celery task)
  - `POST /scrape/{source_id}` — Trigger scraping for a single source (Celery task)
- Auto-generated Swagger documentation at `/docs`

**Pydantic Schemas (Day 37):**

- `SourceResponse` — Source output with `from_attributes` for ORM compatibility
- `SourceCreate` — Source input with URL and political leaning validators
- `SourceUpdate` — Partial update schema (all fields optional)
- `SourceBrief` — Minimal source info embedded in article responses
- `ArticleResponse` — Article output with nested `SourceBrief`
- `ArticleDetail` — Extended article response with description, author, scraped_at
- `SourceStats` — Source activity statistics response
- `ScrapeResponse` — Background task trigger response with optional `task_id`
- Custom validators: URL format validation, political leaning restriction to known values
- Query parameter validation via `Query(ge=1, le=500)` replacing manual if-statements

**FastAPI Dependency Injection (Day 39):**

- `get_db()` generator dependency in `database/db.py` for FastAPI session management
- One database session per request — centralized lifecycle management
- Refactored 7 utility functions to accept injected `Session` parameter:
  - `get_all_sources(db)`, `get_source_by_id(db)`, `get_recent_articles(db)`
  - `get_articles_by_source(db)`, `get_source_stats(db)`, `get_article_by_id(db)`
  - `create_source(db)` with `flush()` instead of `commit()` — route controls transaction
- Standalone wrappers for CLI/background task compatibility:
  - `get_all_sources_standalone()`, `get_source_by_id_standalone()`, etc.
- All 3 route files updated to use `Depends(get_db)` pattern

**API Architecture:**

- Route organization: `api/routes/articles.py`, `api/routes/sources.py`, `api/routes/ingestion.py`
- Pydantic schemas in `database/schemas.py`
- Nested JSON responses (articles embed source data)
- Proper HTTP status codes (200, 201, 202, 400, 404, 422)
- Input validation at both query parameter and request body levels

**Celery Workers & Redis (Day 40):**

- Celery application (`worker/celery_app.py`) with Redis message broker
- Task definitions (`worker/tasks.py`):
  - `scrape_all_sources_task` — scrape all RSS sources via Celery worker
  - `scrape_source_by_id_task` — scrape single source via Celery worker
- Celery Beat schedule — automatic scraping every hour (autonomous operation)
- Redis as message broker (`redis://localhost:6379/0`) and result backend (`redis://localhost:6379/1`)
- Task ID tracking in scrape API responses for future status monitoring
- `ScrapeResponse` schema updated with optional `task_id` field

**Pydantic Settings Configuration (Day 41):**

- Migrated from manual `os.environ.get()` config to Pydantic `BaseSettings`
- Type-safe validation for all settings (auto-cast strings to `int`, `bool`, etc.)
- `SecretStr` for `secret_key` — prevents accidental secret leaking in logs
- `@field_validator` for `log_level` — rejects invalid values at startup
- `@lru_cache` singleton via `get_settings()` — one shared instance app-wide
- `.env.example` template for project documentation
- Removed `python-dotenv` dependency — Pydantic Settings handles `.env` natively
- Removed manual `validate()` method — Pydantic validates on instantiation (fail fast)
- Updated 6 files to use new settings pattern: `main.py`, `db.py`, `celery_app.py`, `feed_parser.py`, `init_db.py`, `utils.py`

### Changed

- Refactored database utility functions to accept injected `Session` parameter (DI pattern)
- Utility functions use `flush()` for write operations — routes control `commit()`
- Scrape endpoints migrated from FastAPI `BackgroundTasks` to Celery tasks
- Source creation retains `BackgroundTasks` for lightweight validation/logging
- `feed_parser.py` updated to use standalone wrapper functions
- Updated `config.py` with `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` settings
- Updated `database/__init__.py` to export `get_db`

### Technical Details

**API Endpoints:** 9 total (5 GET, 3 POST, 1 health check)

**Pydantic Models:** 8 schemas with validation

**Celery Tasks:** 2 (full scrape, single source scrape)

**Beat Schedule:** Scrape all sources every hour (3600s)

**Dependencies Added:** fastapi, uvicorn, celery, redis

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

**Days Completed:** 45 of 84 (54%)

**Current Phase:** Week 7 Complete ✅ — Authentication & Security

**Next Phase:** Week 8 — Testing & Quality Assurance (pytest)

**Technical Milestones:**

- ✅ Python and OOP fundamentals
- ✅ RSS scraping and data ingestion
- ✅ PostgreSQL database design
- ✅ SQLAlchemy ORM implementation
- ✅ Production-ready error handling
- ✅ Comprehensive documentation
- ✅ FastAPI REST API with Pydantic validation
- ✅ Background tasks for scraping and source validation
- ✅ FastAPI Dependency Injection for database sessions
- ✅ Celery workers with Redis broker for async scraping
- ✅ Celery Beat for autonomous hourly scraping
- ✅ JWT authentication with HS256 signing
- ✅ Role-Based Access Control (RBAC) with admin/reader roles
- ✅ Hardened password hashing with bcrypt CryptContext
- ✅ Security audit passed — no hash leaks, generic errors, no hardcoded secrets

**Portfolio Highlights:**

- 1610+ articles from 10+ global news sources
- Production-grade database design with strategic indexes
- Type-safe ORM with automatic relationships
- RESTful API with 9 endpoints and auto-generated docs
- Pydantic schemas with custom validators
- Dependency injection for testable database access
- Celery workers with Redis for distributed task processing
- Autonomous hourly scraping via Celery Beat
- Task ID tracking for async job monitoring
- Clean, documented codebase
- Professional Git workflow with tagged milestones
- Pydantic Settings with type-safe validation and SecretStr

---

## Coming Next

**Week 7 Complete** ✅

- JWT authentication with user registration and login
- Role-Based Access Control with admin/reader roles
- Hardened password hashing and security audit

**Week 8 (Days 50-56):** Testing & Quality Assurance

- Comprehensive pytest suite
- Unit tests for all modules
- Integration tests for database operations
- 80%+ code coverage

**Week 11 (Days 71-77):** LLM Integration

- OpenAI/Anthropic/Google API integration
- RAG (Retrieval-Augmented Generation) pattern
- Comparative bias analysis across sources
- Narrative difference detection

-- Database schema for news article aggregation
DROP TABLE IF EXISTS articles;
DROP TABLE IF EXISTS sources;

-- Sources table (news outlets)
CREATE TABLE sources (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,  -- "BBC News", "CNN"
    url TEXT NOT NULL,
    country TEXT,
    political_leaning TEXT
);

-- Articles table
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    source_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,  -- Short summary from RSS (usually available)
    content TEXT,      -- Full content (might not always be available)
    author TEXT,
    published_at TIMESTAMP NOT NULL,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    url TEXT NOT NULL UNIQUE,
    FOREIGN KEY (source_id) REFERENCES sources(id)
);


-- ==============================================
-- INDEXES FOR QUERY OPTIMIZATION
-- ==============================================

-- Index 1: Foreign Key - Articles to Sources relationship
-- Used by: ALL queries that JOIN articles and sources
-- Impact: Speeds up JOINs dramatically
CREATE INDEX idx_articles_source_id ON articles(source_id);

-- Index 2: Published Date - Time-based filtering and sorting
-- Used by: Query 1 (ORDER BY), Query 2 (7-day filter), Query 3 (24h filter)
-- Impact: Fast sorting by date, quick "recent articles" queries
CREATE INDEX idx_articles_published_at ON articles(published_at DESC);
-- Note: DESC because we usually want newest first

-- Index 3: Composite Index - Most common query pattern
-- Used by: "Get recent articles from a specific source" (Query 5)
-- Impact: Optimizes the most frequent query pattern
CREATE INDEX idx_articles_source_date ON articles(source_id, published_at DESC);
-- Note: Column order matters! (source_id first, then published_at)

-- Index 4: Title - Duplicate detection and event clustering
-- Used by: Query 4 (duplicate detection), future full-text search
-- Impact: Fast grouping by title, find duplicate stories instantly
CREATE INDEX idx_articles_title ON articles(title);

-- Primary keys and UNIQUE constraints are already auto-indexed:
-- - sources.id (PRIMARY KEY)
-- - sources.name (UNIQUE)
-- - articles.id (PRIMARY KEY)
-- - articles.url (UNIQUE)
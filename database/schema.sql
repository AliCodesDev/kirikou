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


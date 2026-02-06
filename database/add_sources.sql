-- Validated RSS feeds for Kirikou
-- All feeds tested and confirmed working (13 sources)
-- Run: psql kirikou_db < database/add_sources.sql

INSERT INTO sources (name, url, country, political_leaning) VALUES
    -- UK Sources (3)
    ('BBC News', 'http://feeds.bbci.co.uk/news/rss.xml', 'UK', 'center'),
    ('The Guardian', 'https://www.theguardian.com/world/rss', 'UK', 'center-left'),
    
    -- US Sources (7)
    ('CNN', 'http://rss.cnn.com/rss/edition.rss', 'US', 'center-left'),
    ('Fox News', 'https://moxie.foxnews.com/google-publisher/latest.xml', 'US', 'right'),
    ('NPR', 'https://feeds.npr.org/1001/rss.xml', 'US', 'center-left'),
    ('The New York Times', 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml', 'US', 'center-left'),
    ('Washington Post', 'https://feeds.washingtonpost.com/rss/world', 'US', 'center-left'),
    ('TechCrunch', 'https://techcrunch.com/feed/', 'US', 'tech-focus'),
    ('The Verge', 'https://www.theverge.com/rss/index.xml', 'US', 'tech-focus'),
    ('Ars Technica', 'http://feeds.arstechnica.com/arstechnica/index', 'US', 'tech-focus'),
    
    -- International Sources (3)
    ('Al Jazeera', 'https://www.aljazeera.com/xml/rss/all.xml', 'Qatar', 'center'),
    ('Deutsche Welle', 'https://rss.dw.com/xml/rss-en-all', 'Germany', 'center'),
    ('France 24', 'https://www.france24.com/en/rss', 'France', 'center')

ON CONFLICT (name) DO NOTHING;
-- Prevents errors if sources already exist
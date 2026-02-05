-- Clear existing data
TRUNCATE articles, sources RESTART IDENTITY CASCADE;

-- Insert test sources
INSERT INTO sources (name, url, country, political_leaning) VALUES
    ('BBC News', 'https://feeds.bbci.co.uk/news/rss.xml', 'UK', 'center'),
    ('CNN', 'https://rss.cnn.com/rss/edition.rss', 'US', 'center-left'),
    ('Fox News', 'https://moxie.foxnews.com/google-publisher/latest.xml', 'US', 'right'),
    ('Al Jazeera', 'https://www.aljazeera.com/xml/rss/all.xml', 'Qatar', 'center'),
    ('Reuters', 'https://www.reutersagency.com/feed/', 'UK', 'center');

-- Insert test articles
INSERT INTO articles (source_id, title, description, url, published_at) VALUES
    -- BBC articles
    (1, 'Breaking: Election Results', 'Election results are in', 'https://bbc.com/election-1', NOW() - INTERVAL '1 hour'),
    (1, 'Weather Update', 'Severe weather warning', 'https://bbc.com/weather-1', NOW() - INTERVAL '3 hours'),
    (1, 'Tech Innovation', 'New AI breakthrough', 'https://bbc.com/tech-1', NOW() - INTERVAL '2 days'),
    
    -- CNN articles (including duplicate title)
    (2, 'Breaking: Election Results', 'CNN coverage of election', 'https://cnn.com/election-1', NOW() - INTERVAL '2 hours'),
    (2, 'Sports Update', 'Championship finals', 'https://cnn.com/sports-1', NOW() - INTERVAL '5 hours'),
    (2, 'Market Analysis', 'Stock market trends', 'https://cnn.com/market-1', NOW() - INTERVAL '1 day'),
    
    -- Fox articles (including duplicate title)
    (3, 'Breaking: Election Results', 'Fox perspective on election', 'https://fox.com/election-1', NOW() - INTERVAL '1.5 hours'),
    (3, 'Political Commentary', 'Analysis of recent events', 'https://fox.com/politics-1', NOW() - INTERVAL '6 hours'),
    
    -- Al Jazeera articles
    (4, 'Middle East Update', 'Regional developments', 'https://aljazeera.com/mideast-1', NOW() - INTERVAL '4 hours'),
    (4, 'Climate Report', 'Global climate trends', 'https://aljazeera.com/climate-1', NOW() - INTERVAL '3 days'),
    
    -- Reuters has NO recent articles (for testing inactive sources)
    (5, 'Old Article', 'This is old', 'https://reuters.com/old-1', NOW() - INTERVAL '2 days');

    
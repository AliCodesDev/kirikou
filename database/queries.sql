--Query 1: Recent Articles Dashboard
--Use case: Homepage showing latest 20 articles with source badges
SELECT
    a.title,
    a.url,
    a.published_at,
    s.name AS source_name,
    s.country,
    s.political_leaning
FROM articles a
JOIN sources s ON a.source_id = s.id
ORDER BY a.published_at DESC
LIMIT 20;

--Query 2: Source Activity Report
--Use case: Analytics showing which sources are most active

SELECT
    s.name AS source_name,
    COUNT(a.id) AS total_articles,
    COUNT(CASE WHEN a.published_at > NOW() - INTERVAL '7 days' THEN 1 END) AS articles_last_7d
    --    ^^^^ Proper CASE syntax: CASE WHEN condition THEN value END
FROM sources s
LEFT JOIN articles a ON s.id = a.source_id
GROUP BY s.id, s.name  -- Include s.name for clarity (PostgreSQL allows grouping just by PK, but this is clearer)
ORDER BY total_articles DESC;


--Query 3: Find Inactive Sources
--Use case: Alert system - which RSS feeds might be broken?
--Requirements:
-- Find sources that have NO articles published in last 24 hours
-- Include sources that have never had articles
-- Show source name, URL, and last article date (or NULL)

SELECT
    s.name AS source_name,
    s.url,
    MAX(a.published_at) AS last_article_date
FROM sources s
LEFT JOIN articles a ON s.id = a.source_id
GROUP BY s.id
HAVING MAX(a.published_at) IS NULL OR MAX(a.published_at) < NOW() - INTERVAL '24 hours'
ORDER BY last_article_date ASC NULLS FIRST;

-- Query 4: Detect Duplicate Stories
-- Use case: Find when multiple sources cover the same event
-- Requirements:

-- Find articles with identical titles
-- Show both source names
-- Only show titles that appear more than once

SELECT
    a1.title,
    s1.name AS source1,
    s2.name AS source2,
    a1.url AS url1,
    a2.url AS url2,
    a1.published_at AS published1,
    a2.published_at AS published2
FROM articles a1
JOIN articles a2 ON a1.title = a2.title AND a1.id < a2.id
JOIN sources s1 ON a1.source_id = s1.id
JOIN sources s2 ON a2.source_id = s2.id
ORDER BY a1.title;

-- Query 5: Articles by Source with Filters
-- Use case: API endpoint /articles?source=BBC&days=7
-- Requirements:

-- Get articles from a specific source
-- Published within last N days
-- Include source metadata
-- Sort by most recent

SELECT
    a.title,
    a.url,
    a.published_at,
    s.name AS source_name,
    s.country,
    s.political_leaning
FROM articles a
JOIN sources s ON a.source_id = s.id
WHERE s.name = %s 
  AND a.published_at >= NOW() - INTERVAL '1 day' * %s
ORDER BY a.published_at DESC;







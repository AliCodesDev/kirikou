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
├── config.py           # Configuration management
├── ingestion/          # Data ingestion module
│   └── feed_parser.py  # RSS feed fetching and parsing
├── test_config.py      # Configuration tests
├── test_setup.py       # Setup verification
├── requirements.txt    # Python dependencies
├── logs/               # Application logs
└── .env.example        # Environment template
```

## Usage

Run the RSS feed scraper:

```bash
python -m ingestion.feed_parser
```

This will fetch articles from configured news sources (BBC, NY Times, Reuters, Al Jazeera) and log the results.

## Status

🚧 **In Development** - Week 3 of 12-week build

**Completed:**

- Configuration and logging system
- RSS feed scraper (Day 21)
  - `fetch_feed()` - Fetch and parse RSS feeds
  - `extract_articles()` - Extract article metadata
  - `scrape_feeds()` - Orchestrate multiple feed scraping

**Next up:** Database integration

## License

MIT

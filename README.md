# Kirikou

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
├── test_config.py      # Configuration tests
├── requirements.txt    # Python dependencies
├── logs/               # Application logs
└── .env.example        # Environment template
```

## Status

🚧 **In Development** - Week 3 of 12-week build

**Currently building:** Configuration and logging system
**Next up:** RSS feed scraper (Day 21)

## License

MIT

from fastapi import FastAPI
from config import Config
from api.routes import sources, articles, ingestion

app = FastAPI(title=Config.APP_NAME, debug=Config.DEBUG)
# Setup logging
Config.setup_logging()

# Validate config
Config.validate()


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Kirikou is alive!"}



# Include API routes
app.include_router(sources.router)
app.include_router(articles.router)
app.include_router(ingestion.router)











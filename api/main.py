from fastapi import FastAPI
from config import get_settings
from api.routes import sources, articles, ingestion

settings = get_settings()
settings.setup_logging()

app = FastAPI(title=settings.app_name, debug=settings.debug)


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Kirikou is alive!"}



# Include API routes
app.include_router(sources.router)
app.include_router(articles.router)
app.include_router(ingestion.router)











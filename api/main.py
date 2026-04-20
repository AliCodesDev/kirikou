from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from config import get_settings
from api.rate_limiter import limiter
from api.routes import sources, articles, ingestion
from auth import routes as auth_routes

settings = get_settings()
settings.setup_logging()

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response


@app.get("/")
@limiter.limit(settings.rate_limit_default)
def read_root(request: Request, response: Response):
    """Health check endpoint."""
    return {"status": "ok", "message": "Kirikou is alive!"}


# Include API routes
app.include_router(sources.router)
app.include_router(articles.router)
app.include_router(ingestion.router)
app.include_router(auth_routes.router)













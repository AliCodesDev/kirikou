"""
Database connection and session management.

Provides:
- Engine: Connection to PostgreSQL
- Session factory: Creates database sessions
- get_session(): Context manager for transactions
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from config import Config
import logging

logger = logging.getLogger(__name__)

# Create engine (connection pool to database)
engine = create_engine(
    Config.DATABASE_URL,
    echo=False,  # Set to True to see SQL queries (debugging)
    pool_size=5,  # Connection pool size
    max_overflow=10  # Max connections beyond pool_size
)

# Session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,  # Manual commit (safer)
    autoflush=False    # Manual flush (more control)
)


@contextmanager
def get_session() -> Session:
    """
    Provide a transactional session.
    
    Usage:
        with get_session() as session:
            article = session.query(Article).first()
            # Automatic commit on success
            # Automatic rollback on error
    
    Yields:
        Session: Database session
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()  # Commit if no exception
        logger.debug("Session committed successfully")
    except Exception as e:
        session.rollback()  # Rollback on error
        logger.error(f"Session rollback due to error: {e}")
        raise
    finally:
        session.close()  # Always close
        logger.debug("Session closed")


def get_session_no_commit() -> Session:
    """
    Get a session without automatic commit (for read-only operations).
    
    Usage:
        session = get_session_no_commit()
        try:
            articles = session.query(Article).all()
        finally:
            session.close()
    
    Returns:
        Session: Database session
    """
    return SessionLocal()
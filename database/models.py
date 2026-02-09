"""
SQLAlchemy models for Kirikou database.

Defines Source and Article tables as Python classes.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime


# Base class for all models
Base = declarative_base()

class Source(Base):
    """
    News source (BBC, CNN, etc.)
    
    Relationships:
        articles: One source has many articles
    """
    __tablename__ = 'sources'

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    url = Column(String, nullable=False)
    country = Column(String, nullable=True)
    political_leaning = Column(String, nullable=True)

    # Relationships
    articles = relationship('Article', back_populates='source')

    def __repr__(self):
        return f"<Source(id={self.id}, name='{self.name}')>"


class Article(Base):
    """
    News article.
    
    Relationships:
        source: Many articles belong to one source
    """
    __tablename__ = 'articles'

    # Columns
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey('sources.id'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    author = Column(String, nullable=True)
    published_at = Column(DateTime, nullable=False)
    scraped_at = Column(DateTime, default=datetime.now)
    url = Column(String, nullable=False)


    # Relationships
    source = relationship('Source', back_populates='articles')

    def __repr__(self):
        return f"<Article(id={self.id}, title='{self.title[:30]}...')>"
    
    def to_dict(self):
        """Convert Article to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'source_id': self.source_id,
            'title': self.title,
            'description': self.description,
            'content': self.content,
            'author': self.author,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'scraped_at': self.scraped_at.isoformat() if self.scraped_at else None,
            'url': self.url
        }
    
    




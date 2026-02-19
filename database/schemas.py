from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime

# --- Schemas ---
class SourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    url: str
    country: str | None = None
    political_leaning: str | None = None


class SourceCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(
        min_length=1,
        max_length=150,
        description="Name of the news source"
    )
    url: str = Field(
        min_length=10,
        description="RSS feed URL"
    )
    country: str | None = Field(
        default=None,
        max_length=50,
        description="Country of origin"
    )
    political_leaning: str | None = Field(
        default=None,
        description="Political leaning classification"
    )

    @field_validator('url')
    @classmethod
    def url_must_be_valid(cls, v: str) -> str:
        """Ensure URL starts with http:// or https://"""
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL must start with http:// or https://')
        return v
    
    @field_validator('political_leaning')
    @classmethod
    def leaning_must_be_valid(cls, v: str | None) -> str | None:
        """Restrict political leaning to known values."""
        if v is None:
            return v
        allowed = {'left', 'center-left', 'center', 'center-right', 'right', 'tech-focus'}
        if v.lower() not in allowed:
            raise ValueError(f'Must be one of: {", ".join(sorted(allowed))}')
        return v.lower()

class SourceUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
        description="Name of the news source"
    )
    url: str | None = Field(
        default=None,
        min_length=10,
        description="RSS feed URL"
    )
    country: str | None = Field(
        default=None,
        max_length=50,
        description="Country of origin"
    )
    political_leaning: str | None = Field(
        default=None,
        description="Political leaning classification"
    )

    @field_validator('url')
    @classmethod
    def url_must_be_valid(cls, v: str | None) -> str | None:
        """Ensure URL starts with http:// or https:// if provided."""
        if v is None:
            return v
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL must start with http:// or https://')
        return v
    
    @field_validator('political_leaning')
    @classmethod
    def leaning_must_be_valid(cls, v: str | None) -> str | None:
        """Restrict political leaning to known values if provided."""
        if v is None:
            return v
        allowed = {'left', 'center-left', 'center', 'center-right', 'right', 'tech-focus'}
        if v.lower() not in allowed:
            raise ValueError(f'Must be one of: {", ".join(sorted(allowed))}')
        return v.lower()

class SourceBrief(BaseModel):
    """Minimal source info for embedding in article responses."""
    id: int
    name: str
    political_leaning: str | None = None


class ArticleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    url: str
    published_at: datetime 
    source: SourceBrief

class ArticleDetail(ArticleResponse):
    description: str | None = None
    author: str | None = None
    scraped_at: datetime


class SourceStats(BaseModel):
    source_name: str
    total_articles: int
    articles_last_7d: int


class ScrapeResponse(BaseModel):
    message: str
    status: str













import os 
import logging
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, field_validator
from functools import lru_cache


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file='.env', 
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra="ignore"
        )

    # Required (no default = crash if missing)
    database_url: str
    secret_key: SecretStr

    log_level: str = 'INFO'
    log_file: str = 'logs/kirikou.log'
    debug: bool = False
    app_name: str = "Kirikou Media Intelligence"
    fetch_interval: int = 3600
    request_timeout: int = 10
    celery_broker_url: str = 'redis://localhost:6379/0'
    celery_result_backend: str = 'redis://localhost:6379/1'

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in allowed:
            raise ValueError(f"log_level must be one of {allowed}")
        return v.upper()
    
    def setup_logging(self):
        os.makedirs('logs', exist_ok=True)
        logging.basicConfig(
            level = getattr(logging, self.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )


@lru_cache()
def get_settings() -> Settings:
    return Settings()

        


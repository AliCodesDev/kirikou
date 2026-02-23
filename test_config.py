# test_config.py (temporary test file)
import logging
from config import get_settings

# Pydantic validates on instantiation; a missing required field raises here
try:
    settings = get_settings()
    print("✅ Config is valid")
except Exception as e:
    print(f"❌ Config error: {e}")
    raise

# Setup logging
settings.setup_logging()

# Print config values
print(f"Database: {settings.database_url}")
print(f"Log Level: {settings.log_level}")
print(f"Debug Mode: {settings.debug}")

# Test logging
logger = logging.getLogger(__name__)
logger.info("Testing logging setup")
logger.debug("This won't show if LOG_LEVEL=INFO")
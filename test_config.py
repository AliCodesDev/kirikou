# test_config.py (temporary test file)
from config import Config

# Setup logging
Config.setup_logging()

# Validate config
try:
    Config.validate()
    print("✅ Config is valid")
except ValueError as e:
    print(f"❌ Config error: {e}")

# Print config values
print(f"Database: {Config.DATABASE_URL}")
print(f"Log Level: {Config.LOG_LEVEL}")
print(f"Debug Mode: {Config.DEBUG}")

# Test logging
import logging
logger = logging.getLogger(__name__)
logger.info("Testing logging setup")
logger.debug("This won't show if LOG_LEVEL=INFO")
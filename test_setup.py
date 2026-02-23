"""Test that configuration system is working."""
import logging
from config import get_settings

def main():
    print("=== Testing Kirikou Configuration System ===\n")

    settings = get_settings()

    # Test 1: Setup logging
    print("1. Setting up logging...")
    settings.setup_logging()
    logger = logging.getLogger(__name__)
    print("   ✅ Logging configured\n")

    # Test 2: Validate config (Pydantic validates on instantiation — if we got here, it passed)
    print("2. Validating configuration...")
    print("   ✅ All required config present\n")

    # Test 3: Display config
    print("3. Current Configuration:")
    print(f"   App Name: {settings.app_name}")
    print(f"   Database: {settings.database_url}")
    print(f"   Log Level: {settings.log_level}")
    print(f"   Log File: {settings.log_file}")
    print(f"   Debug Mode: {settings.debug}")
    print(f"   Fetch Interval: {settings.fetch_interval}s")
    print()

    # Test 4: Test logging at different levels
    print("4. Testing log levels...")
    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")
    print(f"   ✅ Check logs/{settings.log_file.split('/')[-1]} for output\n")

    print("=== All Tests Passed! ===")
    print("Configuration system is ready for the RSS scraper (Day 21)")

if __name__ == "__main__":
    main()
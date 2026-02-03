"""Test that configuration system is working."""
import logging
from config import Config

def main():
    print("=== Testing Kirikou Configuration System ===\n")
    
    # Test 1: Setup logging
    print("1. Setting up logging...")
    Config.setup_logging()
    logger = logging.getLogger(__name__)
    print("   ✅ Logging configured\n")
    
    # Test 2: Validate config
    print("2. Validating configuration...")
    try:
        Config.validate()
        print("   ✅ All required config present\n")
    except ValueError as e:
        print(f"   ❌ Config error: {e}\n")
        return
    
    # Test 3: Display config
    print("3. Current Configuration:")
    print(f"   App Name: {Config.APP_NAME}")
    print(f"   Database: {Config.DATABASE_URL}")
    print(f"   Log Level: {Config.LOG_LEVEL}")
    print(f"   Log File: {Config.LOG_FILE}")
    print(f"   Debug Mode: {Config.DEBUG}")
    print(f"   Fetch Interval: {Config.FETCH_INTERVAL}s")
    print()
    
    # Test 4: Test logging at different levels
    print("4. Testing log levels...")
    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")
    print(f"   ✅ Check logs/{Config.LOG_FILE.split('/')[-1]} for output\n")
    
    print("=== All Tests Passed! ===")
    print("Configuration system is ready for the RSS scraper (Day 21)")

if __name__ == "__main__":
    main()
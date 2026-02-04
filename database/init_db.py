import psycopg2
import logging
from pathlib import Path
from config import Config

Config.setup_logging()
logger = logging.getLogger(__name__)

def init_database():
    """Initialize the database with the schema."""
    conn = None  # Initialize to None for finally block
    cursor = None
    
    try:
        # Connect to kirikou_db
        conn = psycopg2.connect(Config.DATABASE_URL)
        logger.info("Connected to database")

        # Create a cursor
        cursor = conn.cursor()

        # Read schema.sql file
        schema_path = Path(__file__).parent / "schema.sql"
        with open(schema_path, "r") as f:
            sql_content = f.read()

        # Execute the SQL
        cursor.execute(sql_content)

        # Commit the transaction
        conn.commit()
        logger.info("Database schema created successfully")
        
    except psycopg2.Error as db_error:
        logger.error(f"Database error: {db_error}")
        if conn:
            conn.rollback()  # Undo any partial changes
        raise  # Re-raise to notify caller
        
    except FileNotFoundError:
        logger.error(f"Schema file not found: {schema_path}")
        raise
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
        
    finally:
        # Always close resources, even if error occurred
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            logger.info("Connection closed")


if __name__ == "__main__":
    init_database()
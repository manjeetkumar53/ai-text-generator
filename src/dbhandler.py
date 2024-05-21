import os,sys
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv(override=True)

# Add the directory containing dbhandler_mysql to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from dbhandler_mysql import save_to_database as save_to_database_mysql
from dbhandler_sqllite import save_to_database as save_to_database_sqllite
from logging_config import get_logger

# Import the logging module
logger = get_logger()


def save_to_database(input_text, generated_text):
    database_handlers = {
        'mysql': save_to_database_mysql,
        'sqllite': save_to_database_sqllite
    }

    use_database = os.environ.get('DB_NAME', 'sqllite')

    if use_database not in database_handlers:
        logger.error(f"Error: Invalid database name '{use_database}'")
        return None

    try:
        save_function = database_handlers[use_database]
        save_function(input_text, generated_text)
    except Exception as e:
        logger.error(f"Error in saving to database: {e}")
        return None

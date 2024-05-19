import sqlite3
from contextlib import closing
from src.logging_config import get_logger

# Initialize logger
logger = get_logger()

def connect_to_db():
    """
    Connects to the SQLite database and returns a connection object.

    Returns:
        sqlite3.Connection: A connection object for interacting with the SQLite database.
    """
    return sqlite3.connect('database.db')  # Replace with your database connection details

def check_table_exists(cursor, table_name):
    """
    Checks if a table exists in the database.

    Args:
        cursor (sqlite3.Cursor): A cursor object for interacting with the database.
        table_name (str): The name of the table to check for.

    Returns:
        bool: True if the table exists, False otherwise.
    """
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name=?', (table_name,))
    return cursor.fetchone() is not None

def create_table_if_not_exists(cursor, table_name):
    """
    Creates a table if it doesn't exist in the database.

    Args:
        cursor (sqlite3.Cursor): A cursor object for interacting with the database.
        table_name (str): The name of the table to create.
    """
    if not check_table_exists(cursor, table_name):
        cursor.execute(f'''
            CREATE TABLE {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_text TEXT NOT NULL,
                generated_text TEXT NOT NULL
            );
        ''')

def insert_data(cursor, table_name, input_text, generated_text):
    """
    Inserts data into a table.

    Args:
        cursor (sqlite3.Cursor): A cursor object for interacting with the database.
        table_name (str): The name of the table to insert data into.
        input_text (str): The user's input text.
        generated_text (str): The generated text by the model.
    """
    cursor.execute(f'INSERT INTO {table_name} (input_text, generated_text) VALUES (?, ?)', (input_text, generated_text))

def save_to_database(input_text, generated_text):
    """
    Saves data to the database.

    Args:
        input_text (str): The user's input text.
        generated_text (str): The generated text by the model.
    """
    try:
        with closing(connect_to_db()) as conn:
            with closing(conn.cursor()) as cursor:
                create_table_if_not_exists(cursor, "generated_text")  # Ensure table exists before inserting data
                insert_data(cursor, "generated_text", input_text, generated_text)
                conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error saving to database: {e}")

import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from contextlib import closing

# Load environment variables from .env file
load_dotenv(override=True)

def connect_to_db():
    """
    Connects to the MySQL database and returns a connection object.

    Returns:
        mysql.connector.connection.MySQLConnection: A connection object to the MySQL database.

    Raises:
        Error: If connection fails.
    """
    try:
        # Get MySQL connection details from environment variables
        host = os.getenv("MYSQL_HOST")
        user = os.getenv("MYSQL_USER")
        password = os.getenv("MYSQL_PASSWORD")
        database = os.getenv("MYSQL_DATABASE")

        # Connect to the database
        return mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
    except Error as e:
        raise Error(f"Error connecting to database: {e}")

def check_table_exists(cursor, table_name):
    """
    Checks if a table exists in the database.

    Args:
        cursor (mysql.connector.cursor.MySQLCursor): A MySQL cursor object.
        table_name (str): The name of the table to check.

    Returns:
        bool: True if the table exists, False otherwise.
    """
    cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = %s", (table_name,))
    return cursor.fetchone()[0] == 1

def create_table_if_not_exists(cursor, table_name):
    """
    Creates a table if it doesn't exist in the database.

    Args:
        cursor (mysql.connector.cursor.MySQLCursor): A MySQL cursor object.
        table_name (str): The name of the table to create.
    """
    if not check_table_exists(cursor, table_name):
        cursor.execute(f'''
            CREATE TABLE {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                input_text TEXT NOT NULL,
                generated_text TEXT NOT NULL
            );
        ''')

def insert_data(cursor, table_name, input_text, generated_text):
    """
    Inserts data into a table.

    Args:
        cursor (mysql.connector.cursor.MySQLCursor): A MySQL cursor object.
        table_name (str): The name of the table to insert data into.
        input_text (str): The user's input text.
        generated_text (str): The generated text by the model.
    """
    sql = f"INSERT INTO {table_name} (input_text, generated_text) VALUES (%s, %s)"
    val = (input_text, generated_text)
    cursor.execute(sql, val)

def save_to_database(input_text, generated_text):
    """
    Saves data to the database.

    Args:
        input_text (str): The user's input text.
        generated_text (str): The generated text by the model.
    """
    try:
        print(f"input_text: {input_text}, generated_text: {generated_text}")

        with closing(connect_to_db()) as conn:
            with closing(conn.cursor()) as cursor:
                # Create table if it doesn't exist
                create_table_if_not_exists(cursor, "generated_text")

                # Insert data
                insert_data(cursor, "generated_text", input_text, generated_text)

                # Commit changes
                conn.commit()
    except Error as e:
        print(f"Error saving to database: {e}")


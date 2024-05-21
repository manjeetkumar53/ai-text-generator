import sys
import unittest
import mysql.connector
import os
from dotenv import load_dotenv
import pytest
# Load environment variables from .env file
load_dotenv(override=True)

# Add the directory containing dbhandler_mysql to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Import the dbhandler_mysql module
import dbhandler_mysql as dbhandler

@pytest.mark.skip
class TestDBHandler(unittest.TestCase):
    
    def setUp(self):
        # Connect to the test database
        # Get MySQL connection details from environment variables
        host = os.getenv("MYSQL_HOST")
        user = os.getenv("MYSQL_USER")
        password = os.getenv("MYSQL_PASSWORD")
        database = os.getenv("MYSQL_DATABASE")
        
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

    def tearDown(self):
        # Close cursor and connection after each test
        self.cursor.close()
        self.conn.close()

    def test_connect_to_db(self):
        # Test connecting to the database
        self.assertIsNotNone(dbhandler.connect_to_db())

    def test_check_table_exists(self):
        # Test checking if a table exists
        table_name = "generated_text"
        self.assertTrue(dbhandler.check_table_exists(self.cursor, table_name))

        # Create the table
        dbhandler.create_table_if_not_exists(self.cursor, table_name)
        self.assertTrue(dbhandler.check_table_exists(self.cursor, table_name))

    def test_insert_data(self):
        # Test inserting data into a table
        table_name = "generated_text"
        input_text = "Test input text"
        generated_text = "Test generated text"

        # Create the table if not exists
        dbhandler.create_table_if_not_exists(self.cursor, table_name)

        # Insert data
        dbhandler.insert_data(self.cursor, table_name, input_text, generated_text)

        # Check if data was inserted successfully
        self.cursor.execute(f"SELECT * FROM {table_name}")
        result = self.cursor.fetchall()
        #check if result is not empty
        self.assertTrue(len(result) > 0)

if __name__ == '__main__':
    unittest.main()
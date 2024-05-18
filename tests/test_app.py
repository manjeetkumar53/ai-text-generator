import sys, os
import unittest
from flask import json
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Add the directory containing dbhandler_mysql to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Import the app module
from app import app


class TestFlaskApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.client = app.test_client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)  # Assumes your index.html contains <html> tag

    @patch('app.client.initialize_llm')
    @patch('app.client.call_llm')
    @patch('app.save_to_database')
    def test_generate_text_success(self, mock_save_to_database, mock_call_llm, mock_initialize_llm):
        # Setup mock return values
        mock_llm = MagicMock()
        mock_initialize_llm.return_value = mock_llm
        mock_call_llm.return_value = "Generated text"
        
        response = self.client.post('/generate-text', json={'input_text': 'Test input'})
        #print("response-->",response.json)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'generated_text': 'Generated text'})
        mock_initialize_llm.assert_called_once()
        mock_call_llm.assert_called_once_with(mock_llm, 'Test input')
        mock_save_to_database.assert_called_once_with('Test input', 'Generated text')

    def test_generate_text_missing_input(self):
        response = self.client.post('/generate-text', json={'input_text': ''})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'Input text is missing or empty'})

    @patch('app.client.initialize_llm')
    @patch('app.client.call_llm')
    @patch('app.save_to_database')
    def test_generate_text_exception(self, mock_save_to_database, mock_call_llm, mock_initialize_llm):
        mock_initialize_llm.side_effect = Exception("Test exception")
        
        response = self.client.post('/generate-text', json={'input_text': 'Test input'})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {'error': 'Test exception'})
        mock_initialize_llm.assert_called_once()
        mock_call_llm.assert_not_called()
        mock_save_to_database.assert_not_called()

if __name__ == '__main__':
    unittest.main()

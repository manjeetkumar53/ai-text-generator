from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
from src.dbhandler import save_to_database
import src.llm_client as client
import logging

# Load environment variables from .env file
load_dotenv(override=True)

# Configure logging
logging.basicConfig(filename='../app.log', level=logging.INFO, force=True)

# Initialize Flask app
app = Flask(__name__, template_folder='../templates', static_folder='../static')
print("call here app.py")
@app.route('/')
def index():
    """
    Render the index.html template.
    """
    return render_template('index.html')

@app.route('/generate-text', methods=['POST'])
def generate_text():
    """
    Endpoint to generate text using a language model.
    """
    input_text = request.json.get('input_text', '').strip()
    if not input_text:
        logging.warning("Input text is missing or empty")
        return jsonify({'error': 'Input text is missing or empty'}), 400

    try:
        # Initialize and call the language model
        llm = client.initialize_llm()
        response = client.call_llm(llm, input_text)
        generated_text = response.strip()

        # Save data to the database
        save_to_database(input_text, generated_text)
        
        logging.info("Text generated and saved successfully")
        return jsonify({'generated_text': generated_text})

    except Exception as e:
        logging.error(f"Error generating text: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.debug = False
    app.run()

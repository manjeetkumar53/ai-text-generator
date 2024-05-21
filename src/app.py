from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os,sys
# Load environment variables from .env file
load_dotenv(override=True)

# Add the directory containing dbhandler_mysql to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from dbhandler import save_to_database
import llm_client as client
from logging_config import get_logger
import sentiment_analyzer as analyzer

# Import the logging module
logger = get_logger()

# Initialize Flask app
app = Flask(__name__, template_folder='../templates', static_folder='../static')
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
    model = request.json.get('model', 'OpenAI')  # Get the model parameter, default to 'OpenAI'
    temperature = request.json.get('temperature', 0.7)  # Get the temperature parameter, default to 0.7

    if not input_text:
        logger.warning("Input text is missing or empty")
        return jsonify({'error': 'Input text is missing or empty'}), 400

    try:
        # Initialize and call the language model with parameters
        llm = client.initialize_llm(model,temperature)
        response = client.call_llm(model, llm, input_text)
        generated_text = response.strip()
        input_category = analyzer.classify_text(input_text, model, temperature)

        print('Model Name',model,' input text category: ',input_category)

        # Save data to the database
        save_to_database(input_text, generated_text)

        logger.info("Text generated and saved successfully")
        return jsonify({'generated_text': generated_text})

    except Exception as e:
        logger.error(f"Error generating text: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.debug = False
    app.run()

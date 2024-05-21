import os,sys
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_community.llms import Ollama
from langchain_anthropic import ChatAnthropic
# Load environment variables from a .env file, if present
load_dotenv(override=True)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from logging_config import get_logger

# Import the logging module
logger = get_logger()


def initialize_llm(model,temperature):
    """
    Initialize the language model based on the provided model name.
    
    Args:
        model: The name of the language model to initialize.
        
    Returns:
        An instance of the specified language model.
        
    Raises:
        ValueError: If the model name does not match any known model.
    """
    if model == 'OpenAI':
        return OpenAI(temperature=temperature)
    elif model == 'llama3':
        return Ollama(model="llama3",temperature=temperature)
    elif model == 'anthropic':
        return ChatAnthropic(model='claude-2.1',temperature=temperature)
    else:
        logger.error(f"Invalid model name: {model}")
        raise ValueError(f"Invalid model name: {model}")

def call_llm(model, llm, query):
    """
    Call the provided language model with a given query.
    
    Args:
        llm: The language model instance.
        query: The query string to be passed to the language model.
        temperature: The temperature parameter for generation.
        token_size: The token_size parameter for generation.
    
    Returns:
        The response from the language model, or None if an error occurs.
    """
    try:
        response = llm.invoke(query)
        if model == 'anthropic':
            return response.content
        else:
            return response
    except Exception as e:
        logger.error(f"Error calling LLM: {e}")
        return None

from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain_openai import OpenAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os,sys
# Load environment variables from .env file
load_dotenv(override=True)

# Add the directory containing dbhandler_mysql to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import llm_client as client
from logging_config import get_logger

# Import the logging module
logger = get_logger()

def classify_text(sentence, model, temperature):
    template = """
    Classify the following text as one of the following categories with one word only: question, statement, joke, or instruction.
    Text: "{sentence}"
    Answer with only one word.
    """
    
    prompt = PromptTemplate.from_template(template)

    if model == 'OpenAI':
        llm = OpenAI(temperature=temperature)
    elif model == 'llama3':
        llm = Ollama(model="llama3",temperature=temperature)
    elif model == 'anthropic':
        llm = ChatAnthropic(model='claude-2.1',temperature=temperature)
    else:
        logger.error(f"Invalid model name: {model}")
        raise ValueError(f"Invalid model name: {model}")

    llm_chain = prompt | llm
    
    # Get response for the given sentence
    response = llm_chain.invoke(sentence)
    if model == "anthropic":
        return response.content.strip()
    else:
        return response.strip()

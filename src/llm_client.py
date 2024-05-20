import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_community.llms import Ollama
# Load environment variables from a .env file, if present
load_dotenv(override=True)


def initialize_llm():
    """
    Initialize the language model based on the LLM_NAME environment variable.
    
    Returns:
        An instance of the specified language model.
        
    Raises:
        ValueError: If the LLM_NAME environment variable does not match any known model.
    """
    llm_name = os.environ.get('LLM_NAME')
    if llm_name == 'OpenAI':
        return OpenAI()
    elif llm_name == 'Ollama':
        return Ollama(model="llama3")
    else:
        raise ValueError(f"Invalid LLM name: {llm_name}")

def call_llm(llm, query):
    """
    Call the provided language model with a given query.
    
    Args:
        llm: The language model instance.
        query: The query string to be passed to the language model.
    
    Returns:
        The response from the language model, or None if an error occurs.
    """
    try:
        response = llm.invoke(query)
        return response
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return None


# Example usage
if __name__ == "__main__":
    llm = initialize_llm()
    query = "What is facebook?"
    response = call_llm(llm, query)
    if response is not None:
        print(f"Response from LLM: {response}")

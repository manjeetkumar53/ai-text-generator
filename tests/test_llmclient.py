import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_community.llms import Ollama

def initialize_llm():
    llm_name = os.environ.get('LLM_NAME', 'OpenAI')
    if llm_name == 'OpenAI':
        return OpenAI()
    elif llm_name == 'Ollama':
        return Ollama(model="llama3")
    else:
        raise ValueError("Invalid LLM name")

def call_llm(llm, query):
    try:
        response = llm.invoke(query)
        return response
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return None

load_dotenv(override=True)

llm = initialize_llm()
query = "How are you?"
response = call_llm(llm, query)
print(response)

query = "Tell me a joke"
response = call_llm(llm, query)
print(response)
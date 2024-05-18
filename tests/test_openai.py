from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Get OpenAI API key from environment variable
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate.from_template(template)

llm = OpenAI()

#llm = OpenAI(openai_api_key=OPENAI_API_KEY)

llm_chain = prompt | llm

question = "What is capital of Germany?"

response = llm_chain.invoke(question)

print(response)
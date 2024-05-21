from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Get OpenAI API key from environment variable
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

sentence = "tell me a joke"
template = """
    question_prompt = "Is the following sentence a question: '{sentence}'?"
    sentence_prompt = "Is the following sentence a simple statement: '{sentence}'?"
    joke_prompt = "Is the following text a joke: '{sentence}'?"
    instruction_prompt = "Is the following text an instruction: '{sentence}'?"

"""

sentence = "tell me a joke"

template = """
Classify the following text as one of the following categories: question, statement, joke, or instruction:
"{sentence}"
"""
prompt = PromptTemplate.from_template(template)

llm = OpenAI()

#llm = OpenAI(openai_api_key=OPENAI_API_KEY)

llm_chain = prompt | llm


#response = llm_chain.invoke(question)

#print(response)
# streaming the output
for chunk in llm_chain.stream(sentence):
  print(chunk, end="", flush=True)
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate

load_dotenv(override=True)
llm = ChatAnthropic(model='claude-2.1',temperature=1)


sentence = "How to make coffee?"

template = """
Classify the following text as one of the following categories with one word only: question, statement, joke, or instruction.
Text: "{sentence}"
Answer with only one word.
"""

prompt = PromptTemplate.from_template(template)

llm_chain = prompt | llm

# Get response for the given sentence
response = llm_chain.invoke(sentence)

# Print the response, stripping any extraneous whitespace
print(response.content.strip())
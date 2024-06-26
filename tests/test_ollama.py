from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama


sentence = "How to make coffee?"

template = """
Classify the following text as one of the following categories with one word only: question, statement, joke, or instruction.
Text: "{sentence}"
Answer with only one word.
"""

prompt = PromptTemplate.from_template(template)

llm = Ollama(model="llama3")


llm_chain = prompt | llm

# Get response for the given sentence
response = llm_chain.invoke(sentence)

# Print the response, stripping any extraneous whitespace
print(response.strip())
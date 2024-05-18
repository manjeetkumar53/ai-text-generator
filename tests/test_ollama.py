from langchain_community.llms import Ollama

llm = Ollama(model="llama3")

reponse = llm.invoke("Tell me a joke")

print(reponse)
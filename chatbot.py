from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="gemma3")

response = llm.invoke("What is Artificial Intelligence?")

print(response)

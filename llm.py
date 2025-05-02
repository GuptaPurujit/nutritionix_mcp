# llm_provider.py
import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class LLM:
    def __init__(self):
        self.model_name = os.getenv("LLM_MODEL", "llama3-groq-tool-use:latest")
        self.base_url   = os.getenv("OLLAMA_BASE_URL", None)

    def get_llm(self) -> ChatOllama:
        """
        Returns an Ollama-backed LLM. Swap model name via the LLM_MODEL env var.
        The new OllamaLLM class no longer accepts a `mode` parameter.
        """        
        return ChatOllama(model=self.model_name, base_url=self.base_url)

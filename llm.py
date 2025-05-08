# llm_provider.py
import os
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv

load_dotenv()

class LLM:
    def __init__(self):
        pass

    def get_ollama_llm(self) -> ChatOllama:
        """
        Returns an Ollama-backed LLM. Swap model name via the LLM_MODEL env var.
        The new OllamaLLM class no longer accepts a `mode` parameter.
        """
        self.model_name = os.getenv("OLLAMA_LLM_MODEL")
        self.base_url   = os.getenv("OLLAMA_BASE_URL")
        
        return ChatOllama(model=self.model_name, base_url=self.base_url)
    
    def get_openai_llm(self) -> ChatOpenAI:
        """Returns an OpenAI-backed LLM. Uses the model name from LLM_MODEL env var.
        
        Requires OPENAI_API_KEY to be set in environment variables.

        Returns:
            ChatOpenAI: Configured OpenAI chat model instance
        """
        self.model_name = os.getenv("OPENAI_MODEL_NAME")
        return ChatOpenAI(model=self.model_name)

# llm_provider.py
import os
from langchain_ollama.llms import OllamaLLM

def get_llm():
    """
    Returns an Ollama-backed LLM. Swap model name via the LLM_MODEL env var.
    The new OllamaLLM class no longer accepts a `mode` parameter.
    """
    model_name = os.getenv("LLM_MODEL", "llama3-groq-tool-use:latest")
    # Optionally pass base_url if your Ollama server is not at localhost:11434
    base_url   = os.getenv("OLLAMA_BASE_URL", None)
    return OllamaLLM(model=model_name, base_url=base_url)

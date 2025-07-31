from loguru import logger
from langchain_ollama import ChatOllama


def fetch_model_from_ollama(model_name: str = "gemma3:1b", temperature:float= 0.4) -> ChatOllama | None:
    """Attempts to retrieve Ollama model
        :param model_name:str The name of the model from official ollama list
        :return: ChatOllama instance if model is found, else returns None"""
    try:
        model = ChatOllama(model=f"{model_name}",temperature=temperature)
        # logger.info(f"{model_name} model fetched from ollama" if model_name != "llama3.2" else "llama3.2 fetched")
        return model
    except Exception as e:
        logger.error('Failed to fetch model from Ollama. Details below:\n', e)
        return None


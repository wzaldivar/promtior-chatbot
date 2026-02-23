from functools import lru_cache

from langchain_ollama import OllamaEmbeddings

from chatbot.common.llm.config import get_llm_config


def __ollama_embeddings():
    ollama_config = get_llm_config().model

    config = {
        "model": ollama_config.model_name,
        "base_url": ollama_config.base_url,
    }

    config = {key: val for key, val in config.items() if val}

    return OllamaEmbeddings(**config)


@lru_cache
def get_embeddings():
    available_embeddings = {
        'ollama': __ollama_embeddings,
    }

    model_config = get_llm_config().model

    embeddings_factory = available_embeddings.get(model_config.model_provider)
    if embeddings_factory is None:
        raise Exception(f"Unknown model provider: {model_config.model_provider}")

    return embeddings_factory()

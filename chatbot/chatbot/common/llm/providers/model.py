from functools import lru_cache

from langchain.chat_models import init_chat_model

from chatbot.common.llm.config import get_llm_config


@lru_cache
def get_chat_model():
    model_config = get_llm_config().model

    return init_chat_model(
        model_provider=model_config.model_provider,
        model=model_config.model_name,
        base_url=model_config.base_url
    )

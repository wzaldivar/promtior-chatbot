from langchain.chat_models import init_chat_model

from config import settings

chat_args = {
    "model": settings.model,
    "model_provider": settings.provider,
    "api_key": settings.api_key,
    "base_url": settings.base_url,
}

chat_args = {k: v for k, v in chat_args.items() if v is not None}

chat_model = init_chat_model(
    **chat_args
)

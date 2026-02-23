import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from pydantic_yaml import parse_yaml_file_as


def __get_llm_config_path():
    return os.getenv('LLM_CONFIG_PATH', 'llm_config.yml')


class ModelConfig(BaseModel):
    model_provider: str
    model_name: str
    base_url: str | None = None


class OllamaConfig(ModelConfig):
    model_provider: str = Literal['ollama']


class VectorStoreConfig(BaseModel):
    name: str
    can_initialize: bool = False


class FaissConfig(VectorStoreConfig):
    name: str = Literal['faiss']
    path: str | None = None
    can_initialize: bool = True


class LlmConfig(BaseModel):
    model: OllamaConfig
    vector_store: FaissConfig


@lru_cache
def get_llm_config():
    return parse_yaml_file_as(LlmConfig, Path(__get_llm_config_path()))

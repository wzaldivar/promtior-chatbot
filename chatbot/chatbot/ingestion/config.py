import os
from functools import lru_cache
from typing import List, Optional

from pydantic import BaseModel
from pydantic_yaml import parse_yaml_file_as


def __get_ingestion_config_path():
    return os.getenv("INGESTION_CONFIG_PATH", "ingestion_config.yml")


class SourceConfig(BaseModel):
    chunk_size: int = 250
    chunk_overlap: int = 20


class PdfSourceConfig(SourceConfig):
    path: str
    pages: Optional[List[int]] | None = None


class WebSourceConfig(SourceConfig):
    url: str
    follow_links: Optional[bool] = False
    max_depth: Optional[int] = 2


class IngestionConfig(BaseModel):
    pdf_sources: Optional[List[PdfSourceConfig]] = []
    web_sources: Optional[List[WebSourceConfig]] = []


@lru_cache
def get_ingestion_config():
    return parse_yaml_file_as(IngestionConfig, __get_ingestion_config_path())

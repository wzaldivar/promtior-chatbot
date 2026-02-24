from functools import lru_cache

from langchain_text_splitters import RecursiveCharacterTextSplitter

from chatbot.common.llm.config import get_llm_config
from chatbot.common.llm.providers.vector_store import get_vector_store


@lru_cache
def __get_splitter(chunk_size, chunk_overlap):
    return RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)


def __persist_faiss(vector_store, config):
    if config.path:
        try:
            print("persisting vector store")
            vector_store.save_local(config.path)
        except Exception as e:
            print(f"Error saving vector store {config.path}: {e}")


def store_documents(docs, source):
    vector_store_config = get_llm_config().vector_store
    vector_store = get_vector_store()

    splitter = __get_splitter(source.chunk_size, source.chunk_overlap)

    split_docs = splitter.split_documents(docs)

    if vector_store:
        print("saving to vector store")
        vector_store.add_documents(split_docs)

        extra_persist_steps = {
            'faiss': __persist_faiss,
        }

        vector_store_config = get_llm_config().vector_store
        extra_step = extra_persist_steps.get(vector_store_config.name)

        if extra_step is not None:
            extra_step(vector_store, vector_store_config)
    elif vector_store_config.can_initialize:
        # ingest initial docs
        get_vector_store(split_docs)
    else:
        print("Vector store not available and cannot be initialized. Skipping ingestion.")

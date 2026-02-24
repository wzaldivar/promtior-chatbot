import asyncio
from functools import lru_cache

from langchain_text_splitters import RecursiveCharacterTextSplitter

from chatbot.common.llm.config import get_llm_config
from chatbot.common.llm.providers.vector_store import get_vector_store, __persist_faiss


@lru_cache
def __get_splitter(chunk_size, chunk_overlap):
    return RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)


async def store_documents(docs, source):
    vector_store_config = get_llm_config().vector_store
    vector_store = await get_vector_store()

    splitter = __get_splitter(source.chunk_size, source.chunk_overlap)

    split_docs = splitter.split_documents(docs)

    if vector_store:
        print("adding documents to vector store")
        await vector_store.aadd_documents(split_docs)

        extra_persist_steps = {
            'faiss': __persist_faiss,
        }

        vector_store_config = get_llm_config().vector_store
        extra_step = extra_persist_steps.get(vector_store_config.name)

        if extra_step is not None:
            await extra_step(vector_store, vector_store_config)
    elif vector_store_config.can_initialize:
        # ingest initial docs
        await get_vector_store(split_docs)
    else:
        print("Vector store not available and cannot be initialized. Skipping ingestion.")

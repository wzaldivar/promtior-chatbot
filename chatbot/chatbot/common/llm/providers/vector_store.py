import asyncio
import os

from langchain_community.vectorstores import FAISS

from chatbot.common.llm.config import get_llm_config
from chatbot.common.llm.providers.embeddings import get_embeddings

__vector_store = None
__lock = asyncio.Lock()
__store_local_lock = asyncio.Lock()


def is_vector_store_initialized():
    return __vector_store is not None


async def __faiss_vector_store(docs=None):
    faiss_config = get_llm_config().vector_store

    embeddings = get_embeddings()

    # ingestion initialization mode
    if docs is not None:
        print("faiss vector store initialized from documents")
        faiss = await FAISS.afrom_documents(docs, embeddings)
        await __persist_faiss(faiss, faiss_config)
        return faiss
    # load mode
    elif faiss_config.path and os.path.exists(faiss_config.path):
        print("faiss vector store initialized from path")
        return await asyncio.to_thread(
            FAISS.load_local,
            faiss_config.path,
            embeddings,
            allow_dangerous_deserialization=True
        )

    return None


async def __persist_faiss(vector_store, config):
    if config.path:
        async with __store_local_lock:
            try:
                print("persisting vector store")
                await asyncio.to_thread(vector_store.save_local, config.path)
            except Exception as e:
                print(f"Error saving vector store {config.path}: {e}")


def __get_vector_store_factory():
    available_vector_stores = {
        "faiss": __faiss_vector_store
    }

    vector_store_config = get_llm_config().vector_store

    vector_store_factory = available_vector_stores.get(vector_store_config.name)
    if vector_store_factory is None:
        raise Exception(f"Unknown vector_store: {vector_store_config.name}")

    return vector_store_factory


async def get_vector_store(docs=None):
    global __vector_store
    if __vector_store is None:
        async with __lock:
            if __vector_store is None:
                factory = __get_vector_store_factory()
                __vector_store = await factory(docs)
    return __vector_store

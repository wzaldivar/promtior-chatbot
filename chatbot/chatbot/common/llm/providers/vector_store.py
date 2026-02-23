import os
import threading

from langchain_community.vectorstores import FAISS

from chatbot.common.llm.config import get_llm_config
from chatbot.common.llm.providers.embeddings import get_embeddings

__vector_store = None
__lock = threading.Lock()


def is_vector_store_initialized():
    return __vector_store is not None


def __faiss_vector_store(docs=None):
    faiss_config = get_llm_config().vector_store

    embeddings = get_embeddings()

    # ingestion initialization mode
    if docs is not None:
        faiss = FAISS.from_documents(docs, embeddings)
        if faiss_config.path:
            faiss.save_local(faiss_config.path)
        return faiss
    # load mode
    elif faiss_config.path and os.path.exists(faiss_config.path):
        return FAISS.load_local(faiss_config.path, embeddings, allow_dangerous_deserialization=True)

    return None


def __get_vector_store_factory():
    available_vector_stores = {
        "faiss": __faiss_vector_store
    }

    vector_store_config = get_llm_config().vector_store

    vector_store_factory = available_vector_stores.get(vector_store_config.name)
    if vector_store_factory is None:
        raise Exception(f"Unknown vector_store: {vector_store_config.name}")

    return vector_store_factory


def get_vector_store(docs=None):
    global __vector_store
    with __lock:
        if __vector_store is None:
            factory = __get_vector_store_factory()
            __vector_store = factory(docs)
    return __vector_store

from langchain_community.document_loaders import PyPDFLoader

from chatbot.ingestion.config import get_ingestion_config
from chatbot.ingestion.vector_store import store_documents


async def load_pdf(source):
    docs = []

    try:
        loader = PyPDFLoader(source.path)
        all_pages = await loader.aload()
        if source.pages:
            for page in source.pages:
                if 0 < page <= len(all_pages):
                    docs.append(all_pages[page - 1])
                    print(f"{source.path}: page {page} loaded")
                else:
                    print(f"{source.path}: page {page} is out of range")
        else:
            docs.extend(all_pages)
        print(f"{source.path} loaded")
    except Exception as e:
        print(f"Failed to load {source.path}: {e}")

    return docs


async def ingest_pdfs():
    pdf_sources = get_ingestion_config().pdf_sources

    for pdf_source in pdf_sources:
        docs = await load_pdf(pdf_source)
        if len(docs) > 0:
            await store_documents(docs, pdf_source)

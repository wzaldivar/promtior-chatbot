import asyncio

import nest_asyncio

from chatbot.ingestion.pdf import ingest_pdfs
from chatbot.ingestion.web import ingest_websites

nest_asyncio.apply()


async def run_full_ingestion():
    await asyncio.gather(
        ingest_pdfs(),
        ingest_websites()
    )


asyncio.run(run_full_ingestion())

from functools import lru_cache

from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest

from chatbot.common.llm.providers.model import get_chat_model
from chatbot.common.llm.providers.vector_store import get_vector_store, is_vector_store_initialized


@dynamic_prompt
def prompt_with_context(request: ModelRequest) -> str:
    """Inject context into state messages."""
    vector_store = get_vector_store()

    last_query = request.state["messages"][-1].text
    retrieved_docs = vector_store.similarity_search(last_query, k=8)

    docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)

    system_message = f"""
        You are an assistant answering questions about a company named Promtior.

        Rules:

        - Use ONLY the information provided in the CONTEXT.
        - Do NOT use prior knowledge.
        - Do NOT guess or infer missing facts.
        - If the answer is not explicitly stated in the context, respond:
          "I don't know based on the available information."

        CONTEXT:
        ----------------
        {docs_content}
        ----------------
        """

    return system_message


@lru_cache
def get_agent():
    return create_agent(get_chat_model(), tools=[], middleware=[prompt_with_context])


def get_response(query):
    last_message = None
    agent = get_agent()
    for event in agent.stream(
            {"messages": [{"role": "user", "content": f"{query}"}]},
            stream_mode="values",
    ):
        last_message = event["messages"][-1]
    
    return last_message.content


def is_vector_store_present():
    get_vector_store()
    return is_vector_store_initialized()

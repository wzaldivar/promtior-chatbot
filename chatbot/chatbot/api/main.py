from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from chatbot.api.agent import is_vector_store_present, get_agent

app = FastAPI()


class ChatRequest(BaseModel):
    text: str


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
async def chat(request: ChatRequest):
    last_message = None

    for event in get_agent().stream(
            {"messages": [{"role": "user", "content": f"{request.text}"}]},
            stream_mode="values",
    ):
        last_message = event["messages"][-1]

    return {"response": last_message.content}


@app.get("/health")
async def health():
    if is_vector_store_present():
        return {"status": "ok", "message": "Healthy"}
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail="Vector store not available")

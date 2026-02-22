from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from llm.chat_model import chat_model

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
    response = chat_model.invoke(request.text)
    return {"response": response.content}

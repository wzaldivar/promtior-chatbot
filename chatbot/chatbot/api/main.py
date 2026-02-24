from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from chatbot.api.agent import is_vector_store_present, get_response

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
    response = get_response(request.text)
    return {"response": response}


@app.get("/health")
async def health():
    if is_vector_store_present():
        return {"message": "Healthy"}
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail="Vector store not available")


app.mount("/", StaticFiles(directory="ui", html=True), name="static")

from fastapi import FastAPI
from pydantic import BaseModel

from .main import ask_assistant, AnswerResponse


app = FastAPI()


class AskRequest(BaseModel):
    query: str


@app.post("/ask")
def ask(request: AskRequest) -> AnswerResponse:
    return ask_assistant(request.query)



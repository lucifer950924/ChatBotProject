from fastapi import FastAPI
from pydantic import BaseModel
from HarrYPotterChatBot import AskRAG


api = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # for dev only
    allow_methods=["*"],
    allow_headers=["*"],
)
class Chat(BaseModel):
    question : str

@api.post('/chat')    
def chat(req: Chat):
    answer = AskRAG(req.question)

    return answer


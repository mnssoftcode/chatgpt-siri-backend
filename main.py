from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class Query(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Siri Bot 🤖"}

@app.post("/ask")
def ask(query: Query):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": query.query}]
    )
    reply = response['choices'][0]['message']['content']
    return {"response": reply}

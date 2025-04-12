from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# Set the OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the request model
class Query(BaseModel):
    query: str

# Root route
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Siri Bot 🤖"}

# Main /ask endpoint
@app.post("/ask")
def ask(query: Query):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": query.query}]
    )
    reply = response['choices'][0]['message']['content']
    return {"response": reply}

# 🔐 TEMPORARY: Check if API key is set
@app.get("/check-key")
def check_key():
    if openai.api_key:
        return {"status": "✅ OPENAI_API_KEY is set"}
    else:
        return {"status": "❌ OPENAI_API_KEY is NOT set"}


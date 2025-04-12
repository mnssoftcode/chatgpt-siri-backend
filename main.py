from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

app = FastAPI()

api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

class Query(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Siri Bot 🤖"}

@app.get("/check")
def check_api_key():
    if api_key:
        return {"status": "✅ OPENAI_API_KEY is set"}
    else:
        return {"status": "❌ OPENAI_API_KEY is NOT set"}

@app.post("/ask")
def ask(query: Query):
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not set")
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query.query}]
        )
        reply = response['choices'][0]['message']['content']
        return {"response": reply}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")

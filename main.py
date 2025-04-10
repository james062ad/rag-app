# main.py

from fastapi import FastAPI
from pydantic import BaseModel
from basic_functions import add
from retriever import retrieve_top_document
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load OpenAI API key
load_dotenv()
client = OpenAI()

app = FastAPI()

# ----------------------
# Root Health Check
# ----------------------
@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG app!"}

# ----------------------
# /add Endpoint
# ----------------------
class AddRequest(BaseModel):
    a: float
    b: float

@app.post("/add")
def perform_addition(request: AddRequest):
    result = add(request.a, request.b)
    return {"result": result}

# ----------------------
# /generate Endpoint
# ----------------------
class GenerateRequest(BaseModel):
    query: str

@app.post("/generate")
def generate_answer(request: GenerateRequest):
    # Retrieve the most relevant document
    top_doc = retrieve_top_document(request.query)

    # Format context for GPT
    context = top_doc["content"]
    prompt = f"""
You are an expert materials scientist. Use the following scientific abstract to answer the question clearly and accurately.

Abstract:
\"\"\"{context}\"\"\"

Question:
{request.query}
"""

    # Call OpenAI's Chat Completion API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful scientific assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract generated answer
    answer = response.choices[0].message.content

    return {
        "query": request.query,
        "matched_title": top_doc["title"],
        "similarity": round(top_doc["similarity"], 4),
        "answer": answer
    }

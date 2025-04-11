import os
import openai
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from retriever import retrieve_top_document

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow CORS (for Lovable frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class GenerateRequest(BaseModel):
    query: str

# Response model
class GenerateResponse(BaseModel):
    query: str
    matched_title: str
    similarity: float
    answer: str

@app.post("/generate", response_model=GenerateResponse)
async def generate_answer(request: GenerateRequest):
    top_doc, score = retrieve_top_document(request.query)

    prompt = (
        f"You are a scientific assistant. Use the passage below to answer the question as accurately as possible.\n\n"
        f"Context:\n{top_doc['content']}\n\n"
        f"Question: {request.query}\n\nAnswer:"
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can change model
        messages=[
            {"role": "system", "content": "You are a helpful scientific assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    answer = response.choices[0].message.content.strip()

    return {
        "query": request.query,
        "matched_title": top_doc["title"],
        "similarity": round(score, 4),
        "answer": answer,
    }

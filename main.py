from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from retriever import retrieve_top_document

app = FastAPI()

# ✅ Enable full CORS for all origins (or restrict if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with ["https://query-scribe-reveal.lovable.app"] if you want to lock it down
    allow_credentials=True,
    allow_methods=["*"],  # ✅ Must include "OPTIONS" to support browser preflight
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "Scientific RAG Assistant is live!"}

@app.post("/generate")
def generate_answer(request: GenerateRequest):
    top_doc = retrieve_top_document(request.query)
    return {
        "query": request.query,
        "matched_title": top_doc["title"],
        "similarity": round(top_doc["score"], 4),
        "answer": top_doc["content"]
    }

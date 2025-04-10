from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from retriever import retrieve_top_document
from embedder import embedded_documents

app = FastAPI()

# ✅ Allow Lovable.dev frontend to connect (you can restrict later if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or use ["https://query-scribe-reveal.lovable.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "Scientific RAG Assistant is running!"}

@app.post("/generate")
def generate_answer(request: GenerateRequest):
    top_doc = retrieve_top_document(request.query)
    return {
        "query": request.query,
        "matched_title": top_doc["title"],
        "similarity": round(top_doc["score"], 4),
        "answer": top_doc["content"],
    }

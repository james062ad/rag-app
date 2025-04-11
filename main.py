from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from retriever import retrieve_top_document

import os
from supabase import create_client

# ✅ Load .env variables
load_dotenv()

# ✅ Load environment variables
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# ✅ Create Supabase client
supabase = create_client(supabase_url, supabase_key)

# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ Allow CORS from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Input schema
class GenerateRequest(BaseModel):
    query: str

# ✅ Output schema
class GenerateResponse(BaseModel):
    query: str
    matched_title: str
    similarity: float
    answer: str

# ✅ POST endpoint
@app.post("/generate", response_model=GenerateResponse)
def generate_answer(request: GenerateRequest):
    top_doc, top_score = retrieve_top_document(request.query)

    # ✅ Save to Supabase
    supabase.table("documents").insert({
        "title": top_doc["title"],
        "content": top_doc["content"],
        "embedding": top_doc["embedding"]
    }).execute()

    return GenerateResponse(
        query=request.query,
        matched_title=top_doc["title"],
        similarity=top_score,
        answer=top_doc["content"]
    )

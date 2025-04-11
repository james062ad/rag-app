import os
import openai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from retriever import retrieve_top_document

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# ✅ Enable CORS (for Lovable.dev frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Optionally replace with ["https://query-scribe-reveal.lovable.app"]
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
    # ✅ Unpack top doc and score from retriever
    top_doc, top_score = retrieve_top_document(request.query)

    # Construct prompt for OpenAI
    prompt = f"""
    You are a scientific assistant. Use the following passage to answer the user's question as accurately as possible.

    Context:
    {top_doc['content']}

    Question:
    {request.query}

    Answer:
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful scientific assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    answer = response.choices[0].message.content.strip()

    return GenerateResponse(
        query=request.query,
        matched_title=top_doc["title"],
        similarity=round(top_score, 4),
        answer=answer
    )

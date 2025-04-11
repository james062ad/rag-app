import numpy as np
import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(supabase_url, supabase_key)

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1, dtype=np.float32)
    vec2 = np.array(vec2, dtype=np.float32)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def retrieve_top_document(query):
    query_embedding = get_embedding(query)

    response = supabase.table("documents").select("title, content, embedding").execute()
    documents = response.data

    results = []
    for doc in documents:
        score = cosine_similarity(query_embedding, doc["embedding"])
        results.append({
            "doc": doc,
            "score": score
        })

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    top_doc = sorted_results[0]["doc"]
    top_score = sorted_results[0]["score"]

    return top_doc, top_score

def get_embedding(text):
    import openai
    from dotenv import load_dotenv
    load_dotenv()

    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )

    return response['data'][0]['embedding']

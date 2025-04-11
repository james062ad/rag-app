# embedder.py

import os
from dotenv import load_dotenv
from openai import OpenAI
from supabase import create_client, Client
from data import documents

# Load API keys from .env
load_dotenv()

# Set up OpenAI
client = OpenAI()
openai_model = "text-embedding-ada-002"

# Set up Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Generate embedding for given text
def get_embedding(text):
    response = client.embeddings.create(
        model=openai_model,
        input=[text]
    )
    return response.data[0].embedding

# Embed and insert each document
for doc in documents:
    embedding = get_embedding(doc["content"])

    data = {
        "title": doc["title"],
        "content": doc["content"],
        "embedding": embedding
    }

    response = supabase.table("documents").insert(data).execute()

    if response.data:
        print(f"✅ Inserted: {doc['title']}")
    else:
        print(f"❌ Failed to insert: {doc['title']}")
        print(response)

print("✅ All documents processed.")

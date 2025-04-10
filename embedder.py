# embedder.py

import os
from dotenv import load_dotenv
from openai import OpenAI
from data import documents

# Load the .env file to get the OpenAI API key
load_dotenv()
client = OpenAI()

# Function to get the embedding for a given text
def get_embedding(text, model="text-embedding-ada-002"):
    response = client.embeddings.create(
        input=[text],
        model=model
    )
    return response.data[0].embedding

# List to store embedded documents
embedded_documents = []

# Generate and store embeddings
for doc in documents:
    embedding = get_embedding(doc["content"])
    embedded_documents.append({
        "title": doc["title"],
        "content": doc["content"],
        "embedding": embedding
    })

print("✅ Embedded all documents!")

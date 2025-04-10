# retriever.py

import os
from dotenv import load_dotenv
from openai import OpenAI
import numpy as np
from embedder import embedded_documents

# Load OpenAI key from .env
load_dotenv()
client = OpenAI()

# Helper function to get embedding for a user query
def get_query_embedding(text, model="text-embedding-ada-002"):
    response = client.embeddings.create(
        input=[text],
        model=model
    )
    return response.data[0].embedding

# Function to calculate cosine similarity
def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Retrieve the most relevant document
def retrieve_top_document(query):
    query_embedding = get_query_embedding(query)
    
    similarities = []
    for doc in embedded_documents:
        score = cosine_similarity(query_embedding, doc["embedding"])
        similarities.append((score, doc))

    # Sort by similarity (highest first)
    similarities.sort(key=lambda x: x[0], reverse=True)

    top_doc = similarities[0][1]
    return {
        "title": top_doc["title"],
        "content": top_doc["content"],
        "similarity": similarities[0][0]
    }

# Example usage
if __name__ == "__main__":
    query = "What are high-entropy alloys?"
    top = retrieve_top_document(query)
    print("\n🔍 Top Match:")
    print(f"Title: {top['title']}")
    print(f"Similarity: {top['similarity']:.4f}")
    print(f"Content: {top['content']}")

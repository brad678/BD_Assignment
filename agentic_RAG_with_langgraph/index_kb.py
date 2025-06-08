from openai import AzureOpenAI
import os
from dotenv import load_dotenv
import chromadb

load_dotenv(override=True)

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def get_embedding(text: str, deployment="text-embedding-ada-002") -> list:
    response = client.embeddings.create(
        input=[text],
        model=deployment  # Azure deployment name
    )
    return response.data[0].embedding

# chroma_client = chromadb.Client()
chroma_client = chromadb.PersistentClient(path="./agentic_RAG_with_langgraph/chroma_db") 
collection = chroma_client.get_or_create_collection("kb_index")

# Function to embed and upsert knowledge base entries into Chroma vector store
def embed_and_upsert_kb(json_data, collection=collection):
    existing_ids = set(collection.get()["ids"])
    for entry in json_data:
        if entry["doc_id"] not in existing_ids:
            emb = get_embedding(entry['answer_snippet'])
            collection.add(
                documents=[entry['answer_snippet']],
                ids=[entry['doc_id']],
                metadatas=[{
                    "source": entry["source"],
                    "last_updated": entry["last_updated"],
                }],
                embeddings=[emb]
            )


if __name__ == "__main__":
    import json

    # Update with your actual JSON file path
    with open("agentic_RAG_with_langgraph/self_critique_loop_dataset.json", "r") as f:
        data = json.load(f)
    
    embed_and_upsert_kb(data, collection=collection)
    print(f"Upserted {len(data)} KB entries to Chroma vector store.")

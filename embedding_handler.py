# Import necessary libraries
import faiss
import numpy as np
from openai import OpenAI
import json
from data_processor import get_convo

# Initialize OpenAI client
client = OpenAI()


def generate_embedding(text, model="text-embedding-3-small"):
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding

def create_embeddings(knowledge_base, index_file="embeddings.index", json_file="knowledge_base.json"):

    embeddings = []
    for item in knowledge_base:
        embedding = generate_embedding(item["text"])
        item["embedding"] = embedding
        embeddings.append(embedding)


    dimension = len(embeddings[0])
    index = faiss.IndexFlatIP(dimension)  
    embedding_matrix = np.array(embeddings).astype('float32')
    index.add(embedding_matrix)


    faiss.write_index(index, index_file)
    

    with open(json_file, 'w') as f:
        json.dump(knowledge_base, f)
    
    print("Embeddings and index successfully saved.")

def load_embeddings(index_file="embeddings.index", json_file="knowledge_base.json"):

    index = faiss.read_index(index_file)

    with open(json_file, 'r') as f:
        knowledge_base = json.load(f)
    
    return index, knowledge_base

def retrieve_relevant_knowledge(query, index, knowledge_base, k=3):
    query_embedding = generate_embedding(query)
    query_vector = np.array([query_embedding]).astype('float32')
   
    D, I = index.search(query_vector, k)  # noqa: E741
    
    relevant_knowledge = [knowledge_base[i]["text"] for i in I[0]]
    return relevant_knowledge

def get_relevant_context(query, k=3):
    index, knowledge_base = load_embeddings()

    relevant_knowledge = retrieve_relevant_knowledge(query, index, knowledge_base, k)
    return relevant_knowledge

if __name__ == "__main__":
    synthetic_conversation = get_convo()

    knowledge_base = []
    for i in range(0, len(synthetic_conversation), 2):
        if i + 1 < len(synthetic_conversation):
            combined_text = f"User: {synthetic_conversation[i]['content']} Assistant: {synthetic_conversation[i+1]['content']}"
            knowledge_base.append({"text": combined_text})

    create_embeddings(knowledge_base)

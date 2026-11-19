
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


# Generate an embedding for one question
def generate_embedding(text: str) -> list[float]:
    embedding = model.encode(text)
    return embedding.tolist()


# Generate embeddings for multiple document chunks
def generate_embeddings(chunks: list[str]) -> list[list[float]]:
    embeddings = model.encode(chunks)
    return embeddings.tolist()

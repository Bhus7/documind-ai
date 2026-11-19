from uuid import uuid4
from qdrant_client.models import PointStruct
from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")

COLLECTION_NAME = "documents"


def create_collection():
    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=384,
                distance=models.Distance.COSINE
            )
        )
        print("Collection created successfully")
    else:
        print("Collection already exists")


def store_embeddings(
    chunks: list[str],
    embeddings: list[list[float]],
    document_id: int,
    filename: str
) -> None:

    if len(chunks) != len(embeddings):
        raise ValueError("Chunks and embeddings count must match")

    points = []

    for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        point = PointStruct(
            id=str(uuid4()),
            vector=embedding,
            payload={
                "text": chunk,
                "document_id": document_id,
                "filename": filename,
                "chunk_index": index
            }
        )

        points.append(point)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )



def search_similar_chunks(
    query_embedding: list[float],
    document_id: int,
    limit: int = 5
):
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        query_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="document_id",
                    match=models.MatchValue(value=document_id)
                )
            ]
        ),
        limit=limit,
        with_payload=True
    )

    return results.points


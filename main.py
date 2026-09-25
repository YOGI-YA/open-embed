from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-small-en-v1.5"

app = FastAPI(
    title="Open Embed",
    description="Open-source embedding API",
    version="0.1.0",
)

model = SentenceTransformer(MODEL_NAME)


class EmbeddingRequest(BaseModel):
    input: list[str]


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": MODEL_NAME,
        "dimensions": 384,
    }


@app.post("/v1/embeddings")
def create_embeddings(request: EmbeddingRequest):
    embeddings = model.encode(
        request.input,
        normalize_embeddings=True,
        batch_size=32,
    )

    return {
        "object": "list",
        "data": [
            {
                "object": "embedding",
                "index": index,
                "embedding": embedding.tolist(),
            }
            for index, embedding in enumerate(embeddings)
        ],
        "model": MODEL_NAME,
    }










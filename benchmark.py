import time
from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-small-en-v1.5"

model = SentenceTransformer(MODEL_NAME)

texts = [
    "PostgreSQL is a powerful relational database.",
    "Vector databases are useful for semantic search.",
    "Machine learning allows computers to learn from data.",
    "React is a JavaScript library for building user interfaces.",
] * 25

# Warm-up
model.encode(
    texts[:4],
    normalize_embeddings=True,
)

start = time.perf_counter()

embeddings = model.encode(
    texts,
    batch_size=32,
    normalize_embeddings=True,
)

elapsed = time.perf_counter() - start

print(f"Texts: {len(texts)}")
print(f"Time: {elapsed:.3f} seconds")
print(f"Embeddings/sec: {len(texts) / elapsed:.2f}")
print(f"Dimensions: {len(embeddings[0])}")
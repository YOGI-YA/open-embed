import time
import requests

URL = "http://127.0.0.1:8000/v1/embeddings"

texts = [
    "PostgreSQL is a powerful relational database.",
    "Vector databases are useful for semantic search.",
    "Machine learning allows computers to learn from data.",
    "React is a JavaScript library for building user interfaces.",
]


def benchmark(batch_size):
    payload = {
        "input": texts[:batch_size] if batch_size <= 4 else texts * (batch_size // 4)
    }

    start = time.perf_counter()

    response = requests.post(URL, json=payload)

    elapsed = time.perf_counter() - start

    response.raise_for_status()

    actual_count = len(response.json()["data"])

    print(
        f"Batch: {actual_count:3} | "
        f"Time: {elapsed:.3f}s | "
        f"Per text: {(elapsed / actual_count) * 1000:.2f}ms"
    )


for size in [1, 4, 32, 100]:
    benchmark(size)
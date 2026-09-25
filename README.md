# ⚡ Open Embed (`open-embed`)

> **Blazing-fast, lightweight, self-hosted, OpenAI-compatible text embedding microservice built with FastAPI and Sentence Transformers.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Model](https://img.shields.io/badge/Model-BAAI%2Fbge--small--en--v1.5-orange.svg)](https://huggingface.co/BAAI/bge-small-en-v1.5)
[![Dimensions](https://img.shields.io/badge/Dimensions-384-purple.svg)](#)
[![Docker Ready](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](#-docker-deployment)

---

<img width="1515" height="935" alt="image" src="https://github.com/user-attachments/assets/7628fa9d-266d-44d4-8f0d-1d185759362f" />


## 🚀 Why Open Embed?

Cloud embedding providers (OpenAI, Cohere, Jina) introduce **recurring token costs**, **rate limits**, **network latency**, and **data privacy risks**. Heavy local inference servers (like Ollama or vLLM) often consume excessive RAM and disk space just to generate lightweight vector embeddings.

**Open Embed** provides a minimal, high-throughput microservice that acts as a **100% drop-in replacement for OpenAI `/v1/embeddings`** with:

* 🔒 **100% Local & Air-Gapped Privacy**: Zero data leaves your machine or private VPC.
* ⚡ **Ultra High Performance**: ~500+ embeddings/second on standard CPU (~2ms per text).
* 🎯 **MTEB State-of-the-Art Model**: Ships with `BAAI/bge-small-en-v1.5` (384 dims, normalized vectors ready for cosine similarity / `pgvector`).
* 🔌 **Zero-Config Integration**: Seamlessly works with OpenAI SDK, LangChain, LlamaIndex, Next.js, and raw HTTP clients.
* 🪶 **Ultra Lightweight**: Footprint of < 150MB model weights and minimal memory consumption.

---

## 📊 Comparison Matrix

| Feature | Open Embed | OpenAI (`text-embedding-3-small`) | Ollama | Jina AI |
| :--- | :--- | :--- | :--- | :--- |
| **Cost** | **$0.00 (Free forever)** | Pay-per-token ($0.02 / 1M tokens) | Free | Pay-per-token |
| **Privacy / Offline** | ✅ **100% Local** | ❌ Sent to Cloud | ✅ Local | ❌ Sent to Cloud |
| **Latency** | ⚡ **< 5ms (Localhost)** | ⏱️ 80ms - 250ms (Network) | ⏱️ 20ms - 80ms | ⏱️ 100ms - 300ms |
| **OpenAI Compatible** | ✅ **Yes (`/v1/embeddings`)** | ✅ Yes | ⚠️ Partial / Custom port | ✅ Yes |
| **Memory Footprint** | 🪶 **~300 MB RAM** | N/A | 🐘 2 GB - 5 GB | N/A |
| **Dependencies** | FastAPI + PyTorch | API Key | Heavy background daemon | API Key |

---

## ⚡ Performance Benchmarks

Tested on standard consumer hardware (CPU only, single process):

<img width="1395" height="678" alt="image" src="https://github.com/user-attachments/assets/721d865b-615f-4706-aeea-8fc46121fe7c" />



| Batch Size | Total Execution Time | Throughput | Avg Time Per Text |
| :--- | :--- | :--- | :--- |
| **1 text** | `3.2 ms` | ~310 texts/sec | **3.2 ms** |
| **4 texts** | `8.1 ms` | ~490 texts/sec | **2.0 ms** |
| **32 texts** | `64.8 ms` | ~494 texts/sec | **2.0 ms** |
| **100 texts** | `204.0 ms` | **~491 texts/sec** | **2.0 ms** |

> 💡 *Run your own benchmarks using `python benchmark.py` and `python api_benchmark.py`!*

---

## 📦 Quickstart

### Option 1: Local Python (Virtual Environment)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOGI-YA/open-embed.git
   cd open-embed
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Linux/macOS
   python3 -m venv .venv
   source .venv/bin/activate

   # Windows (PowerShell)
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the service:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Verify health:**
   Open [http://localhost:8000/health](http://localhost:8000/health) or explore the interactive API docs at [http://localhost:8000/docs](http://localhost:8000/docs).

---

### Option 2: Docker / Docker Compose

#### Run with Docker:
```bash
docker build -t open-embed .
docker run -d -p 8000:8000 --name open-embed open-embed
```

#### Run with Docker Compose:
```bash
docker compose up -d
```

---

## 🔌 API Reference & Usage

### 1. Health Check (`GET /health`)
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "ok",
  "model": "BAAI/bge-small-en-v1.5",
  "dimensions": 384
}
```

---

### 2. Generate Embeddings (`POST /v1/embeddings`)

#### cURL Example:
```bash
curl -X POST "http://localhost:8000/v1/embeddings" \
  -H "Content-Type: application/json" \
  -d '{
    "input": [
      "Vector search enables semantic retrieval.",
      "PostgreSQL with pgvector is awesome."
    ]
  }'
```

**Response:**
```json
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "index": 0,
      "embedding": [-0.0124, 0.0481, 0.0039, "...384 dimensions..."]
    },
    {
      "object": "embedding",
      "index": 1,
      "embedding": [0.0312, -0.0152, 0.0891, "...384 dimensions..."]
    }
  ],
  "model": "BAAI/bge-small-en-v1.5"
}
```

---

### 3. Drop-in OpenAI SDK Replacement

#### Python (`openai` client):
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed"  # Local server does not require authentication
)

response = client.embeddings.create(
    model="BAAI/bge-small-en-v1.5",
    input=["Retrieval-Augmented Generation is effective.", "FastAPI is fast."]
)

print("Dimensions:", len(response.data[0].embedding))
# Output: Dimensions: 384
```

#### TypeScript / JavaScript / Next.js:
```typescript
import OpenAI from "openai";

const openai = new OpenAI({
  baseURL: "http://localhost:8000/v1",
  apiKey: "not-needed",
});

async function getEmbedding(text: string) {
  const res = await openai.embeddings.create({
    model: "BAAI/bge-small-en-v1.5",
    input: [text],
  });
  return res.data[0].embedding;
}
```

#### Raw Fetch (TypeScript / Node.js):
```typescript
export async function embed(texts: string[]): Promise<number[][]> {
  const res = await fetch("http://localhost:8000/v1/embeddings", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ input: texts }),
  });

  const json = await res.json();
  return json.data.map((item: { embedding: number[] }) => item.embedding);
}
```

---

## 🛠️ Configuration & Model Selection

You can easily swap the default model in `main.py` for any HuggingFace / Sentence-Transformers model:

| Model | Dimensions | Size | Best For |
| :--- | :--- | :--- | :--- |
| `BAAI/bge-small-en-v1.5` *(Default)* | **384** | ~130 MB | **Best balance of speed & quality (English)** |
| `all-MiniLM-L6-v2` | **384** | ~90 MB | Ultra-fast lightweight embeddings |
| `BAAI/bge-base-en-v1.5` | **768** | ~430 MB | Higher accuracy for complex documents |
| `sentence-transformers/all-mpnet-base-v2` | **768** | ~420 MB | General purpose high-precision |
| `BAAI/bge-m3` | **1024** | ~2.2 GB | Multi-lingual (100+ languages) & hybrid search |

---

## 📈 Benchmarking

Run the built-in benchmarking scripts to test on your own machine:

```bash
# Direct in-memory model inference speed
python benchmark.py

# End-to-end HTTP API benchmark over network
python api_benchmark.py
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'feat: add some amazing feature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

<p align="center">
  Built with ❤️ for the open-source AI community. If you find this useful, please ⭐ star the repository!
</p>

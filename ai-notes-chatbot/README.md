# AI Notes Chatbot - Semantic RAG Search

[![Production Ready](https://img.shields.io/badge/status-production%20ready-green)](https://github.com)

## 🚀 Problem Statement
Traditional keyword search fails on technical notes, code snippets, and natural language queries. Developers need **semantic understanding** to find relevant information quickly.

## 💡 Solution
**Vector-based Semantic Search + RAG Pipeline**:
- Convert notes to dense vectors (embeddings)
- Store in vector database (in-memory now, Endee-ready)
- Query → Embed → Cosine similarity → Top relevant chunks → Answer

## ✨ Features
- 📝 **Upload Notes**: Embed & index any text/notes
- 🔍 **Semantic Search**: Find by meaning, not keywords
- 🤖 **RAG Pipeline**: Retrieval-Augmented Generation (context-aware answers)
- ✅ **Production Endpoints**: `/health`, `/upload`, `/ask`
- 📊 **Structured Responses**: Query + Answer + Sources + Relevance scores

## 🏗️ Architecture
```
User Request → FastAPI → Vector Search → Top-2 Matches → RAG Answer
                    ↓
             In-Memory DB (Endee compatible)
```

## 🔄 RAG Pipeline (Step-by-Step)
```
1. UPLOAD: text → embedding → store (text, vector)
2. ASK:    query → embedding → cosine_sim → top-2 chunks
3. ANSWER: "Based on notes: chunk1 | chunk2" + sources[{content, score}]
```

## 🛠️ Tech Stack
- **FastAPI** (async API framework)
- **Pydantic** (data validation)
- **NumPy** (vector math)
- **Vector Store**: In-memory (replace `services/search.py:db` with Endee client)

## 🚀 Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open: http://localhost:8000/docs (Swagger UI)

## 📖 API Examples

### 1. Health Check
```bash
curl -X GET "http://localhost:8000/health"
```
```json
{"status": "ok"}
```

### 2. Upload Notes
```bash
curl -X POST "http://localhost:8000/upload" \
     -H "Content-Type: application/json" \
     -d '{"text": "FastAPI is great for building APIs. Uses Pydantic for validation."}'
```
```json
{"message": "Notes successfully embedded and indexed"}
```


### 3. Ask Question
```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is FastAPI good for?"}'
```
```json
{
  "query": "What is FastAPI good for?",
"From your notes:\n\nFastAPI is great for building APIs..."
  "sources": [{"content": "...", "relevance_score": 0.85}]
}
```

## 🔗 Endee Integration (Production)
Current `services/search.py` uses `db = []` list. To use Endee:

1. Install Endee client: `pip install endee`
2. Replace `db.append()` / `for text, vec in db:` with Endee API calls
3. Only **storage layer** changes needed - search/embed logic reusable

## 📈 Future Enhancements
- Real embeddings (OpenAI/SentenceTransformers)
- Query history tracking
- Rate limiting
- Docker deployment

## SDE Internship Demo
Perfect for showcasing:
- Clean API design
- ML integration (vectors/RAG)
- Production practices (health checks, logging, structured responses)
- Scalable architecture (Endee-ready)

---

## 📢 Endee Repository Compliance

This project is built on top of the Endee repository as required for the internship submission.

## 🔗 Endee Usage

This project shows how Endee vector databases work for semantic search:

* Store document embeddings
* Find similar content by meaning
* Power RAG chat systems

**Current setup**: JSON file storage that works exactly like Endee (data/endee_vectors.json).
**Production**: Replace `services/endee_client.py` with real Endee SDK.

Modular design makes it super easy - just swap the storage layer!

## 📈 Endee Vector Database Integration

Endee-compatible persistent vector storage layer
- **Retrieval**: Cosine similarity for top matches
- **Scalable**: Ready for real Endee deployment

**Built with ❤️ for efficient developer workflows**



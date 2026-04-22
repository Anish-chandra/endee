from fastapi import FastAPI, status
from pydantic import BaseModel, Field
from typing import List
from services.search import add_doc, search

class Source(BaseModel):
    content: str = Field(..., description="Relevant note content")
    relevance_score: float = Field(..., description="Cosine similarity score (0-1)", ge=0.0, le=1.0)

class AskResponse(BaseModel):
    query: str = Field(..., description="User question")
    answer: str = Field(..., description="RAG-generated response from notes")
    sources: List[Source] = Field(..., description="Top relevant sources with scores")

app = FastAPI(
    title="AI Notes Chatbot",
    description="Production-ready RAG-based notes Q&A using semantic vector search (Endee compatible)",
    version="1.0.0"
)

@app.get("/health", tags=["System"], summary="Health check")
def health_check():
    """Production health check endpoint"""
    return {"status": "ok"}

class TextInput(BaseModel):
    """Notes to upload and index"""
    text: str = Field(..., min_length=1, example="FastAPI is a modern web framework for building APIs with Python.")

class QueryInput(BaseModel):
    """Question about your notes"""
    query: str = Field(..., min_length=1, example="How does FastAPI handle request validation?")

@app.post("/upload", tags=["Data"], summary="Upload notes", status_code=status.HTTP_201_CREATED)
def upload_notes(input: TextInput):
    """Embed notes using semantic vectors and index in vector store (Endee compatible)"""
    add_doc(input.text)
    return {"message": "Notes successfully embedded and indexed"}

@app.post("/ask", tags=["Query"], summary="Semantic Q&A", response_model=AskResponse)
def ask_question(input: QueryInput):
    """
    Production RAG Pipeline:
    1. Embed query → cosine similarity search (top 2)
    2. Retrieve most relevant note chunks  
    3. Generate natural answer + structured sources with scores
    """
    results = search(input.query, top_k=2)
    if not results:
        return AskResponse(
            query=input.query,
            answer="No relevant notes found. Please upload notes using /upload first.",
            sources=[]
        )
    
    # Create natural, readable answer from top results
    source_snippets = [r[0][:250] + "..." if len(r[0]) > 250 else r[0] for r in results[:2]]
    answer = "From your notes:\n\n" + "\n\n---\n\n".join(source_snippets)
    
    sources = [Source(content=r[0], relevance_score=float(r[1])) for r in results]
    
    return AskResponse(
        query=input.query,
        answer=answer,
        sources=sources
    )



from fastapi import FastAPI
from backend.api.routers import upload, query, simplify, classify, entities

app = FastAPI(title="ClauseWise: Legal Document Analyzer", description="AI-powered legal document analysis using IBM Watson & Granite")

# Add a root endpoint for testing
@app.get("/")
def read_root():
    return {"message": "ClauseWise Legal Document Analyzer API is running!", "powered_by": "IBM Watson & Granite AI"}

@app.get("/health")
def health_check():
    """Health check endpoint with AI model status"""
    try:
        from backend.services.granite_llm import get_granite_service
        granite = get_granite_service()
        
        return {
            "status": "healthy",
            "backend": "online",
            "ai_model_loaded": granite.model_loaded if granite else False,
            "device": granite.device if granite else "unknown"
        }
    except Exception as e:
        return {
            "status": "degraded",
            "backend": "online",
            "ai_model_loaded": False,
            "error": str(e)
        }

app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(query.router, prefix="/query", tags=["query"])
app.include_router(simplify.router, prefix="/simplify", tags=["simplify"])
app.include_router(classify.router, prefix="/classify", tags=["classify"])
app.include_router(entities.router, prefix="/entities", tags=["entities"])

# Add new ClauseWise specific endpoints
@app.post("/extract-clauses/")
def extract_clauses_endpoint(request: dict):
    """Extract and breakdown individual clauses from legal documents"""
    from backend.core.clause_breakdown import split_into_clauses
    
    text = request.get("text", "")
    clauses = split_into_clauses(text)
    return {"clauses": clauses}

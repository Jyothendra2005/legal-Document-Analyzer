from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.granite_llm import get_granite_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class QueryReq(BaseModel):
    question: str
    context: str = ""

@router.post("/")
def query(q: QueryReq):
    """
    ClauseWise AI Assistant using IBM Granite
    Answers questions about legal concepts, document analysis, or specific clauses
    """
    try:
        # Get Granite service
        granite = get_granite_service()
        
        # Generate answer using Granite AI
        answer = granite.answer_question(q.question, q.context)
        
        return {"answer": answer}
        
    except Exception as e:
        logger.error(f"Error in document query: {e}")
        return {"answer": f"I apologize, but I encountered an error while processing your question: {str(e)}. Please try rephrasing your question or contact support if the issue persists."}

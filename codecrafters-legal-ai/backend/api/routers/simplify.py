from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.granite_llm import get_granite_service
from backend.core.clause_breakdown import split_into_clauses
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class SimplifyRequest(BaseModel):
    text: str

@router.post("/")
def simplify(req: SimplifyRequest):
    """
    ClauseWise Clause Simplification using IBM Granite
    Converts complex legal language into plain, understandable terms
    """
    try:
        # Extract clauses first
        clauses = split_into_clauses(req.text)
        
        if not clauses:
            return {"simplified_clauses": ["No distinct clauses found in the document."]}
        
        # Get Granite service
        granite = get_granite_service()
        
        # Simplify each clause using Granite AI
        simplified_clauses = []
        for clause in clauses[:10]:  # Limit to first 10 clauses for performance
            if len(clause.strip()) > 20:  # Only simplify meaningful clauses
                simplified = granite.simplify_clause(clause)
                simplified_clauses.append({
                    "original": clause,
                    "simplified": simplified
                })
        
        return {"simplified_clauses": simplified_clauses}
        
    except Exception as e:
        logger.error(f"Error in clause simplification: {e}")
        return {"simplified_clauses": [f"Error simplifying clauses: {str(e)}"]}

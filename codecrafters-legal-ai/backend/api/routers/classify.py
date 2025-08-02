from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.granite_llm import get_granite_service
import re
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class ClassifyRequest(BaseModel):
    text: str

@router.post("/")
def classify_document(request: ClassifyRequest):
    """
    ClauseWise Document Type Classification using IBM Granite
    Accurately classifies uploaded legal documents into categories like NDA, lease, employment contract, or service agreement.
    """
    try:
        # Get Granite service
        granite = get_granite_service()
        
        # Use Granite AI for document classification
        ai_classification = granite.classify_document_with_ai(request.text)
        
        # Also use rule-based classification as backup/enhancement
        rule_classification = classify_document_rule_based(request.text)
        
        # Combine AI and rule-based results
        final_classification = merge_classification_results(ai_classification, rule_classification)
        
        return {"classification": final_classification}
        
    except Exception as e:
        logger.error(f"Error in document classification: {e}")
        # Fallback to rule-based only if AI fails
        rule_classification = classify_document_rule_based(request.text)
        return {"classification": rule_classification}

def classify_document_rule_based(text: str) -> dict:
    """Rule-based document classification as backup"""
    text_lower = text.lower()
    
    # Document classification patterns
    document_types = {
        "Non-Disclosure Agreement (NDA)": {
            "keywords": ["confidential", "non-disclosure", "proprietary", "trade secret", "confidentiality"],
            "phrases": ["confidential information", "proprietary information", "trade secrets", "non-disclosure agreement"],
            "description": "A legal contract that establishes confidential relationships between parties"
        },
        "Employment Contract": {
            "keywords": ["employment", "employee", "employer", "salary", "wages", "benefits", "termination"],
            "phrases": ["employment agreement", "terms of employment", "job duties", "compensation package"],
            "description": "A contract between an employer and employee outlining terms of employment"
        },
        "Service Agreement": {
            "keywords": ["services", "provider", "client", "deliverables", "scope of work", "statement of work"],
            "phrases": ["service agreement", "professional services", "scope of services", "service provider"],
            "description": "A contract for the provision of services between a service provider and client"
        },
        "Lease Agreement": {
            "keywords": ["lease", "rent", "tenant", "landlord", "premises", "property", "rental"],
            "phrases": ["lease agreement", "rental agreement", "leased premises", "monthly rent"],
            "description": "A contract between a landlord and tenant for the rental of property"
        },
        "Purchase Agreement": {
            "keywords": ["purchase", "sale", "buyer", "seller", "goods", "merchandise", "payment"],
            "phrases": ["purchase agreement", "sale agreement", "purchase price", "delivery terms"],
            "description": "A contract for the sale and purchase of goods or services"
        },
        "Partnership Agreement": {
            "keywords": ["partnership", "partner", "profit", "loss", "business", "venture"],
            "phrases": ["partnership agreement", "business partnership", "profit sharing", "joint venture"],
            "description": "A contract establishing terms of a business partnership"
        },
        "License Agreement": {
            "keywords": ["license", "licensor", "licensee", "intellectual property", "patent", "copyright"],
            "phrases": ["license agreement", "licensing terms", "intellectual property rights", "license fee"],
            "description": "A contract granting permission to use intellectual property or other assets"
        }
    }
    
    scores = {}
    
    # Calculate scores for each document type
    for doc_type, patterns in document_types.items():
        score = 0
        
        # Check keywords
        for keyword in patterns["keywords"]:
            if keyword in text_lower:
                score += 2
        
        # Check phrases (higher weight)
        for phrase in patterns["phrases"]:
            if phrase in text_lower:
                score += 5
        
        scores[doc_type] = score
    
    # Find the best match
    if not scores or max(scores.values()) == 0:
        return {
            "type": "General Legal Document",
            "confidence": 0.3,
            "description": "Unable to classify into a specific category",
            "key_characteristics": ["Contains legal terminology", "Formal document structure"]
        }
    
    best_match = max(scores, key=scores.get)
    max_score = scores[best_match]
    confidence = min(max_score / 15.0, 1.0)  # Normalize to 0-1 range
    
    # Generate key characteristics
    characteristics = []
    doc_info = document_types[best_match]
    
    for keyword in doc_info["keywords"]:
        if keyword in text_lower:
            characteristics.append(f"Contains '{keyword}' terminology")
    
    for phrase in doc_info["phrases"]:
        if phrase in text_lower:
            characteristics.append(f"Includes '{phrase}' language")
    
    return {
        "type": best_match,
        "confidence": confidence,
        "description": doc_info["description"],
        "key_characteristics": characteristics[:4]  # Limit to top 4 characteristics
    }

def merge_classification_results(ai_result: dict, rule_result: dict) -> dict:
    """Merge AI and rule-based classification results"""
    # Prefer AI result if confidence is reasonable, otherwise use rule-based
    if ai_result.get("confidence", 0) > 0.3:
        # Use AI result but enhance with rule-based characteristics
        merged = ai_result.copy()
        rule_chars = rule_result.get("key_characteristics", [])
        ai_chars = merged.get("key_characteristics", [])
        
        # Combine characteristics without duplicates
        all_chars = list(set(ai_chars + rule_chars))
        merged["key_characteristics"] = all_chars[:5]
        
        return merged
    else:
        # Use rule-based result as primary
        return rule_result

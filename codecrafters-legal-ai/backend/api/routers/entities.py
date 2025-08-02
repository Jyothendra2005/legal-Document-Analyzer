from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.granite_llm import get_granite_service
import re
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter()

class EntityRequest(BaseModel):
    text: str

@router.post("/")
def extract_entities(request: EntityRequest):
    """
    ClauseWise Named Entity Recognition using IBM Granite
    Extracts parties, dates, monetary values, obligations, and legal terms from legal documents
    """
    try:
        # Get Granite service
        granite = get_granite_service()
        
        # Use Granite AI for advanced entity extraction
        ai_entities = granite.extract_entities_with_ai(request.text)
        
        # Also use rule-based extraction as backup/enhancement
        rule_entities = extract_entities_rule_based(request.text)
        
        # Combine AI and rule-based results
        combined_entities = merge_entity_results(ai_entities, rule_entities)
        
        return {"entities": combined_entities}
        
    except Exception as e:
        logger.error(f"Error in entity extraction: {e}")
        # Fallback to rule-based only if AI fails
        rule_entities = extract_entities_rule_based(request.text)
        return {"entities": rule_entities}

def extract_entities_rule_based(text: str) -> dict:
    """Rule-based entity extraction as backup"""
    entities = {
        "parties": extract_parties(text),
        "dates": extract_dates(text),
        "monetary_values": extract_monetary_values(text),
        "obligations": extract_obligations(text),
        "legal_terms": extract_legal_terms(text)
    }
    return entities

def merge_entity_results(ai_entities: dict, rule_entities: dict) -> dict:
    """Merge AI and rule-based entity extraction results"""
    merged = {}
    
    for category in ["parties", "dates", "monetary_values", "obligations", "legal_terms"]:
        ai_items = ai_entities.get(category, [])
        rule_items = rule_entities.get(category, [])
        
        # Combine and deduplicate
        combined = list(set(ai_items + rule_items))
        # Remove empty items
        combined = [item for item in combined if item and item.strip()]
        
        merged[category] = combined[:10]  # Limit to top 10 items per category
    
    return merged

def extract_parties(text: str) -> list[str]:
    """Extract party names and organizations"""
    party_patterns = [
        r'\b[A-Z][a-z]+ [A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',  # Person names
        r'\b[A-Z][A-Z\s&]+(?:LLC|Inc|Corp|Company|Ltd|LP|LLP)\b',  # Company names
        r'(?:Company|Corporation|LLC|Inc|Ltd|LP|LLP)(?:\s+[A-Z][a-z]+)*',  # Company entities
        r'(?:Party|Parties|Client|Contractor|Employee|Employer|Lessor|Lessee)(?:\s+[A-Z][a-z]+)*'  # Legal party terms
    ]
    
    parties = []
    for pattern in party_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        parties.extend(matches)
    
    # Remove duplicates and clean
    return list(set([p.strip() for p in parties if len(p.strip()) > 3]))[:5]

def extract_dates(text: str) -> list[str]:
    """Extract dates and time periods"""
    date_patterns = [
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # MM/DD/YYYY or MM-DD-YYYY
        r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',  # YYYY/MM/DD or YYYY-MM-DD
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',  # Month DD, YYYY
        r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',  # DD Month YYYY
        r'\b(?:within|after|before|during)\s+\d+\s+(?:days|months|years)\b',  # Time periods
    ]
    
    dates = []
    for pattern in date_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        dates.extend(matches)
    
    return list(set(dates))[:5]

def extract_monetary_values(text: str) -> list[str]:
    """Extract monetary amounts and financial terms"""
    monetary_patterns = [
        r'\$[\d,]+(?:\.\d{2})?',  # $1,000.00
        r'\b\d+(?:,\d{3})*(?:\.\d{2})?\s*dollars?\b',  # 1,000 dollars
        r'\b(?:USD|EUR|GBP)\s*[\d,]+(?:\.\d{2})?\b',  # USD 1,000.00
        r'\b(?:salary|wage|fee|payment|compensation|amount)\s*:?\s*\$?[\d,]+(?:\.\d{2})?\b',  # salary: $1,000
        r'\b(?:per|each|every)\s+(?:hour|month|year|week)\s*:?\s*\$?[\d,]+(?:\.\d{2})?\b',  # per hour: $25
    ]
    
    amounts = []
    for pattern in monetary_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        amounts.extend(matches)
    
    return list(set(amounts))[:5]

def extract_obligations(text: str) -> list[str]:
    """Extract obligations and responsibilities"""
    obligation_patterns = [
        r'(?:shall|must|will|agrees? to|required to|responsible for)\s+[^.]+[.]',  # Modal verbs indicating obligations
        r'(?:obligation|duty|responsibility|requirement)\s+[^.]+[.]',  # Direct obligation terms
        r'(?:Party|Employee|Contractor|Company)\s+(?:shall|must|will|agrees?)\s+[^.]+[.]',  # Party-specific obligations
    ]
    
    obligations = []
    for pattern in obligation_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
        obligations.extend([match.strip() for match in matches])
    
    # Clean and limit
    cleaned_obligations = [obs for obs in obligations if len(obs) > 20 and len(obs) < 200]
    return cleaned_obligations[:5]

def extract_legal_terms(text: str) -> list[str]:
    """Extract key legal terms and concepts"""
    legal_terms = [
        'confidentiality', 'non-disclosure', 'liability', 'indemnification', 'breach',
        'termination', 'jurisdiction', 'governing law', 'force majeure', 'arbitration',
        'intellectual property', 'copyright', 'trademark', 'patent', 'trade secret',
        'warranty', 'guarantee', 'representation', 'covenant', 'consideration'
    ]
    
    found_terms = []
    for term in legal_terms:
        if re.search(r'\b' + re.escape(term) + r'\b', text, re.IGNORECASE):
            found_terms.append(term.title())
    
    return found_terms[:8]

import re

def split_into_clauses(text: str) -> list[str]:
    """
    ClauseWise: Enhanced clause extraction and breakdown
    Detects and segments individual clauses from lengthy legal documents for focused analysis.
    """
    # Enhanced patterns for better clause detection
    clause_patterns = [
        r'\n\s*\d+\.\s+',  # Numbered clauses (1. 2. 3.)
        r'\n\s*\([a-z]\)\s+',  # Lettered sub-clauses (a) (b) (c))
        r'\n\s*[A-Z][A-Z\s]+:\s*',  # Section headers (WHEREAS:, THEREFORE:)
        r'\.(?=\s+[A-Z])',  # Sentence boundaries
        r';\s+(?=[A-Z])',  # Semicolon separations
        r'\n\s*\n+',  # Paragraph breaks
    ]
    
    # Combine all patterns
    pattern = '|'.join(f'({p})' for p in clause_patterns)
    
    # Split text using combined pattern
    clauses = re.split(pattern, text, flags=re.MULTILINE)
    
    # Clean and filter clauses
    cleaned_clauses = []
    for clause in clauses:
        if clause and not re.match(r'^[\s\d\.\(\)a-z]*$', clause):  # Skip separators
            cleaned = clause.strip()
            if len(cleaned) > 20:  # Only include substantial clauses
                cleaned_clauses.append(cleaned)
    
    # If no clauses found with advanced splitting, fall back to simple method
    if len(cleaned_clauses) < 2:
        simple_clauses = re.split(r"\n\s*\n|;|\.\s+", text)
        cleaned_clauses = [c.strip() for c in simple_clauses if c.strip() and len(c.strip()) > 20]
    
    return cleaned_clauses[:10]  # Limit to first 10 clauses for UI performance

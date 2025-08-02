from backend.core.simplifier import simplify_clause

def answer_query(doc_texts: list[str], user_question: str) -> str:
    # naive stub: just echoes simplified question
    return simplify_clause(user_question)

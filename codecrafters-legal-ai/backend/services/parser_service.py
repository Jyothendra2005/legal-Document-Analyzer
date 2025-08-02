from backend.ingestion.pdf_parser import parse_pdf_bytes
from docx import Document
import io

def parse_document(filename: str, content: bytes) -> str:
    if filename.lower().endswith(".pdf"):
        return parse_pdf_bytes(content)
    if filename.lower().endswith(".docx"):
        doc = Document(io.BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs)
    if filename.lower().endswith(".txt"):
        return content.decode("utf-8", errors="ignore")
    raise ValueError("Unsupported format")

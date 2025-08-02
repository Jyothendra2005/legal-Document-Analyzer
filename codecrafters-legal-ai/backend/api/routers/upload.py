from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.services.parser_service import parse_document

router = APIRouter()

@router.post("/")
async def upload_document(file: UploadFile = File(...)):
    # Check file extension as well as MIME type for better compatibility
    allowed_extensions = ['.pdf', '.docx', '.txt']
    file_extension = '.' + file.filename.lower().split('.')[-1] if '.' in file.filename else ''
    
    allowed_mime_types = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
    ]
    
    # Accept file if either MIME type is correct OR file extension is allowed
    if (file.content_type not in allowed_mime_types and 
        file_extension not in allowed_extensions):
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    content = await file.read()
    try:
        text = parse_document(file.filename, content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"text": text}

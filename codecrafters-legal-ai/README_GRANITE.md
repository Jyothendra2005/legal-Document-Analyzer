# ClauseWise: Legal Document Analyzer - Granite AI Integration Guide

## 🚀 Setup Complete!

Your ClauseWise application has been successfully updated with **IBM Granite 3.3-2B Instruct** model integration from Hugging Face. Here's what's been implemented:

## ✅ **Granite AI Features Implemented**

### 1. **Clause Simplification** (`backend/api/routers/simplify.py`)
- Uses Granite AI to convert complex legal language into plain English
- Combines AI insights with rule-based clause extraction
- Returns both original and simplified versions

### 2. **Named Entity Recognition** (`backend/api/routers/entities.py`)
- Granite AI extracts parties, dates, monetary values, obligations, and legal terms
- Hybrid approach: AI + rule-based for maximum accuracy
- Structured output for easy frontend display

### 3. **Document Classification** (`backend/api/routers/classify.py`)
- Granite AI classifies documents into legal categories
- Enhanced confidence scoring and characteristics
- Fallback to rule-based classification if needed

### 4. **AI Assistant** (`backend/api/routers/query.py`)
- Granite-powered Q&A for legal document analysis
- Contextual understanding of legal concepts
- Natural language responses

## 🧠 **Granite LLM Service** (`backend/services/granite_llm.py`)

### Core Features:
- **Model**: `ibm-granite/granite-3.3-2b-instruct` from Hugging Face
- **Automatic GPU/CPU detection** for optimal performance
- **Memory optimization** with float16 precision (GPU) / float32 (CPU)
- **Structured prompting** for legal document analysis
- **Error handling** with graceful fallbacks

### Supported Operations:
1. `simplify_clause()` - Legal text simplification
2. `extract_entities_with_ai()` - AI-powered entity extraction
3. `classify_document_with_ai()` - Document type classification
4. `answer_question()` - General legal Q&A
5. `generate_response()` - Core text generation

## 📦 **Updated Dependencies**

```
fastapi
uvicorn[standard]
streamlit
transformers
torch
accelerate
huggingface_hub
sentence-transformers
pydantic
pdfplumber
python-docx
tqdm
```

## 🎯 **Next Steps to Run ClauseWise**

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Backend (Terminal 1)
```bash
cd c:\codecrafters-legal-ai
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Start Frontend (Terminal 2)
```bash
cd c:\codecrafters-legal-ai
python -m streamlit run frontend/streamlit_app.py --server.port 8501
```

### 4. Test Granite Integration
```bash
python test_granite.py
```

## 🔧 **Configuration**

### GPU Requirements (Recommended):
- **VRAM**: 4GB+ for optimal performance
- **RAM**: 8GB+ system memory
- **CUDA**: Compatible GPU for acceleration

### CPU Fallback:
- **RAM**: 8GB+ required
- **Processing**: May be slower but fully functional

## 🌟 **ClauseWise Features**

### Frontend Interface:
1. **Document Upload** - PDF, DOCX, TXT support
2. **Clause Breakdown** - AI-powered clause extraction
3. **Clause Simplification** - Plain language conversion
4. **Named Entity Recognition** - Extract key legal entities
5. **Document Classification** - Automatic document categorization
6. **AI Assistant** - Natural language Q&A

### Backend API Endpoints:
- `POST /upload/` - Document upload and parsing
- `POST /extract-clauses/` - Clause extraction
- `POST /simplify/` - Clause simplification
- `POST /entities/` - Named entity recognition
- `POST /classify/` - Document classification
- `POST /query/` - AI assistant queries

## 🔍 **Testing the System**

### 1. Upload a legal document (PDF/DOCX/TXT)
### 2. Try each feature tab:
- Extract clauses to see document structure
- Simplify clauses for plain language versions
- Extract entities to identify key information
- Classify document to determine type
- Ask questions in the AI assistant

## ⚡ **Performance Notes**

- **First Load**: Model download (~2.5GB) may take time
- **GPU Mode**: Faster inference, lower memory usage
- **CPU Mode**: Slower but works on any system
- **Caching**: Model loads once, subsequent requests are fast

## 🛠 **Troubleshooting**

### Model Loading Issues:
- Ensure adequate RAM/VRAM
- Check internet connection for model download
- Verify transformers and torch versions

### Memory Issues:
- Close other applications
- Use CPU mode if GPU memory insufficient
- Reduce max_length parameters if needed

## 🎉 **Ready to Use!**

Your ClauseWise application now features state-of-the-art IBM Granite AI capabilities for comprehensive legal document analysis. The system combines the power of large language models with robust rule-based fallbacks for reliable performance.

**Access your application at:**
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

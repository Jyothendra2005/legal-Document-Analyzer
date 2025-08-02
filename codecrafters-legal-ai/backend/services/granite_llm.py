"""
Granite LLM Service for ClauseWise
Uses IBM Granite 3.3-2B Instruct model from Hugging Face
"""

import os
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from typing import List, Dict, Any
import re
import logging
from huggingface_hub import login

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GraniteLLMService:
    def __init__(self):
        self.model_name = "ibm-granite/granite-3.3-2b-instruct"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self.model_loaded = False
        self._setup_huggingface_auth()
        # Don't initialize model immediately - do it lazily
    
    def _setup_huggingface_auth(self):
        """Setup Hugging Face authentication"""
        try:
            # Try to get token from environment
            hf_token = os.getenv('HUGGINGFACE_TOKEN')
            if hf_token and hf_token != 'your_huggingface_token_here':
                logger.info("Using Hugging Face token for authentication")
                login(token=hf_token)
            else:
                logger.info("No Hugging Face token provided, using public access")
        except Exception as e:
            logger.warning(f"Hugging Face authentication failed: {e}")
            logger.info("Continuing without authentication (public models only)")
    
    def _ensure_model_loaded(self):
        """Lazy loading of the model when first needed"""
        if not self.model_loaded:
            self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the Granite model and tokenizer"""
        try:
            logger.info(f"Loading Granite model: {self.model_name}")
            logger.info(f"Using device: {self.device}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            
            # Load model with appropriate settings
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
            
            # Create text generation pipeline
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.device == "cuda" else -1,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            )
            
            logger.info("Granite model loaded successfully!")
            self.model_loaded = True
            
        except Exception as e:
            logger.error(f"Error loading Granite model: {e}")
            self.model_loaded = False
            # Don't raise the error - allow graceful fallback
    
    def generate_response(self, prompt: str, max_length: int = 512, temperature: float = 0.7) -> str:
        """Generate response using Granite model"""
        try:
            self._ensure_model_loaded()
            
            if not self.model_loaded or not self.pipeline:
                return "Model not available. Please check system requirements and try again."
            
            # Format prompt for Granite instruction format
            formatted_prompt = f"<|user|>\n{prompt}\n<|assistant|>\n"
            
            # Generate response with optimized parameters for speed
            try:
                outputs = self.pipeline(
                    formatted_prompt,
                    max_new_tokens=min(max_length, 100),  # Reduce max tokens for speed
                    temperature=0.3,  # Lower temperature for faster, more focused responses
                    do_sample=True,
                    top_p=0.8,
                    repetition_penalty=1.05,
                    pad_token_id=self.tokenizer.eos_token_id,
                    num_return_sequences=1
                )
                
                # Extract generated text
                full_response = outputs[0]['generated_text']
                # Remove the prompt part and extract only the assistant's response
                response = full_response.split("<|assistant|>\n")[-1].strip()
                
                # If response is empty or too short, provide a basic response
                if not response or len(response) < 10:
                    return "I understand your question. Due to current processing constraints, please try a more specific question or check back shortly."
                
                return response
                
            except Exception as gen_error:
                logger.error(f"Generation error: {gen_error}")
                return "I'm experiencing some technical difficulties with text generation. Please try again with a simpler question."
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"I apologize, but I'm experiencing technical difficulties. Please try again later."
    
    def simplify_clause(self, clause_text: str) -> str:
        """Simplify legal clause using Granite"""
        try:
            self._ensure_model_loaded()
            
            if not self.model_loaded:
                # Fallback to simple text processing
                return f"Simplified: {clause_text[:200]}... (AI model not available)"
            
            prompt = f"""Please simplify the following legal clause into plain, everyday language that a non-lawyer can easily understand. Keep the essential meaning but make it clear and simple:

Legal Clause: {clause_text}

Simplified Version:"""
            
            return self.generate_response(prompt, max_length=300)
        except Exception as e:
            logger.error(f"Error in clause simplification: {e}")
            return f"Error simplifying clause: {str(e)}"
    
    def extract_entities_with_ai(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities using Granite AI"""
        try:
            self._ensure_model_loaded()
            
            if not self.model_loaded:
                # Fallback to empty entities
                return {
                    "parties": [],
                    "dates": [],
                    "monetary_values": [],
                    "obligations": [],
                    "legal_terms": []
                }
            
            prompt = f"""Analyze the following legal document and extract key information. Return the results in this exact format:

PARTIES: [list the individuals, companies, or organizations involved]
DATES: [list all dates mentioned]
MONETARY VALUES: [list all money amounts, fees, or financial terms]
OBLIGATIONS: [list key duties, responsibilities, or requirements]
LEGAL TERMS: [list important legal concepts or technical terms]

Document: {text[:2000]}...

Analysis:"""
            
            response = self.generate_response(prompt, max_length=400)
            
            # Parse the response into structured data
            entities = {
                "parties": [],
                "dates": [],
                "monetary_values": [],
                "obligations": [],
                "legal_terms": []
            }
            
            try:
                lines = response.split('\n')
                current_category = None
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('PARTIES:'):
                        current_category = "parties"
                        # Extract items from the same line
                        items = line.replace('PARTIES:', '').strip()
                        if items and items != '[list the individuals, companies, or organizations involved]':
                            entities[current_category].extend([item.strip() for item in items.split(',') if item.strip()])
                    elif line.startswith('DATES:'):
                        current_category = "dates"
                        items = line.replace('DATES:', '').strip()
                        if items and items != '[list all dates mentioned]':
                            entities[current_category].extend([item.strip() for item in items.split(',') if item.strip()])
                    elif line.startswith('MONETARY VALUES:'):
                        current_category = "monetary_values"
                        items = line.replace('MONETARY VALUES:', '').strip()
                        if items and items != '[list all money amounts, fees, or financial terms]':
                            entities[current_category].extend([item.strip() for item in items.split(',') if item.strip()])
                    elif line.startswith('OBLIGATIONS:'):
                        current_category = "obligations"
                        items = line.replace('OBLIGATIONS:', '').strip()
                        if items and items != '[list key duties, responsibilities, or requirements]':
                            entities[current_category].extend([item.strip() for item in items.split(',') if item.strip()])
                    elif line.startswith('LEGAL TERMS:'):
                        current_category = "legal_terms"
                        items = line.replace('LEGAL TERMS:', '').strip()
                        if items and items != '[list important legal concepts or technical terms]':
                            entities[current_category].extend([item.strip() for item in items.split(',') if item.strip()])
                    elif current_category and line.startswith('-') or line.startswith('•'):
                        # Handle bullet points
                        item = line.lstrip('-•').strip()
                        if item:
                            entities[current_category].append(item)
            
            except Exception as e:
                logger.error(f"Error parsing entities: {e}")
            
            return entities
            
        except Exception as e:
            logger.error(f"Error in AI entity extraction: {e}")
            return {
                "parties": [],
                "dates": [],
                "monetary_values": [],
                "obligations": [],
                "legal_terms": []
            }
    
    def classify_document_with_ai(self, text: str) -> Dict[str, Any]:
        """Classify document type using Granite AI"""
        try:
            self._ensure_model_loaded()
            
            if not self.model_loaded:
                # Fallback classification
                return {
                    "type": "General Legal Document",
                    "confidence": 0.3,
                    "description": "AI model not available for detailed classification",
                    "key_characteristics": ["Document contains legal terminology"]
                }
            
            prompt = f"""Analyze the following legal document and classify its type. Choose from these categories:
- Non-Disclosure Agreement (NDA)
- Employment Contract
- Service Agreement
- Lease Agreement
- Purchase Agreement
- Partnership Agreement
- License Agreement
- General Legal Document

Also provide confidence level (0.0 to 1.0) and key characteristics.

Document excerpt: {text[:1500]}...

Classification:
Type:
Confidence:
Description:
Key Characteristics:"""
        
            response = self.generate_response(prompt, max_length=300)
            
            # Parse response
            result = {
                "type": "General Legal Document",
                "confidence": 0.5,
                "description": "Legal document analysis",
                "key_characteristics": []
            }
            
            try:
                lines = response.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('Type:'):
                        doc_type = line.replace('Type:', '').strip()
                        if doc_type:
                            result["type"] = doc_type
                    elif line.startswith('Confidence:'):
                        conf_str = line.replace('Confidence:', '').strip()
                        try:
                            # Extract numeric value
                            conf_match = re.search(r'(\d+\.?\d*)', conf_str)
                            if conf_match:
                                conf_val = float(conf_match.group(1))
                                if conf_val > 1.0:  # If it's a percentage
                                    conf_val = conf_val / 100.0
                                result["confidence"] = conf_val
                        except:
                            pass
                    elif line.startswith('Description:'):
                        desc = line.replace('Description:', '').strip()
                        if desc:
                            result["description"] = desc
                    elif line.startswith('Key Characteristics:'):
                        continue
                    elif line.startswith('-') or line.startswith('•'):
                        char = line.lstrip('-•').strip()
                        if char:
                            result["key_characteristics"].append(char)
            
            except Exception as e:
                logger.error(f"Error parsing classification: {e}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in AI document classification: {e}")
            return {
                "type": "General Legal Document",
                "confidence": 0.3,
                "description": f"Classification error: {str(e)}",
                "key_characteristics": ["Document analysis failed"]
            }
    
    def answer_question(self, question: str, context: str = "") -> str:
        """Answer questions about legal documents using Granite"""
        try:
            # Quick check for simple questions that can be answered without AI
            simple_answers = self._try_simple_answer(question, context)
            if simple_answers:
                return simple_answers
            
            self._ensure_model_loaded()
            
            if not self.model_loaded:
                return self._fallback_answer(question, context)
            
            prompt = f"""You are ClauseWise AI, a legal document analysis assistant. Answer the following question about legal concepts or document analysis.

Context: {context[:1000] if context else "General legal knowledge"}

Question: {question}

Answer:"""
            
            return self.generate_response(prompt, max_length=200)  # Reduced for faster response
            
        except Exception as e:
            logger.error(f"Error in AI question answering: {e}")
            return self._fallback_answer(question, context)
    
    def _try_simple_answer(self, question: str, context: str = "") -> str:
        """Try to answer simple questions without AI model"""
        question_lower = question.lower()
        
        # Simple question patterns
        if "what is" in question_lower or "define" in question_lower:
            if "nda" in question_lower or "non-disclosure" in question_lower:
                return "An NDA (Non-Disclosure Agreement) is a legal contract that prevents parties from sharing confidential information with third parties."
            elif "contract" in question_lower:
                return "A contract is a legally binding agreement between two or more parties that creates mutual obligations enforceable by law."
            elif "clause" in question_lower:
                return "A clause is a specific provision or section within a legal document that addresses a particular aspect of the agreement."
        
        elif "how to" in question_lower:
            if "simplify" in question_lower:
                return "To simplify legal language: 1) Replace complex terms with everyday words, 2) Break long sentences into shorter ones, 3) Use active voice, 4) Define technical terms."
        
        elif "summarize" in question_lower:
            if context:
                # Simple context-based summary
                sentences = context.split('.')[:3]  # First 3 sentences
                return f"Summary: {'. '.join(sentences)}... (This is a basic summary. Upload a document for detailed AI analysis.)"
            else:
                return "Please upload a document first, then I can provide a detailed summary using AI analysis."
        
        return ""  # No simple answer found
    
    def _fallback_answer(self, question: str, context: str = "") -> str:
        """Provide fallback answers when AI model is not available"""
        question_lower = question.lower()
        
        if "summarize" in question_lower or "summary" in question_lower:
            return "I can help summarize documents, but the AI model is currently loading. Please try again in a few moments, or upload a document for rule-based analysis."
        
        elif "parties" in question_lower or "who" in question_lower:
            return "To identify parties in a legal document, look for names of individuals, companies, or organizations mentioned in the beginning sections or signature areas."
        
        elif "obligation" in question_lower or "responsibility" in question_lower:
            return "Legal obligations are typically found in sections containing words like 'shall', 'must', 'agrees to', or 'responsible for'."
        
        elif "date" in question_lower or "when" in question_lower:
            return "Important dates in legal documents include effective dates, expiration dates, and deadlines. Look for date formats like MM/DD/YYYY or spelled-out dates."
        
        else:
            return "I'm still loading the AI model for detailed analysis. For immediate help, try uploading a document to use our rule-based analysis features."

# Global instance
granite_service = None

def get_granite_service() -> GraniteLLMService:
    """Get or create Granite service instance"""
    global granite_service
    if granite_service is None:
        granite_service = GraniteLLMService()
    return granite_service

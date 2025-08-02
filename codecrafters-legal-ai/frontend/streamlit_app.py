import streamlit as st
import requests
import time

# Page configuration with wide layout for better responsiveness
st.set_page_config(
    page_title="ClauseWise: Legal Document Analyzer", 
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        color: #1f4e79;
        border-bottom: 2px solid #e6f3ff;
        margin-bottom: 2rem;
    }
    
    .upload-section {
        background: #f8fcff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e1ecf4;
        margin-bottom: 1rem;
    }
    
    .result-section {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #d1d5db;
        margin: 1rem 0;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #1f4e79, #2563eb);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #1e40af, #1d4ed8);
        transform: translateY(-1px);
    }
    
    .sidebar-info {
        background: #f0f9ff;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #0ea5e9;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">⚖️ ClauseWise: Legal Document Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #6b7280; margin-bottom: 2rem; font-style: italic;">Powered by IBM Watson & Granite AI</p>', unsafe_allow_html=True)

# Sidebar for app info and settings
with st.sidebar:
    st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
    st.markdown("### 🎯 ClauseWise Features")
    st.markdown("""
    - 📄 **Multi-Format Support**: PDF, DOCX, TXT
    - 🔍 **Clause Extraction**: Automated breakdown
    - ✨ **Clause Simplification**: Layman-friendly language
    - 🏷️ **Named Entity Recognition**: Extract key entities
    - 📂 **Document Classification**: Contract type detection
    - ❓ **Document Analysis**: AI-powered Q&A
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ⚙️ Analysis Settings")
    show_raw_text = st.checkbox("Show extracted text", value=True)
    auto_simplify = st.checkbox("Auto-simplify clauses", value=False)
    extract_entities = st.checkbox("Extract named entities", value=True)
    classify_document = st.checkbox("Classify document type", value=True)
    
    st.markdown("---")
    st.markdown("### 🤖 AI Model Status")
    
    # Check AI model status
    try:
        model_status_resp = requests.get("http://localhost:8000/", timeout=5)
        if model_status_resp.ok:
            st.success("✅ Backend connected")
        else:
            st.error("❌ Backend error")
    except:
        st.error("❌ Backend offline")
    
    st.info("💡 **First AI request may take 2-5 minutes as the model loads**")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Upload section
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown("### 📤 Upload Document")
    uploaded = st.file_uploader(
        "Choose a legal document", 
        type=["pdf", "docx", "txt"],
        help="Supported formats: PDF, DOCX, TXT (max 200MB)"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Status/Info panel
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Status")
    if uploaded:
        st.success("✅ Document uploaded")
        st.metric("File size", f"{len(uploaded.getvalue())/1024:.1f} KB")
        st.metric("File type", uploaded.type or "Unknown")
    else:
        st.info("🔄 Waiting for upload")
    st.markdown('</div>', unsafe_allow_html=True)

if uploaded:
    # Progress indicator
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    files = {"file": (uploaded.name, uploaded.getvalue())}
    
    try:
        # Update progress
        progress_bar.progress(25)
        status_text.text("🔄 Uploading document...")
        
        resp = requests.post("http://localhost:8000/upload/", files=files, timeout=30)
        
        progress_bar.progress(75)
        status_text.text("📝 Processing document...")
        
        if resp.ok:
            progress_bar.progress(100)
            status_text.text("✅ Document processed successfully!")
            time.sleep(1)
            progress_bar.empty()
            status_text.empty()
            
            text = resp.json().get("text", "")
            
            # Create tabs for ClauseWise features
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📄 Extracted Text", 
                "🔍 Clause Breakdown", 
                "✨ Simplified Clauses", 
                "🏷️ Named Entities",
                "📂 Document Classification"
            ])
            
            with tab1:
                if show_raw_text:
                    st.markdown('<div class="result-section">', unsafe_allow_html=True)
                    st.markdown("### 📄 Extracted Text")
                    # Text statistics
                    char_count = len(text)
                    word_count = len(text.split())
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Characters", f"{char_count:,}")
                    with col_b:
                        st.metric("Words", f"{word_count:,}")
                    
                    # Text area with better height management
                    height = min(max(300, len(text) // 50), 600)
                    st.text_area("Document content", text, height=height, label_visibility="collapsed")
                    st.markdown('</div>', unsafe_allow_html=True)
            
            with tab2:
                st.markdown('<div class="result-section">', unsafe_allow_html=True)
                st.markdown("### 🔍 Clause Extraction & Breakdown")
                
                col_btn1, col_btn2 = st.columns([1, 3])
                with col_btn1:
                    extract_clicked = st.button("🔍 Extract Clauses", key="extract_btn")
                
                if extract_clicked:
                    with st.spinner("🔄 AI is extracting clauses..."):
                        # This will be implemented with IBM Watson/Granite
                        extract_resp = requests.post("http://localhost:8000/extract-clauses/", json={"text": text}, timeout=30)
                        if extract_resp.ok:
                            clauses = extract_resp.json().get("clauses", [])
                            
                            if clauses:
                                st.success(f"✅ Extracted {len(clauses)} clauses")
                                for i, clause in enumerate(clauses, 1):
                                    with st.expander(f"📝 Clause {i}", expanded=i<=2):
                                        st.write(clause)
                            else:
                                st.warning("⚠️ No distinct clauses found")
                        else:
                            st.error("❌ Failed to extract clauses")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab3:
                st.markdown('<div class="result-section">', unsafe_allow_html=True)
                st.markdown("### ✨ Clause Simplification")
                st.markdown("*Converting complex legal language into layman-friendly terms*")
                
                col_btn1, col_btn2 = st.columns([1, 3])
                with col_btn1:
                    simplify_clicked = st.button("🚀 Simplify Clauses", key="simplify_btn")
                
                if simplify_clicked or auto_simplify:
                    with st.spinner("🔄 AI is simplifying clauses..."):
                        try:
                            simplify_resp = requests.post(
                                "http://localhost:8000/simplify/", 
                                json={"text": text}, 
                                timeout=90  # Increased timeout
                            )
                            if simplify_resp.ok:
                                simplified_clauses = simplify_resp.json().get("simplified_clauses", [])
                                
                                if simplified_clauses:
                                    st.success(f"✅ Simplified {len(simplified_clauses)} clauses")
                                    for i, clause_pair in enumerate(simplified_clauses, 1):
                                        with st.expander(f"📝 Simplified Clause {i}", expanded=i<=2):
                                            if isinstance(clause_pair, dict):
                                                st.markdown("**Original:**")
                                                st.write(clause_pair.get("original", ""))
                                                st.markdown("**Simplified:**")
                                                st.success(clause_pair.get("simplified", ""))
                                            else:
                                                st.write(clause_pair)
                                else:
                                    st.warning("⚠️ No clauses found to simplify")
                            else:
                                st.error("❌ Failed to simplify clauses")
                        except requests.exceptions.Timeout:
                            st.warning("⏱️ Clause simplification is taking longer than expected. The AI model may be loading for the first time.")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab4:
                st.markdown('<div class="result-section">', unsafe_allow_html=True)
                st.markdown("### 🏷️ Named Entity Recognition")
                st.markdown("*Extracting parties, dates, obligations, and monetary values*")
                
                col_btn1, col_btn2 = st.columns([1, 3])
                with col_btn1:
                    ner_clicked = st.button("🔍 Extract Entities", key="ner_btn")
                
                if ner_clicked or extract_entities:
                    with st.spinner("🔄 AI is extracting entities..."):
                        try:
                            ner_resp = requests.post(
                                "http://localhost:8000/entities/", 
                                json={"text": text}, 
                                timeout=90  # Increased timeout
                            )
                            if ner_resp.ok:
                                entities = ner_resp.json().get("entities", {})
                                
                                if entities:
                                    st.success("✅ Named entities extracted")
                                    
                                    # Display entities in organized columns
                                    col_e1, col_e2 = st.columns(2)
                                    
                                    with col_e1:
                                        if entities.get("parties"):
                                            st.markdown("**👥 Parties:**")
                                            for party in entities["parties"]:
                                                st.write(f"• {party}")
                                        
                                        if entities.get("dates"):
                                            st.markdown("**📅 Dates:**")
                                            for date in entities["dates"]:
                                                st.write(f"• {date}")
                                    
                                    with col_e2:
                                        if entities.get("monetary_values"):
                                            st.markdown("**💰 Monetary Values:**")
                                            for value in entities["monetary_values"]:
                                                st.write(f"• {value}")
                                        
                                        if entities.get("obligations"):
                                            st.markdown("**📋 Obligations:**")
                                            for obligation in entities["obligations"]:
                                                st.write(f"• {obligation}")
                                else:
                                    st.warning("⚠️ No named entities found")
                            else:
                                st.error("❌ Failed to extract entities")
                        except requests.exceptions.Timeout:
                            st.warning("⏱️ Entity extraction is taking longer than expected. The AI model may be loading for the first time.")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab5:
                st.markdown('<div class="result-section">', unsafe_allow_html=True)
                st.markdown("### 📂 Document Type Classification")
                st.markdown("*Identifying contract type: NDA, lease, employment, service agreement, etc.*")
                
                col_btn1, col_btn2 = st.columns([1, 3])
                with col_btn1:
                    classify_clicked = st.button("🔍 Classify Document", key="classify_btn")
                
                if classify_clicked or classify_document:
                    with st.spinner("🔄 AI is classifying document..."):
                        try:
                            classify_resp = requests.post(
                                "http://localhost:8000/classify/", 
                                json={"text": text}, 
                                timeout=90  # Increased timeout
                            )
                            if classify_resp.ok:
                                classification = classify_resp.json().get("classification", {})
                                
                                if classification:
                                    document_type = classification.get("type", "Unknown")
                                    confidence = classification.get("confidence", 0)
                                    
                                    st.success(f"✅ Document classified")
                                    
                                    # Display classification results
                                    col_c1, col_c2 = st.columns(2)
                                    with col_c1:
                                        st.metric("Document Type", document_type)
                                    with col_c2:
                                        st.metric("Confidence", f"{confidence:.1%}")
                                    
                                    # Additional details
                                    if classification.get("description"):
                                        st.info(f"**Description:** {classification['description']}")
                                    
                                    if classification.get("key_characteristics"):
                                        st.markdown("**Key Characteristics:**")
                                        for char in classification["key_characteristics"]:
                                            st.write(f"• {char}")
                                else:
                                    st.warning("⚠️ Unable to classify document")
                            else:
                                st.error("❌ Failed to classify document")
                        except requests.exceptions.Timeout:
                            st.warning("⏱️ Document classification is taking longer than expected. The AI model may be loading for the first time.")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
        else:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ Upload failed: {resp.text}")
            
    except requests.exceptions.Timeout:
        progress_bar.empty()
        status_text.empty()
        st.error("⏱️ Request timed out. Please try again.")
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"❌ Error: {e}")

# Document Analysis Q&A Section
st.markdown("---")
st.markdown('<div class="result-section">', unsafe_allow_html=True)
st.markdown("### ❓ ClauseWise AI Assistant")
st.markdown("*Ask questions about legal concepts, document analysis, or specific clauses*")

general_question = st.text_input(
    "Ask ClauseWise AI", 
    placeholder="e.g., What are the key obligations in this contract? Who are the parties involved?",
    key="general_q"
)

col_g1, col_g2 = st.columns([1, 3])
with col_g1:
    general_ask = st.button("🔍 Analyze", key="general_ask_btn", disabled=not general_question)

if general_ask and general_question:
    with st.spinner("🤔 ClauseWise AI is analyzing..."):
        try:
            # Increase timeout for AI processing
            qresp = requests.post(
                "http://localhost:8000/query/", 
                json={"question": general_question}, 
                timeout=120  # Increased to 2 minutes for model loading
            )
            if qresp.ok:
                answer = qresp.json().get("answer", "")
                st.markdown("#### 💡 ClauseWise Analysis:")
                st.success(answer)
            else:
                st.error("❌ Analysis failed")
        except requests.exceptions.Timeout:
            st.warning("⏱️ The AI model is taking longer than expected. This may be the first time loading the model (which can take 2-5 minutes). Please try again in a few moments.")
        except Exception as e:
            st.error(f"❌ Error: {e}")

st.markdown('</div>', unsafe_allow_html=True)

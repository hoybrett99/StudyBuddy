# frontend/streamlit_app.py

import streamlit as st
import requests
from datetime import datetime
import time

# ============================================================================
# Configuration
# ============================================================================

API_URL = "http://127.0.0.1:8000"

# ============================================================================
# Page Configuration
# ============================================================================

st.set_page_config(
    page_title="Study Buddy - AI Learning Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# Custom CSS
# ============================================================================

st.markdown("""
    <style>
    /* Use full viewport width */
    .main .block-container {
        max-width: none;
        padding: 2rem 3rem;
    }
    
    /* Upload box styling */
    .upload-box {
        border: 2px dashed #4CAF50;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: rgba(76, 175, 80, 0.1);
    }
    
    /* Stat card styling */
    .stat-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# Session State Initialization
# ============================================================================

if 'messages' not in st.session_state:
    st.session_state.messages = []

# ============================================================================
# Helper Functions
# ============================================================================

def check_api_health():
    """Check if the API is running."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def upload_document(file):
    """Upload a document to the API."""
    files = {"file": (file.name, file.getvalue(), file.type)}
    response = requests.post(f"{API_URL}/upload", files=files)
    return response

def query_api(question, num_contexts=4):
    """Query the API with a question."""
    payload = {
        "question": question,
        "num_contexts": num_contexts
    }
    response = requests.post(f"{API_URL}/query", json=payload)
    return response.json()

def get_stats():
    """Get system statistics from the API."""
    try:
        response = requests.get(f"{API_URL}/stats", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Stats endpoint returned status {response.status_code}")
            return {
                "total_documents": 0,
                "total_chunks": 0,
                "total_queries": 0
            }
    except Exception as e:
        print(f"Error getting stats: {str(e)}")
        return {
            "total_documents": 0,
            "total_chunks": 0,
            "total_queries": 0
        }

# ============================================================================
# Sidebar
# ============================================================================

with st.sidebar:
    st.title("📚 Study Buddy")
    st.markdown("---")
    
    # API Health Check
    api_status = check_api_health()
    if api_status:
        st.success("✅ API Connected")
    else:
        st.error("❌ API Disconnected")
        st.info("Make sure the FastAPI server is running:\n```\nuvicorn app.main:app --reload\n```")
    
    st.markdown("---")
    
    # System Stats
    st.subheader("📊 System Stats")
    stats = get_stats()
    if stats:
        st.metric("Total Documents", stats.get('total_documents', 0))
        st.metric("Total Chunks", stats.get('total_chunks', 0))
        st.metric("Total Queries", stats.get('total_queries', 0))
    else:
        st.warning("Unable to load stats")
    
    st.markdown("---")
    
    # Settings
    st.subheader("⚙️ Settings")
    num_contexts = st.slider(
        "Context chunks per query",
        min_value=1,
        max_value=10,
        value=4,
        help="Number of relevant text chunks to use for answering questions"
    )
    
    st.markdown("---")
    
    # About
    st.subheader("ℹ️ About")
    st.markdown("""
    **Study Buddy** is an AI-powered learning assistant that helps you study by:
    - 📤 Uploading your study materials
    - 💬 Asking questions about your documents
    - 🎯 Getting accurate, source-backed answers
    
    **Powered by:**
    - Claude Sonnet 4
    - ChromaDB
    - FastAPI
    """)

# ============================================================================
# Main Content
# ============================================================================

st.title("📚 Study Buddy - AI Learning Assistant")
st.markdown("Upload your study materials and ask questions to get AI-powered answers with source citations.")

# ============================================================================
# Tabs
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📤 Upload", "📖 Library", "🔍 Preview"])

# ============================================================================
# TAB 1: Chat Interface
# ============================================================================

with tab1:
    st.markdown("### Ask questions about your study materials")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Display sources if available
            if message["role"] == "assistant" and "sources" in message:
                if message["sources"]:
                    with st.expander("📎 View Sources", expanded=False):
                        for i, source in enumerate(message["sources"], 1):
                            # Source header
                            col1, col2, col3 = st.columns([2, 1, 1])
                            
                            with col1:
                                st.markdown(f"### 📄 Source {i}")
                                st.caption(f"`{source['document_name']}`")
                            
                            with col2:
                                st.metric("Relevance", f"{source['relevance_score']:.3f}")
                            
                            with col3:
                                st.caption("Chunk ID")
                                st.code(source['chunk_id'][-8:], language=None)
                            
                            # Display chunk text if available
                            if source.get('chunk_text'):
                                with st.expander("📖 View chunk content", expanded=False):
                                    st.markdown(source['chunk_text'])
                            
                            # Add divider between sources
                            if i < len(message["sources"]):
                                st.divider()
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your study materials..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    response = query_api(prompt, num_contexts)
                    answer = response['answer']
                    sources = response.get('sources', [])
                    query_time = response.get('query_time_seconds', 0)
                    
                    st.markdown(answer)
                    st.caption(f"⏱️ Answered in {query_time:.2f}s")
                    
                    # Display sources
                    if sources:
                        with st.expander("📎 View Sources", expanded=False):
                            for i, source in enumerate(sources, 1):
                                col1, col2, col3 = st.columns([2, 1, 1])
                                
                                with col1:
                                    st.markdown(f"### 📄 Source {i}")
                                    st.caption(f"`{source['document_name']}`")
                                
                                with col2:
                                    st.metric("Relevance", f"{source['relevance_score']:.3f}")
                                
                                with col3:
                                    st.caption("Chunk ID")
                                    st.code(source['chunk_id'][-8:], language=None)
                                
                                # Display chunk text
                                if source.get('chunk_text'):
                                    with st.expander("📖 View chunk content", expanded=False):
                                        st.markdown(source['chunk_text'])
                                
                                if i < len(sources):
                                    st.divider()
                    
                    # Save to session state
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })
                
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
    
    # Clear chat button
    if st.session_state.messages:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

# ============================================================================
# TAB 2: Upload Documents
# ============================================================================

with tab2:
    st.markdown("### Upload your study materials")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="upload-box">', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'txt', 'docx'],
            help="Upload PDF, TXT, or DOCX files (max 50MB)"
        )
        
        if uploaded_file is not None:
            st.write(f"**📄 Filename:** {uploaded_file.name}")
            st.write(f"**📦 Size:** {uploaded_file.size / 1024:.2f} KB")
            st.write(f"**📋 Type:** {uploaded_file.type}")
            
            if st.button("📤 Upload and Process", type="primary", use_container_width=True):
                with st.spinner("Processing document..."):
                    try:
                        # Reset file pointer
                        uploaded_file.seek(0)
                        
                        # Upload file
                        response = upload_document(uploaded_file)
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.success("✅ Document uploaded successfully!")
                            
                            # Display results
                            col_a, col_b, col_c = st.columns(3)
                            with col_a:
                                st.metric("Document ID", result['document_id'][:8] + "...")
                            with col_b:
                                st.metric("Chunks Created", result['chunks_created'])
                            with col_c:
                                st.metric("Status", "✓ Ready")
                            
                            st.info("💡 You can now ask questions about this document in the Chat tab!")
                        else:
                            error_detail = response.json().get('detail', 'Unknown error')
                            st.error(f"❌ Upload failed: {error_detail}")
                    
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📝 Supported Formats")
        st.markdown("""
        - **PDF** (.pdf)
        - **Text** (.txt)
        - **Word** (.docx)
        
        ### 💡 Tips
        - Files should be text-based
        - Max file size: 50MB
        - Clear, readable text works best
        - Multiple uploads are supported
        """)

# ============================================================================
# TAB 3: Library
# ============================================================================

with tab3:
    st.markdown("### 📖 Document Library")
    
    stats = get_stats()
    
    if stats:
        total_docs = stats.get('total_documents', 0)
        total_chunks = stats.get('total_chunks', 0)
        total_queries = stats.get('total_queries', 0)
        
        if total_docs > 0:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown('<div class="stat-card">', unsafe_allow_html=True)
                st.metric("Total Documents", total_docs)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="stat-card">', unsafe_allow_html=True)
                st.metric("Total Chunks", total_chunks)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="stat-card">', unsafe_allow_html=True)
                st.metric("Queries Processed", total_queries)
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            st.info("📚 All your uploaded documents are stored and ready for querying!")
        else:
            st.info("📭 No documents uploaded yet. Go to the Upload tab to add your first document!")
    else:
        st.warning("⚠️ Unable to connect to API. Please check if the backend is running.")

# ============================================================================
# TAB 4: Preview Document Extraction
# ============================================================================

with tab4:
    st.markdown("### 🔍 Preview Document Extraction")
    st.info("📋 Upload a document to see the extracted text. Useful for checking PDF quality before processing.")
    
    preview_file = st.file_uploader(
        "Choose a file to preview",
        type=['pdf', 'txt', 'docx'],
        key="preview_uploader",
        help="Upload a file to see how text is extracted"
    )
    
    if preview_file is not None:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"**📄 File:** {preview_file.name}")
            st.write(f"**📦 Size:** {preview_file.size / 1024:.2f} KB")
        
        with col2:
            preview_button = st.button("🔍 Extract Text", type="primary", use_container_width=True)
        
        if preview_button:
            with st.spinner("Extracting text from document..."):
                try:
                    # Reset file pointer
                    preview_file.seek(0)
                    
                    # Call preview endpoint
                    files = {"file": (preview_file.name, preview_file.getvalue(), preview_file.type)}
                    response = requests.post(f"{API_URL}/preview", files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Display stats
                        st.markdown("---")
                        st.markdown("### 📊 Extraction Statistics")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Characters", f"{result['extracted_length']:,}")
                        with col2:
                            st.metric("Words", f"{result['word_count']:,}")
                        with col3:
                            st.metric("Lines", f"{result['line_count']:,}")
                        with col4:
                            st.metric("File Type", result['file_type'].upper())
                        
                        # Quality check
                        st.markdown("---")
                        st.markdown("### ✅ Quality Check")
                        
                        quality_issues = []
                        text = result['full_text']
                        
                        import re
                        
                        # Check for common OCR issues
                        single_letters = len([w for w in text.split() if len(w) == 1 and w.isupper() and w not in ['A', 'I']])
                        if single_letters > 50:
                            quality_issues.append(f"⚠️ {single_letters} stray single capital letters detected (possible OCR errors)")
                        
                        consonant_clusters = len(re.findall(r'[bcdfghjklmnpqrstvwxyz]{6,}', text.lower()))
                        if consonant_clusters > 20:
                            quality_issues.append(f"⚠️ {consonant_clusters} unusual consonant clusters (possible gibberish)")
                        
                        excessive_spaces = len(re.findall(r'\s{4,}', text))
                        if excessive_spaces > 10:
                            quality_issues.append(f"⚠️ {excessive_spaces} instances of excessive spacing")
                        
                        non_ascii = len([c for c in text if ord(c) > 127])
                        non_ascii_percent = (non_ascii / len(text) * 100) if text else 0
                        if non_ascii_percent > 10:
                            quality_issues.append(f"⚠️ {non_ascii_percent:.1f}% non-ASCII characters")
                        
                        if quality_issues:
                            for issue in quality_issues:
                                st.warning(issue)
                            st.info("💡 **Tip:** Try using `pdfplumber` instead of `pypdf` for better extraction quality.")
                        else:
                            st.success("✅ Text extraction looks clean! No major issues detected.")
                        
                        # Display extracted text in tabs
                        st.markdown("---")
                        st.markdown("### 📄 Extracted Text")

                        text_tab1, text_tab2, text_tab3 = st.tabs([
                            "📖 First 500 chars", 
                            "📖 Last 500 chars", 
                            "📄 Full Text"
                        ])

                        with text_tab1:
                            st.caption("Preview of the beginning of the document")
                            st.text_area(
                                "First 500 characters",
                                value=result['preview_first_500'],
                                height=300,
                                label_visibility="collapsed",
                                key="preview_first_500_area"
                            )

                        with text_tab2:
                            st.caption("Preview of the end of the document")
                            if result['preview_last_500']:
                                st.text_area(
                                    "Last 500 characters",
                                    value=result['preview_last_500'],
                                    height=300,
                                    label_visibility="collapsed",
                                    key="preview_last_500_area"
                                )
                            else:
                                st.info("Document is less than 500 characters")

                        with text_tab3:
                            st.caption(f"Complete extracted text - {len(result['full_text']):,} characters")
                            
                            # Add search functionality
                            search_term = st.text_input(
                                "🔍 Search in text (optional):", 
                                key="search_preview",
                                placeholder="Enter text to search..."
                            )
                            
                            if search_term:
                                # Count occurrences
                                count = result['full_text'].lower().count(search_term.lower())
                                st.caption(f"Found {count} occurrence(s) of '{search_term}'")
                                
                                # Highlight search term
                                import re
                                # Case-insensitive replacement with markers
                                highlighted_text = re.sub(
                                    f'({re.escape(search_term)})',
                                    r'>>> \1 <<<',
                                    result['full_text'],
                                    flags=re.IGNORECASE
                                )
                                st.text_area(
                                    "Full text with search results",
                                    value=highlighted_text,
                                    height=500,
                                    label_visibility="collapsed",
                                    key="preview_full_highlighted"
                                )
                            else:
                                st.text_area(
                                    "Full text",
                                    value=result['full_text'],
                                    height=500,
                                    label_visibility="collapsed",
                                    key="preview_full_text_area"
                                )
                        
                    else:
                        error_detail = response.json().get('detail', 'Unknown error')
                        st.error(f"❌ Error: {error_detail}")
                
                except Exception as e:
                    st.error(f"❌ Error previewing file: {str(e)}")
                    import traceback
                    with st.expander("🐛 Debug Info"):
                        st.code(traceback.format_exc())

# ============================================================================
# Footer
# ============================================================================

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        Made with ❤️ using Claude, FastAPI, and Streamlit<br>
        Study Buddy v1.0 | Powered by AI
    </div>
    """,
    unsafe_allow_html=True
)
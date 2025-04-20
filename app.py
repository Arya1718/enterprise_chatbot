import streamlit as st
import os
import time  # Added this import
from chatbot import get_response_from_rag
from document_handler import extract_text_from_pdf, summarize_text, extract_keywords, save_extracted_text
from utils import load_bad_words, clean_input

# Load profanity list once
bad_words = load_bad_words()

# UI Configuration
st.set_page_config(
    page_title="Enterprise Assistant",
    layout="wide",
    page_icon="🧠",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            padding: 10px 24px;
        }
        .stTextInput>div>div>input {
            padding: 12px;
            border-radius: 8px;
        }
        .stFileUploader>div>div>button {
            border-radius: 8px;
        }
        .stMarkdown h2 {
            border-bottom: 1px solid #e1e4e8;
            padding-bottom: 0.3em;
        }
        .stSuccess, .stInfo, .stWarning, .stError {
            border-radius: 8px;
            padding: 12px;
        }
        .chat-message {
            padding: 12px 16px;
            border-radius: 8px;
            margin: 8px 0;
            line-height: 1.6;
        }
        .user-message {
            background-color: #e3f2fd;
        }
        .bot-message {
            background-color: #f5f5f5;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar for document upload and info
with st.sidebar:
    st.title("📘 Enterprise Assistant")
    st.markdown("""
        <div style='margin-bottom: 20px;'>
            Upload documents to ask questions, extract insights, and summarize content.
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Document Upload")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        try:
            extracted_text = extract_text_from_pdf(uploaded_file)
            if extracted_text:
                st.success("PDF text extracted successfully!")
                save_extracted_text(extracted_text)
                st.session_state.doc_text = extracted_text
                st.session_state.file_name = uploaded_file.name
            else:
                st.error("Unable to extract text. The PDF might be scanned or unreadable.")
        except Exception as e:
            st.error(f"Error extracting PDF text: {e}")
    
    st.markdown("---")
    st.markdown("""
        <div style='font-size: small; color: #666;'>
            <p>This assistant uses RAG technology to provide answers based on your documents.</p>
            <p>All processing happens locally - your data remains private.</p>
        </div>
    """, unsafe_allow_html=True)

# Main content area
st.title("Document Analysis Center")

if "doc_text" in st.session_state and st.session_state.doc_text:
    # Document info header
    st.markdown(f"""
        <div style='background-color: #f8f9fa; padding: 16px; border-radius: 8px; margin-bottom: 24px;'>
            <h3 style='margin-top: 0;'>📄 Active Document: {st.session_state.file_name}</h3>
            <p style='margin-bottom: 0; color: #666;'>{len(st.session_state.doc_text.split())} words extracted</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Analysis tabs
    tab1, tab2, tab3 = st.tabs(["💬 Chat with Document", "🔍 Quick Analysis", "📊 Advanced Tools"])

    with tab1:
        st.subheader("Ask Questions About Your Document")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages from history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Accept user input
        if prompt := st.chat_input("Type your question here..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                try:
                    clean_query = clean_input(prompt, bad_words)
                    response = get_response_from_rag(clean_query, st.session_state.doc_text)
                    
                    # Simulate stream of response
                    for chunk in response.split():
                        full_response += chunk + " "
                        message_placeholder.markdown(full_response + "▌")
                        time.sleep(0.05)
                    message_placeholder.markdown(full_response)
                    
                except Exception as e:
                    st.error(f"Error generating response: {e}")
                    full_response = "Sorry, I encountered an error processing your request."
                    message_placeholder.markdown(full_response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})

    with tab2:
        st.subheader("Quick Document Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Key Takeaways")
            if st.button("Generate Summary", key="quick_summary"):
                with st.spinner("Analyzing document..."):
                    try:
                        summary = summarize_text(st.session_state.doc_text)
                        st.markdown(summary)
                    except Exception as e:
                        st.error(f"Failed to summarize text: {e}")
        
        with col2:
            st.markdown("#### Important Keywords")
            if st.button("Extract Keywords", key="quick_keywords"):
                with st.spinner("Identifying keywords..."):
                    try:
                        keywords = extract_keywords(st.session_state.doc_text)
                        st.markdown(", ".join(f"`{kw}`" for kw in keywords))
                    except Exception as e:
                        st.error(f"Failed to extract keywords: {e}")

    with tab3:
        st.subheader("Advanced Document Tools")
        
        with st.expander("📝 Detailed Summary", expanded=False):
            st.markdown("Generate a comprehensive summary of the document.")
            if st.button("Generate Detailed Summary"):
                with st.spinner("Creating detailed summary..."):
                    try:
                        summary = summarize_text(st.session_state.doc_text)
                        st.markdown(summary)
                    except Exception as e:
                        st.error(f"Failed to summarize text: {e}")
        
        with st.expander("🔎 Keyword Analysis", expanded=False):
            st.markdown("Get detailed keyword analysis with frequency and relevance.")
            if st.button("Run Advanced Keyword Analysis"):
                with st.spinner("Performing keyword analysis..."):
                    try:
                        keywords = extract_keywords(st.session_state.doc_text)
                        st.dataframe(keywords)
                    except Exception as e:
                        st.error(f"Failed to analyze keywords: {e}")
        
else:
    st.info("""
        **Welcome to the Enterprise Assistant!**  
        To get started, please upload a PDF document using the file uploader in the sidebar.
    """)
    
    # Placeholder for demo purposes
    st.image("https://via.placeholder.com/800x400?text=Upload+a+PDF+to+Begin", use_column_width=True)
    
    st.markdown("""
        <div style='margin-top: 32px;'>
            <h3>📌 How to use this assistant:</h3>
            <ol>
                <li>Upload a PDF document using the sidebar</li>
                <li>Ask questions about the document content</li>
                <li>Generate summaries and extract keywords</li>
                <li>Use advanced tools for deeper analysis</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)
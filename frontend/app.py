import streamlit as st
import requests
import json
from typing import List, Dict, Any
import os
from datetime import datetime

# Configure API settings
API_URL = "http://localhost:8000/api"
API_KEY = "development-key-123"

def check_api_connection() -> bool:
    """Check if the API is accessible."""
    try:
        response = requests.get(
            f"{API_URL}/health",
            headers={"X-API-Key": API_KEY}
        )
        return response.status_code == 200
    except:
        return False

def upload_documents(files: List[Any]) -> Dict[str, Any]:
    """Upload documents to the API."""
    try:
        files_to_upload = []
        for file in files:
            files_to_upload.append(("files", file))
        
        response = requests.post(
            f"{API_URL}/documents/upload",
            files=files_to_upload,
            headers={"X-API-Key": API_KEY}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error uploading documents: {str(e)}")
        return None

def delete_document(doc_id: str) -> bool:
    """Delete a document from the API."""
    try:
        response = requests.delete(
            f"{API_URL}/documents/{doc_id}",
            headers={"X-API-Key": API_KEY}
        )
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Error deleting document: {str(e)}")
        return False

def list_documents() -> List[Dict[str, Any]]:
    """List all documents from the API."""
    try:
        response = requests.get(
            f"{API_URL}/documents",
            headers={"X-API-Key": API_KEY}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error listing documents: {str(e)}")
        return []

def query_documents(query: str) -> Dict[str, Any]:
    """Query documents using the API."""
    try:
        response = requests.post(
            f"{API_URL}/query",
            json={"query": query},
            headers={"X-API-Key": API_KEY}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error querying documents: {str(e)}")
        return None

# Configure Streamlit page
st.set_page_config(
    page_title="Document Query System",
    page_icon="📚",
    layout="wide"
)

# Add title and description
st.title("Document Query System")
st.markdown("""
This application allows you to:
1. Upload documents (PDF, DOCX, TXT, JPG, PNG)
2. Query the documents using natural language
3. View and manage uploaded documents
""")

# Check API connection
if not check_api_connection():
    st.error("Could not connect to the API. Please make sure the backend server is running.")
    st.stop()

# Create tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["Upload Documents", "Query Documents", "Manage Documents"])

# Upload Documents Tab
with tab1:
    st.header("Upload Documents")
    uploaded_files = st.file_uploader(
        "Choose files to upload",
        type=["pdf", "docx", "txt", "jpg", "jpeg", "png"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.button("Upload"):
            with st.spinner("Uploading documents..."):
                result = upload_documents(uploaded_files)
                if result:
                    st.success(f"Successfully uploaded {len(result['results'])} files")
                    for file_result in result["results"]:
                        if file_result["status"] == "success":
                            st.info(f"File: {file_result['filename']}")
                            st.json(file_result["metadata"])
                        elif file_result["status"] == "processing":
                            st.warning(f"File: {file_result['filename']} is being processed")
                        else:
                            st.error(f"File: {file_result['filename']} - {file_result['message']}")

# Query Documents Tab
with tab2:
    st.header("Query Documents")
    query = st.text_area("Enter your query", height=100)
    
    if query:
        if st.button("Submit Query"):
            with st.spinner("Processing query..."):
                result = query_documents(query)
                if result:
                    st.markdown("### Answer")
                    st.write(result["answer"])

# Manage Documents Tab
with tab3:
    st.header("Manage Documents")
    
    # List documents
    documents = list_documents()
    if documents:
        st.subheader("Uploaded Documents")
        for doc in documents:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{doc['filename']}**")
                st.write(f"Type: {doc['file_type']}")
                st.write(f"Size: {doc['file_size']} bytes")
                st.write(f"Upload Date: {doc['upload_date']}")
                if doc.get('page_count'):
                    st.write(f"Pages: {doc['page_count']}")
                if doc.get('word_count'):
                    st.write(f"Words: {doc['word_count']}")
            with col2:
                if st.button("Delete", key=f"delete_{doc['filename']}"):
                    if delete_document(doc['filename']):
                        st.success(f"Deleted {doc['filename']}")
                        st.experimental_rerun()
    else:
        st.info("No documents uploaded yet.") 
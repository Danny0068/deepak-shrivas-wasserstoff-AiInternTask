import os
import logging
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import time

# Configure logging
logger = logging.getLogger(__name__)

# Configure ChromaDB client
CHROMA_DB_DIR = ".chroma"
os.makedirs(CHROMA_DB_DIR, exist_ok=True)

# Initialize ChromaDB client
client = chromadb.Client(
    Settings(
        persist_directory=CHROMA_DB_DIR,
        anonymized_telemetry=False,
        allow_reset=True
    )
)

# Initialize embedding function
try:
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2",
        device="cpu"
    )
except Exception as e:
    logger.error(f"Error initializing embedding function: {str(e)}")
    embedding_function = None

def get_chroma_collection(collection_name: str = "theme_docs"):
    """Get or create a ChromaDB collection."""
    try:
        # Try to get existing collection
        collection = client.get_collection(
            name=collection_name,
            embedding_function=embedding_function
        )
        logger.info(f"Retrieved existing collection: {collection_name}")
        return collection
    except Exception as e:
        # If collection doesn't exist or has issues, create new one
        try:
            # Delete existing collection if it exists
            try:
                client.delete_collection(collection_name)
                logger.info(f"Deleted existing collection: {collection_name}")
            except:
                pass
            
            # Create new collection
            collection = client.create_collection(
                name=collection_name,
                embedding_function=embedding_function
            )
            logger.info(f"Created new collection: {collection_name}")
            return collection
        except Exception as e:
            logger.error(f"Error creating collection: {str(e)}")
            raise

def add_to_vector_store(
    text: str,
    metadata: Dict[str, str],
    collection_name: str = "theme_docs"
) -> None:
    """Add text to the vector store."""
    try:
        collection = get_chroma_collection(collection_name)
        
        # Generate a unique ID for the document
        doc_id = f"{metadata.get('filename', '')}_{int(time.time())}"
        
        # Add document to collection
        collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )
        logger.info(f"Added document to collection: {doc_id}")
    except Exception as e:
        logger.error(f"Error adding to vector store: {str(e)}")
        raise

def query_vector_store(
    query: str,
    n_results: int = 5,
    collection_name: str = "theme_docs"
) -> List[Dict[str, Any]]:
    """Query the vector store."""
    try:
        collection = get_chroma_collection(collection_name)
        
        # Get actual number of documents
        doc_count = collection.count()
        if doc_count == 0:
            return []
        
        # Adjust n_results if needed
        n_results = min(n_results, doc_count)
        if n_results < 1:
            n_results = 1
        
        # Query collection
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results["documents"][0])):
            formatted_results.append({
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i] if "distances" in results else None
            })
        
        return formatted_results
    except Exception as e:
        logger.error(f"Error querying vector store: {str(e)}")
        raise

def delete_from_vector_store(
    doc_ids: List[str],
    collection_name: str = "theme_docs"
) -> None:
    """Delete documents from the vector store."""
    try:
        collection = get_chroma_collection(collection_name)
        collection.delete(ids=doc_ids)
        logger.info(f"Deleted documents from collection: {doc_ids}")
    except Exception as e:
        logger.error(f"Error deleting from vector store: {str(e)}")
        raise
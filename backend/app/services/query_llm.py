from app.services.embedding import generate_embeddings
from app.services.vector_store import get_chroma_collection, query_vector_store
from app.services.llm_handler import query_llm

import logging
from typing import List, Dict, Any, Tuple
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def retrieve_context(user_query: str, n_results: int = 5) -> Tuple[List[str], List[Dict[str, Any]]]:
    """Retrieve relevant context from the vector store."""
    try:
        logger.info(f"Retrieving context for query: {user_query}")
        results = query_vector_store(user_query, n_results)
        
        # Extract text and metadata from results
        context_chunks = [result['text'] for result in results]
        sources = [result['metadata'] for result in results]
        
        logger.info(f"Retrieved {len(context_chunks)} context chunks")
        return context_chunks, sources
        
    except Exception as e:
        logger.error(f"Error in retrieving context: {str(e)}", exc_info=True)
        raise


def format_sources(sources: list[tuple[str, str]]) -> str:
    """
    Create a formatted string of sources for citation display.
    """
    citations = []
    for doc, para in sources:
        citations.append(f"{doc}.pdf (Paragraph {para})")
    return "Sources:\n" + "\n".join(citations)


def answer_query_with_context(user_query: str, n_results: int = 5) -> Dict[str, Any]:
    """Answer a query using the retrieved context."""
    try:
        # Retrieve relevant context
        context_chunks, sources = retrieve_context(user_query, n_results)
        
        if not context_chunks:
            return {
                "query_type": "error",
                "answer": "No relevant context found to answer your query.",
                "citations": [],
                "processing_time": 0.0,
                "timestamp": datetime.now().isoformat()
            }
        
        # Format context for LLM
        formatted_context = "\n\n".join([
            f"[{i+1}] {chunk}\nSource: {source['filename']}"
            for i, (chunk, source) in enumerate(zip(context_chunks, sources))
        ])
        
        # TODO: Replace with actual LLM call
        # For now, return a simple response
        return {
            "query_type": "theme_analysis",
            "answer": f"Based on the provided context, here's what I found:\n\n{formatted_context}",
            "citations": [f"Source: {source['filename']}" for source in sources],
            "processing_time": 0.0,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in answer_query_with_context: {str(e)}", exc_info=True)
        raise

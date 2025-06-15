import logging
from typing import Optional, Dict, Any, List
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def query_llm(
    user_prompt: str,
    context: str = "",
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None
) -> str:
    """
    Simple LLM handler that returns a formatted response based on the context.
    
    Args:
        user_prompt: The user's query
        context: Context to include
        system_prompt: Optional system prompt
        temperature: Response temperature (0.0 to 1.0)
        max_tokens: Optional maximum tokens in response
    
    Returns:
        str: The formatted response
    """
    try:
        # Format the response based on the query type
        if "theme" in user_prompt.lower():
            response = {
                "query_type": "THEME_SEARCH",
                "answer": f"Based on the provided documents, here are the main themes:\n\n{context[:500]}...",
                "citations": ["(doc_1, 1)", "(doc_2, 1)"]
            }
        elif "file" in user_prompt.lower() or "document" in user_prompt.lower():
            response = {
                "query_type": "FILE_SEARCH",
                "answer": "The information can be found in the following documents:\n\n" + context[:500] + "...",
                "citations": ["(doc_1, 1)"]
            }
        else:
            response = {
                "query_type": "CONTENT_SEARCH",
                "answer": "Here's what I found in the documents:\n\n" + context[:500] + "...",
                "citations": ["(doc_1, 1)", "(doc_2, 1)"]
            }
        
        return json.dumps(response)
        
    except Exception as e:
        logger.error(f"Error in query_llm: {str(e)}", exc_info=True)
        raise

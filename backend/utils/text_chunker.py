"""
Text chunking utility for RAG.
Implements semantic chunking with overlap.
"""
import logging
import re

logger = logging.getLogger(__name__)

def chunk_text(text, chunk_size=1000, chunk_overlap=200):
    """
    Split text into chunks with overlap.
    
    Args:
        text: Text to chunk
        chunk_size: Target size of each chunk (characters)
        chunk_overlap: Number of characters to overlap between chunks
    
    Returns:
        List of text chunks
    """
    if not text or len(text) <= chunk_size:
        return [text] if text else []
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # Try to break at sentence boundary
        if end < len(text):
            # Look for sentence endings
            sentence_end = max(
                text.rfind('.', start, end),
                text.rfind('!', start, end),
                text.rfind('?', start, end),
                text.rfind('\n', start, end)
            )
            
            if sentence_end > start:
                end = sentence_end + 1
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # Move start position with overlap
        start = end - chunk_overlap
        if start < 0:
            start = 0
    
    logger.info(f"Chunked text into {len(chunks)} chunks")
    return chunks

def chunk_with_metadata(text, source, metadata=None, chunk_size=1000, chunk_overlap=200):
    """
    Chunk text and attach metadata.
    
    Returns:
        List of dicts with 'text', 'source', and metadata
    """
    chunks = chunk_text(text, chunk_size, chunk_overlap)
    
    result = []
    for i, chunk in enumerate(chunks):
        chunk_data = {
            'text': chunk,
            'source': source,
            'chunk_index': i,
            'total_chunks': len(chunks)
        }
        if metadata:
            chunk_data.update(metadata)
        result.append(chunk_data)
    
    return result


"""
RAG Engine - Retrieval Augmented Generation pipeline.
Handles content ingestion, vectorization, and semantic search.
"""
import logging
import numpy as np
import faiss
import os
import pickle
from backend.config import Config
from backend.services.llm_service import LLMService
from backend.utils.pdf_extractor import extract_pdf_from_url
from backend.utils.youtube_extractor import get_transcript, format_transcript_as_text
from backend.utils.text_chunker import chunk_with_metadata

logger = logging.getLogger(__name__)

class RAGEngine:
    """RAG engine for semantic search over ingested content"""
    
    def __init__(self):
        self.llm_service = LLMService()
        self.chunks = []
        self.index = None
        self.is_initialized = False
        self.vector_dim = 1536  # OpenAI embedding dimension
    
    def initialize(self):
        """Initialize RAG engine by ingesting all content sources"""
        logger.info("Initializing RAG engine...")
        
        all_chunks = []
        
        # Ingest PDFs (support multiple PDFs)
        pdf_urls = Config.PDF_URLS if hasattr(Config, 'PDF_URLS') and Config.PDF_URLS else []
        if not pdf_urls and hasattr(Config, 'PDF_URL') and Config.PDF_URL:
            # Backward compatibility
            pdf_urls = [Config.PDF_URL]
        
        for pdf_url in pdf_urls:
            if not pdf_url or not pdf_url.strip():
                continue
            try:
                logger.info(f"Ingesting PDF: {pdf_url}")
                pdf_pages = extract_pdf_from_url(pdf_url.strip())
                for page in pdf_pages:
                    page_chunks = chunk_with_metadata(
                        page['text'],
                        source=f'PDF: {pdf_url[:50]}...',
                        metadata={'page': page['page'], 'pdf_url': pdf_url},
                        chunk_size=Config.CHUNK_SIZE,
                        chunk_overlap=Config.CHUNK_OVERLAP
                    )
                    all_chunks.extend(page_chunks)
                logger.info(f"Ingested {len(pdf_pages)} pages from PDF")
            except Exception as e:
                logger.error(f"Failed to ingest PDF {pdf_url}: {e}")
        
        # Ingest YouTube videos
        video_urls = Config.YOUTUBE_VIDEOS if hasattr(Config, 'YOUTUBE_VIDEOS') and Config.YOUTUBE_VIDEOS else []
        for video_url in video_urls:
            if not video_url or not video_url.strip():
                continue
            try:
                logger.info(f"Ingesting video: {video_url}")
                transcript, video_id = get_transcript(video_url.strip())
                transcript_text = format_transcript_as_text(transcript)
                
                video_chunks = chunk_with_metadata(
                    transcript_text,
                    source=f'Video: {video_id}',
                    metadata={'video_url': video_url, 'video_id': video_id},
                    chunk_size=Config.CHUNK_SIZE,
                    chunk_overlap=Config.CHUNK_OVERLAP
                )
                all_chunks.extend(video_chunks)
                logger.info(f"Ingested video {video_id}: {len(video_chunks)} chunks")
            except Exception as e:
                logger.error(f"Failed to ingest video {video_url}: {e}")
        
        if not all_chunks:
            raise ValueError("No content was successfully ingested")
        
        self.chunks = all_chunks
        logger.info(f"Total chunks: {len(self.chunks)}")
        
        # Generate embeddings
        logger.info("Generating embeddings...")
        texts = [chunk['text'] for chunk in self.chunks]
        embeddings = self.llm_service.generate_embeddings(texts)
        
        # Build FAISS index
        logger.info("Building vector index...")
        embeddings_array = np.array(embeddings).astype('float32')
        
        # Use L2 distance (Euclidean)
        self.index = faiss.IndexFlatL2(self.vector_dim)
        self.index.add(embeddings_array)
        
        self.is_initialized = True
        logger.info("RAG engine initialized successfully")
    
    def search(self, query, top_k=5):
        """
        Search for relevant chunks using semantic similarity.
        
        Args:
            query: Search query text
            top_k: Number of results to return
        
        Returns:
            List of relevant chunks with similarity scores
        """
        if not self.is_initialized:
            raise ValueError("RAG engine not initialized. Call initialize() first.")
        
        # Generate query embedding
        query_embedding = self.llm_service.generate_embeddings([query])[0]
        query_vector = np.array([query_embedding]).astype('float32')
        
        # Search
        distances, indices = self.index.search(query_vector, top_k)
        
        # Format results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.chunks):
                chunk = self.chunks[idx].copy()
                # Convert L2 distance to similarity score (lower distance = higher similarity)
                similarity = 1 / (1 + distances[0][i])
                chunk['similarity'] = float(similarity)
                
                # Filter by similarity threshold
                if similarity >= Config.SIMILARITY_THRESHOLD:
                    results.append(chunk)
        
        return results
    
    def save_index(self, filepath='backend/data/rag_index.pkl'):
        """Save the RAG index to disk"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump({
                'chunks': self.chunks,
                'index': self.index
            }, f)
        logger.info(f"Saved RAG index to {filepath}")
    
    def load_index(self, filepath='backend/data/rag_index.pkl'):
        """Load the RAG index from disk"""
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
                self.chunks = data['chunks']
                self.index = data['index']
                self.is_initialized = True
            logger.info(f"Loaded RAG index from {filepath}")
        else:
            logger.warning(f"Index file not found: {filepath}")


"""
LLM Service - Abstracts OpenAI and Gemini APIs.
Provides unified interface for text generation.
"""
import logging
from openai import OpenAI
import google.generativeai as genai
from backend.config import Config

logger = logging.getLogger(__name__)

class LLMService:
    """Service for interacting with LLM providers"""
    
    def __init__(self):
        self.provider = Config.LLM_PROVIDER
        
        if self.provider == 'openai':
            if not Config.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not set")
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
            self.model = Config.OPENAI_MODEL
        elif self.provider == 'gemini':
            if not Config.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY not set")
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def generate_response(self, system_prompt, user_message, context=None, max_tokens=1000):
        """
        Generate a response from the LLM.
        
        Args:
            system_prompt: System prompt defining the AI's role
            user_message: User's message/question
            context: Optional context to include
            max_tokens: Maximum tokens in response
        
        Returns:
            Generated response text
        """
        try:
            if self.provider == 'openai':
                return self._generate_openai(system_prompt, user_message, context, max_tokens)
            elif self.provider == 'gemini':
                return self._generate_gemini(system_prompt, user_message, context, max_tokens)
        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            raise
    
    def _generate_openai(self, system_prompt, user_message, context, max_tokens):
        """Generate response using OpenAI"""
        messages = [
            {'role': 'system', 'content': system_prompt}
        ]
        
        if context:
            user_content = f"Context:\n{context}\n\nQuestion: {user_message}"
        else:
            user_content = user_message
        
        messages.append({'role': 'user', 'content': user_content})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def _generate_gemini(self, system_prompt, user_message, context, max_tokens):
        """Generate response using Gemini"""
        prompt = f"{system_prompt}\n\n"
        
        if context:
            prompt += f"Context:\n{context}\n\n"
        
        prompt += f"Question: {user_message}"
        
        response = self.model.generate_content(
            prompt,
            generation_config={
                'max_output_tokens': max_tokens,
                'temperature': 0.7
            }
        )
        
        return response.text
    
    def generate_embeddings(self, texts):
        """
        Generate embeddings for texts.
        Currently only supports OpenAI embeddings.
        """
        if self.provider == 'openai':
            response = self.client.embeddings.create(
                model=Config.OPENAI_EMBEDDING_MODEL,
                input=texts
            )
            return [item.embedding for item in response.data]
        else:
            # For Gemini, would need to use a different embedding model
            # For now, fallback to OpenAI embeddings
            if not Config.OPENAI_API_KEY:
                raise ValueError("Embeddings require OpenAI API key")
            client = OpenAI(api_key=Config.OPENAI_API_KEY)
            response = client.embeddings.create(
                model=Config.OPENAI_EMBEDDING_MODEL,
                input=texts
            )
            return [item.embedding for item in response.data]


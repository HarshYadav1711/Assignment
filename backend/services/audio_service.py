"""
Audio Service - Handles two-person dialogue generation with TTS.
Manages turn-based conversation flow and audio file generation.
"""
import logging
import os
import uuid
from openai import OpenAI
from backend.config import Config
from backend.services.llm_service import LLMService

logger = logging.getLogger(__name__)

class AudioService:
    """Service for generating audio dialogues"""
    
    def __init__(self):
        self.llm_service = LLMService()
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY) if Config.OPENAI_API_KEY else None
        self.dialogues = {}  # In-memory storage for dialogues
        self.audio_dir = Config.AUDIO_OUTPUT_DIR
        os.makedirs(self.audio_dir, exist_ok=True)
    
    def create_dialogue(self, topic, teacher_message, student_message, session_id=None):
        """
        Create a new dialogue session.
        
        Returns:
            dialogue_id: Unique identifier for the dialogue
        """
        dialogue_id = str(uuid.uuid4())
        
        dialogue_state = {
            'id': dialogue_id,
            'topic': topic,
            'session_id': session_id,
            'turns': [
                {'speaker': 'teacher', 'message': teacher_message},
                {'speaker': 'student', 'message': student_message}
            ],
            'current_turn': 0,
            'state': 'active'
        }
        
        self.dialogues[dialogue_id] = dialogue_state
        
        # Generate audio for initial messages
        self._generate_audio(dialogue_id, 'teacher', teacher_message)
        self._generate_audio(dialogue_id, 'student', student_message)
        
        return dialogue_id
    
    def continue_dialogue(self, dialogue_id, user_question=None):
        """
        Continue the dialogue with the next turn.
        
        Args:
            dialogue_id: Dialogue identifier
            user_question: Optional user question to inject
        
        Returns:
            Dict with speaker, message, and audio_url
        """
        if dialogue_id not in self.dialogues:
            raise ValueError(f"Dialogue {dialogue_id} not found")
        
        dialogue = self.dialogues[dialogue_id]
        
        if dialogue['state'] != 'active':
            raise ValueError(f"Dialogue {dialogue_id} is not active")
        
        # Determine next speaker (alternate between teacher and student)
        last_turn = dialogue['turns'][-1]
        next_speaker = 'student' if last_turn['speaker'] == 'teacher' else 'teacher'
        
        # Generate next message
        if user_question and next_speaker == 'student':
            # User injected a question, use it
            next_message = user_question
        else:
            # Generate AI response
            context = self._build_context(dialogue)
            
            if next_speaker == 'teacher':
                system_prompt = Config.TEACHER_SYSTEM_PROMPT
                user_prompt = f"Continue the conversation. Last student question: {last_turn['message']}"
            else:
                system_prompt = Config.STUDENT_SYSTEM_PROMPT
                user_prompt = f"Ask a follow-up question based on: {last_turn['message']}"
            
            next_message = self.llm_service.generate_response(
                system_prompt=system_prompt,
                user_message=user_prompt,
                context=context,
                max_tokens=300
            )
        
        # Add turn to dialogue
        dialogue['turns'].append({
            'speaker': next_speaker,
            'message': next_message
        })
        dialogue['current_turn'] = len(dialogue['turns']) - 1
        
        # Generate audio
        audio_url = self._generate_audio(dialogue_id, next_speaker, next_message)
        
        return {
            'speaker': next_speaker,
            'message': next_message,
            'audio_url': audio_url,
            'turn_number': dialogue['current_turn']
        }
    
    def _generate_audio(self, dialogue_id, speaker, text):
        """
        Generate audio file for a message.
        
        Returns:
            audio_url: URL path to the audio file
        """
        if not self.client:
            logger.warning("OpenAI client not available, skipping audio generation")
            return None
        
        # Select voice based on speaker
        voice = Config.TEACHER_VOICE if speaker == 'teacher' else Config.STUDENT_VOICE
        
        try:
            # Generate speech
            response = self.client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )
            
            # Save audio file
            audio_filename = f"{dialogue_id}_{speaker}_{len(self.dialogues.get(dialogue_id, {}).get('turns', []))}.mp3"
            audio_path = os.path.join(self.audio_dir, audio_filename)
            
            response.stream_to_file(audio_path)
            
            audio_url = f"/api/audio/{audio_filename}"
            logger.info(f"Generated audio: {audio_url}")
            
            return audio_url
        
        except Exception as e:
            logger.error(f"Failed to generate audio: {e}")
            return None
    
    def _build_context(self, dialogue):
        """Build context string from dialogue history"""
        # Get last few turns for context
        recent_turns = dialogue['turns'][-3:]
        context_parts = [f"{turn['speaker'].title()}: {turn['message']}" for turn in recent_turns]
        return "\n".join(context_parts)
    
    def get_audio_path(self, audio_id):
        """Get file path for an audio ID"""
        return os.path.join(self.audio_dir, audio_id)
    
    def pause_dialogue(self, dialogue_id):
        """Pause a dialogue"""
        if dialogue_id in self.dialogues:
            self.dialogues[dialogue_id]['state'] = 'paused'
    
    def resume_dialogue(self, dialogue_id):
        """Resume a paused dialogue"""
        if dialogue_id in self.dialogues:
            self.dialogues[dialogue_id]['state'] = 'active'


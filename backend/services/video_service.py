"""
Video Service - Generates AI video summaries.
Creates explainer videos with slides and voice-over.
"""
import logging
import os
import uuid
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, TextClip
from backend.config import Config
from backend.services.llm_service import LLMService
from backend.services.audio_service import AudioService

logger = logging.getLogger(__name__)

class VideoService:
    """Service for generating video summaries"""
    
    def __init__(self):
        self.llm_service = LLMService()
        self.audio_service = AudioService()
        self.video_dir = Config.VIDEO_OUTPUT_DIR
        self.summaries = {}  # In-memory storage
        os.makedirs(self.video_dir, exist_ok=True)
    
    def generate_summary(self, topic, content, video_type='concept'):
        """
        Generate a video summary for a topic.
        
        Args:
            topic: Topic name
            content: Content to summarize
            video_type: Type of video (concept, exam_tips, definition)
        
        Returns:
            (video_id, video_url) tuple
        """
        video_id = str(uuid.uuid4())
        
        try:
            # Generate script based on type
            script = self._generate_script(topic, content, video_type)
            
            # Create slides
            slides = self._create_slides(topic, script, video_type)
            
            # Generate narration audio
            audio_path = self._generate_narration(script)
            
            # Combine into video
            video_path = self._create_video(slides, audio_path, video_id)
            
            # Store summary metadata
            self.summaries[video_id] = {
                'id': video_id,
                'topic': topic,
                'type': video_type,
                'video_url': f"/api/video/{video_id}",
                'created_at': str(uuid.uuid4())  # Placeholder
            }
            
            return video_id, f"/api/video/{video_id}"
        
        except Exception as e:
            logger.error(f"Failed to generate video: {e}")
            raise
    
    def _generate_script(self, topic, content, video_type):
        """Generate video script using LLM"""
        if video_type == 'exam_tips':
            prompt = f"Create a concise script for exam tips about: {topic}\n\nContent: {content}\n\nFormat as bullet points suitable for narration."
        elif video_type == 'definition':
            prompt = f"Create a concise script defining: {topic}\n\nContent: {content}\n\nKeep it short and clear."
        else:  # concept
            prompt = f"Create a concise educational script explaining: {topic}\n\nContent: {content}\n\nBreak it into 3-5 key points."
        
        script = self.llm_service.generate_response(
            system_prompt="You are a video script writer. Create clear, concise scripts for educational videos.",
            user_message=prompt,
            context=content,
            max_tokens=500
        )
        
        return script
    
    def _create_slides(self, topic, script, video_type):
        """Create image slides for the video"""
        # Split script into sentences for slides
        sentences = [s.strip() for s in script.split('.') if s.strip()]
        slides = []
        
        # Create title slide
        title_slide = self._create_slide_image(
            title=topic,
            subtitle=f"{video_type.replace('_', ' ').title()}",
            is_title=True
        )
        slides.append(('title', title_slide))
        
        # Create content slides
        for i, sentence in enumerate(sentences[:5]):  # Limit to 5 slides
            slide = self._create_slide_image(
                title=f"Point {i+1}",
                subtitle=sentence[:100] + "..." if len(sentence) > 100 else sentence
            )
            slides.append((f'slide_{i+1}', slide))
        
        return slides
    
    def _create_slide_image(self, title, subtitle, is_title=False):
        """Create a single slide image"""
        width, height = 1920, 1080
        img = Image.new('RGB', (width, height), color='#1a1a2e')
        draw = ImageDraw.Draw(img)
        
        try:
            # Try to use a nice font
            title_font = ImageFont.truetype("arial.ttf", 80 if is_title else 60)
            subtitle_font = ImageFont.truetype("arial.ttf", 40)
        except:
            # Fallback to default font
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
        
        # Draw title
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (width - title_width) // 2
        title_y = height // 3
        
        draw.text((title_x, title_y), title, fill='#ffffff', font=title_font)
        
        # Draw subtitle
        if subtitle:
            # Word wrap subtitle
            words = subtitle.split()
            lines = []
            current_line = []
            for word in words:
                test_line = ' '.join(current_line + [word])
                bbox = draw.textbbox((0, 0), test_line, font=subtitle_font)
                if bbox[2] - bbox[0] < width - 200:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(' '.join(current_line))
            
            subtitle_y = title_y + 150
            for line in lines[:3]:  # Max 3 lines
                line_bbox = draw.textbbox((0, 0), line, font=subtitle_font)
                line_width = line_bbox[2] - line_bbox[0]
                line_x = (width - line_width) // 2
                draw.text((line_x, subtitle_y), line, fill='#a0a0a0', font=subtitle_font)
                subtitle_y += 60
        
        # Save slide
        slide_path = os.path.join(self.video_dir, f"slide_{uuid.uuid4()}.png")
        img.save(slide_path)
        
        return slide_path
    
    def _generate_narration(self, script):
        """Generate narration audio for the script"""
        # Use audio service to generate TTS
        temp_dialogue_id = str(uuid.uuid4())
        audio_url = self.audio_service._generate_audio(temp_dialogue_id, 'teacher', script)
        
        if audio_url:
            audio_path = self.audio_service.get_audio_path(audio_url.split('/')[-1])
            return audio_path
        else:
            # Fallback: create silent audio
            logger.warning("Could not generate narration, using silent audio")
            return None
    
    def _create_video(self, slides, audio_path, video_id):
        """Combine slides and audio into video"""
        try:
            clips = []
            duration_per_slide = 3  # seconds per slide
            
            for slide_name, slide_path in slides:
                clip = ImageClip(slide_path, duration=duration_per_slide)
                clips.append(clip)
            
            # Concatenate all clips
            video = CompositeVideoClip(clips, method='chain')
            
            # Add audio if available
            if audio_path and os.path.exists(audio_path):
                audio = AudioFileClip(audio_path)
                # Adjust video duration to match audio
                if audio.duration > video.duration:
                    # Extend last slide
                    last_clip = clips[-1]
                    extended_last = last_clip.set_duration(audio.duration - sum(c.duration for c in clips[:-1]))
                    clips[-1] = extended_last
                    video = CompositeVideoClip(clips, method='chain')
                video = video.set_audio(audio)
            
            # Write video file
            video_path = os.path.join(self.video_dir, f"{video_id}.mp4")
            video.write_videofile(video_path, fps=24, codec='libx264', audio_codec='aac', verbose=False, logger=None)
            
            # Cleanup slide images
            for _, slide_path in slides:
                if os.path.exists(slide_path):
                    os.remove(slide_path)
            
            return video_path
        
        except Exception as e:
            logger.error(f"Failed to create video: {e}")
            raise
    
    def list_summaries(self):
        """List all generated video summaries"""
        return list(self.summaries.values())
    
    def get_video_path(self, video_id):
        """Get file path for a video ID"""
        return os.path.join(self.video_dir, f"{video_id}.mp4")


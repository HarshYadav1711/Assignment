"""
YouTube transcript extraction utility.
Fetches transcripts from YouTube videos.
"""
import logging
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)

def extract_video_id(url):
    """
    Extract video ID from YouTube URL.
    Supports various YouTube URL formats.
    """
    try:
        # Handle youtu.be format
        if 'youtu.be' in url:
            return url.split('youtu.be/')[-1].split('?')[0]
        
        # Handle youtube.com format
        parsed = urlparse(url)
        if parsed.hostname in ['www.youtube.com', 'youtube.com']:
            if parsed.path == '/watch':
                return parse_qs(parsed.query)['v'][0]
            elif parsed.path.startswith('/embed/'):
                return parsed.path.split('/embed/')[-1]
        
        return None
    except Exception as e:
        logger.error(f"Failed to extract video ID: {e}")
        return None

def get_transcript(video_url):
    """
    Get transcript for a YouTube video.
    Returns: list of transcript entries with text and timestamps
    """
    try:
        video_id = extract_video_id(video_url)
        if not video_id:
            raise ValueError(f"Could not extract video ID from URL: {video_url}")
        
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Format transcript entries
        transcript = []
        for entry in transcript_list:
            transcript.append({
                'text': entry['text'],
                'start': entry['start'],
                'duration': entry.get('duration', 0)
            })
        
        logger.info(f"Extracted transcript for video {video_id}: {len(transcript)} entries")
        return transcript, video_id
    except Exception as e:
        logger.error(f"Failed to get transcript: {e}")
        # Try to get transcript in a different language
        try:
            video_id = extract_video_id(video_url)
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en-US', 'en'])
            transcript = [{'text': e['text'], 'start': e['start'], 'duration': e.get('duration', 0)} 
                         for e in transcript_list]
            return transcript, video_id
        except:
            raise

def format_transcript_as_text(transcript):
    """
    Format transcript entries as continuous text.
    """
    return ' '.join([entry['text'] for entry in transcript])


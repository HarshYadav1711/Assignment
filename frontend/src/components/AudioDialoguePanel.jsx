import React, { useState, useRef } from 'react';
import { FaPlay, FaPause, FaStop, FaMicrophone } from 'react-icons/fa';
import api from '../services/api';
import './AudioDialoguePanel.css';

function AudioDialoguePanel() {
  const [dialogue, setDialogue] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTurn, setCurrentTurn] = useState(0);
  const [topic, setTopic] = useState('');
  const [loading, setLoading] = useState(false);
  const audioRef = useRef(null);

  const startDialogue = async () => {
    if (!topic.trim() || loading) return;

    setLoading(true);
    try {
      const response = await api.startDialogue(topic.trim());
      setDialogue({
        id: response.dialogue_id,
        turns: [
          { speaker: 'teacher', message: response.initial_message },
          { speaker: 'student', message: response.student_question }
        ],
        currentTurn: 0
      });
      setCurrentTurn(0);
    } catch (error) {
      console.error('Failed to start dialogue:', error);
      alert('Failed to start dialogue. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const continueDialogue = async () => {
    if (!dialogue || loading) return;

    setLoading(true);
    try {
      const response = await api.continueDialogue(dialogue.id);
      
      setDialogue(prev => ({
        ...prev,
        turns: [...prev.turns, {
          speaker: response.speaker,
          message: response.message
        }],
        currentTurn: response.turn_number
      }));
      
      setCurrentTurn(response.turn_number);
    } catch (error) {
      console.error('Failed to continue dialogue:', error);
    } finally {
      setLoading(false);
    }
  };

  const playAudio = (audioUrl) => {
    if (audioRef.current) {
      audioRef.current.pause();
    }
    
    const audio = new Audio(`http://localhost:5000${audioUrl}`);
    audioRef.current = audio;
    audio.play();
    setIsPlaying(true);
    
    audio.onended = () => {
      setIsPlaying(false);
    };
    
    audio.onerror = () => {
      setIsPlaying(false);
      console.error('Audio playback failed');
    };
  };

  const pauseAudio = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      setIsPlaying(false);
    }
  };

  const stopDialogue = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current = null;
    }
    setIsPlaying(false);
    setDialogue(null);
    setCurrentTurn(0);
  };

  return (
    <div className="audio-dialogue-panel">
      <div className="card">
        <h2 className="card-title">🎙️ Two-Person Audio Dialogue</h2>
        <p className="card-description">
          Start a conversation between a teacher and student about any topic from your study materials.
          The AI will generate natural dialogue with distinct voices.
        </p>

        <div className="topic-input-section">
          <input
            type="text"
            className="input"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="Enter a topic from your study materials (e.g., 'photosynthesis', 'quantum mechanics', 'Shakespeare')"
            disabled={loading || dialogue}
            onKeyPress={(e) => e.key === 'Enter' && startDialogue()}
          />
          <button
            className="btn btn-primary"
            onClick={startDialogue}
            disabled={loading || !topic.trim() || dialogue}
          >
            Start Dialogue
          </button>
        </div>
      </div>

      {dialogue && (
        <div className="card">
          <div className="dialogue-header">
            <h3>Dialogue: {topic || 'Study Discussion'}</h3>
            <button className="btn btn-secondary" onClick={stopDialogue}>
              <FaStop /> Stop
            </button>
          </div>

          <div className="dialogue-turns">
            {dialogue.turns.map((turn, index) => (
              <div key={index} className={`dialogue-turn ${turn.speaker}`}>
                <div className="turn-header">
                  <span className="speaker-badge">{turn.speaker === 'teacher' ? '👨‍🏫 Teacher' : '👨‍🎓 Student'}</span>
                  {turn.audio_url && (
                    <button
                      className="play-audio-btn"
                      onClick={() => {
                        if (isPlaying && audioRef.current) {
                          pauseAudio();
                        } else {
                          playAudio(turn.audio_url);
                        }
                      }}
                    >
                      {isPlaying ? <FaPause /> : <FaPlay />}
                    </button>
                  )}
                </div>
                <div className="turn-message">{turn.message}</div>
              </div>
            ))}
          </div>

          <div className="dialogue-controls">
            <button
              className="btn btn-primary"
              onClick={continueDialogue}
              disabled={loading}
            >
              {loading ? 'Generating...' : 'Continue Conversation'}
            </button>
          </div>
        </div>
      )}

      {loading && !dialogue && (
        <div className="card">
          <div className="loading-state">
            <div className="loading-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <p>Generating dialogue...</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default AudioDialoguePanel;


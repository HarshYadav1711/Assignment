import React, { useState, useEffect } from 'react';
import { FaPlay, FaDownload, FaSpinner } from 'react-icons/fa';
import api from '../services/api';
import './VideoGallery.css';

function VideoGallery() {
  const [summaries, setSummaries] = useState([]);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [topic, setTopic] = useState('');
  const [videoType, setVideoType] = useState('concept');

  useEffect(() => {
    loadSummaries();
  }, []);

  const loadSummaries = async () => {
    setLoading(true);
    try {
      const response = await api.listVideoSummaries();
      setSummaries(response.summaries || []);
    } catch (error) {
      console.error('Failed to load summaries:', error);
    } finally {
      setLoading(false);
    }
  };

  const generateVideo = async () => {
    if (!topic.trim() || generating) return;

    setGenerating(true);
    try {
      const response = await api.generateVideo(topic.trim(), videoType);
      await loadSummaries(); // Reload list
      setTopic('');
    } catch (error) {
      console.error('Failed to generate video:', error);
      alert('Failed to generate video. Please try again.');
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="video-gallery">
      <div className="card">
        <h2 className="card-title">🎥 AI Video Summaries</h2>
        <p className="card-description">
          Generate short explainer videos for any concepts, exam tips, or definitions from your study materials.
        </p>

        <div className="video-generator">
          <div className="generator-inputs">
            <input
              type="text"
              className="input"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="Enter a topic from your study materials (e.g., 'photosynthesis', 'derivatives', 'World War II')"
              disabled={generating}
              onKeyPress={(e) => e.key === 'Enter' && generateVideo()}
            />
            <select
              className="input"
              value={videoType}
              onChange={(e) => setVideoType(e.target.value)}
              disabled={generating}
            >
              <option value="concept">Concept Explanation</option>
              <option value="exam_tips">Exam Tips</option>
              <option value="definition">Definition</option>
            </select>
            <button
              className="btn btn-primary"
              onClick={generateVideo}
              disabled={generating || !topic.trim()}
            >
              {generating ? (
                <>
                  <FaSpinner className="spinner" /> Generating...
                </>
              ) : (
                'Generate Video'
              )}
            </button>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="card">
          <div className="loading-state">
            <div className="loading-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <p>Loading videos...</p>
          </div>
        </div>
      ) : summaries.length === 0 ? (
        <div className="card">
          <div className="empty-state">
            <p>No videos generated yet. Create your first video above!</p>
          </div>
        </div>
      ) : (
        <div className="video-grid">
          {summaries.map((summary) => (
            <div key={summary.id} className="video-card">
              <div className="video-card-header">
                <h3>{summary.topic || 'Study Topic'}</h3>
                <span className="video-type-badge">{summary.type || 'concept'}</span>
              </div>
              <div className="video-card-content">
                <p className="video-description">
                  {summary.type === 'exam_tips' && '📝 Exam Tips'}
                  {summary.type === 'definition' && '📖 Definition'}
                  {summary.type === 'concept' && '💡 Concept Explanation'}
                </p>
              </div>
              <div className="video-card-actions">
                <a
                  href={`http://localhost:5000${summary.video_url}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-primary"
                >
                  <FaPlay /> Watch
                </a>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default VideoGallery;


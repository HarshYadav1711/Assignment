/**
 * API service for communicating with the Flask backend.
 */
import axios from 'axios';

// API base URL - set REACT_APP_API_URL in environment for production
// For local dev: http://localhost:5000/api
// For production: https://your-backend.railway.app/api
const API_BASE_URL = process.env.REACT_APP_API_URL || 'assignment-production-e519.up.railway.app';

const api = {
  /**
   * Send a chat message
   */
  async chat(message, sessionId = null, mode = 'normal') {
    const response = await axios.post(`${API_BASE_URL}/chat`, {
      message,
      session_id: sessionId,
      mode
    });
    return response.data;
  },

  /**
   * Start an audio dialogue
   */
  async startDialogue(topic, sessionId = null) {
    const response = await axios.post(`${API_BASE_URL}/audio/dialogue`, {
      topic,
      session_id: sessionId
    });
    return response.data;
  },

  /**
   * Continue an audio dialogue
   */
  async continueDialogue(dialogueId, userQuestion = null) {
    const response = await axios.post(`${API_BASE_URL}/audio/dialogue/${dialogueId}/next`, {
      user_question: userQuestion
    });
    return response.data;
  },

  /**
   * List video summaries
   */
  async listVideoSummaries() {
    const response = await axios.get(`${API_BASE_URL}/video/summaries`);
    return response.data;
  },

  /**
   * Generate a video summary
   */
  async generateVideo(topic, videoType = 'concept') {
    const response = await axios.post(`${API_BASE_URL}/video/generate`, {
      topic,
      type: videoType
    });
    return response.data;
  },

  /**
   * Health check
   */
  async healthCheck() {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  }
};

export default api;


/**
 * API service for communicating with the Flask backend.
 */
import axios from 'axios';

// API base URL - set REACT_APP_API_URL in environment for production
// For local dev: http://localhost:5000/api
// For production: https://your-backend.railway.app/api
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = {
  /**
   * Send a chat message
   */
  async chat(message, sessionId = null, mode = 'normal') {
    try {
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        message,
        session_id: sessionId,
        mode
      });
      return response.data;
    } catch (error) {
      // If backend returns an error response with a message, use it
      if (error.response?.data?.response) {
        return error.response.data;
      }
      // Otherwise, rethrow the error
      throw error;
    }
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
  },

  /**
   * List content sources
   */
  async listContentSources() {
    const response = await axios.get(`${API_BASE_URL}/content/sources`);
    return response.data;
  },

  /**
   * Add content source (URL-based)
   */
  async addContentSource(data) {
    const response = await axios.post(`${API_BASE_URL}/content/sources`, data);
    return response.data;
  },

  /**
   * Upload PDF file
   */
  async uploadPDF(formData) {
    const response = await axios.post(`${API_BASE_URL}/content/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  },

  /**
   * Delete content source
   */
  async deleteContentSource(sourceId) {
    const response = await axios.delete(`${API_BASE_URL}/content/sources/${sourceId}`);
    return response.data;
  }
};

export default api;


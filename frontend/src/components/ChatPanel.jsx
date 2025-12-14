import React, { useState, useRef, useEffect } from 'react';
import { FaPaperPlane, FaBook, FaGraduationCap, FaChild } from 'react-icons/fa';
import api from '../services/api';
import './ChatPanel.css';

function ChatPanel() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [mode, setMode] = useState('normal');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');
    setLoading(true);

    // Add user message to UI
    const newUserMessage = {
      id: Date.now(),
      role: 'user',
      content: userMessage,
      sources: [],
      mode
    };
    setMessages(prev => [...prev, newUserMessage]);

    try {
      const response = await api.chat(userMessage, sessionId, mode);
      
      const aiMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.response,
        sources: response.sources || [],
        mode
      };
      
      setMessages(prev => [...prev, aiMessage]);
      setSessionId(response.session_id);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        sources: [],
        mode
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chat-panel">
      <div className="mode-selector">
        <button
          className={`mode-btn ${mode === 'normal' ? 'active' : ''}`}
          onClick={() => setMode('normal')}
          title="Normal mode"
        >
          <FaBook /> Normal
        </button>
        <button
          className={`mode-btn ${mode === 'exam' ? 'active' : ''}`}
          onClick={() => setMode('exam')}
          title="Exam mode - concise, bullet-pointed answers"
        >
          <FaGraduationCap /> Exam Mode
        </button>
        <button
          className={`mode-btn ${mode === 'simple' ? 'active' : ''}`}
          onClick={() => setMode('simple')}
          title="Simple mode - explain like I'm 12"
        >
          <FaChild /> Simple Mode
        </button>
      </div>

      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="welcome-message">
            <h2>Welcome to AI Study Tool!</h2>
            <p>Ask me anything about the economics chapter. I'm grounded in the PDF and video materials.</p>
            <div className="example-questions">
              <p className="example-title">Try asking:</p>
              <ul>
                <li>"What is supply and demand?"</li>
                <li>"Explain market equilibrium"</li>
                <li>"What are the key exam points about inflation?"</li>
              </ul>
            </div>
          </div>
        )}
        
        {messages.map((msg) => (
          <div key={msg.id} className={`message ${msg.role}`}>
            <div className="message-content">
              {msg.content.split('\n').map((line, i) => (
                <p key={i}>{line}</p>
              ))}
              {msg.sources && msg.sources.length > 0 && (
                <div className="sources">
                  <span className="sources-label">Sources:</span>
                  {msg.sources.map((source, i) => (
                    <span key={i} className="source-badge">{source}</span>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        
        {loading && (
          <div className="message assistant">
            <div className="message-content">
              <div className="loading-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <input
          type="text"
          className="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask a question about economics..."
          disabled={loading}
        />
        <button
          className="send-button"
          onClick={sendMessage}
          disabled={loading || !input.trim()}
        >
          <FaPaperPlane />
        </button>
      </div>
    </div>
  );
}

export default ChatPanel;


import React, { useState } from 'react';
import './App.css';
import ChatPanel from './components/ChatPanel';
import AudioDialoguePanel from './components/AudioDialoguePanel';
import VideoGallery from './components/VideoGallery';
import ContentManager from './components/ContentManager';
import Header from './components/Header';

function App() {
  const [activeTab, setActiveTab] = useState('content');

  return (
    <div className="App">
      <Header />
      <div className="tab-container">
        <button
          className={`tab-button ${activeTab === 'content' ? 'active' : ''}`}
          onClick={() => setActiveTab('content')}
        >
          📚 My Materials
        </button>
        <button
          className={`tab-button ${activeTab === 'chat' ? 'active' : ''}`}
          onClick={() => setActiveTab('chat')}
        >
          💬 Chat
        </button>
        <button
          className={`tab-button ${activeTab === 'audio' ? 'active' : ''}`}
          onClick={() => setActiveTab('audio')}
        >
          🎙️ Audio Dialogue
        </button>
        <button
          className={`tab-button ${activeTab === 'videos' ? 'active' : ''}`}
          onClick={() => setActiveTab('videos')}
        >
          🎥 Video Summaries
        </button>
      </div>
      <div className="content-container">
        {activeTab === 'content' && <ContentManager />}
        {activeTab === 'chat' && <ChatPanel />}
        {activeTab === 'audio' && <AudioDialoguePanel />}
        {activeTab === 'videos' && <VideoGallery />}
      </div>
    </div>
  );
}

export default App;


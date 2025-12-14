import React, { useState, useEffect } from 'react';
import { FaPlus, FaTrash, FaFilePdf, FaYoutube, FaLink, FaUpload, FaSpinner } from 'react-icons/fa';
import api from '../services/api';
import './ContentManager.css';

function ContentManager() {
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [showAddForm, setShowAddForm] = useState(false);
  const [formType, setFormType] = useState('youtube'); // youtube, pdf_url, pdf_file
  const [formData, setFormData] = useState({
    url: '',
    title: '',
    description: ''
  });
  const [selectedFile, setSelectedFile] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    loadSources();
  }, []);

  const loadSources = async () => {
    setLoading(true);
    try {
      const response = await api.listContentSources();
      setSources(response.sources || []);
    } catch (error) {
      console.error('Failed to load sources:', error);
      setError('Failed to load content sources');
    } finally {
      setLoading(false);
    }
  };

  const handleAddSource = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setUploading(true);

    try {
      if (formType === 'pdf_file') {
        // File upload
        if (!selectedFile) {
          setError('Please select a PDF file');
          setUploading(false);
          return;
        }

        const formDataToSend = new FormData();
        formDataToSend.append('file', selectedFile);
        formDataToSend.append('title', formData.title || selectedFile.name);
        formDataToSend.append('description', formData.description);

        await api.uploadPDF(formDataToSend);
      } else {
        // URL-based source
        if (!formData.url.trim()) {
          setError('Please enter a URL');
          setUploading(false);
          return;
        }

        await api.addContentSource({
          type: formType,
          url: formData.url,
          title: formData.title || formData.url,
          description: formData.description
        });
      }

      setSuccess('Content source added successfully! The system is processing it...');
      setFormData({ url: '', title: '', description: '' });
      setSelectedFile(null);
      setShowAddForm(false);
      
      // Reload sources after a delay (to allow processing)
      setTimeout(() => {
        loadSources();
      }, 2000);
    } catch (error) {
      console.error('Failed to add source:', error);
      setError(error.response?.data?.error || 'Failed to add content source');
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteSource = async (sourceId) => {
    if (!window.confirm('Are you sure you want to remove this content source?')) {
      return;
    }

    try {
      await api.deleteContentSource(sourceId);
      setSuccess('Content source removed successfully!');
      loadSources();
    } catch (error) {
      console.error('Failed to delete source:', error);
      setError('Failed to remove content source');
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.type !== 'application/pdf') {
        setError('Please select a PDF file');
        return;
      }
      if (file.size > 50 * 1024 * 1024) { // 50MB limit
        setError('File size must be less than 50MB');
        return;
      }
      setSelectedFile(file);
      setError('');
    }
  };

  const getSourceIcon = (type) => {
    switch (type) {
      case 'pdf_url':
      case 'pdf_file':
        return <FaFilePdf />;
      case 'youtube':
        return <FaYoutube />;
      default:
        return <FaLink />;
    }
  };

  return (
    <div className="content-manager">
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">📚 Manage Your Study Materials</h2>
          <p className="card-description">
            Add PDFs and YouTube videos to create your personalized study knowledge base.
            Works with any subject - just add your materials!
          </p>
        </div>

        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}

        {success && (
          <div className="alert alert-success">
            {success}
          </div>
        )}

        <div className="sources-header">
          <h3>Your Content Sources ({sources.length})</h3>
          <button
            className="btn btn-primary"
            onClick={() => setShowAddForm(!showAddForm)}
          >
            <FaPlus /> Add Content
          </button>
        </div>

        {showAddForm && (
          <div className="add-source-form">
            <div className="form-tabs">
              <button
                className={`tab ${formType === 'youtube' ? 'active' : ''}`}
                onClick={() => setFormType('youtube')}
              >
                <FaYoutube /> YouTube Video
              </button>
              <button
                className={`tab ${formType === 'pdf_url' ? 'active' : ''}`}
                onClick={() => setFormType('pdf_url')}
              >
                <FaLink /> PDF URL
              </button>
              <button
                className={`tab ${formType === 'pdf_file' ? 'active' : ''}`}
                onClick={() => setFormType('pdf_file')}
              >
                <FaUpload /> Upload PDF
              </button>
            </div>

            <form onSubmit={handleAddSource}>
              {formType === 'pdf_file' ? (
                <div className="form-group">
                  <label>Select PDF File</label>
                  <div className="file-upload-area">
                    <input
                      type="file"
                      accept=".pdf"
                      onChange={handleFileSelect}
                      className="file-input"
                      id="pdf-upload"
                    />
                    <label htmlFor="pdf-upload" className="file-upload-label">
                      {selectedFile ? (
                        <span>📄 {selectedFile.name}</span>
                      ) : (
                        <span>Click to select PDF file</span>
                      )}
                    </label>
                  </div>
                  <small>Maximum file size: 50MB</small>
                </div>
              ) : (
                <div className="form-group">
                  <label>
                    {formType === 'youtube' ? 'YouTube Video URL' : 'PDF URL'}
                  </label>
                  <input
                    type="url"
                    className="input"
                    value={formData.url}
                    onChange={(e) => setFormData({ ...formData, url: e.target.value })}
                    placeholder={
                      formType === 'youtube'
                        ? 'https://youtu.be/VIDEO_ID or https://www.youtube.com/watch?v=VIDEO_ID'
                        : 'https://drive.google.com/file/d/FILE_ID/view or direct PDF URL'
                    }
                    required
                  />
                </div>
              )}

              <div className="form-group">
                <label>Title (Optional)</label>
                <input
                  type="text"
                  className="input"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  placeholder="Give it a name (e.g., 'Chapter 5 - Physics')"
                />
              </div>

              <div className="form-group">
                <label>Description (Optional)</label>
                <textarea
                  className="input"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  placeholder="Add a description..."
                  rows="3"
                />
              </div>

              <div className="form-actions">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => {
                    setShowAddForm(false);
                    setFormData({ url: '', title: '', description: '' });
                    setSelectedFile(null);
                    setError('');
                  }}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={uploading}
                >
                  {uploading ? (
                    <>
                      <FaSpinner className="spinner" /> Processing...
                    </>
                  ) : (
                    <>
                      <FaPlus /> Add Source
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        )}

        {loading ? (
          <div className="loading-state">
            <FaSpinner className="spinner" />
            <p>Loading content sources...</p>
          </div>
        ) : sources.length === 0 ? (
          <div className="empty-state">
            <p>No content sources yet. Add your first PDF or YouTube video above!</p>
          </div>
        ) : (
          <div className="sources-list">
            {sources.map((source) => (
              <div key={source.id} className="source-item">
                <div className="source-icon">
                  {getSourceIcon(source.source_type)}
                </div>
                <div className="source-info">
                  <h4>{source.title || 'Untitled'}</h4>
                  <p className="source-type">
                    {source.source_type === 'pdf_file' && '📄 Uploaded PDF'}
                    {source.source_type === 'pdf_url' && '🔗 PDF URL'}
                    {source.source_type === 'youtube' && '▶️ YouTube Video'}
                  </p>
                  {source.description && (
                    <p className="source-description">{source.description}</p>
                  )}
                  <p className="source-url">
                    {source.source_url || source.file_path}
                  </p>
                </div>
                <button
                  className="btn-icon"
                  onClick={() => handleDeleteSource(source.id)}
                  title="Remove"
                >
                  <FaTrash />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default ContentManager;


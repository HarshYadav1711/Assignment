#!/bin/bash
# Railway start script
# This script ensures the app starts correctly on Railway

# Change to backend directory
cd backend

# Start with gunicorn (Railway's preferred method for Flask)
# PORT is automatically set by Railway
exec gunicorn app:app --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 120


@echo off
REM Railway start script for Windows (local testing)
cd backend
gunicorn app:app --bind 0.0.0.0:5000 --workers 2 --timeout 120


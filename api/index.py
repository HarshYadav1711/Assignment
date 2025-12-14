"""
Vercel serverless function entry point.
Routes requests to appropriate handlers.
"""
from flask import Flask
from vercel import Vercel

# Import your Flask app
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import Flask app
from backend.app import app

# Create Vercel handler
vercel = Vercel(app)

# Export handler for Vercel
handler = vercel.handler


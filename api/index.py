"""
Vercel Serverless Function Entry Point for ANALYTIX
This module adapts the Flask app for Vercel's serverless environment.
"""

import sys
import os

# Add parent directory to path to import app module
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app

# Vercel serverless function handler
handler = app

# For local testing compatibility
if __name__ == "__main__":
    app.run(debug=True, port=5000)

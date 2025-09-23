#!/usr/bin/env python3
"""
WSGI Entry Point for Production Deployment
==========================================

This file serves as the entry point for production WSGI servers like Gunicorn.
It properly exports the SocketIO app instance for deployment on platforms like Render.
"""

import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the SocketIO app from web_ui
from web_ui import socketio, app

# Export the SocketIO app for Gunicorn
application = socketio

if __name__ == "__main__":
    # This allows the file to be run directly for testing
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
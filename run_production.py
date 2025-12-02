"""Production server runner using Waitress WSGI server

This script runs the API using Waitress, a production-ready WSGI server.
Waitress is cross-platform and works well on Windows, Linux, and Mac.

Usage:
    python run_production.py

To stop the server, press CTRL+C
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from waitress import serve
from src.api.app import create_app

if __name__ == '__main__':
    # Create app in production mode (debug=False)
    app = create_app(debug=False)
    
    print("=" * 60)
    print("Bookstore Management System API - Production Server")
    print("=" * 60)
    print("Server: Waitress WSGI Server")
    print("Mode: Production (Debug: OFF)")
    print("URL: http://0.0.0.0:5000")
    print("API Docs: http://localhost:5000/apidocs")
    print("Health: http://localhost:5000/health")
    print("=" * 60)
    print("\nDefault API Keys:")
    print("  - test-api-key-123 (admin)")
    print("  - demo-api-key-456 (user)")
    print("=" * 60)
    print("\nPress CTRL+C to stop the server")
    print("=" * 60)
    
    # Start Waitress server
    # threads=4 means 4 worker threads for handling requests
    # This is suitable for moderate traffic
    serve(app, host='0.0.0.0', port=5000, threads=4)


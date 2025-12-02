"""Authentication module for API key validation"""

from functools import wraps
from flask import request, jsonify


# Default API key for development
# In production, this should be stored securely (environment variable, database, etc.)
VALID_API_KEYS = {
    'test-api-key-123': 'admin',
    'demo-api-key-456': 'user'
}


def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({
                'error': 'API key is missing',
                'message': 'Please provide an API key in the X-API-Key header'
            }), 401
        
        if api_key not in VALID_API_KEYS:
            return jsonify({
                'error': 'Invalid API key',
                'message': 'The provided API key is not valid'
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated_function


def get_api_key_role(api_key: str) -> str:
    """Get the role associated with an API key"""
    return VALID_API_KEYS.get(api_key, 'unknown')


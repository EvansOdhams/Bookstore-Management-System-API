"""Main Flask Application"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
from src.api.routes.inventory import inventory_bp
from src.api.routes.sales import sales_bp
from src.api.routes.delivery import delivery_bp
from src.api.routes.integration import integration_bp


def create_app(debug=False):
    """Create and configure Flask application
    
    Args:
        debug: Enable debug mode (default: False for production)
    """
    app = Flask(__name__)
    app.config['DEBUG'] = debug
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
    app.register_blueprint(sales_bp, url_prefix='/api/sales')
    app.register_blueprint(delivery_bp, url_prefix='/api/delivery')
    app.register_blueprint(integration_bp, url_prefix='/api')
    
    # Swagger configuration
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Bookstore Management System API",
            "description": "A RESTful API that integrates Inventory, Sales, and Delivery systems",
            "version": "1.0.0",
            "contact": {
                "name": "API Support"
            }
        },
        "securityDefinitions": {
            "ApiKeyAuth": {
                "type": "apiKey",
                "name": "X-API-Key",
                "in": "header",
                "description": "API key for authentication"
            }
        },
        "security": [
            {
                "ApiKeyAuth": []
            }
        ]
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'service': 'Bookstore Management System API',
            'version': '1.0.0'
        }), 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        """Root endpoint with API information"""
        return jsonify({
            'message': 'Welcome to Bookstore Management System API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/health',
                'api_docs': '/apidocs',
                'inventory': '/api/inventory',
                'sales': '/api/sales',
                'delivery': '/api/delivery',
                'integration': '/api/orders'
            },
            'authentication': 'All endpoints require X-API-Key header'
        }), 200
    
    return app


if __name__ == '__main__':
    app = create_app()
    print("=" * 60)
    print("Bookstore Management System API")
    print("=" * 60)
    print("Server starting on http://localhost:5000")
    print("API Documentation: http://localhost:5000/apidocs")
    print("Health Check: http://localhost:5000/health")
    print("=" * 60)
    print("\nDefault API Keys:")
    print("  - test-api-key-123 (admin)")
    print("  - demo-api-key-456 (user)")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)


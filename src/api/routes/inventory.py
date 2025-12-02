"""Inventory System API Routes"""

from flask import Blueprint, jsonify, request
from src.api.auth import require_api_key
from src.services.inventory_service import InventoryService

inventory_bp = Blueprint('inventory', __name__)
inventory_service = InventoryService()


@inventory_bp.route('/books', methods=['GET'])
@require_api_key
def get_all_books():
    """
    Get all books in inventory
    ---
    tags:
      - Inventory
    parameters:
      - in: header
        name: X-API-Key
        required: true
        schema:
          type: string
        description: API key for authentication
    responses:
      200:
        description: List of all books
        schema:
          type: object
          properties:
            books:
              type: array
              items:
                type: object
      401:
        description: Unauthorized - Invalid or missing API key
    """
    books = inventory_service.get_all_books()
    return jsonify({
        'books': [book.to_dict() for book in books],
        'count': len(books)
    }), 200


@inventory_bp.route('/books/<book_id>', methods=['GET'])
@require_api_key
def get_book_by_id(book_id):
    """
    Get a specific book by ID
    ---
    tags:
      - Inventory
    parameters:
      - in: path
        name: book_id
        required: true
        schema:
          type: string
        description: Book ID
      - in: header
        name: X-API-Key
        required: true
        schema:
          type: string
    responses:
      200:
        description: Book details
      404:
        description: Book not found
      401:
        description: Unauthorized
    """
    book = inventory_service.get_book_by_id(book_id)
    if not book:
        return jsonify({
            'error': 'Book not found',
            'message': f'No book found with ID: {book_id}'
        }), 404
    
    return jsonify(book.to_dict()), 200


@inventory_bp.route('/books/<book_id>/stock', methods=['GET'])
@require_api_key
def check_stock(book_id):
    """
    Check stock availability for a book
    ---
    tags:
      - Inventory
    parameters:
      - in: path
        name: book_id
        required: true
        schema:
          type: string
      - in: query
        name: quantity
        schema:
          type: integer
          default: 1
        description: Quantity to check
      - in: header
        name: X-API-Key
        required: true
        schema:
          type: string
    responses:
      200:
        description: Stock availability information
      404:
        description: Book not found
    """
    quantity = request.args.get('quantity', 1, type=int)
    book = inventory_service.get_book_by_id(book_id)
    
    if not book:
        return jsonify({
            'error': 'Book not found',
            'message': f'No book found with ID: {book_id}'
        }), 404
    
    available = inventory_service.check_stock(book_id, quantity)
    
    return jsonify({
        'book_id': book_id,
        'book_title': book.title,
        'requested_quantity': quantity,
        'available_quantity': book.stock_quantity,
        'is_available': available
    }), 200


"""Sales System API Routes"""

from flask import Blueprint, jsonify, request
from src.api.auth import require_api_key
from src.services.sales_service import SalesService

sales_bp = Blueprint('sales', __name__)
sales_service = SalesService()


@sales_bp.route('/orders', methods=['GET'])
@require_api_key
def get_all_orders():
    """
    Get all orders
    ---
    tags:
      - Sales
    parameters:
      - in: header
        name: X-API-Key
        required: true
        schema:
          type: string
    responses:
      200:
        description: List of all orders
    """
    orders = sales_service.get_all_orders()
    return jsonify({
        'orders': [order.to_dict() for order in orders],
        'count': len(orders)
    }), 200


@sales_bp.route('/orders', methods=['POST'])
@require_api_key
def create_order():
    """
    Create a new order
    ---
    tags:
      - Sales
    parameters:
      - in: header
        name: X-API-Key
        required: true
        schema:
          type: string
      - in: body
        name: order
        required: true
        schema:
          type: object
          required:
            - customer_name
            - customer_email
            - items
          properties:
            customer_name:
              type: string
            customer_email:
              type: string
            items:
              type: array
              items:
                type: object
                properties:
                  book_id:
                    type: string
                  quantity:
                    type: integer
                  unit_price:
                    type: number
            shipping_address:
              type: string
    responses:
      201:
        description: Order created successfully
      400:
        description: Invalid request data
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'error': 'Invalid request',
            'message': 'Request body must be JSON'
        }), 400
    
    required_fields = ['customer_name', 'customer_email', 'items']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'error': 'Missing required field',
                'message': f'{field} is required'
            }), 400
    
    if not isinstance(data['items'], list) or len(data['items']) == 0:
        return jsonify({
            'error': 'Invalid items',
            'message': 'items must be a non-empty array'
        }), 400
    
    try:
        order = sales_service.create_order(
            customer_name=data['customer_name'],
            customer_email=data['customer_email'],
            items=data['items'],
            shipping_address=data.get('shipping_address')
        )
        
        return jsonify({
            'message': 'Order created successfully',
            'order': order.to_dict()
        }), 201
    except Exception as e:
        return jsonify({
            'error': 'Failed to create order',
            'message': str(e)
        }), 400


@sales_bp.route('/orders/<order_id>', methods=['GET'])
@require_api_key
def get_order_by_id(order_id):
    """
    Get an order by ID
    ---
    tags:
      - Sales
    parameters:
      - in: path
        name: order_id
        required: true
        schema:
          type: string
      - in: header
        name: X-API-Key
        required: true
        schema:
          type: string
    responses:
      200:
        description: Order details
      404:
        description: Order not found
    """
    order = sales_service.get_order_by_id(order_id)
    if not order:
        return jsonify({
            'error': 'Order not found',
            'message': f'No order found with ID: {order_id}'
        }), 404
    
    return jsonify(order.to_dict()), 200


@sales_bp.route('/orders/<order_id>/payment', methods=['POST'])
@require_api_key
def process_payment(order_id):
    """
    Process payment for an order
    ---
    tags:
      - Sales
    parameters:
      - in: path
        name: order_id
        required: true
        schema:
          type: string
      - in: header
        name: X-API-Key
        required: true
        schema:
          type: string
      - in: body
        name: payment
        schema:
          type: object
          properties:
            payment_method:
              type: string
              default: credit_card
    responses:
      200:
        description: Payment processed successfully
      400:
        description: Payment failed or order not found
    """
    data = request.get_json() or {}
    payment_method = data.get('payment_method', 'credit_card')
    
    success, payment_id, order = sales_service.process_payment(order_id, payment_method)
    
    if not success:
        if order:
            return jsonify({
                'error': 'Payment already processed',
                'message': f'Order {order_id} has already been paid'
            }), 400
        else:
            return jsonify({
                'error': 'Order not found',
                'message': f'No order found with ID: {order_id}'
            }), 404
    
    return jsonify({
        'message': 'Payment processed successfully',
        'payment_id': payment_id,
        'order': order.to_dict()
    }), 200


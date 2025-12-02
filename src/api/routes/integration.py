"""Integrated workflow API Routes"""

from flask import Blueprint, jsonify, request
from src.api.auth import require_api_key
from src.services.inventory_service import InventoryService
from src.services.sales_service import SalesService
from src.services.delivery_service import DeliveryService

integration_bp = Blueprint('integration', __name__)
inventory_service = InventoryService()
sales_service = SalesService()
delivery_service = DeliveryService()


@integration_bp.route('/orders/complete', methods=['POST'])
@require_api_key
def complete_order_flow():
    """
    Complete order flow: Check inventory → Create order → Process payment → Create delivery
    ---
    tags:
      - Integration
    parameters:
      - in: header
        name: X-API-Key
        required: true
        schema:
          type: string
      - in: body
        name: order_request
        required: true
        schema:
          type: object
          required:
            - customer_name
            - customer_email
            - items
            - shipping_address
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
            shipping_address:
              type: string
            payment_method:
              type: string
    responses:
      201:
        description: Order completed successfully
      400:
        description: Invalid request or insufficient stock
      404:
        description: Book not found
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'error': 'Invalid request',
            'message': 'Request body must be JSON'
        }), 400
    
    required_fields = ['customer_name', 'customer_email', 'items', 'shipping_address']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'error': 'Missing required field',
                'message': f'{field} is required'
            }), 400
    
    # Step 1: Check inventory for all items
    order_items = []
    for item in data['items']:
        book_id = item['book_id']
        quantity = item['quantity']
        
        book = inventory_service.get_book_by_id(book_id)
        if not book:
            return jsonify({
                'error': 'Book not found',
                'message': f'Book with ID {book_id} not found in inventory'
            }), 404
        
        if not inventory_service.check_stock(book_id, quantity):
            return jsonify({
                'error': 'Insufficient stock',
                'message': f'Insufficient stock for book "{book.title}". Available: {book.stock_quantity}, Requested: {quantity}'
            }), 400
        
        order_items.append({
            'book_id': book_id,
            'title': book.title,
            'quantity': quantity,
            'unit_price': book.price
        })
    
    # Step 2: Reserve stock and create order
    try:
        # Reserve stock
        for item in order_items:
            inventory_service.reserve_stock(item['book_id'], item['quantity'])
        
        # Create order
        order = sales_service.create_order(
            customer_name=data['customer_name'],
            customer_email=data['customer_email'],
            items=order_items,
            shipping_address=data['shipping_address']
        )
        
        # Step 3: Process payment
        payment_method = data.get('payment_method', 'credit_card')
        payment_success, payment_id, order = sales_service.process_payment(
            order.id, 
            payment_method
        )
        
        if not payment_success:
            # Restore stock if payment fails
            for item in order_items:
                inventory_service.restore_stock(item['book_id'], item['quantity'])
            return jsonify({
                'error': 'Payment failed',
                'message': 'Could not process payment for the order'
            }), 400
        
        # Step 4: Create delivery record
        delivery = delivery_service.create_delivery(
            order_id=order.id,
            shipping_address=data['shipping_address'],
            carrier=data.get('carrier')
        )
        
        return jsonify({
            'message': 'Order completed successfully',
            'order': order.to_dict(),
            'delivery': delivery.to_dict(),
            'payment_id': payment_id
        }), 201
        
    except Exception as e:
        # Restore stock on any error
        for item in order_items:
            try:
                inventory_service.restore_stock(item['book_id'], item['quantity'])
            except:
                pass
        
        return jsonify({
            'error': 'Order processing failed',
            'message': str(e)
        }), 400


@integration_bp.route('/orders/<order_id>/status', methods=['GET'])
@require_api_key
def get_complete_order_status(order_id):
    """
    Get complete order status across all systems
    ---
    tags:
      - Integration
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
        description: Complete order status
      404:
        description: Order not found
    """
    order = sales_service.get_order_by_id(order_id)
    if not order:
        return jsonify({
            'error': 'Order not found',
            'message': f'No order found with ID: {order_id}'
        }), 404
    
    delivery = delivery_service.get_delivery_by_order_id(order_id)
    
    # Get book details for order items
    order_items_details = []
    for item in order.items:
        book = inventory_service.get_book_by_id(item.book_id)
        order_items_details.append({
            'book_id': item.book_id,
            'title': item.title,
            'quantity': item.quantity,
            'unit_price': item.unit_price,
            'subtotal': item.subtotal,
            'book_details': book.to_dict() if book else None
        })
    
    response = {
        'order_id': order_id,
        'order_status': order.status,
        'payment_status': order.payment_status,
        'payment_id': order.payment_id,
        'customer': {
            'name': order.customer_name,
            'email': order.customer_email
        },
        'items': order_items_details,
        'total_amount': order.total_amount,
        'created_at': order.created_at,
        'updated_at': order.updated_at,
        'delivery': delivery.to_dict() if delivery else None
    }
    
    return jsonify(response), 200


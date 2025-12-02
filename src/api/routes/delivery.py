"""Delivery System API Routes"""

from flask import Blueprint, jsonify, request
from src.api.auth import require_api_key
from src.services.delivery_service import DeliveryService

delivery_bp = Blueprint('delivery', __name__)
delivery_service = DeliveryService()


@delivery_bp.route('/orders/<order_id>', methods=['POST'])
@require_api_key
def create_delivery(order_id):
    """
    Create a delivery record for an order
    ---
    tags:
      - Delivery
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
        name: delivery
        required: true
        schema:
          type: object
          required:
            - shipping_address
          properties:
            shipping_address:
              type: string
            carrier:
              type: string
    responses:
      201:
        description: Delivery record created
      400:
        description: Invalid request
    """
    data = request.get_json()
    
    if not data or 'shipping_address' not in data:
        return jsonify({
            'error': 'Invalid request',
            'message': 'shipping_address is required'
        }), 400
    
    # Check if delivery already exists for this order
    existing = delivery_service.get_delivery_by_order_id(order_id)
    if existing:
        return jsonify({
            'error': 'Delivery already exists',
            'message': f'Delivery record already exists for order {order_id}',
            'delivery': existing.to_dict()
        }), 400
    
    delivery = delivery_service.create_delivery(
        order_id=order_id,
        shipping_address=data['shipping_address'],
        carrier=data.get('carrier')
    )
    
    return jsonify({
        'message': 'Delivery record created successfully',
        'delivery': delivery.to_dict()
    }), 201


@delivery_bp.route('/orders/<order_id>', methods=['GET'])
@require_api_key
def get_delivery_by_order_id(order_id):
    """
    Get delivery status by order ID
    ---
    tags:
      - Delivery
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
        description: Delivery details
      404:
        description: Delivery not found
    """
    delivery = delivery_service.get_delivery_by_order_id(order_id)
    if not delivery:
        return jsonify({
            'error': 'Delivery not found',
            'message': f'No delivery found for order ID: {order_id}'
        }), 404
    
    return jsonify(delivery.to_dict()), 200


@delivery_bp.route('/orders/<order_id>/status', methods=['PUT'])
@require_api_key
def update_delivery_status(order_id):
    """
    Update delivery status
    ---
    tags:
      - Delivery
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
        name: status_update
        required: true
        schema:
          type: object
          required:
            - status
          properties:
            status:
              type: string
              enum: [pending, preparing, shipped, in_transit, delivered, failed]
            notes:
              type: string
    responses:
      200:
        description: Delivery status updated
      400:
        description: Invalid request
      404:
        description: Delivery not found
    """
    data = request.get_json()
    
    if not data or 'status' not in data:
        return jsonify({
            'error': 'Invalid request',
            'message': 'status is required'
        }), 400
    
    valid_statuses = ['pending', 'preparing', 'shipped', 'in_transit', 'delivered', 'failed']
    if data['status'] not in valid_statuses:
        return jsonify({
            'error': 'Invalid status',
            'message': f'Status must be one of: {", ".join(valid_statuses)}'
        }), 400
    
    delivery = delivery_service.update_delivery_by_order_id(
        order_id=order_id,
        status=data['status'],
        notes=data.get('notes')
    )
    
    if not delivery:
        return jsonify({
            'error': 'Delivery not found',
            'message': f'No delivery found for order ID: {order_id}'
        }), 404
    
    return jsonify({
        'message': 'Delivery status updated successfully',
        'delivery': delivery.to_dict()
    }), 200


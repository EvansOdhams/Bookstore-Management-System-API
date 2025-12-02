"""Sales Service - Tracks customer orders and payments"""

import json
import os
from typing import List, Optional
from pathlib import Path
from datetime import datetime
import uuid
from src.models.order import Order, OrderItem


class SalesService:
    """Service for managing sales operations"""
    
    def __init__(self, data_file: str = "data/orders.json"):
        """Initialize sales service with data file path"""
        self.data_file = data_file
        self._ensure_data_file()
        self._load_data()
    
    def _ensure_data_file(self):
        """Ensure data directory and file exist"""
        data_path = Path(self.data_file)
        data_path.parent.mkdir(parents=True, exist_ok=True)
        if not data_path.exists():
            with open(self.data_file, 'w') as f:
                json.dump([], f)
    
    def _load_data(self):
        """Load orders from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.orders = {order['id']: Order.from_dict(order) for order in data}
        except (FileNotFoundError, json.JSONDecodeError):
            self.orders = {}
    
    def _save_data(self):
        """Save orders to JSON file"""
        with open(self.data_file, 'w') as f:
            orders_list = [order.to_dict() for order in self.orders.values()]
            json.dump(orders_list, f, indent=2)
    
    def get_all_orders(self) -> List[Order]:
        """Get all orders"""
        # Reload data to ensure we have the latest
        self._load_data()
        return list(self.orders.values())
    
    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        """Get an order by its ID"""
        # Reload data to ensure we have the latest
        self._load_data()
        return self.orders.get(order_id)
    
    def create_order(self, customer_name: str, customer_email: str, 
                    items: List[dict], shipping_address: Optional[str] = None) -> Order:
        """Create a new order"""
        order_id = str(uuid.uuid4())
        order_items = []
        
        for item in items:
            order_item = OrderItem(
                book_id=item['book_id'],
                title=item.get('title', ''),
                quantity=item['quantity'],
                unit_price=item['unit_price'],
                subtotal=item['quantity'] * item['unit_price']
            )
            order_items.append(order_item)
        
        total_amount = sum(item.subtotal for item in order_items)
        
        order = Order(
            id=order_id,
            customer_name=customer_name,
            customer_email=customer_email,
            items=order_items,
            total_amount=total_amount,
            status='pending',
            payment_status='pending',
            created_at=datetime.now().isoformat(),
            shipping_address=shipping_address
        )
        
        self.orders[order_id] = order
        self._save_data()
        return order
    
    def process_payment(self, order_id: str, payment_method: str = "credit_card") -> tuple[bool, Optional[str], Optional[Order]]:
        """Process payment for an order. Returns (success, payment_id, order)"""
        order = self.orders.get(order_id)
        if not order:
            return False, None, None
        
        if order.payment_status == 'paid':
            return False, None, order  # Already paid
        
        # Simulate payment processing
        payment_id = f"PAY-{uuid.uuid4().hex[:8].upper()}"
        order.update_payment_status('paid', payment_id)
        order.update_status('processing')
        
        self._save_data()
        return True, payment_id, order
    
    def update_order_status(self, order_id: str, status: str) -> Optional[Order]:
        """Update order status"""
        order = self.orders.get(order_id)
        if not order:
            return None
        
        order.update_status(status)
        self._save_data()
        return order
    
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order"""
        order = self.orders.get(order_id)
        if not order:
            return False
        
        if order.status in ['delivered', 'shipped']:
            return False  # Cannot cancel shipped/delivered orders
        
        order.update_status('cancelled')
        if order.payment_status == 'paid':
            order.update_payment_status('refunded')
        
        self._save_data()
        return True


"""Order model for the Sales System"""

from dataclasses import dataclass, asdict
from typing import List, Optional
from datetime import datetime


@dataclass
class OrderItem:
    """Represents an item in an order"""
    book_id: str
    title: str
    quantity: int
    unit_price: float
    subtotal: float

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'OrderItem':
        return cls(**data)


@dataclass
class Order:
    """Represents a customer order"""
    id: str
    customer_name: str
    customer_email: str
    items: List[OrderItem]
    total_amount: float
    status: str  # 'pending', 'paid', 'processing', 'shipped', 'delivered', 'cancelled'
    payment_status: str  # 'pending', 'paid', 'failed', 'refunded'
    created_at: str
    updated_at: Optional[str] = None
    payment_id: Optional[str] = None
    shipping_address: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert order to dictionary"""
        data = asdict(self)
        data['items'] = [item.to_dict() for item in self.items]
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'Order':
        """Create order from dictionary"""
        items = [OrderItem.from_dict(item) for item in data.get('items', [])]
        return cls(
            id=data['id'],
            customer_name=data['customer_name'],
            customer_email=data['customer_email'],
            items=items,
            total_amount=data['total_amount'],
            status=data['status'],
            payment_status=data['payment_status'],
            created_at=data['created_at'],
            updated_at=data.get('updated_at'),
            payment_id=data.get('payment_id'),
            shipping_address=data.get('shipping_address')
        )

    def calculate_total(self) -> float:
        """Recalculate total amount from items"""
        return sum(item.subtotal for item in self.items)

    def update_status(self, new_status: str):
        """Update order status"""
        self.status = new_status
        self.updated_at = datetime.now().isoformat()

    def update_payment_status(self, new_status: str, payment_id: Optional[str] = None):
        """Update payment status"""
        self.payment_status = new_status
        if payment_id:
            self.payment_id = payment_id
        self.updated_at = datetime.now().isoformat()


"""Delivery model for the Delivery System"""

from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime


@dataclass
class Delivery:
    """Represents a delivery record"""
    id: str
    order_id: str
    status: str  # 'pending', 'preparing', 'shipped', 'in_transit', 'delivered', 'failed'
    shipping_address: str
    created_at: str
    tracking_number: Optional[str] = None
    carrier: Optional[str] = None
    estimated_delivery_date: Optional[str] = None
    actual_delivery_date: Optional[str] = None
    updated_at: Optional[str] = None
    notes: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert delivery to dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Delivery':
        """Create delivery from dictionary"""
        return cls(**data)

    def update_status(self, new_status: str, notes: Optional[str] = None):
        """Update delivery status"""
        self.status = new_status
        self.updated_at = datetime.now().isoformat()
        if notes:
            self.notes = notes
        
        # Auto-set delivery date when status is 'delivered'
        if new_status == 'delivered' and not self.actual_delivery_date:
            self.actual_delivery_date = datetime.now().isoformat()

    def set_tracking(self, tracking_number: str, carrier: str):
        """Set tracking information"""
        self.tracking_number = tracking_number
        self.carrier = carrier
        self.updated_at = datetime.now().isoformat()


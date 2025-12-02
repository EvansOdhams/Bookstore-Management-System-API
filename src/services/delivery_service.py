"""Delivery Service - Manages order deliveries"""

import json
import os
from typing import List, Optional
from pathlib import Path
from datetime import datetime, timedelta
import uuid
from src.models.delivery import Delivery


class DeliveryService:
    """Service for managing delivery operations"""
    
    def __init__(self, data_file: str = "data/deliveries.json"):
        """Initialize delivery service with data file path"""
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
        """Load deliveries from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.deliveries = {delivery['id']: Delivery.from_dict(delivery) for delivery in data}
        except (FileNotFoundError, json.JSONDecodeError):
            self.deliveries = {}
    
    def _save_data(self):
        """Save deliveries to JSON file"""
        with open(self.data_file, 'w') as f:
            deliveries_list = [delivery.to_dict() for delivery in self.deliveries.values()]
            json.dump(deliveries_list, f, indent=2)
    
    def get_all_deliveries(self) -> List[Delivery]:
        """Get all deliveries"""
        # Reload data to ensure we have the latest
        self._load_data()
        return list(self.deliveries.values())
    
    def get_delivery_by_id(self, delivery_id: str) -> Optional[Delivery]:
        """Get a delivery by its ID"""
        # Reload data to ensure we have the latest
        self._load_data()
        return self.deliveries.get(delivery_id)
    
    def get_delivery_by_order_id(self, order_id: str) -> Optional[Delivery]:
        """Get delivery by order ID"""
        # Reload data to ensure we have the latest
        self._load_data()
        for delivery in self.deliveries.values():
            if delivery.order_id == order_id:
                return delivery
        return None
    
    def create_delivery(self, order_id: str, shipping_address: str, 
                       carrier: Optional[str] = None) -> Delivery:
        """Create a new delivery record"""
        delivery_id = str(uuid.uuid4())
        tracking_number = f"TRACK-{uuid.uuid4().hex[:12].upper()}"
        estimated_delivery = (datetime.now() + timedelta(days=5)).isoformat()
        
        delivery = Delivery(
            id=delivery_id,
            order_id=order_id,
            status='preparing',
            shipping_address=shipping_address,
            tracking_number=tracking_number,
            carrier=carrier or "Standard Shipping",
            estimated_delivery_date=estimated_delivery,
            created_at=datetime.now().isoformat()
        )
        
        self.deliveries[delivery_id] = delivery
        self._save_data()
        return delivery
    
    def update_delivery_status(self, delivery_id: str, status: str, 
                              notes: Optional[str] = None) -> Optional[Delivery]:
        """Update delivery status"""
        delivery = self.deliveries.get(delivery_id)
        if not delivery:
            return None
        
        delivery.update_status(status, notes)
        self._save_data()
        return delivery
    
    def update_delivery_by_order_id(self, order_id: str, status: str, 
                                    notes: Optional[str] = None) -> Optional[Delivery]:
        """Update delivery status by order ID"""
        delivery = self.get_delivery_by_order_id(order_id)
        if not delivery:
            return None
        
        return self.update_delivery_status(delivery.id, status, notes)
    
    def set_tracking(self, delivery_id: str, tracking_number: str, carrier: str) -> Optional[Delivery]:
        """Set tracking information for delivery"""
        delivery = self.deliveries.get(delivery_id)
        if not delivery:
            return None
        
        delivery.set_tracking(tracking_number, carrier)
        self._save_data()
        return delivery


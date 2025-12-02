"""Unit tests for Delivery Service"""

import pytest
from pathlib import Path
from src.services.delivery_service import DeliveryService
from src.models.delivery import Delivery


@pytest.fixture
def temp_data_file(tmp_path):
    """Create a temporary data file for testing"""
    data_file = tmp_path / "test_deliveries.json"
    return str(data_file)


@pytest.fixture
def delivery_service(temp_data_file):
    """Create a delivery service instance with temporary data file"""
    service = DeliveryService(data_file=temp_data_file)
    return service


class TestDeliveryService:
    """Test cases for DeliveryService"""
    
    def test_get_all_deliveries_empty(self, delivery_service):
        """Test getting all deliveries when empty"""
        deliveries = delivery_service.get_all_deliveries()
        assert deliveries == []
    
    def test_create_delivery(self, delivery_service):
        """Test creating a new delivery record"""
        delivery = delivery_service.create_delivery(
            order_id="order-001",
            shipping_address="123 Main St, City, Country",
            carrier="Express Shipping"
        )
        
        assert delivery.id is not None
        assert delivery.order_id == "order-001"
        assert delivery.shipping_address == "123 Main St, City, Country"
        assert delivery.carrier == "Express Shipping"
        assert delivery.status == "preparing"
        assert delivery.tracking_number is not None
    
    def test_get_delivery_by_id(self, delivery_service):
        """Test retrieving a delivery by ID"""
        delivery = delivery_service.create_delivery(
            order_id="order-002",
            shipping_address="456 Oak Ave"
        )
        
        retrieved = delivery_service.get_delivery_by_id(delivery.id)
        assert retrieved is not None
        assert retrieved.id == delivery.id
        assert retrieved.order_id == "order-002"
    
    def test_get_delivery_by_order_id(self, delivery_service):
        """Test retrieving a delivery by order ID"""
        delivery = delivery_service.create_delivery(
            order_id="order-003",
            shipping_address="789 Pine Rd"
        )
        
        retrieved = delivery_service.get_delivery_by_order_id("order-003")
        assert retrieved is not None
        assert retrieved.id == delivery.id
    
    def test_update_delivery_status(self, delivery_service):
        """Test updating delivery status"""
        delivery = delivery_service.create_delivery(
            order_id="order-004",
            shipping_address="321 Elm St"
        )
        
        updated = delivery_service.update_delivery_status(
            delivery.id,
            "shipped",
            notes="Package shipped via standard mail"
        )
        
        assert updated is not None
        assert updated.status == "shipped"
        assert updated.notes == "Package shipped via standard mail"
    
    def test_update_delivery_by_order_id(self, delivery_service):
        """Test updating delivery status by order ID"""
        delivery = delivery_service.create_delivery(
            order_id="order-005",
            shipping_address="654 Maple Dr"
        )
        
        updated = delivery_service.update_delivery_by_order_id(
            "order-005",
            "in_transit"
        )
        
        assert updated is not None
        assert updated.status == "in_transit"
    
    def test_set_tracking(self, delivery_service):
        """Test setting tracking information"""
        delivery = delivery_service.create_delivery(
            order_id="order-006",
            shipping_address="987 Cedar Ln"
        )
        
        updated = delivery_service.set_tracking(
            delivery.id,
            "TRACK123456789",
            "FedEx"
        )
        
        assert updated is not None
        assert updated.tracking_number == "TRACK123456789"
        assert updated.carrier == "FedEx"
    
    def test_delivery_status_delivered(self, delivery_service):
        """Test that delivered status sets actual_delivery_date"""
        delivery = delivery_service.create_delivery(
            order_id="order-007",
            shipping_address="111 Birch Way"
        )
        
        assert delivery.actual_delivery_date is None
        
        updated = delivery_service.update_delivery_status(delivery.id, "delivered")
        
        assert updated is not None
        assert updated.status == "delivered"
        assert updated.actual_delivery_date is not None


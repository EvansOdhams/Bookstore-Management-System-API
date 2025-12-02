"""Unit tests for Sales Service"""

import pytest
from pathlib import Path
from src.services.sales_service import SalesService
from src.models.order import Order


@pytest.fixture
def temp_data_file(tmp_path):
    """Create a temporary data file for testing"""
    data_file = tmp_path / "test_orders.json"
    return str(data_file)


@pytest.fixture
def sales_service(temp_data_file):
    """Create a sales service instance with temporary data file"""
    service = SalesService(data_file=temp_data_file)
    return service


@pytest.fixture
def sample_order_items():
    """Create sample order items"""
    return [
        {
            'book_id': 'book-001',
            'title': 'Test Book 1',
            'quantity': 2,
            'unit_price': 19.99
        },
        {
            'book_id': 'book-002',
            'title': 'Test Book 2',
            'quantity': 1,
            'unit_price': 24.99
        }
    ]


class TestSalesService:
    """Test cases for SalesService"""
    
    def test_get_all_orders_empty(self, sales_service):
        """Test getting all orders when empty"""
        orders = sales_service.get_all_orders()
        assert orders == []
    
    def test_create_order(self, sales_service, sample_order_items):
        """Test creating a new order"""
        order = sales_service.create_order(
            customer_name="John Doe",
            customer_email="john@example.com",
            items=sample_order_items,
            shipping_address="123 Main St"
        )
        
        assert order.id is not None
        assert order.customer_name == "John Doe"
        assert order.customer_email == "john@example.com"
        assert len(order.items) == 2
        assert order.status == "pending"
        assert order.payment_status == "pending"
        assert order.total_amount == (2 * 19.99) + (1 * 24.99)
    
    def test_get_order_by_id(self, sales_service, sample_order_items):
        """Test retrieving an order by ID"""
        order = sales_service.create_order(
            customer_name="Jane Doe",
            customer_email="jane@example.com",
            items=sample_order_items
        )
        
        retrieved = sales_service.get_order_by_id(order.id)
        assert retrieved is not None
        assert retrieved.id == order.id
        assert retrieved.customer_name == "Jane Doe"
    
    def test_get_order_by_id_not_found(self, sales_service):
        """Test retrieving a non-existent order"""
        order = sales_service.get_order_by_id("non-existent")
        assert order is None
    
    def test_process_payment(self, sales_service, sample_order_items):
        """Test processing payment for an order"""
        order = sales_service.create_order(
            customer_name="Test User",
            customer_email="test@example.com",
            items=sample_order_items
        )
        
        success, payment_id, updated_order = sales_service.process_payment(order.id)
        
        assert success is True
        assert payment_id is not None
        assert updated_order.payment_status == "paid"
        assert updated_order.status == "processing"
        assert updated_order.payment_id == payment_id
    
    def test_process_payment_already_paid(self, sales_service, sample_order_items):
        """Test processing payment for an already paid order"""
        order = sales_service.create_order(
            customer_name="Test User",
            customer_email="test@example.com",
            items=sample_order_items
        )
        
        sales_service.process_payment(order.id)
        success, payment_id, order = sales_service.process_payment(order.id)
        
        assert success is False
        assert payment_id is None
    
    def test_update_order_status(self, sales_service, sample_order_items):
        """Test updating order status"""
        order = sales_service.create_order(
            customer_name="Test User",
            customer_email="test@example.com",
            items=sample_order_items
        )
        
        updated = sales_service.update_order_status(order.id, "shipped")
        assert updated is not None
        assert updated.status == "shipped"
    
    def test_cancel_order(self, sales_service, sample_order_items):
        """Test cancelling an order"""
        order = sales_service.create_order(
            customer_name="Test User",
            customer_email="test@example.com",
            items=sample_order_items
        )
        
        success = sales_service.cancel_order(order.id)
        assert success is True
        
        cancelled_order = sales_service.get_order_by_id(order.id)
        assert cancelled_order.status == "cancelled"
    
    def test_cancel_paid_order(self, sales_service, sample_order_items):
        """Test cancelling a paid order (should refund)"""
        order = sales_service.create_order(
            customer_name="Test User",
            customer_email="test@example.com",
            items=sample_order_items
        )
        
        sales_service.process_payment(order.id)
        success = sales_service.cancel_order(order.id)
        
        assert success is True
        cancelled_order = sales_service.get_order_by_id(order.id)
        assert cancelled_order.payment_status == "refunded"


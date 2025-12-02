"""Integration tests for complete workflows"""

import pytest
from pathlib import Path
from src.services.inventory_service import InventoryService
from src.services.sales_service import SalesService
from src.services.delivery_service import DeliveryService
from src.models.book import Book


@pytest.fixture
def temp_files(tmp_path):
    """Create temporary data files for all services"""
    return {
        'books': str(tmp_path / "test_books.json"),
        'orders': str(tmp_path / "test_orders.json"),
        'deliveries': str(tmp_path / "test_deliveries.json")
    }


@pytest.fixture
def services(temp_files):
    """Create service instances with temporary data files"""
    inventory = InventoryService(data_file=temp_files['books'])
    sales = SalesService(data_file=temp_files['orders'])
    delivery = DeliveryService(data_file=temp_files['deliveries'])
    return {
        'inventory': inventory,
        'sales': sales,
        'delivery': delivery
    }


@pytest.fixture
def sample_books(services):
    """Add sample books to inventory"""
    books = [
        Book(
            id="book-001",
            title="Test Book 1",
            author="Author 1",
            isbn="978-0-123456-78-9",
            price=19.99,
            stock_quantity=10
        ),
        Book(
            id="book-002",
            title="Test Book 2",
            author="Author 2",
            isbn="978-0-987654-32-1",
            price=24.99,
            stock_quantity=5
        )
    ]
    
    for book in books:
        services['inventory'].add_book(book)
    
    return books


class TestIntegration:
    """Integration test cases for complete workflows"""
    
    def test_complete_order_flow(self, services, sample_books):
        """Test complete order flow: inventory check → order → payment → delivery"""
        inventory = services['inventory']
        sales = services['sales']
        delivery = services['delivery']
        
        # Step 1: Check inventory
        book1 = inventory.get_book_by_id("book-001")
        assert book1.stock_quantity == 10
        
        # Step 2: Create order
        order_items = [
            {
                'book_id': 'book-001',
                'title': 'Test Book 1',
                'quantity': 2,
                'unit_price': 19.99
            }
        ]
        
        order = sales.create_order(
            customer_name="Test Customer",
            customer_email="test@example.com",
            items=order_items,
            shipping_address="123 Test St"
        )
        
        assert order.status == "pending"
        assert order.payment_status == "pending"
        
        # Step 3: Reserve stock
        success = inventory.reserve_stock("book-001", 2)
        assert success is True
        
        book1_after = inventory.get_book_by_id("book-001")
        assert book1_after.stock_quantity == 8
        
        # Step 4: Process payment
        payment_success, payment_id, order = sales.process_payment(order.id)
        assert payment_success is True
        assert order.payment_status == "paid"
        
        # Step 5: Create delivery
        delivery_record = delivery.create_delivery(
            order_id=order.id,
            shipping_address="123 Test St"
        )
        
        assert delivery_record.order_id == order.id
        assert delivery_record.status == "preparing"
    
    def test_insufficient_stock_prevents_order(self, services, sample_books):
        """Test that insufficient stock prevents order completion"""
        inventory = services['inventory']
        
        # Try to reserve more than available
        success = inventory.reserve_stock("book-002", 10)  # Only 5 available
        assert success is False
        
        book2 = inventory.get_book_by_id("book-002")
        assert book2.stock_quantity == 5  # Unchanged
    
    def test_order_status_across_systems(self, services, sample_books):
        """Test retrieving order status across all systems"""
        inventory = services['inventory']
        sales = services['sales']
        delivery = services['delivery']
        
        # Create complete order
        order_items = [
            {
                'book_id': 'book-001',
                'title': 'Test Book 1',
                'quantity': 1,
                'unit_price': 19.99
            }
        ]
        
        order = sales.create_order(
            customer_name="Test Customer",
            customer_email="test@example.com",
            items=order_items,
            shipping_address="123 Test St"
        )
        
        sales.process_payment(order.id)
        delivery_record = delivery.create_delivery(
            order_id=order.id,
            shipping_address="123 Test St"
        )
        
        # Verify status across systems
        order_status = sales.get_order_by_id(order.id)
        delivery_status = delivery.get_delivery_by_order_id(order.id)
        book_status = inventory.get_book_by_id("book-001")
        
        assert order_status.payment_status == "paid"
        assert delivery_status.status == "preparing"
        assert book_status.stock_quantity == 9  # 10 - 1


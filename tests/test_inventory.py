"""Unit tests for Inventory Service"""

import pytest
import json
import os
from pathlib import Path
from src.services.inventory_service import InventoryService
from src.models.book import Book


@pytest.fixture
def temp_data_file(tmp_path):
    """Create a temporary data file for testing"""
    data_file = tmp_path / "test_books.json"
    return str(data_file)


@pytest.fixture
def inventory_service(temp_data_file):
    """Create an inventory service instance with temporary data file"""
    service = InventoryService(data_file=temp_data_file)
    return service


@pytest.fixture
def sample_book():
    """Create a sample book for testing"""
    return Book(
        id="test-book-001",
        title="Test Book",
        author="Test Author",
        isbn="978-0-123456-78-9",
        price=19.99,
        stock_quantity=100,
        description="A test book",
        category="Test"
    )


class TestInventoryService:
    """Test cases for InventoryService"""
    
    def test_get_all_books_empty(self, inventory_service):
        """Test getting all books when inventory is empty"""
        books = inventory_service.get_all_books()
        assert books == []
    
    def test_add_book(self, inventory_service, sample_book):
        """Test adding a book to inventory"""
        added_book = inventory_service.add_book(sample_book)
        assert added_book.id == sample_book.id
        assert added_book.title == sample_book.title
    
    def test_get_book_by_id(self, inventory_service, sample_book):
        """Test retrieving a book by ID"""
        inventory_service.add_book(sample_book)
        retrieved = inventory_service.get_book_by_id(sample_book.id)
        assert retrieved is not None
        assert retrieved.id == sample_book.id
        assert retrieved.title == sample_book.title
    
    def test_get_book_by_id_not_found(self, inventory_service):
        """Test retrieving a non-existent book"""
        book = inventory_service.get_book_by_id("non-existent")
        assert book is None
    
    def test_update_stock_increase(self, inventory_service, sample_book):
        """Test increasing stock quantity"""
        inventory_service.add_book(sample_book)
        success, book = inventory_service.update_stock(sample_book.id, 10)
        assert success is True
        assert book.stock_quantity == 110
    
    def test_update_stock_decrease(self, inventory_service, sample_book):
        """Test decreasing stock quantity"""
        inventory_service.add_book(sample_book)
        success, book = inventory_service.update_stock(sample_book.id, -20)
        assert success is True
        assert book.stock_quantity == 80
    
    def test_update_stock_insufficient(self, inventory_service, sample_book):
        """Test decreasing stock below zero (should fail)"""
        inventory_service.add_book(sample_book)
        success, book = inventory_service.update_stock(sample_book.id, -150)
        assert success is False
        assert book.stock_quantity == 100  # Should remain unchanged
    
    def test_check_stock_available(self, inventory_service, sample_book):
        """Test checking stock availability when sufficient"""
        inventory_service.add_book(sample_book)
        available = inventory_service.check_stock(sample_book.id, 50)
        assert available is True
    
    def test_check_stock_unavailable(self, inventory_service, sample_book):
        """Test checking stock availability when insufficient"""
        inventory_service.add_book(sample_book)
        available = inventory_service.check_stock(sample_book.id, 150)
        assert available is False
    
    def test_reserve_stock(self, inventory_service, sample_book):
        """Test reserving stock (decreasing)"""
        inventory_service.add_book(sample_book)
        success = inventory_service.reserve_stock(sample_book.id, 30)
        assert success is True
        book = inventory_service.get_book_by_id(sample_book.id)
        assert book.stock_quantity == 70
    
    def test_restore_stock(self, inventory_service, sample_book):
        """Test restoring stock (increasing)"""
        inventory_service.add_book(sample_book)
        success = inventory_service.restore_stock(sample_book.id, 25)
        assert success is True
        book = inventory_service.get_book_by_id(sample_book.id)
        assert book.stock_quantity == 125
    
    def test_persistence(self, temp_data_file, sample_book):
        """Test that data persists across service instances"""
        service1 = InventoryService(data_file=temp_data_file)
        service1.add_book(sample_book)
        
        service2 = InventoryService(data_file=temp_data_file)
        book = service2.get_book_by_id(sample_book.id)
        assert book is not None
        assert book.id == sample_book.id


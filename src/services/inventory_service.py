"""Inventory Service - Manages book stock and details"""

import json
import os
from typing import List, Optional
from pathlib import Path
from src.models.book import Book


class InventoryService:
    """Service for managing inventory operations"""
    
    def __init__(self, data_file: str = "data/books.json"):
        """Initialize inventory service with data file path"""
        self.data_file = data_file
        self._ensure_data_file()
        self._load_data()
    
    def _ensure_data_file(self):
        """Ensure data directory and file exist"""
        data_path = Path(self.data_file)
        data_path.parent.mkdir(parents=True, exist_ok=True)
        if not data_path.exists():
            # Initialize with empty list
            with open(self.data_file, 'w') as f:
                json.dump([], f)
    
    def _load_data(self):
        """Load books from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.books = {book['id']: Book.from_dict(book) for book in data}
        except (FileNotFoundError, json.JSONDecodeError):
            self.books = {}
    
    def _save_data(self):
        """Save books to JSON file"""
        with open(self.data_file, 'w') as f:
            books_list = [book.to_dict() for book in self.books.values()]
            json.dump(books_list, f, indent=2)
    
    def get_all_books(self) -> List[Book]:
        """Get all books in inventory"""
        return list(self.books.values())
    
    def get_book_by_id(self, book_id: str) -> Optional[Book]:
        """Get a book by its ID"""
        return self.books.get(book_id)
    
    def get_book_by_isbn(self, isbn: str) -> Optional[Book]:
        """Get a book by its ISBN"""
        for book in self.books.values():
            if book.isbn == isbn:
                return book
        return None
    
    def add_book(self, book: Book) -> Book:
        """Add a new book to inventory"""
        self.books[book.id] = book
        self._save_data()
        return book
    
    def update_book(self, book_id: str, **kwargs) -> Optional[Book]:
        """Update book information"""
        book = self.books.get(book_id)
        if not book:
            return None
        
        for key, value in kwargs.items():
            if hasattr(book, key):
                setattr(book, key, value)
        
        book.updated_at = __import__('datetime').datetime.now().isoformat()
        self._save_data()
        return book
    
    def update_stock(self, book_id: str, quantity: int) -> tuple[bool, Optional[Book]]:
        """Update stock quantity. Returns (success, book)"""
        book = self.books.get(book_id)
        if not book:
            return False, None
        
        success = book.update_stock(quantity)
        if success:
            self._save_data()
        return success, book
    
    def check_stock(self, book_id: str, quantity: int = 1) -> bool:
        """Check if book is available in requested quantity"""
        book = self.books.get(book_id)
        if not book:
            return False
        return book.is_available(quantity)
    
    def reserve_stock(self, book_id: str, quantity: int) -> bool:
        """Reserve stock (decrease by quantity). Returns True if successful."""
        return self.update_stock(book_id, -quantity)[0]
    
    def restore_stock(self, book_id: str, quantity: int) -> bool:
        """Restore stock (increase by quantity). Returns True if successful."""
        return self.update_stock(book_id, quantity)[0]


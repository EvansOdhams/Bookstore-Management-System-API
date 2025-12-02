"""Book model for the Inventory System"""

from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime


@dataclass
class Book:
    """Represents a book in the inventory"""
    id: str
    title: str
    author: str
    isbn: str
    price: float
    stock_quantity: int
    description: Optional[str] = None
    category: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert book to dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        """Create book from dictionary"""
        return cls(**data)

    def update_stock(self, quantity: int) -> bool:
        """Update stock quantity. Returns True if successful, False if insufficient stock."""
        if self.stock_quantity + quantity < 0:
            return False
        self.stock_quantity += quantity
        self.updated_at = datetime.now().isoformat()
        return True

    def is_available(self, quantity: int = 1) -> bool:
        """Check if book is available in requested quantity"""
        return self.stock_quantity >= quantity


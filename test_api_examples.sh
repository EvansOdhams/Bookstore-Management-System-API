#!/bin/bash
# Example API test scripts using cURL
# Make sure the API server is running on http://localhost:5000

API_KEY="test-api-key-123"
BASE_URL="http://localhost:5000"

echo "=== Testing Bookstore Management System API ==="
echo ""

# Health check
echo "1. Health Check:"
curl -X GET "$BASE_URL/health"
echo -e "\n"

# Get all books
echo "2. Get All Books:"
curl -X GET "$BASE_URL/api/inventory/books" \
  -H "X-API-Key: $API_KEY"
echo -e "\n"

# Get specific book
echo "3. Get Book by ID:"
curl -X GET "$BASE_URL/api/inventory/books/book-001" \
  -H "X-API-Key: $API_KEY"
echo -e "\n"

# Check stock
echo "4. Check Stock:"
curl -X GET "$BASE_URL/api/inventory/books/book-001/stock?quantity=5" \
  -H "X-API-Key: $API_KEY"
echo -e "\n"

# Create order
echo "5. Create Order:"
curl -X POST "$BASE_URL/api/sales/orders" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "items": [
      {
        "book_id": "book-001",
        "quantity": 2,
        "unit_price": 12.99
      }
    ],
    "shipping_address": "123 Main St, City, Country"
  }'
echo -e "\n"

# Complete order flow (integration)
echo "6. Complete Order Flow:"
curl -X POST "$BASE_URL/api/orders/complete" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Jane Smith",
    "customer_email": "jane@example.com",
    "items": [
      {
        "book_id": "book-002",
        "quantity": 1
      }
    ],
    "shipping_address": "456 Oak Avenue, City, Country"
  }'
echo -e "\n"

echo "=== Tests Complete ==="


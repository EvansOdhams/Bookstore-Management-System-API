# Quick Start Guide

## Installation

1. **Install Python 3.8+** (if not already installed)

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the API

1. **Start the server:**
   ```bash
   python src/api/app.py
   ```

2. **Verify it's running:**
   - Open browser: http://localhost:5000
   - Health check: http://localhost:5000/health
   - API Docs: http://localhost:5000/apidocs

## Testing the API

### Using cURL

**Get all books:**
```bash
curl -X GET "http://localhost:5000/api/inventory/books" \
  -H "X-API-Key: test-api-key-123"
```

**Create an order:**
```bash
curl -X POST "http://localhost:5000/api/sales/orders" \
  -H "X-API-Key: test-api-key-123" \
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
    "shipping_address": "123 Main St"
  }'
```

**Complete order flow (integration):**
```bash
curl -X POST "http://localhost:5000/api/orders/complete" \
  -H "X-API-Key: test-api-key-123" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Jane Smith",
    "customer_email": "jane@example.com",
    "items": [
      {
        "book_id": "book-001",
        "quantity": 1
      }
    ],
    "shipping_address": "456 Oak Ave"
  }'
```

### Using Postman

1. Import the API endpoints from Swagger: http://localhost:5000/apispec.json
2. Set the `X-API-Key` header to `test-api-key-123` for all requests
3. Test the endpoints using the Postman collection

## Running Tests

**Run all tests:**
```bash
pytest tests/ -v
```

**Run with coverage:**
```bash
pytest tests/ --cov=src --cov-report=html
```

**Run specific test file:**
```bash
pytest tests/test_inventory.py -v
```

## Default API Keys

- `test-api-key-123` (admin)
- `demo-api-key-456` (user)

## Sample Data

The API comes with 8 sample books pre-loaded in `data/books.json`:
- Fiction books (The Great Gatsby, 1984, etc.)
- Technology books (Clean Code, Design Patterns, etc.)

Orders and deliveries start empty and are created through API calls.

## Troubleshooting

**Port already in use:**
- Change the port in `src/api/app.py` (line 99): `app.run(..., port=5001)`

**Import errors:**
- Make sure you're running from the project root directory
- Verify Python path includes the project directory

**Data not persisting:**
- Check that `data/` directory exists and is writable
- Verify JSON files are being created/updated


# Testing Guide for Bookstore Management System API

## Quick Start Testing

### 1. Using Swagger UI (Easiest Method)

1. **Open Swagger UI**: http://localhost:5000/apidocs
2. **Authorize**: Click the green "Authorize" button at the top right
3. **Enter API Key**: Type `test-api-key-123` in the value field
4. **Click Authorize** and then **Close**
5. **Test Endpoints**: Click "Try it out" on any endpoint and execute

### 2. Using PowerShell (Windows)

#### Get All Books
```powershell
$headers = @{"X-API-Key" = "test-api-key-123"}
Invoke-RestMethod -Uri "http://localhost:5000/api/inventory/books" -Headers $headers
```

#### Get Specific Book
```powershell
$headers = @{"X-API-Key" = "test-api-key-123"}
Invoke-RestMethod -Uri "http://localhost:5000/api/inventory/books/book-001" -Headers $headers
```

#### Create an Order
```powershell
$headers = @{
    "X-API-Key" = "test-api-key-123"
    "Content-Type" = "application/json"
}
$body = @{
    customer_name = "John Doe"
    customer_email = "john@example.com"
    items = @(
        @{
            book_id = "book-001"
            quantity = 2
            unit_price = 12.99
        }
    )
    shipping_address = "123 Main St, City, Country"
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "http://localhost:5000/api/sales/orders" -Method POST -Headers $headers -Body $body
```

#### Complete Order Flow (Integration)
```powershell
$headers = @{
    "X-API-Key" = "test-api-key-123"
    "Content-Type" = "application/json"
}
$body = @{
    customer_name = "Jane Smith"
    customer_email = "jane@example.com"
    items = @(
        @{
            book_id = "book-001"
            quantity = 1
        }
    )
    shipping_address = "456 Oak Avenue, City, Country"
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "http://localhost:5000/api/orders/complete" -Method POST -Headers $headers -Body $body
```

### 3. Using cURL (Cross-platform)

#### Get All Books
```bash
curl -X GET "http://localhost:5000/api/inventory/books" \
  -H "X-API-Key: test-api-key-123"
```

#### Create Order
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

#### Complete Order Flow
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

### 4. Using Postman

1. **Import Swagger Spec**: 
   - Open Postman
   - Click "Import"
   - Enter URL: `http://localhost:5000/apispec.json`
   - Or download the spec and import the file

2. **Set API Key**:
   - Create an environment variable `api_key` with value `test-api-key-123`
   - Or manually add header `X-API-Key: test-api-key-123` to each request

3. **Test Endpoints**: Use the imported collection

## Test Scenarios

### Scenario 1: Browse Inventory
1. GET `/api/inventory/books` - List all books
2. GET `/api/inventory/books/book-001` - Get specific book details
3. GET `/api/inventory/books/book-001/stock?quantity=5` - Check stock availability

### Scenario 2: Create and Process Order
1. POST `/api/sales/orders` - Create a new order
2. POST `/api/sales/orders/{order_id}/payment` - Process payment
3. POST `/api/delivery/orders/{order_id}` - Create delivery record
4. PUT `/api/delivery/orders/{order_id}/status` - Update delivery status

### Scenario 3: Complete Order Flow (Integration)
1. POST `/api/orders/complete` - Complete workflow (inventory → sales → delivery)
2. GET `/api/orders/{order_id}/status` - Get complete order status

### Scenario 4: Error Handling
1. Try accessing without API key (should get 401)
2. Try accessing non-existent book (should get 404)
3. Try ordering more than available stock (should get 400)
4. Try creating order with invalid data (should get 400)

## Running Unit Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_inventory.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# View coverage report
# Open htmlcov/index.html in browser
```

## Expected Test Results

All tests should pass:
- ✅ Inventory Service: 12 tests
- ✅ Sales Service: 8 tests  
- ✅ Delivery Service: 8 tests
- ✅ Integration: 3 tests

Total: ~31 tests

## API Key Reference

- `test-api-key-123` - Admin key (for all operations)
- `demo-api-key-456` - User key (for all operations)

Both keys work the same way in this implementation.


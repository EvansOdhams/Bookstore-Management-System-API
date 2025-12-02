# Quick Test: Get Delivery Status

## The Issue
You're using `book-001` which is a **book ID**, but the delivery endpoint needs an **order ID**.

## Solution: Get a Valid Order ID First

### Option 1: Use Complete Order Flow (Easiest!)

This creates an order AND delivery automatically:

1. **Go to Integration section** in Swagger
2. **Click** `POST /api/orders/complete`
3. **Click** "Try it out"
4. **Enter this JSON:**
   ```json
   {
     "customer_name": "Test Customer",
     "customer_email": "test@example.com",
     "items": [
       {
         "book_id": "book-001",
         "quantity": 1
       }
     ],
     "shipping_address": "123 Main Street"
   }
   ```
5. **Click** "Execute"
6. **Copy the `order.id`** from the response (it will be a UUID like `a1b2c3d4-e5f6-7890-abcd-ef1234567890`)
7. **Now use that order_id** in the delivery GET endpoint!

### Option 2: Create Order Manually

1. **Go to Sales section**
2. **Click** `POST /api/sales/orders`
3. **Click** "Try it out"
4. **Enter this JSON:**
   ```json
   {
     "customer_name": "Test Customer",
     "customer_email": "test@example.com",
     "items": [
       {
         "book_id": "book-001",
         "quantity": 1,
         "unit_price": 12.99
       }
     ],
     "shipping_address": "123 Main Street"
   }
   ```
5. **Click** "Execute"
6. **Copy the `order.id`** from response
7. **Process payment** (optional but recommended):
   - Go to `POST /api/sales/orders/{order_id}/payment`
   - Use the order_id you copied
   - Click "Execute"
8. **Create delivery**:
   - Go to `POST /api/delivery/orders/{order_id}`
   - Use the order_id
   - Enter JSON:
     ```json
     {
       "shipping_address": "123 Main Street"
     }
     ```
   - Click "Execute"
9. **Now get delivery status**:
   - Go to `GET /api/delivery/orders/{order_id}`
   - Use the same order_id
   - Click "Execute"
   - ✅ Should work!

## Step-by-Step Visual Guide

### Step 1: Create Complete Order
```
Integration → POST /api/orders/complete
↓
Execute with book_id: "book-001"
↓
Response contains: order.id = "abc-123-def-456"
```

### Step 2: Get Delivery Status
```
Delivery → GET /api/delivery/orders/{order_id}
↓
Paste: "abc-123-def-456" (NOT "book-001"!)
↓
Execute
↓
✅ Success! Delivery details shown
```

## Common Mistakes

❌ **Wrong**: Using `book-001` as order_id
✅ **Right**: Use the UUID from order creation (e.g., `386561b2-7227-4ceb-a551-8a4952154a67`)

❌ **Wrong**: Trying to get delivery before creating it
✅ **Right**: Create delivery first, then get it

## Quick PowerShell Test

Run this to create an order and test delivery:

```powershell
# Step 1: Create complete order
$headers = @{"X-API-Key" = "test-api-key-123"; "Content-Type" = "application/json"}
$body = @{
    customer_name = "Test User"
    customer_email = "test@example.com"
    items = @(@{book_id = "book-001"; quantity = 1})
    shipping_address = "123 Test St"
} | ConvertTo-Json -Depth 10

$result = Invoke-RestMethod -Uri "http://localhost:5000/api/orders/complete" -Method POST -Headers $headers -Body $body
$orderId = $result.order.id

Write-Host "Order ID: $orderId" -ForegroundColor Green

# Step 2: Get delivery status
$delivery = Invoke-RestMethod -Uri "http://localhost:5000/api/delivery/orders/$orderId" -Headers @{"X-API-Key" = "test-api-key-123"}
Write-Host "Delivery Status: $($delivery.status)" -ForegroundColor Green
Write-Host "Tracking Number: $($delivery.tracking_number)" -ForegroundColor Green
```

## Understanding the IDs

- **Book ID**: `book-001`, `book-002`, etc. (from inventory)
- **Order ID**: UUID like `386561b2-7227-4ceb-a551-8a4952154a67` (created when you place an order)
- **Delivery ID**: UUID like `c5d59e8d-cb67-4680-b415-49332117f9c8` (created when delivery is created)

The delivery endpoint uses **Order ID**, not Book ID!


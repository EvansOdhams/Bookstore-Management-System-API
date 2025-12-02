# PowerShell Script to Test Bookstore API
# Make sure the server is running on http://localhost:5000

$apiKey = "test-api-key-123"
$baseUrl = "http://localhost:5000"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Testing Bookstore Management System API" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "1. Testing Health Check..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/health" -Method GET
    Write-Host "   ✓ Health Check: $($response.status)" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Health Check Failed: $_" -ForegroundColor Red
}
Write-Host ""

# Test 2: Get All Books
Write-Host "2. Testing Get All Books..." -ForegroundColor Yellow
try {
    $headers = @{"X-API-Key" = $apiKey}
    $response = Invoke-RestMethod -Uri "$baseUrl/api/inventory/books" -Headers $headers -Method GET
    Write-Host "   ✓ Found $($response.count) books" -ForegroundColor Green
    Write-Host "   First book: $($response.books[0].title)" -ForegroundColor Gray
} catch {
    Write-Host "   ✗ Get Books Failed: $_" -ForegroundColor Red
}
Write-Host ""

# Test 3: Get Specific Book
Write-Host "3. Testing Get Book by ID..." -ForegroundColor Yellow
try {
    $headers = @{"X-API-Key" = $apiKey}
    $response = Invoke-RestMethod -Uri "$baseUrl/api/inventory/books/book-001" -Headers $headers -Method GET
    Write-Host "   ✓ Book found: $($response.title)" -ForegroundColor Green
    Write-Host "   Stock: $($response.stock_quantity)" -ForegroundColor Gray
} catch {
    Write-Host "   ✗ Get Book Failed: $_" -ForegroundColor Red
}
Write-Host ""

# Test 4: Create Order
Write-Host "4. Testing Create Order..." -ForegroundColor Yellow
try {
    $headers = @{
        "X-API-Key" = $apiKey
        "Content-Type" = "application/json"
    }
    $body = @{
        customer_name = "Test Customer"
        customer_email = "test@example.com"
        items = @(
            @{
                book_id = "book-001"
                quantity = 1
                unit_price = 12.99
            }
        )
        shipping_address = "123 Test Street"
    } | ConvertTo-Json -Depth 10
    
    $response = Invoke-RestMethod -Uri "$baseUrl/api/sales/orders" -Headers $headers -Method POST -Body $body
    $orderId = $response.order.id
    Write-Host "   ✓ Order created: $orderId" -ForegroundColor Green
    Write-Host "   Total: `$$($response.order.total_amount)" -ForegroundColor Gray
    
    # Test 5: Process Payment
    Write-Host "5. Testing Process Payment..." -ForegroundColor Yellow
    try {
        $paymentBody = @{
            payment_method = "credit_card"
        } | ConvertTo-Json
        
        $paymentResponse = Invoke-RestMethod -Uri "$baseUrl/api/sales/orders/$orderId/payment" -Headers $headers -Method POST -Body $paymentBody
        Write-Host "   ✓ Payment processed: $($paymentResponse.payment_id)" -ForegroundColor Green
    } catch {
        Write-Host "   ✗ Payment Failed: $_" -ForegroundColor Red
    }
    Write-Host ""
    
    # Test 6: Create Delivery
    Write-Host "6. Testing Create Delivery..." -ForegroundColor Yellow
    try {
        $deliveryBody = @{
            shipping_address = "123 Test Street"
            carrier = "Standard Shipping"
        } | ConvertTo-Json
        
        $deliveryResponse = Invoke-RestMethod -Uri "$baseUrl/api/delivery/orders/$orderId" -Headers $headers -Method POST -Body $deliveryBody
        Write-Host "   ✓ Delivery created: $($deliveryResponse.delivery.tracking_number)" -ForegroundColor Green
    } catch {
        Write-Host "   ✗ Delivery Failed: $_" -ForegroundColor Red
    }
    Write-Host ""
    
} catch {
    Write-Host "   ✗ Create Order Failed: $_" -ForegroundColor Red
}
Write-Host ""

# Test 7: Complete Order Flow (Integration)
Write-Host "7. Testing Complete Order Flow..." -ForegroundColor Yellow
try {
    $headers = @{
        "X-API-Key" = $apiKey
        "Content-Type" = "application/json"
    }
    $body = @{
        customer_name = "Integration Test"
        customer_email = "integration@example.com"
        items = @(
            @{
                book_id = "book-002"
                quantity = 1
            }
        )
        shipping_address = "456 Integration Ave"
    } | ConvertTo-Json -Depth 10
    
    $response = Invoke-RestMethod -Uri "$baseUrl/api/orders/complete" -Headers $headers -Method POST -Body $body
    Write-Host "   ✓ Complete flow successful!" -ForegroundColor Green
    Write-Host "   Order ID: $($response.order.id)" -ForegroundColor Gray
    Write-Host "   Payment ID: $($response.payment_id)" -ForegroundColor Gray
    Write-Host "   Delivery Status: $($response.delivery.status)" -ForegroundColor Gray
} catch {
    Write-Host "   ✗ Complete Flow Failed: $_" -ForegroundColor Red
    Write-Host "   Error details: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Testing Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan


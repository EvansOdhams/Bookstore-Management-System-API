# Step-by-Step Swagger UI Testing Guide

## Important: Test Order Matters!

You need to **create data before you can retrieve it**. Follow these steps in order:

## Step 1: Get Books (Inventory)

1. Go to **Inventory** section
2. Click on `GET /api/inventory/books`
3. Click **"Try it out"**
4. Click **"Execute"**
5. **Copy a book ID** from the response (e.g., `book-001`)

## Step 2: Create an Order (Sales)

1. Go to **Sales** section
2. Click on `POST /api/sales/orders`
3. Click **"Try it out"**
4. Fill in the request body:
   ```json
   {
     "customer_name": "John Doe",
     "customer_email": "john@example.com",
     "items": [
       {
         "book_id": "book-001",
         "quantity": 1,
         "unit_price": 12.99
       }
     ],
     "shipping_address": "123 Main St, City, Country"
   }
   ```
5. Click **"Execute"**
6. **Copy the order ID** from the response (e.g., `a1b2c3d4-e5f6-7890-abcd-ef1234567890`)

## Step 3: Process Payment (Sales)

1. Still in **Sales** section
2. Click on `POST /api/sales/orders/{order_id}/payment`
3. Click **"Try it out"**
4. Paste the **order_id** from Step 2
5. Request body (optional):
   ```json
   {
     "payment_method": "credit_card"
   }
   ```
6. Click **"Execute"**

## Step 4: Create Delivery Record

1. Go to **Delivery** section
2. Click on `POST /api/delivery/orders/{order_id}`
3. Click **"Try it out"**
4. Paste the **order_id** from Step 2
5. Fill in request body:
   ```json
   {
     "shipping_address": "123 Main St, City, Country",
     "carrier": "Standard Shipping"
   }
   ```
6. Click **"Execute"**
7. **Copy the delivery ID** from response

## Step 5: Get Delivery Status (NOW THIS WILL WORK!)

1. Still in **Delivery** section
2. Click on `GET /api/delivery/orders/{order_id}`
3. Click **"Try it out"**
4. Paste the **order_id** from Step 2
5. Click **"Execute"**
6. ✅ You should now see the delivery details!

## Alternative: Use Complete Order Flow (Easier!)

Instead of steps 2-4, you can use the integrated endpoint:

1. Go to **Integration** section
2. Click on `POST /api/orders/complete`
3. Click **"Try it out"**
4. Fill in request body:
   ```json
   {
     "customer_name": "Jane Smith",
     "customer_email": "jane@example.com",
     "items": [
       {
         "book_id": "book-001",
         "quantity": 1
       }
     ],
     "shipping_address": "456 Oak Ave, City, Country"
   }
   ```
5. Click **"Execute"**
6. This creates: Order → Payment → Delivery automatically!
7. **Copy the order_id** from response
8. Now you can use `GET /api/delivery/orders/{order_id}` with that order_id

## Common Issues

### Issue: "Delivery not found" (404)
**Solution**: You need to create a delivery record first using `POST /api/delivery/orders/{order_id}`

### Issue: Request Stuck Loading
**Solution**: 
1. Check if server is running: http://localhost:5000/health
2. Make sure you've authorized with API key
3. Try refreshing the Swagger page
4. Check browser console for errors (F12)

### Issue: "Order not found" (404)
**Solution**: Create an order first using `POST /api/sales/orders`

### Issue: "Insufficient stock" (400)
**Solution**: Use a different book_id or reduce quantity. Check stock with `GET /api/inventory/books/{id}/stock`

## Quick Test Sequence

**Fastest way to test delivery endpoint:**

1. Use `POST /api/orders/complete` with any book_id
2. Copy the order_id from response
3. Use `GET /api/delivery/orders/{order_id}` with that order_id
4. ✅ Success!

## Testing Checklist

- [ ] Health check works
- [ ] Can get all books
- [ ] Can get specific book
- [ ] Can create order
- [ ] Can process payment
- [ ] Can create delivery
- [ ] Can get delivery status
- [ ] Can update delivery status
- [ ] Complete order flow works
- [ ] Get complete order status works


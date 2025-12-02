# Bookstore Management System API

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask)](https://flask.palletsprojects.com/)
[![Tests](https://img.shields.io/badge/Tests-Pytest-0A9EDC?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/License-Educational-blue)](#license)

A fully documented RESTful API that orchestrates **Inventory**, **Sales**, and **Delivery** subsystems for a fictional bookstore.  
It includes mock integrations, API-key authentication, Swagger UI, and automated tests so you can focus on experimenting with service integration patterns.

---

## Table of Contents

1. [Features](#features)
2. [Architecture & Tech Stack](#architecture--tech-stack)
3. [Quick Start](#quick-start)
4. [Running the API](#running-the-api)
5. [API Documentation & Authentication](#api-documentation--authentication)
6. [Sample Requests](#sample-requests)
7. [Testing](#testing)
8. [Project Structure](#project-structure)
9. [Mock Data](#mock-data)
10. [License](#license)

---

## Features

- **Inventory Service** – CRUD-style book catalogue with stock tracking.
- **Sales Service** – Order placement, payment simulation, and lifecycle states.
- **Delivery Service** – Shipment creation, tracking numbers, and status updates.
- **Integrated Workflow** – `/api/orders/complete` performs stock check → reserve → order → payment → delivery in a single call.
- **API Key Authentication** – Lightweight security via `X-API-Key` header.
- **Swagger UI** – Interactive docs powered by Flasgger.
- **JSON-backed Mock Services** – Simple persistence for demos and testing.
- **Pytest Suite** – Unit + integration coverage for core flows.

---

## Architecture & Tech Stack

| Layer        | Details |
|--------------|---------|
| Framework    | Flask 3 + Flasgger (Swagger) |
| Auth         | Header-based API Key (`X-API-Key`) |
| Persistence  | JSON files (`data/books.json`, `orders.json`, `deliveries.json`) |
| Tooling      | Pytest, Waitress (production-ready WSGI), PowerShell/cURL scripts |

Each subsystem exposes a service class (`src/services`) and a route blueprint (`src/api/routes`).  
This keeps domain logic separate from the HTTP layer and makes the project easy to extend.

---

## Quick Start

### 1. Prerequisites
- Python **3.11+**
- `pip`

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set environment variables (optional)
```bash
set FLASK_ENV=development
set API_KEYS=test-api-key-123
```

---

## Running the API

### Development server (auto-reload, debug on)
```bash
python src/api/app.py
```
Server: http://localhost:5000

### Production-ready server (Waitress WSGI)
```bash
python run_production.py
```
Server logs include health, docs, and default API keys for quick reference.

---

## API Documentation & Authentication

- Swagger UI: **http://localhost:5000/apidocs**
- Raw OpenAPI spec: **http://localhost:5000/apispec.json**

All routes (except `/` and `/health`) require an API key:
```
X-API-Key: test-api-key-123
```
Use Swagger’s **Authorize** button or include the header in Postman/cURL requests.

---

## Sample Requests

```bash
# List all books in inventory
curl -H "X-API-Key: test-api-key-123" \
     http://localhost:5000/api/inventory/books

# Complete an order (inventory → sales → delivery)
curl -X POST http://localhost:5000/api/orders/complete \
     -H "Content-Type: application/json" \
     -H "X-API-Key: test-api-key-123" \
     -d '{
           "customer_name": "Jane Doe",
           "customer_email": "jane@example.com",
           "items": [{"book_id": "book-001", "quantity": 1}],
           "shipping_address": "456 Oak Ave"
         }'
```

More scripted examples are available in `test_api_examples.sh` and `test_api.ps1`.

---

## Testing

```bash
# Run all unit + integration tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=src --cov-report=html
```

Tests cover inventory operations, order/payment logic, delivery lifecycle, and the end-to-end integration path.

---

## Project Structure

```
bookstore-api/
├── src/
│   ├── api/
│   │   ├── routes/        # Flask blueprints (inventory, sales, delivery, integration)
│   │   ├── auth.py        # API key guard
│   │   └── app.py         # Flask app factory + Swagger config
│   ├── services/          # Domain logic + JSON persistence helpers
│   └── models/            # Dataclasses for Book, Order, Delivery
├── data/                  # Mock JSON datasets
├── tests/                 # Pytest suites
├── docs & guides:
│   ├── QUICK_START.md
│   ├── TESTING_GUIDE.md
│   ├── PRODUCTION_SETUP.md
│   └── DEPLOYMENT_GUIDE.md
├── run_production.py      # Waitress entrypoint
├── requirements.txt
└── README.md
```

---

## Mock Data

The repo ships with ready-to-use JSON fixtures located in `data/`:

| File | Description |
|------|-------------|
| `books.json` | 8 curated titles (fiction + tech) with prices & stock |
| `orders.json` | Starts empty; populated as you interact with the Sales service |
| `deliveries.json` | Starts empty; populated by Delivery service |

Replace these with your own datasets or wire real databases for advanced scenarios.

---

## License

Educational use only. Feel free to fork, extend, and experiment.

---

Happy building! If you publish improvements, open a PR or tag me at [@EvansOdhams](https://github.com/EvansOdhams). ✨


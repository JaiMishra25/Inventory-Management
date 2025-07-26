# Inventory Management Tool - API Documentation

## Overview

The Inventory Management Tool provides RESTful APIs for managing inventory for small businesses. All endpoints return JSON responses and use standard HTTP status codes.

**Base URL**: `http://localhost:8080`

## Authentication

The API uses JWT (JSON Web Token) authentication. Most endpoints require authentication via the `Authorization` header:

```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### 1. User Registration

**Endpoint**: `POST /register`

**Description**: Register a new user account.

**Request Body**:
```json
{
  "username": "string",
  "password": "string"
}
```

**Constraints**:
- `username`: 3-50 characters, must be unique
- `password`: 6-100 characters

**Response**:
- **201 Created**: User registered successfully
- **409 Conflict**: Username already exists
- **422 Unprocessable Entity**: Validation error

**Example Response (201)**:
```json
{
  "message": "User registered successfully",
  "user_id": 1
}
```

### 2. User Login

**Endpoint**: `POST /login`

**Description**: Authenticate user and receive JWT token.

**Request Body**:
```json
{
  "username": "string",
  "password": "string"
}
```

**Response**:
- **200 OK**: Login successful
- **401 Unauthorized**: Invalid credentials
- **422 Unprocessable Entity**: Validation error

**Example Response (200)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Add Product

**Endpoint**: `POST /products`

**Description**: Add a new product to inventory.

**Authentication**: Required

**Request Body**:
```json
{
  "name": "string",
  "type": "string",
  "sku": "string",
  "image_url": "string (optional)",
  "description": "string (optional)",
  "quantity": "integer",
  "price": "number"
}
```

**Constraints**:
- `name`: 1-100 characters
- `type`: 1-50 characters
- `sku`: 1-50 characters, must be unique
- `quantity`: Non-negative integer
- `price`: Positive number

**Response**:
- **201 Created**: Product added successfully
- **409 Conflict**: SKU already exists
- **401 Unauthorized**: Missing or invalid token
- **422 Unprocessable Entity**: Validation error

**Example Response (201)**:
```json
{
  "product_id": 1,
  "message": "Product added successfully"
}
```

### 4. Update Product Quantity

**Endpoint**: `PUT /products/{id}/quantity`

**Description**: Update the quantity of a specific product.

**Authentication**: Required

**Path Parameters**:
- `id`: Product ID (integer)

**Request Body**:
```json
{
  "quantity": "integer"
}
```

**Constraints**:
- `quantity`: Non-negative integer

**Response**:
- **200 OK**: Quantity updated successfully
- **404 Not Found**: Product not found
- **401 Unauthorized**: Missing or invalid token
- **422 Unprocessable Entity**: Validation error

**Example Response (200)**:
```json
{
  "id": 1,
  "name": "iPhone 15 Pro",
  "quantity": 30,
  "message": "Product quantity updated successfully"
}
```

### 5. Get All Products

**Endpoint**: `GET /products`

**Description**: Retrieve all products with pagination.

**Authentication**: Required

**Query Parameters**:
- `page` (optional): Page number (default: 1, minimum: 1)
- `per_page` (optional): Items per page (default: 10, minimum: 1, maximum: 100)

**Response**:
- **200 OK**: Products retrieved successfully
- **401 Unauthorized**: Missing or invalid token

**Example Response (200)**:
```json
{
  "products": [
    {
      "id": 1,
      "name": "iPhone 15 Pro",
      "type": "Electronics",
      "sku": "IPH15PRO-001",
      "image_url": "https://example.com/iphone15pro.jpg",
      "description": "Latest iPhone with titanium design",
      "quantity": 30,
      "price": 1199.99,
      "created_at": "2024-01-15T10:30:00",
      "updated_at": "2024-01-15T11:45:00"
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 10
}
```

### 6. Get Product by ID

**Endpoint**: `GET /products/{id}`

**Description**: Retrieve a specific product by its ID.

**Authentication**: Required

**Path Parameters**:
- `id`: Product ID (integer)

**Response**:
- **200 OK**: Product retrieved successfully
- **404 Not Found**: Product not found
- **401 Unauthorized**: Missing or invalid token

**Example Response (200)**:
```json
{
  "id": 1,
  "name": "iPhone 15 Pro",
  "type": "Electronics",
  "sku": "IPH15PRO-001",
  "image_url": "https://example.com/iphone15pro.jpg",
  "description": "Latest iPhone with titanium design",
  "quantity": 30,
  "price": 1199.99,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T11:45:00"
}
```

### 7. Root Endpoint

**Endpoint**: `GET /`

**Description**: Get API information and available documentation links.

**Response**:
- **200 OK**: API information

**Example Response (200)**:
```json
{
  "message": "Inventory Management Tool API",
  "version": "1.0.0",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

## Error Responses

### Standard Error Format

All error responses follow this format:

```json
{
  "detail": "Error message description"
}
```

### HTTP Status Codes

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Missing or invalid authentication
- **404 Not Found**: Resource not found
- **409 Conflict**: Resource already exists (e.g., duplicate username or SKU)
- **422 Unprocessable Entity**: Validation error

### Common Error Examples

**401 Unauthorized**:
```json
{
  "detail": "Could not validate credentials"
}
```

**404 Not Found**:
```json
{
  "detail": "Product not found"
}
```

**409 Conflict**:
```json
{
  "detail": "Username already registered"
}
```

**422 Unprocessable Entity**:
```json
{
  "detail": [
    {
      "loc": ["body", "username"],
      "msg": "ensure this value has at least 3 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider implementing rate limiting to prevent abuse.

## CORS

The API supports Cross-Origin Resource Sharing (CORS) and is configured to allow requests from any origin. For production, consider restricting this to specific domains.

## Security Considerations

1. **JWT Tokens**: Tokens expire after 30 minutes
2. **Password Hashing**: Passwords are hashed using bcrypt
3. **Input Validation**: All inputs are validated using Pydantic
4. **SQL Injection Protection**: Uses SQLAlchemy ORM with parameterized queries

## Testing

Use the provided `test_api.py` script to test all endpoints:

```bash
python test_api.py
```

Or use the Postman collection (`postman_collection.json`) for manual testing.

## Interactive Documentation

- **Swagger UI**: `http://localhost:8080/docs`
- **ReDoc**: `http://localhost:8080/redoc`

These provide interactive documentation where you can test endpoints directly in the browser. 
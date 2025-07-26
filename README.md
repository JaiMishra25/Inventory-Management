# Inventory Management Tool

A REST API backend application for managing inventory for small businesses. Built with FastAPI, SQLAlchemy, and SQLite.

## Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **Product Management**: Add, update, and retrieve products with inventory tracking
- **RESTful APIs**: Clean, well-documented REST endpoints
- **Database**: SQLite database with SQLAlchemy ORM
- **Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Security**: JWT tokens, password hashing, and input validation

## API Endpoints

### Authentication
- `POST /register` - Register a new user
- `POST /login` - Authenticate user and get JWT token

### Products
- `POST /products` - Add a new product (requires authentication)
- `GET /products` - Get all products with pagination (requires authentication)
- `GET /products/{id}` - Get a specific product (requires authentication)
- `PUT /products/{id}/quantity` - Update product quantity (requires authentication)

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd inventory-management
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
   ```

5. **Access the API**
   - API Base URL: `http://localhost:8080`
   - Interactive API Documentation: `http://localhost:8080/docs`
   - Alternative Documentation: `http://localhost:8080/redoc`

## Database Schema

The application uses SQLite with the following schema:

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);
```

### Products Table
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    type VARCHAR NOT NULL,
    sku VARCHAR UNIQUE NOT NULL,
    image_url VARCHAR,
    description TEXT,
    quantity INTEGER DEFAULT 0 NOT NULL,
    price FLOAT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);
```

## API Usage Examples

### 1. Register a User
```bash
curl -X POST "http://localhost:8080/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "john_doe",
       "password": "securepassword123"
     }'
```

### 2. Login
```bash
curl -X POST "http://localhost:8080/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "john_doe",
       "password": "securepassword123"
     }'
```

### 3. Add a Product
```bash
curl -X POST "http://localhost:8080/products" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -d '{
       "name": "iPhone 15",
       "type": "Electronics",
       "sku": "IPH15-001",
       "image_url": "https://example.com/iphone15.jpg",
       "description": "Latest iPhone model",
       "quantity": 10,
       "price": 999.99
     }'
```

### 4. Update Product Quantity
```bash
curl -X PUT "http://localhost:8080/products/1/quantity" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -d '{
       "quantity": 15
     }'
```

### 5. Get All Products
```bash
curl -X GET "http://localhost:8080/products?page=1&per_page=10" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Testing

Run the provided test script to verify all endpoints:

```bash
python test_api.py
```

The test script will:
1. Register a test user
2. Login and get JWT token
3. Add a test product
4. Update product quantity
5. Retrieve products and verify the update

## Security Features

- **Password Hashing**: Uses bcrypt for secure password storage
- **JWT Authentication**: Secure token-based authentication
- **Input Validation**: Comprehensive request validation using Pydantic
- **SQL Injection Protection**: Uses SQLAlchemy ORM with parameterized queries
- **CORS Support**: Configured for cross-origin requests

## Error Handling

The API provides comprehensive error handling with appropriate HTTP status codes:

- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Missing or invalid authentication
- `404 Not Found`: Resource not found
- `409 Conflict`: Duplicate resource (e.g., existing username or SKU)
- `422 Unprocessable Entity`: Validation errors

## Development

### Project Structure
```
inventory-management/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── database.py      # Database configuration
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   └── auth.py          # Authentication utilities
├── requirements.txt     # Python dependencies
├── test_api.py         # API test script
└── README.md           # This file
```

### Adding New Features

1. **New Models**: Add to `app/models.py`
2. **New Schemas**: Add to `app/schemas.py`
3. **New Endpoints**: Add to `app/main.py`
4. **Database Migrations**: Use Alembic for schema changes

## Production Deployment

For production deployment, consider:

1. **Environment Variables**: Move sensitive configuration to environment variables
2. **Database**: Use PostgreSQL or MySQL instead of SQLite
3. **Security**: Change the JWT secret key
4. **HTTPS**: Enable SSL/TLS
5. **Rate Limiting**: Implement API rate limiting
6. **Logging**: Add comprehensive logging
7. **Monitoring**: Add health checks and monitoring

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

For questions or issues, please open an issue on the GitHub repository. 
-- Inventory Management Tool Database Schema
-- This script creates the database tables for the Inventory Management Tool

-- Users table for authentication
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);

-- Products table for inventory management
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    sku VARCHAR(50) UNIQUE NOT NULL,
    image_url VARCHAR(500),
    description TEXT,
    quantity INTEGER DEFAULT 0 NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_products_name ON products(name);
CREATE INDEX IF NOT EXISTS idx_products_sku ON products(sku);
CREATE INDEX IF NOT EXISTS idx_products_type ON products(type);

-- Insert sample data (optional)
-- Uncomment the following lines to add sample data

-- Sample user
-- INSERT INTO users (username, hashed_password) VALUES 
-- ('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQe.'); -- password: admin123

-- Sample products
-- INSERT INTO products (name, type, sku, image_url, description, quantity, price) VALUES 
-- ('iPhone 15 Pro', 'Electronics', 'IPH15PRO-001', 'https://example.com/iphone15pro.jpg', 'Latest iPhone with titanium design', 25, 1199.99),
-- ('MacBook Air M2', 'Electronics', 'MBA-M2-001', 'https://example.com/macbook-air.jpg', 'Lightweight laptop with M2 chip', 15, 1299.99),
-- ('Wireless Headphones', 'Electronics', 'WH-001', 'https://example.com/headphones.jpg', 'Noise-cancelling wireless headphones', 50, 199.99),
-- ('Office Chair', 'Furniture', 'OC-001', 'https://example.com/chair.jpg', 'Ergonomic office chair', 30, 299.99),
-- ('Coffee Maker', 'Appliances', 'CM-001', 'https://example.com/coffee-maker.jpg', 'Automatic coffee maker', 20, 89.99);

-- Create trigger to update the updated_at timestamp
CREATE TRIGGER IF NOT EXISTS update_users_updated_at 
    AFTER UPDATE ON users
    FOR EACH ROW
    BEGIN
        UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_products_updated_at 
    AFTER UPDATE ON products
    FOR EACH ROW
    BEGIN
        UPDATE products SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END; 
from datetime import timedelta
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app.models import Base, User, Product
from app.schemas import (
    UserCreate, UserLogin, Token, ProductCreate, ProductUpdate, 
    Product as ProductSchema, ProductResponse, QuantityUpdateResponse, 
    ProductsListResponse
)
from app.auth import (
    get_password_hash, authenticate_user, create_access_token, 
    ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Inventory Management Tool",
    description="A REST API for managing inventory for small businesses",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Inventory Management Tool API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.post("/register", response_model=dict, status_code=201)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    - **username**: Unique username (3-50 characters)
    - **password**: Password (6-100 characters)
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"message": "User registered successfully", "user_id": db_user.id}

@app.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token.
    
    - **username**: User's username
    - **password**: User's password
    """
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/products", response_model=ProductResponse, status_code=201)
async def add_product(
    product: ProductCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add a new product to inventory.
    
    - **name**: Product name
    - **type**: Product type/category
    - **sku**: Unique SKU code
    - **image_url**: Product image URL (optional)
    - **description**: Product description (optional)
    - **quantity**: Initial quantity
    - **price**: Product price
    """
    # Check if SKU already exists
    existing_product = db.query(Product).filter(Product.sku == product.sku).first()
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product with this SKU already exists"
        )
    
    # Create new product
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return {"product_id": db_product.id, "message": "Product added successfully"}

@app.put("/products/{product_id}/quantity", response_model=QuantityUpdateResponse)
async def update_product_quantity(
    product_id: int,
    quantity_update: ProductUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update product quantity.
    
    - **product_id**: ID of the product to update
    - **quantity**: New quantity value
    """
    # Find the product
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Update quantity
    product.quantity = quantity_update.quantity
    db.commit()
    db.refresh(product)
    
    return {
        "id": product.id,
        "name": product.name,
        "quantity": product.quantity,
        "message": "Product quantity updated successfully"
    }

@app.get("/products", response_model=ProductsListResponse)
async def get_products(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page")
):
    """
    Get all products with pagination.
    
    - **page**: Page number (default: 1)
    - **per_page**: Items per page (default: 10, max: 100)
    """
    # Calculate offset
    offset = (page - 1) * per_page
    
    # Get total count
    total = db.query(Product).count()
    
    # Get products with pagination
    products = db.query(Product).offset(offset).limit(per_page).all()
    
    return {
        "products": products,
        "total": total,
        "page": page,
        "per_page": per_page
    }

@app.get("/products/{product_id}", response_model=ProductSchema)
async def get_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific product by ID.
    
    - **product_id**: ID of the product to retrieve
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 
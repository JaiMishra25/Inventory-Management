from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Product schemas
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., min_length=1, max_length=50)
    sku: str = Field(..., min_length=1, max_length=50)
    image_url: Optional[str] = None
    description: Optional[str] = None
    quantity: int = Field(..., ge=0)
    price: float = Field(..., gt=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    quantity: int = Field(..., ge=0)

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Response schemas
class ProductResponse(BaseModel):
    product_id: int
    message: str

class QuantityUpdateResponse(BaseModel):
    id: int
    name: str
    quantity: int
    message: str

class ProductsListResponse(BaseModel):
    products: List[Product]
    total: int
    page: int
    per_page: int 
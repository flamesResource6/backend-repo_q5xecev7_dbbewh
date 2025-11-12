"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Optional, List
from datetime import datetime

# Core site schemas for EABL website

class Brand(BaseModel):
    name: str = Field(..., description="Brand name")
    category: str = Field(..., description="Category: Beer | Spirits | Non-Alcoholic")
    tagline: Optional[str] = Field(None, description="Short tagline")
    image: Optional[HttpUrl] = Field(None, description="Bottle/can image URL")
    color: Optional[str] = Field(None, description="Hex color representing brand accent")
    featured: bool = Field(default=False, description="Highlight on homepage")

class NewsPost(BaseModel):
    title: str
    summary: str
    image: Optional[HttpUrl] = None
    link: Optional[HttpUrl] = None
    published_at: Optional[datetime] = None
    tags: Optional[List[str]] = None

class InvestorMetric(BaseModel):
    revenue: float = Field(..., description="Annual revenue in billions KES")
    growth_percent: float = Field(..., description="YoY growth percentage")
    share_price: float = Field(..., description="Latest share price in KES")
    updated_at: Optional[datetime] = None
    report_url: Optional[HttpUrl] = None
    nse_url: Optional[HttpUrl] = None

class Location(BaseModel):
    name: str
    country: str
    city: Optional[str] = None
    address: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    photo: Optional[HttpUrl] = None

class Subscriber(BaseModel):
    email: EmailStr
    language: Optional[str] = Field(default="en", description="Preferred language code")

# Keep example schemas for reference
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True

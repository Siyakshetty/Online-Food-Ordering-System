from pydantic import BaseModel, Field
from typing import List, Optional


# =========================================================
# RESTAURANT SCHEMAS
# =========================================================

class RestaurantCreate(BaseModel):
    name: str
    image: str
    rating: float
    delivery_time: str
    cuisines: str
    location: str


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None
    rating: Optional[float] = None
    delivery_time: Optional[str] = None
    cuisines: Optional[str] = None
    location: Optional[str] = None


# =========================================================
# FOOD SCHEMAS
# =========================================================

class FoodCreate(BaseModel):
    restaurant_id: int
    name: str
    category: str
    price: float
    image: str
    description: str


class FoodUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    image: Optional[str] = None
    description: Optional[str] = None


# =========================================================
# ORDER ITEM SCHEMA
# =========================================================

class OrderItemCreate(BaseModel):
    food_id: int
    food_name: str
    quantity: int
    price: float

    selected_options: dict = Field(
        default_factory=dict
    )


# =========================================================
# ORDER CREATE
# =========================================================

class OrderCreate(BaseModel):
    customer_name: str
    phone: str
    address: str
    total_amount: float

    items: List[OrderItemCreate]


# =========================================================
# ORDER UPDATE
# =========================================================

class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    status: Optional[str] = None
    total_amount: Optional[float] = None
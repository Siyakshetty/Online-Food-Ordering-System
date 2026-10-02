from pydantic import BaseModel
from typing import List, Dict, Any


class OrderItemCreate(BaseModel):
    food_id: int
    food_name: str
    quantity: int
    price: float
    selected_options: Dict[str, Any] = {}


class OrderCreate(BaseModel):
    customer_name: str
    phone: str
    address: str
    total_amount: float
    items: List[OrderItemCreate]
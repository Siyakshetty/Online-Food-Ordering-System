from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    image = Column(String, nullable=False)
    rating = Column(Float, nullable=False)
    delivery_time = Column(String, nullable=False)
    cuisines = Column(String, nullable=False)
    location = Column(String, nullable=False)

    foods = relationship(
        "Food",
        back_populates="restaurant",
        cascade="all, delete-orphan"
    )


class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    image = Column(String, nullable=False)
    description = Column(String, default="")

    restaurant = relationship(
        "Restaurant",
        back_populates="foods"
    )

    options = relationship(
        "FoodOption",
        back_populates="food",
        cascade="all, delete-orphan"
    )


class FoodOption(Base):
    __tablename__ = "food_options"

    id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, ForeignKey("foods.id"))
    option_group = Column(String, nullable=False)
    option_name = Column(String, nullable=False)
    extra_price = Column(Float, default=0)

    food = relationship(
        "Food",
        back_populates="options"
    )


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(Text, nullable=False)

    total_amount = Column(Float, nullable=False)
    status = Column(String, default="Order Placed")

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.id"))
    food_id = Column(Integer, ForeignKey("foods.id"))

    food_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    selected_options = Column(Text, default="")

    order = relationship(
        "Order",
        back_populates="items"
    )
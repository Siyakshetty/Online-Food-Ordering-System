from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import json

from database import engine, SessionLocal, Base
from models import Restaurant, Food, FoodOption, Order, OrderItem

from schemas import (
    OrderCreate,
    RestaurantCreate,
    RestaurantUpdate,
    FoodCreate,
    FoodUpdate,
    OrderUpdate
)


# =========================================================
# DATABASE
# =========================================================

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Online Food Ordering System",
    description="Swiggy Style Online Food Ordering System API",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# =========================================================
# SEED DATABASE
# =========================================================

def seed_database():

    db = SessionLocal()

    try:

        if db.query(Restaurant).count() > 0:
            return

        # =================================================
        # RESTAURANTS
        # =================================================

        restaurants = [

            Restaurant(
                name="Andhra Gunpowder",
                image="https://images.unsplash.com/photo-1601050690597-df0568f70950",
                rating=4.5,
                delivery_time="25-30 mins",
                cuisines="South Indian, Biryani",
                location="Mysore"
            ),

            Restaurant(
                name="Paris Panini - Gourmet Sandwiches",
                image="https://images.unsplash.com/photo-1553909489-cd47e0ef937f",
                rating=4.4,
                delivery_time="20-25 mins",
                cuisines="Sandwiches, Fast Food",
                location="Mysore"
            ),

            Restaurant(
                name="Bakingo",
                image="https://images.unsplash.com/photo-1578985545062-69928b1d9587",
                rating=4.6,
                delivery_time="30-35 mins",
                cuisines="Cakes, Desserts",
                location="Mysore"
            ),

            Restaurant(
                name="Burger King",
                image="https://images.unsplash.com/photo-1571091718767-18b5b1457add",
                rating=4.3,
                delivery_time="20-25 mins",
                cuisines="Burgers, Fast Food",
                location="Mysore"
            ),

            Restaurant(
                name="Pizza Hut",
                image="https://images.unsplash.com/photo-1574071318508-1cdbab80d002",
                rating=4.2,
                delivery_time="25-30 mins",
                cuisines="Pizza, Italian",
                location="Mysore"
            ),

            Restaurant(
                name="The Dessert Heaven",
                image="https://images.unsplash.com/photo-1551024506-0bccd828d307",
                rating=4.5,
                delivery_time="25-30 mins",
                cuisines="Desserts, Cakes",
                location="Mysore"
            )
        ]

        db.add_all(restaurants)
        db.commit()

        for restaurant in restaurants:
            db.refresh(restaurant)

        # =================================================
        # FOODS
        # =================================================

        foods = [

            Food(
                restaurant_id=restaurants[0].id,
                name="Chicken Biryani",
                category="Biryani",
                price=220,
                image="https://images.unsplash.com/photo-1563379091339-03246963d96c",
                description="Aromatic basmati rice with spicy chicken"
            ),

            Food(
                restaurant_id=restaurants[0].id,
                name="Paneer Biryani",
                category="Biryani",
                price=190,
                image="https://images.unsplash.com/photo-1589302168068-964664d93dc0",
                description="Flavourful paneer biryani"
            ),

            Food(
                restaurant_id=restaurants[1].id,
                name="Classic Chicken Panini",
                category="Sandwiches",
                price=180,
                image="https://images.unsplash.com/photo-1528735602780-2552fd46c7af",
                description="Grilled chicken sandwich with cheese"
            ),

            Food(
                restaurant_id=restaurants[1].id,
                name="Veggie Panini",
                category="Sandwiches",
                price=150,
                image="https://images.unsplash.com/photo-1553909489-cd47e0ef937f",
                description="Fresh vegetables and cheese in grilled bread"
            ),

            Food(
                restaurant_id=restaurants[2].id,
                name="Chocolate Truffle Cake",
                category="Cakes",
                price=499,
                image="https://images.unsplash.com/photo-1578985545062-69928b1d9587",
                description="Rich chocolate truffle cake"
            ),

            Food(
                restaurant_id=restaurants[2].id,
                name="Red Velvet Cake",
                category="Cakes",
                price=549,
                image="https://images.unsplash.com/photo-1586788224331-947f68671cf1",
                description="Soft red velvet cake with cream cheese frosting"
            ),

            Food(
                restaurant_id=restaurants[3].id,
                name="Whopper",
                category="Burgers",
                price=199,
                image="https://images.unsplash.com/photo-1568901346375-23c9450c58cd",
                description="Classic Burger King Whopper"
            ),

            Food(
                restaurant_id=restaurants[3].id,
                name="Chicken Burger",
                category="Burgers",
                price=179,
                image="https://images.unsplash.com/photo-1571091718767-18b5b1457add",
                description="Crispy chicken burger"
            ),

            Food(
                restaurant_id=restaurants[4].id,
                name="Margherita Pizza",
                category="Pizza",
                price=299,
                image="https://images.unsplash.com/photo-1574071318508-1cdbab80d002",
                description="Classic tomato and mozzarella pizza"
            ),

            Food(
                restaurant_id=restaurants[4].id,
                name="Farmhouse Pizza",
                category="Pizza",
                price=399,
                image="https://images.unsplash.com/photo-1565299624946-b28f40a0ae38",
                description="Loaded vegetable farmhouse pizza"
            ),

            Food(
                restaurant_id=restaurants[5].id,
                name="Chocolate Brownie",
                category="Desserts",
                price=149,
                image="https://images.unsplash.com/photo-1564355808539-22fda35bed7e",
                description="Warm chocolate brownie"
            ),

            Food(
                restaurant_id=restaurants[5].id,
                name="Chocolate Sundae",
                category="Desserts",
                price=129,
                image="https://images.unsplash.com/photo-1551024506-0bccd828d307",
                description="Creamy chocolate sundae"
            )
        ]

        db.add_all(foods)
        db.commit()

    finally:
        db.close()


seed_database()


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Online Food Ordering System API is running",
        "docs": "/docs"
    }


# =========================================================
# RESTAURANTS
# =========================================================


# GET ALL RESTAURANTS
@app.get("/restaurants")
def get_restaurants(
    db: Session = Depends(get_db)
):

    restaurants = db.query(Restaurant).all()

    return restaurants


# GET ONE RESTAURANT
@app.get("/restaurants/{restaurant_id}")
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db)
):

    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id
    ).first()

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    return restaurant


# POST RESTAURANT
@app.post("/restaurants")
def create_restaurant(
    restaurant_data: RestaurantCreate,
    db: Session = Depends(get_db)
):

    restaurant = Restaurant(
        name=restaurant_data.name,
        image=restaurant_data.image,
        rating=restaurant_data.rating,
        delivery_time=restaurant_data.delivery_time,
        cuisines=restaurant_data.cuisines,
        location=restaurant_data.location
    )

    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)

    return {
        "message": "Restaurant created successfully",
        "restaurant": restaurant
    }


# PUT RESTAURANT
@app.put("/restaurants/{restaurant_id}")
def update_restaurant(
    restaurant_id: int,
    restaurant_data: RestaurantUpdate,
    db: Session = Depends(get_db)
):

    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id
    ).first()

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    if hasattr(restaurant_data, "model_dump"):
        data = restaurant_data.model_dump(
            exclude_unset=True
        )
    else:
        data = restaurant_data.dict(
            exclude_unset=True
        )

    for key, value in data.items():
        setattr(restaurant, key, value)

    db.commit()
    db.refresh(restaurant)

    return {
        "message": "Restaurant updated successfully",
        "restaurant": restaurant
    }


# DELETE RESTAURANT
@app.delete("/restaurants/{restaurant_id}")
def delete_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db)
):

    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id
    ).first()

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    db.delete(restaurant)
    db.commit()

    return {
        "message": "Restaurant deleted successfully",
        "restaurant_id": restaurant_id
    }


# =========================================================
# FOOD
# =========================================================


# GET RESTAURANT FOODS
@app.get("/restaurants/{restaurant_id}/foods")
def get_restaurant_foods(
    restaurant_id: int,
    db: Session = Depends(get_db)
):

    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id
    ).first()

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    foods = db.query(Food).filter(
        Food.restaurant_id == restaurant_id
    ).all()

    result = []

    for food in foods:

        options = []

        for option in food.options:

            options.append({
                "id": option.id,
                "group": option.option_group,
                "name": option.option_name,
                "extra_price": option.extra_price
            })

        result.append({
            "id": food.id,
            "name": food.name,
            "category": food.category,
            "price": food.price,
            "image": food.image,
            "description": food.description,
            "options": options
        })

    return result


# GET ONE FOOD
@app.get("/foods/{food_id}")
def get_food(
    food_id: int,
    db: Session = Depends(get_db)
):

    food = db.query(Food).filter(
        Food.id == food_id
    ).first()

    if not food:
        raise HTTPException(
            status_code=404,
            detail="Food not found"
        )

    options = []

    for option in food.options:

        options.append({
            "id": option.id,
            "group": option.option_group,
            "name": option.option_name,
            "extra_price": option.extra_price
        })

    return {
        "id": food.id,
        "restaurant_id": food.restaurant_id,
        "name": food.name,
        "category": food.category,
        "price": food.price,
        "image": food.image,
        "description": food.description,
        "options": options
    }


# POST FOOD
@app.post("/foods")
def create_food(
    food_data: FoodCreate,
    db: Session = Depends(get_db)
):

    restaurant = db.query(Restaurant).filter(
        Restaurant.id == food_data.restaurant_id
    ).first()

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    food = Food(
        restaurant_id=food_data.restaurant_id,
        name=food_data.name,
        category=food_data.category,
        price=food_data.price,
        image=food_data.image,
        description=food_data.description
    )

    db.add(food)
    db.commit()
    db.refresh(food)

    return {
        "message": "Food created successfully",
        "food": food
    }


# PUT FOOD
@app.put("/foods/{food_id}")
def update_food(
    food_id: int,
    food_data: FoodUpdate,
    db: Session = Depends(get_db)
):

    food = db.query(Food).filter(
        Food.id == food_id
    ).first()

    if not food:
        raise HTTPException(
            status_code=404,
            detail="Food not found"
        )

    if hasattr(food_data, "model_dump"):
        data = food_data.model_dump(
            exclude_unset=True
        )
    else:
        data = food_data.dict(
            exclude_unset=True
        )

    for key, value in data.items():
        setattr(food, key, value)

    db.commit()
    db.refresh(food)

    return {
        "message": "Food updated successfully",
        "food": food
    }


# DELETE FOOD
@app.delete("/foods/{food_id}")
def delete_food(
    food_id: int,
    db: Session = Depends(get_db)
):

    food = db.query(Food).filter(
        Food.id == food_id
    ).first()

    if not food:
        raise HTTPException(
            status_code=404,
            detail="Food not found"
        )

    db.delete(food)
    db.commit()

    return {
        "message": "Food deleted successfully",
        "food_id": food_id
    }


# =========================================================
# ORDERS
# =========================================================


# POST ORDER
@app.post("/orders")
def place_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):

    new_order = Order(
        customer_name=order_data.customer_name,
        phone=order_data.phone,
        address=order_data.address,
        total_amount=order_data.total_amount,
        status="Order Placed"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in order_data.items:

        order_item = OrderItem(
            order_id=new_order.id,
            food_id=item.food_id,
            food_name=item.food_name,
            quantity=item.quantity,
            price=item.price,
            selected_options=json.dumps(
                item.selected_options
            )
        )

        db.add(order_item)

    db.commit()

    return {
        "message": "Order placed successfully",
        "order_id": new_order.id,
        "status": new_order.status,
        "total": new_order.total_amount
    }


# GET ALL ORDERS
@app.get("/orders")
def get_orders(
    db: Session = Depends(get_db)
):

    orders = db.query(Order).all()

    return orders


# GET ONE ORDER
@app.get("/orders/{order_id}")
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):

    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {
        "id": order.id,
        "customer_name": order.customer_name,
        "phone": order.phone,
        "address": order.address,
        "total_amount": order.total_amount,
        "status": order.status
    }


# PUT ORDER
@app.put("/orders/{order_id}")
def update_order(
    order_id: int,
    order_data: OrderUpdate,
    db: Session = Depends(get_db)
):

    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if hasattr(order_data, "model_dump"):
        data = order_data.model_dump(
            exclude_unset=True
        )
    else:
        data = order_data.dict(
            exclude_unset=True
        )

    for key, value in data.items():
        setattr(order, key, value)

    db.commit()
    db.refresh(order)

    return {
        "message": "Order updated successfully",
        "order": order
    }


# DELETE ORDER
@app.delete("/orders/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):

    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    db.delete(order)
    db.commit()

    return {
        "message": "Order deleted successfully",
        "order_id": order_id
    }
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import json

from database import engine, SessionLocal, Base
from models import (
    Restaurant,
    Food,
    FoodOption,
    Order,
    OrderItem
)
from schemas import OrderCreate


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Swiggy Style Food Ordering System"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# --------------------------------------------------
# SEED RESTAURANTS AND FOOD
# --------------------------------------------------

def seed_database():

    db = SessionLocal()

    try:

        if db.query(Restaurant).count() > 0:
            return

        restaurants = [

            Restaurant(
                name="Andhra Gunpowder",
                image="https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=900&q=80",
                rating=4.5,
                delivery_time="30–40 mins",
                cuisines="Andhra, Biryani, South Indian",
                location="Malleswaram"
            ),

            Restaurant(
                name="Paris Panini - Gourmet Sandwiches",
                image="https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=900&q=80",
                rating=4.6,
                delivery_time="45–55 mins",
                cuisines="Sandwich, Wrap, Fast Food",
                location="Central Bangalore"
            ),

            Restaurant(
                name="Bakingo",
                image="https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=900&q=80",
                rating=4.6,
                delivery_time="30–35 mins",
                cuisines="Bakery, Desserts, Beverages",
                location="Vasanth Nagar"
            ),

            Restaurant(
                name="Burger King",
                image="https://images.unsplash.com/photo-1571091718767-18b5b1457add?auto=format&fit=crop&w=900&q=80",
                rating=4.4,
                delivery_time="25–35 mins",
                cuisines="Burgers, Fast Food, Beverages",
                location="Indiranagar"
            ),

            Restaurant(
                name="Pizza Hut",
                image="https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=900&q=80",
                rating=4.3,
                delivery_time="25–30 mins",
                cuisines="Pizza, Italian, Fast Food",
                location="Koramangala"
            ),

            Restaurant(
                name="The Dessert Heaven",
                image="https://images.unsplash.com/photo-1551024506-0bccd828d307?auto=format&fit=crop&w=900&q=80",
                rating=4.7,
                delivery_time="20–30 mins",
                cuisines="Desserts, Cakes, Ice Cream",
                location="HSR Layout"
            )
        ]

        db.add_all(restaurants)
        db.commit()

        for restaurant in restaurants:
            db.refresh(restaurant)

        # --------------------------------------------------
        # RESTAURANT 1
        # --------------------------------------------------

        foods = [

            Food(
                restaurant_id=restaurants[0].id,
                name="Andhra Chicken Biryani",
                category="Biryani",
                price=299,
                image="https://images.unsplash.com/photo-1563379091339-03246963d96c?auto=format&fit=crop&w=700&q=80",
                description="Aromatic Andhra style chicken biryani"
            ),

            Food(
                restaurant_id=restaurants[0].id,
                name="Chicken Tawa Fry",
                category="Starters",
                price=249,
                image="https://images.unsplash.com/photo-1601050690117-94f5f6fa8bd7?auto=format&fit=crop&w=700&q=80",
                description="Spicy crispy chicken tawa fry"
            ),

            Food(
                restaurant_id=restaurants[0].id,
                name="Paneer Biryani",
                category="Biryani",
                price=229,
                image="https://images.unsplash.com/photo-1589302168068-964664d93dc0?auto=format&fit=crop&w=700&q=80",
                description="Flavourful paneer biryani"
            ),

            # RESTAURANT 2

            Food(
                restaurant_id=restaurants[1].id,
                name="Classic Veg Panini",
                category="Sandwich",
                price=189,
                image="https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=700&q=80",
                description="Grilled gourmet vegetable panini"
            ),

            Food(
                restaurant_id=restaurants[1].id,
                name="Chicken Cheese Panini",
                category="Sandwich",
                price=249,
                image="https://images.unsplash.com/photo-1550507992-eb63ffee0847?auto=format&fit=crop&w=700&q=80",
                description="Chicken, cheese and fresh vegetables"
            ),

            Food(
                restaurant_id=restaurants[1].id,
                name="Peri Peri Chicken Wrap",
                category="Wrap",
                price=219,
                image="https://images.unsplash.com/photo-1626700051175-6818013e1d4f?auto=format&fit=crop&w=700&q=80",
                description="Spicy peri peri chicken wrap"
            ),

            # RESTAURANT 3

            Food(
                restaurant_id=restaurants[2].id,
                name="Chocolate Truffle Cake",
                category="Cake",
                price=499,
                image="https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=700&q=80",
                description="Rich chocolate truffle cake"
            ),

            Food(
                restaurant_id=restaurants[2].id,
                name="Chocolate Pastry",
                category="Dessert",
                price=149,
                image="https://images.unsplash.com/photo-1575377427642-087cf684f04d?auto=format&fit=crop&w=700&q=80",
                description="Soft chocolate pastry"
            ),

            # RESTAURANT 4

            Food(
                restaurant_id=restaurants[3].id,
                name="Whopper Burger",
                category="Burger",
                price=249,
                image="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=700&q=80",
                description="Classic loaded burger"
            ),

            Food(
                restaurant_id=restaurants[3].id,
                name="Cheese Burger",
                category="Burger",
                price=199,
                image="https://images.unsplash.com/photo-1553979459-d2229ba7433b?auto=format&fit=crop&w=700&q=80",
                description="Juicy burger with melted cheese"
            ),

            # RESTAURANT 5

            Food(
                restaurant_id=restaurants[4].id,
                name="Margherita Pizza",
                category="Pizza",
                price=299,
                image="https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=700&q=80",
                description="Classic tomato and mozzarella pizza"
            ),

            Food(
                restaurant_id=restaurants[4].id,
                name="Farmhouse Pizza",
                category="Pizza",
                price=399,
                image="https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=700&q=80",
                description="Loaded with fresh vegetables"
            ),

            # RESTAURANT 6

            Food(
                restaurant_id=restaurants[5].id,
                name="Chocolate Donut",
                category="Dessert",
                price=99,
                image="https://images.unsplash.com/photo-1551024506-0bccd828d307?auto=format&fit=crop&w=700&q=80",
                description="Soft chocolate glazed donut"
            ),

            Food(
                restaurant_id=restaurants[5].id,
                name="Chocolate Brownie",
                category="Dessert",
                price=149,
                image="https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=700&q=80",
                description="Warm chocolate brownie"
            )
        ]

        db.add_all(foods)
        db.commit()

        for food in foods:
            db.refresh(food)

        # OPTIONS

        for food in foods:

            if food.category == "Pizza":

                db.add_all([
                    FoodOption(
                        food_id=food.id,
                        option_group="Size",
                        option_name="Regular",
                        extra_price=0
                    ),
                    FoodOption(
                        food_id=food.id,
                        option_group="Size",
                        option_name="Medium",
                        extra_price=70
                    ),
                    FoodOption(
                        food_id=food.id,
                        option_group="Size",
                        option_name="Large",
                        extra_price=130
                    ),
                    FoodOption(
                        food_id=food.id,
                        option_group="Crust",
                        option_name="Thin Crust",
                        extra_price=0
                    ),
                    FoodOption(
                        food_id=food.id,
                        option_group="Crust",
                        option_name="Cheese Burst",
                        extra_price=80
                    )
                ])

            elif food.category == "Burger":

                db.add_all([
                    FoodOption(
                        food_id=food.id,
                        option_group="Size",
                        option_name="Regular",
                        extra_price=0
                    ),
                    FoodOption(
                        food_id=food.id,
                        option_group="Size",
                        option_name="Large",
                        extra_price=50
                    ),
                    FoodOption(
                        food_id=food.id,
                        option_group="Add-on",
                        option_name="Extra Cheese",
                        extra_price=30
                    ),
                    FoodOption(
                        food_id=food.id,
                        option_group="Add-on",
                        option_name="Extra Patty",
                        extra_price=70
                    )
                ])

            elif food.category == "Biryani":

                db.add_all([
                    FoodOption(
                        food_id=food.id,
                        option_group="Portion",
                        option_name="Regular",
                        extra_price=0
                    ),
                    FoodOption(
                        food_id=food.id,
                        option_group="Portion",
                        option_name="Large",
                        extra_price=80
                    )
                ])

            elif food.category == "Sandwich" or food.category == "Wrap":

                db.add_all([
                    FoodOption(
                        food_id=food.id,
                        option_group="Size",
                        option_name="Regular",
                        extra_price=0
                    ),
                    FoodOption(
                        food_id=food.id,
                        option_group="Size",
                        option_name="Large",
                        extra_price=50
                    ),
                    FoodOption(
                        food_id=food.id,
                        option_group="Add-on",
                        option_name="Extra Cheese",
                        extra_price=30
                    )
                ])

            elif food.category == "Dessert" or food.category == "Cake":

                db.add_all([
                    FoodOption(
                        food_id=food.id,
                        option_group="Serving",
                        option_name="Single",
                        extra_price=0
                    ),
                    FoodOption(
                        food_id=food.id,
                        option_group="Serving",
                        option_name="Double",
                        extra_price=80
                    )
                ])

        db.commit()

    finally:
        db.close()


seed_database()


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Swiggy Style Food Ordering System"
    }


# --------------------------------------------------
# RESTAURANTS
# --------------------------------------------------

@app.get("/restaurants")
def get_restaurants(
    db: Session = Depends(get_db)
):

    restaurants = db.query(Restaurant).all()

    return [
        {
            "id": r.id,
            "name": r.name,
            "image": r.image,
            "rating": r.rating,
            "delivery_time": r.delivery_time,
            "cuisines": r.cuisines,
            "location": r.location
        }
        for r in restaurants
    ]


# --------------------------------------------------
# SINGLE RESTAURANT
# --------------------------------------------------

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

    return {
        "id": restaurant.id,
        "name": restaurant.name,
        "image": restaurant.image,
        "rating": restaurant.rating,
        "delivery_time": restaurant.delivery_time,
        "cuisines": restaurant.cuisines,
        "location": restaurant.location
    }


# --------------------------------------------------
# RESTAURANT MENU
# --------------------------------------------------

@app.get("/restaurants/{restaurant_id}/foods")
def get_restaurant_foods(
    restaurant_id: int,
    db: Session = Depends(get_db)
):

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


# --------------------------------------------------
# PLACE ORDER
# --------------------------------------------------

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


# --------------------------------------------------
# GET ORDER
# --------------------------------------------------

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
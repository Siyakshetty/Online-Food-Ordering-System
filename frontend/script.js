// ======================================================
// FOODIE - RESTAURANT FOOD ORDERING SYSTEM
// ======================================================

const API_URL = "http://127.0.0.1:8000";


// ======================================================
// GLOBAL VARIABLES
// ======================================================

let restaurants = [];
let currentRestaurant = null;
let currentFood = null;

let cart = JSON.parse(localStorage.getItem("foodieCart")) || [];


// ======================================================
// PAGE LOAD
// ======================================================

document.addEventListener("DOMContentLoaded", () => {

    loadRestaurants();

    updateCart();

});


// ======================================================
// LOAD RESTAURANTS
// ======================================================

async function loadRestaurants() {

    try {

        const response = await fetch(`${API_URL}/restaurants`);

        if (!response.ok) {
            throw new Error("Could not load restaurants");
        }

        restaurants = await response.json();

        renderTopRestaurants(restaurants);
        renderRestaurants(restaurants);

    } catch (error) {

        console.error(error);

        document.getElementById("restaurantGrid").innerHTML = `
            <div class="error-message">
                <h3>Unable to load restaurants</h3>

                <p>
                    Make sure your FastAPI server is running.
                </p>

                <p>
                    Run:
                    <br>
                    <strong>uvicorn main:app --reload</strong>
                </p>
            </div>
        `;

    }

}


// ======================================================
// TOP RESTAURANTS
// ======================================================

function renderTopRestaurants(data) {

    const container =
        document.getElementById("topRestaurants");

    container.innerHTML = "";

    data.slice(0, 6).forEach(restaurant => {

        const card =
            document.createElement("div");

        card.className = "top-restaurant-card";

        card.innerHTML = `

            <img
                src="${restaurant.image}"
                alt="${restaurant.name}"
                onerror="this.src='https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800'"
            >

            <div class="restaurant-card-content">

                <h3>
                    ${restaurant.name}
                </h3>

                <div class="rating">
                    ⭐ ${restaurant.rating}
                </div>

                <p>
                    ${restaurant.cuisines}
                </p>

                <small>
                    ${restaurant.delivery_time}
                </small>

            </div>

        `;

        card.onclick = () => {
            openRestaurant(restaurant.id);
        };

        container.appendChild(card);

    });

}


// ======================================================
// ALL RESTAURANTS
// ======================================================

function renderRestaurants(data) {

    const container =
        document.getElementById("restaurantGrid");

    container.innerHTML = "";

    if (data.length === 0) {

        container.innerHTML = `
            <div class="no-results">
                <h3>No restaurants found</h3>
                <p>Try another restaurant or cuisine.</p>
            </div>
        `;

        return;

    }


    data.forEach(restaurant => {

        const card =
            document.createElement("div");

        card.className = "restaurant-card";


        card.innerHTML = `

            <div class="restaurant-image-container">

                <img
                    src="${restaurant.image}"
                    alt="${restaurant.name}"
                    class="restaurant-image"

                    onerror="
                        this.src='https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800'
                    "
                >

                <div class="delivery-badge">
                    ${restaurant.delivery_time}
                </div>

            </div>


            <div class="restaurant-card-body">

                <h2>
                    ${restaurant.name}
                </h2>


                <div class="restaurant-rating">

                    <span class="rating-star">
                        ★
                    </span>

                    <strong>
                        ${restaurant.rating}
                    </strong>

                </div>


                <p class="cuisine">
                    ${restaurant.cuisines}
                </p>


                <p class="location-text">
                    📍 ${restaurant.location}
                </p>


                <button
                    class="view-menu-button"
                >
                    View Menu
                </button>

            </div>

        `;


        card.onclick = () => {

            openRestaurant(restaurant.id);

        };


        container.appendChild(card);

    });

}


// ======================================================
// SEARCH RESTAURANTS
// ======================================================

function searchRestaurants() {

    const searchInput =
        document.getElementById("searchInput");

    const searchText =
        searchInput.value.toLowerCase().trim();


    if (searchText === "") {

        renderTopRestaurants(restaurants);

        renderRestaurants(restaurants);

        return;

    }


    const filteredRestaurants =
        restaurants.filter(restaurant => {

            const name =
                restaurant.name.toLowerCase();

            const cuisines =
                restaurant.cuisines.toLowerCase();

            const location =
                restaurant.location.toLowerCase();


            return (
                name.includes(searchText) ||
                cuisines.includes(searchText) ||
                location.includes(searchText)
            );

        });


    renderTopRestaurants(filteredRestaurants);

    renderRestaurants(filteredRestaurants);

}


// ======================================================
// RESTAURANT PAGE
// ======================================================

async function openRestaurant(restaurantId) {

    try {

        const response =
            await fetch(
                `${API_URL}/restaurants/${restaurantId}`
            );


        if (!response.ok) {

            throw new Error(
                "Restaurant could not be loaded"
            );

        }


        currentRestaurant =
            await response.json();


        document.getElementById("homePage")
            .style.display = "none";


        document.getElementById("restaurantPage")
            .style.display = "block";


        renderRestaurantHeader(
            currentRestaurant
        );


        await loadRestaurantMenu(
            restaurantId
        );


        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });


    } catch (error) {

        console.error(error);

        alert(
            "Unable to open restaurant. Please try again."
        );

    }

}


// ======================================================
// RESTAURANT HEADER
// ======================================================

function renderRestaurantHeader(restaurant) {

    const container =
        document.getElementById("restaurantHeader");


    container.innerHTML = `

        <div class="restaurant-header-image">

            <img
                src="${restaurant.image}"
                alt="${restaurant.name}"

                onerror="
                    this.src='https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800'
                "
            >

        </div>


        <div class="restaurant-header-info">

            <h1>
                ${restaurant.name}
            </h1>


            <p class="restaurant-header-cuisine">
                ${restaurant.cuisines}
            </p>


            <p>
                📍 ${restaurant.location}
            </p>


            <div class="restaurant-meta">

                <span>
                    ⭐ ${restaurant.rating}
                </span>

                <span>
                    🕒 ${restaurant.delivery_time}
                </span>

            </div>

        </div>

    `;

}


// ======================================================
// LOAD RESTAURANT MENU
// ======================================================

async function loadRestaurantMenu(restaurantId) {

    const container =
        document.getElementById("menuContainer");


    container.innerHTML = `

        <div class="loading">
            Loading menu...
        </div>

    `;


    try {

        const response =
            await fetch(
                `${API_URL}/restaurants/${restaurantId}/foods`
            );


        if (!response.ok) {

            throw new Error(
                "Menu could not be loaded"
            );

        }


        const foods =
            await response.json();


        renderMenu(foods);


    } catch (error) {

        console.error(error);


        container.innerHTML = `

            <div class="error-message">

                <h3>
                    Unable to load menu
                </h3>

                <p>
                    Please try again.
                </p>

            </div>

        `;

    }

}


// ======================================================
// RENDER MENU
// ======================================================

function renderMenu(foods) {

    const container =
        document.getElementById("menuContainer");


    container.innerHTML = "";


    if (foods.length === 0) {

        container.innerHTML = `
            <div class="no-results">
                No food items available.
            </div>
        `;

        return;

    }


    // Group foods by category

    const categories = {};


    foods.forEach(food => {

        if (!categories[food.category]) {

            categories[food.category] = [];

        }

        categories[food.category].push(food);

    });


    Object.keys(categories).forEach(category => {

        const categorySection =
            document.createElement("div");


        categorySection.className =
            "menu-category";


        categorySection.innerHTML = `

            <h3 class="category-title">
                ${category}
            </h3>

        `;


        const foodList =
            document.createElement("div");


        foodList.className =
            "food-list";


        categories[category].forEach(food => {

            const foodCard =
                createFoodCard(food);

            foodList.appendChild(foodCard);

        });


        categorySection.appendChild(foodList);

        container.appendChild(categorySection);

    });

}


// ======================================================
// FOOD CARD
// ======================================================

function createFoodCard(food) {

    const card =
        document.createElement("div");


    card.className = "food-card";


    card.innerHTML = `

        <div class="food-info">

            <h3>
                ${food.name}
            </h3>


            <div class="food-price">
                ₹${Number(food.price).toFixed(0)}
            </div>


            <p>
                ${food.description || "Delicious and freshly prepared."}
            </p>


            <button
                class="add-food-button"
            >
                ADD
            </button>

        </div>


        <div class="food-image-container">

            <img
                src="${food.image}"
                alt="${food.name}"

                onerror="
                    this.src='https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600'
                "
            >

        </div>

    `;


    const addButton =
        card.querySelector(".add-food-button");


    addButton.onclick = (event) => {

        event.stopPropagation();

        startAddFood(food);

    };


    return card;

}


// ======================================================
// ADD FOOD
// ======================================================

function startAddFood(food) {

    currentFood = food;


    if (
        !food.options ||
        food.options.length === 0
    ) {

        addToCart(
            food,
            {},
            Number(food.price)
        );

        return;

    }


    openCustomize(food);

}


// ======================================================
// CUSTOMIZATION MODAL
// ======================================================

function openCustomize(food) {

    currentFood = food;


    const modal =
        document.getElementById("customizeModal");


    const content =
        document.getElementById("customizeContent");


    let html = `

        <div class="customize-header">

            <h2>
                ${food.name}
            </h2>

            <p>
                Base Price: ₹${Number(food.price).toFixed(0)}
            </p>

        </div>

    `;


    // Group options

    const groups = {};


    food.options.forEach(option => {

        if (!groups[option.option_group]) {

            groups[option.option_group] = [];

        }

        groups[option.option_group].push(option);

    });


    Object.keys(groups).forEach(
        (groupName, groupIndex) => {

            html += `

                <div class="option-group">

                    <h3>
                        ${groupName}
                    </h3>

            `;


            groups[groupName].forEach(
                (option, optionIndex) => {

                    const checked =
                        optionIndex === 0
                            ? "checked"
                            : "";


                    const extraPrice =
                        Number(option.extra_price);


                    html += `

                        <label class="option-row">

                            <div>

                                <input

                                    type="radio"

                                    name="option_${groupIndex}"

                                    value="${option.id}"

                                    data-group="${escapeHtml(
                                        option.option_group
                                    )}"

                                    data-name="${escapeHtml(
                                        option.option_name
                                    )}"

                                    data-price="${extraPrice}"

                                    ${checked}

                                >

                                <span>
                                    ${option.option_name}
                                </span>

                            </div>


                            ${
                                extraPrice > 0
                                ?
                                `<strong>
                                    + ₹${extraPrice.toFixed(0)}
                                </strong>`
                                :
                                `<span>
                                    Included
                                </span>`
                            }

                        </label>

                    `;

                }
            );


            html += `
                </div>
            `;

        }
    );


    html += `

        <div class="customize-footer">

            <button
                class="confirm-add-button"
                onclick="confirmCustomization()"
            >
                Add to Cart
            </button>

        </div>

    `;


    content.innerHTML = html;


    modal.style.display = "flex";

}


// ======================================================
// CONFIRM CUSTOMIZATION
// ======================================================

function confirmCustomization() {

    if (!currentFood) {

        return;

    }


    const selectedInputs =
        document.querySelectorAll(
            '#customizeContent input[type="radio"]:checked'
        );


    const selectedOptions = {};

    let extraPrice = 0;


    selectedInputs.forEach(input => {

        const group =
            input.dataset.group;

        const name =
            input.dataset.name;

        const price =
            Number(input.dataset.price || 0);


        selectedOptions[group] = {
            name: name,
            extra_price: price
        };


        extraPrice += price;

    });


    const finalPrice =
        Number(currentFood.price) +
        extraPrice;


    addToCart(
        currentFood,
        selectedOptions,
        finalPrice
    );


    closeCustomize();

}


// ======================================================
// ADD TO CART
// ======================================================

function addToCart(
    food,
    selectedOptions = {},
    finalPrice = null
) {

    const unitPrice =
        finalPrice !== null
            ? Number(finalPrice)
            : Number(food.price);


    const optionKey =
        JSON.stringify(selectedOptions);


    // Find same food + same customization

    const existingIndex =
        cart.findIndex(item => {

            return (
                item.food_id === food.id &&
                JSON.stringify(item.selected_options)
                    === optionKey
            );

        });


    if (existingIndex !== -1) {

        cart[existingIndex].quantity += 1;

    } else {

        cart.push({

            cart_id:
                Date.now() +
                Math.random(),

            food_id:
                food.id,

            food_name:
                food.name,

            quantity:
                1,

            price:
                unitPrice,

            selected_options:
                selectedOptions,

            image:
                food.image

        });

    }


    saveCart();

    updateCart();


    showCartNotification(
        `${food.name} added to cart`
    );

}


// ======================================================
// SAVE CART
// ======================================================

function saveCart() {

    localStorage.setItem(
        "foodieCart",
        JSON.stringify(cart)
    );

}


// ======================================================
// UPDATE CART
// ======================================================

function updateCart() {

    renderCart();

    updateCartCount();

}


// ======================================================
// CART COUNT
// ======================================================

function updateCartCount() {

    const count =
        cart.reduce(
            (total, item) =>
                total + item.quantity,
            0
        );


    const countElement =
        document.getElementById("cartCount");


    if (countElement) {

        countElement.textContent =
            count;

    }

}


// ======================================================
// RENDER CART
// ======================================================

function renderCart() {

    const container =
        document.getElementById("cartItems");


    if (!container) {

        return;

    }


    container.innerHTML = "";


    if (cart.length === 0) {

        container.innerHTML = `

            <div class="empty-cart">

                <div class="empty-cart-icon">
                    🛒
                </div>

                <h3>
                    Your cart is empty
                </h3>

                <p>
                    Add something delicious!
                </p>

            </div>

        `;


        updateBill(0);

        return;

    }


    let itemTotal = 0;


    cart.forEach((item, index) => {

        const itemSubtotal =
            Number(item.price) *
            Number(item.quantity);


        itemTotal += itemSubtotal;


        const cartItem =
            document.createElement("div");


        cartItem.className =
            "cart-item";


        let optionsHTML = "";


        if (
            item.selected_options &&
            Object.keys(item.selected_options).length > 0
        ) {

            optionsHTML =
                `<div class="cart-options">`;


            Object.entries(
                item.selected_options
            ).forEach(
                ([group, option]) => {

                    optionsHTML += `

                        <span>
                            ${group}: ${option.name}
                        </span>

                    `;

                }
            );


            optionsHTML += `
                </div>
            `;

        }


        cartItem.innerHTML = `

            <div class="cart-item-image">

                <img
                    src="${item.image || "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=300"}"
                    alt="${item.food_name}"

                    onerror="
                        this.src='https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=300'
                    "
                >

            </div>


            <div class="cart-item-details">

                <h3>
                    ${item.food_name}
                </h3>


                ${optionsHTML}


                <div class="cart-item-price">
                    ₹${Number(item.price).toFixed(0)}
                </div>


                <div class="quantity-control">

                    <button
                        onclick="changeQuantity(${index}, -1)"
                    >
                        −
                    </button>


                    <span>
                        ${item.quantity}
                    </span>


                    <button
                        onclick="changeQuantity(${index}, 1)"
                    >
                        +
                    </button>

                </div>

            </div>


            <div class="cart-item-total">

                ₹${itemSubtotal.toFixed(0)}

            </div>

        `;


        container.appendChild(cartItem);

    });


    updateBill(itemTotal);

}


// ======================================================
// CHANGE QUANTITY
// ======================================================

function changeQuantity(
    cartIndex,
    change
) {

    if (
        cartIndex < 0 ||
        cartIndex >= cart.length
    ) {

        return;

    }


    cart[cartIndex].quantity += change;


    if (
        cart[cartIndex].quantity <= 0
    ) {

        cart.splice(
            cartIndex,
            1
        );

    }


    saveCart();

    updateCart();

}


// ======================================================
// CALCULATE BILL
// ======================================================

function calculateBill() {

    let itemTotal = 0;


    cart.forEach(item => {

        itemTotal +=
            Number(item.price) *
            Number(item.quantity);

    });


    const deliveryFee =
        cart.length > 0
            ? 40
            : 0;


    const tax =
        itemTotal * 0.05;


    const total =
        itemTotal +
        deliveryFee +
        tax;


    return {

        itemTotal,
        deliveryFee,
        tax,
        total

    };

}


// ======================================================
// UPDATE BILL
// ======================================================

function updateBill(itemTotal) {

    const deliveryFee =
        cart.length > 0
            ? 40
            : 0;


    const tax =
        itemTotal * 0.05;


    const total =
        itemTotal +
        deliveryFee +
        tax;


    const itemTotalElement =
        document.getElementById("itemTotal");


    const taxElement =
        document.getElementById("tax");


    const totalElement =
        document.getElementById("cartTotal");


    if (itemTotalElement) {

        itemTotalElement.textContent =
            `₹${itemTotal.toFixed(0)}`;

    }


    if (taxElement) {

        taxElement.textContent =
            `₹${tax.toFixed(0)}`;

    }


    if (totalElement) {

        totalElement.textContent =
            `₹${total.toFixed(0)}`;

    }

}


// ======================================================
// OPEN CART
// ======================================================

function openCart() {

    updateCart();


    const overlay =
        document.getElementById("cartOverlay");


    overlay.classList.add("active");

}


// ======================================================
// CLOSE CART
// ======================================================

function closeCart() {

    const overlay =
        document.getElementById("cartOverlay");


    overlay.classList.remove("active");

}


// ======================================================
// OPEN CHECKOUT
// ======================================================

function openCheckout() {

    if (cart.length === 0) {

        alert(
            "Your cart is empty. Add some food first."
        );

        return;

    }


    closeCart();


    const modal =
        document.getElementById("checkoutModal");


    modal.style.display = "flex";

}


// ======================================================
// CLOSE CHECKOUT
// ======================================================

function closeCheckout() {

    const modal =
        document.getElementById("checkoutModal");


    modal.style.display = "none";

}


// ======================================================
// CLOSE CUSTOMIZATION
// ======================================================

function closeCustomize() {

    const modal =
        document.getElementById("customizeModal");


    modal.style.display = "none";


    currentFood = null;

}


// ======================================================
// PLACE ORDER
// ======================================================

async function placeOrder() {

    if (cart.length === 0) {

        alert(
            "Your cart is empty."
        );

        return;

    }


    const customerName =
        document.getElementById(
            "customerName"
        ).value.trim();


    const phone =
        document.getElementById(
            "customerPhone"
        ).value.trim();


    const address =
        document.getElementById(
            "customerAddress"
        ).value.trim();


    // Validation

    if (!customerName) {

        alert(
            "Please enter your name."
        );

        return;

    }


    if (!phone) {

        alert(
            "Please enter your phone number."
        );

        return;

    }


    if (!/^[0-9]{10}$/.test(phone)) {

        alert(
            "Please enter a valid 10-digit phone number."
        );

        return;

    }


    if (!address) {

        alert(
            "Please enter your delivery address."
        );

        return;

    }


    const bill =
        calculateBill();


    const orderItems =
        cart.map(item => {

            return {

                food_id:
                    item.food_id,

                food_name:
                    item.food_name,

                quantity:
                    item.quantity,

                price:
                    Number(item.price),

                selected_options:
                    item.selected_options || {}

            };

        });


    const orderData = {

        customer_name:
            customerName,

        phone:
            phone,

        address:
            address,

        total_amount:
            Number(bill.total.toFixed(2)),

        items:
            orderItems

    };


    try {

        const response =
            await fetch(
                `${API_URL}/orders`,
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            orderData
                        )

                }
            );


        if (!response.ok) {

            const errorText =
                await response.text();


            console.error(
                "Order error:",
                errorText
            );


            throw new Error(
                "Order could not be placed"
            );

        }


        const order =
            await response.json();


        // Clear cart

        cart = [];

        saveCart();

        updateCart();


        closeCheckout();


        // Clear checkout fields

        document.getElementById(
            "customerName"
        ).value = "";


        document.getElementById(
            "customerPhone"
        ).value = "";


        document.getElementById(
            "customerAddress"
        ).value = "";


        // Show success

        showOrderSuccess(
            order.id
        );


    } catch (error) {

        console.error(error);


        alert(
            "Unable to place order. Please make sure the FastAPI server is running."
        );

    }

}


// ======================================================
// SUCCESS MODAL
// ======================================================

function showOrderSuccess(orderId) {

    const modal =
        document.getElementById(
            "successModal"
        );


    const orderNumber =
        document.getElementById(
            "orderNumber"
        );


    orderNumber.textContent =
        `Order #${orderId}`;


    modal.style.display =
        "flex";

}


// ======================================================
// GO HOME
// ======================================================

function goHome() {

    document.getElementById(
        "restaurantPage"
    ).style.display = "none";


    document.getElementById(
        "homePage"
    ).style.display = "block";


    document.getElementById(
        "successModal"
    ).style.display = "none";


    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });


    currentRestaurant = null;

}


// ======================================================
// RESTAURANT CAROUSEL
// ======================================================

function scrollRestaurants(direction) {

    const container =
        document.getElementById(
            "topRestaurants"
        );


    const scrollAmount = 350;


    container.scrollBy({

        left:
            direction * scrollAmount,

        behavior:
            "smooth"

    });

}


// ======================================================
// CART NOTIFICATION
// ======================================================

function showCartNotification(message) {

    const existing =
        document.querySelector(
            ".cart-notification"
        );


    if (existing) {

        existing.remove();

    }


    const notification =
        document.createElement("div");


    notification.className =
        "cart-notification";


    notification.innerHTML = `

        <span>
            ✓
        </span>

        ${message}

    `;


    document.body.appendChild(
        notification
    );


    setTimeout(() => {

        notification.classList.add(
            "hide"
        );

    }, 1800);


    setTimeout(() => {

        notification.remove();

    }, 2300);

}


// ======================================================
// ESCAPE HTML
// ======================================================

function escapeHtml(value) {

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");

}


// ======================================================
// CLOSE MODALS WHEN CLICKING OUTSIDE
// ======================================================

window.addEventListener(
    "click",
    function(event) {

        const customizeModal =
            document.getElementById(
                "customizeModal"
            );


        const checkoutModal =
            document.getElementById(
                "checkoutModal"
            );


        const successModal =
            document.getElementById(
                "successModal"
            );


        if (
            event.target ===
            customizeModal
        ) {

            closeCustomize();

        }


        if (
            event.target ===
            checkoutModal
        ) {

            closeCheckout();

        }


        if (
            event.target ===
            successModal
        ) {

            successModal.style.display =
                "none";

        }

    }
);


// ======================================================
// ESC KEY
// ======================================================

document.addEventListener(
    "keydown",
    function(event) {

        if (event.key !== "Escape") {

            return;

        }


        closeCustomize();

        closeCheckout();

    }
);
from flask import request, jsonify
from marshmallow import ValidationError
from datetime import datetime
from sqlalchemy import select
from models import  User, Product, Order
from schemas import (
    user_schema, users_schema,
    product_schema, products_schema,
    order_schema, orders_schema
)
from extensions import db 


def register_routes(app):
    # User routes
    app.add_url_rule("/users", view_func=get_users, methods=["GET"])
    app.add_url_rule("/users/<int:id>", view_func=get_user, methods=["GET"])
    app.add_url_rule("/users", view_func=create_user, methods=["POST"])
    app.add_url_rule("/users/<int:id>", view_func=update_user, methods=["PUT"])
    app.add_url_rule("/users/<int:id>", view_func=delete_user, methods=["DELETE"])

    # Product routes
    app.add_url_rule("/products", view_func=get_products, methods=["GET"])
    app.add_url_rule("/products/<int:id>", view_func=get_product, methods=["GET"])
    app.add_url_rule("/products", view_func=create_product, methods=["POST"])
    app.add_url_rule("/products/<int:id>", view_func=update_product, methods=["PUT"])
    app.add_url_rule("/products/<int:id>", view_func=delete_product, methods=["DELETE"])

    # Order routes
    app.add_url_rule("/orders", view_func=create_order, methods=["POST"])
    app.add_url_rule("/orders/<int:order_id>/add_product/<int:product_id>", view_func=add_product_to_order, methods=["PUT"])
    app.add_url_rule("/orders/<int:order_id>/remove_product/<int:product_id>", view_func=delete_product_from_order, methods=["DELETE"])
    app.add_url_rule("/orders/user/<int:user_id>", view_func=get_orders, methods=["GET"])
    app.add_url_rule("/orders/<int:order_id>/products", view_func=get_products_for_order, methods=["GET"])

# --- Route Functions --- 
# ----- Routes ----- 

# --- User Endpoints ---

# Retrieve all Users
def get_users():
    query = select(User)
    users = db.session.execute(query).scalars().all()

    return users_schema.jsonify(users), 200 

# Retrieve User by ID                                    
def get_user(id):
    user = db.session.get(User, id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    return user_schema.jsonify(user), 200 

# Create New User
def create_user():
    try:
        user_data = user_schema.load(request.json) # deserialize json data 
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_user = User(name=user_data['name'], address=user_data['address'], email=user_data['email']) 
    db.session.add(new_user)
    db.session.commit()
    
    return user_schema.jsonify(new_user), 201 

# Update User by ID
def update_user(id):
    user = db.session.get(User, id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404 
    
    try:
        user_data = user_schema.load(request.json) 
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    user.name = user_data['name'] 
    user.address = user_data['address'] 
    user.email = user_data['email'] 
    
    db.session.commit() 
    return user_schema.jsonify(user), 200 

# Delete User by ID 
def delete_user(id):
    user = db.session.get(User, id)
    
    if not user:
        return jsonify({"message": "Invalid user id"}), 400
    
    db.session.delete(user)
    db.session.commit() 
    return jsonify({"message": f"Successfully deleted user {id}"}), 200 


# --- Product Endpoints ---

# Retrieve All Products
def get_products():
    query = select(Product) 
    products = db.session.execute(query).scalars().all()

    return products_schema.jsonify(products), 200 

# Retrieve Product by ID
def get_product(id):
    product = db.session.get(Product, id)
    
    if not product:
        return jsonify({"message": "Product not found"}), 404
    
    return product_schema.jsonify(product), 200 

# Create a new Product
def create_product():
    try:
        product_data = product_schema.load(request.json) # deserialize json data 
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_product = Product(product_name=product_data['product_name'], price=product_data['price']) 
    db.session.add(new_product)
    db.session.commit()
    
    return product_schema.jsonify(new_product), 200

# Update Product by ID
def update_product(id):
    product = db.session.get(Product, id)
    
    if not product:
        return jsonify({"message": "Product not found"}), 404 
    
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400 
    
    product.product_name = product_data['product_name']
    product.price = product_data['price'] 
    
    db.session.commit()
    return product_schema.jsonify(product), 200 

# Delete Product by ID 
def delete_product(id):
    product = db.session.get(Product, id)
    
    if not product:
        return jsonify({"message": "Invalid product id"}), 400
    
    db.session.delete(product)
    db.session.commit() 
    return jsonify({"message": f"Successfully deleted product {id}"}), 200 


# --- Order Endpoints --- 

# Create a new Order (requires user ID and Order Date) 
def create_order():
    try:
        order_data = request.json
        user_id = order_data.get("user_id")
        order_date_str = order_data.get("order_date")
        
        order_date = datetime.strptime(order_date_str, "%Y-%m-%dT%H:%M:%S")
        
        user = db.session.get(User, user_id)
        if not user: 
            return jsonify({"message": "User not found"}), 404
        
        new_order = Order(user_id=user_id, order_date=order_date)
        db.session.add(new_order)
        db.session.commit() 
        
        return order_schema.jsonify(new_order), 201
    except ValidationError as e:
        return jsonify(e.messages), 400 
        

# Add product to an Order (prevent duplicates) 
def add_product_to_order(order_id, product_id):
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({"message": "Order not found"}), 404

    # Validate product existence
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    # Prevent duplicate entry
    if product in order.products:
        return jsonify({"message": "Product already added to this order"}), 400

    # Add product to the order
    order.products.append(product)
    db.session.commit()

    return jsonify({"message": f"Product '{product.product_name}' added to Order {order_id}"}), 200


# Remove Product from an Order
def delete_product_from_order(order_id, product_id):
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({"message": "Order not found"}), 404
    
    product = db.session.get(Product, product_id)
    if not product:
         return jsonify({"message": "Product not found"}), 404
     
    order.products.remove(product)
    db.session.commit()
    
    return jsonify({"message" : f"Product '{product_id}' successfully removed from Order {order_id}"}), 200 

# Get all Orders for a User 
def get_orders(user_id):
    # Check if the user exists
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Retrieve orders along with their products
    query = select(Order).where(Order.user_id == user_id)
    orders = db.session.execute(query).scalars().all()

    return orders_schema.jsonify(orders), 200


# Get all Products for an Order
def get_products_for_order(order_id):
    # Check if order exists
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({"message": "Order not found"}), 404  
    
    products = order.products
    
    return products_schema.jsonify(products), 200 


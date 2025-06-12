from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column, String, select, DateTime, Float, UniqueConstraint
from marshmallow import ValidationError
from typing import List, Optional
from datetime import datetime, timezone

# Initialize Flask App 
app = Flask(__name__) 

# DB Configuration 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Hawaii2024*@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Base Model 
class Base(DeclarativeBase): 
    pass 

# Initialize SQLAlchemy and Marshmallow 
db = SQLAlchemy(model_class=Base) 
db.init_app(app) 
ma = Marshmallow(app) 

# ----- Models ----- 

'''
# User-Orders Association Table
user_orders = Table(
    "user_orders", 
    Base.metadata, 
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("order_id", ForeignKey("orders.id"), primary_key=True)
)
'''

# Order-Products Association Table 
order_products = Table(
    "order_product", 
    Base.metadata, 
    Column("order_id", ForeignKey("orders.id"), primary_key=True),
    Column("product_id", ForeignKey("products.id"), primary_key=True),
    UniqueConstraint("order_id", "product_id", name="uq_order_product") # Ensure unique products 
)

# User Model
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    address: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(200), unique=True) 
    
    # One-to-Many Relationship with Orders (one user can place many orders)
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="user")
    
# Order Model
class Order(Base):
    __tablename__ = "orders"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    order_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False) 
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)


    # One-to-Many with User (one user many orders) 
    user: Mapped["User"] = relationship("User", back_populates="orders")
    # Many to Many with Products
    products: Mapped[List["Product"]] = relationship("Product", secondary=order_products, back_populates="orders")
    
# Product Model 
class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    
    # many to many with orders
    orders: Mapped[List["Order"]] = relationship("Order", secondary=order_products, back_populates="products")
    

# ----- Schemas ----- 

# User Schema 
class UserSchema(ma.SQLAlchemyAutoSchema):
     class Meta:
        model = User
         
# Order Schema
class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_fk = True
        
    products = ma.Nested("ProductSchema", many=True) 
        
# Product Schema
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta: 
        model = Product
        

# ----- Instances of schemas 
user_schema = UserSchema() # individual user
users_schema = UserSchema(many=True) # many users 

order_schema = OrderSchema() # single order 
orders_schema = OrderSchema(many=True) # many orders 

product_schema = ProductSchema() # single product
products_schema = ProductSchema(many=True) # many products


# ----- Routes ----- 

# --- User Endpoints ---

# Retrieve all Users
@app.route('/users', methods=["GET"])
def get_users():
    query = select(User)
    users = db.session.execute(query).scalars().all()

    return users_schema.jsonify(users), 200 

# Retrieve User by ID                                    
@app.route('/users/<int:id>', methods=["GET"])
def get_user(id):
    user = db.session.get(User, id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    return user_schema.jsonify(user), 200 

# Create New User
@app.route("/users", methods=["POST"])
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
@app.route('/users/<int:id>', methods=["PUT"])
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
@app.route('/users/<int:id>', methods=["DELETE"]) 
def delete_user(id):
    user = db.session.get(User, id)
    
    if not user:
        return jsonify({"message": "Invalid user id"}), 400
    
    db.session.delete(user)
    db.session.commit() 
    return jsonify({"message": f"Successfully deleted user {id}"}), 200 


# --- Product Endpoints ---

# Retrieve All Products
@app.route("/products", methods=["GET"])
def get_products():
    query = select(Product) 
    products = db.session.execute(query).scalars().all()

    return products_schema.jsonify(products), 200 

# Retrieve Product by ID
@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = db.session.get(Product, id)
    
    if not product:
        return jsonify({"message": "Product not found"}), 404
    
    return product_schema.jsonify(product), 200 

# Create a new Product
@app.route("/products", methods=["POST"])
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
@app.route("/products/<int:id>", methods=["PUT"])
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
@app.route('/products/<int:id>', methods=["DELETE"]) 
def delete_product(id):
    product = db.session.get(Product, id)
    
    if not product:
        return jsonify({"message": "Invalid product id"}), 400
    
    db.session.delete(product)
    db.session.commit() 
    return jsonify({"message": f"Successfully deleted product {id}"}), 200 


# --- Order Endpoints --- 

# Create a new Order (requires user ID and Order Date) 

# Add product to an Order (prevent duplicates) 

# Remove Product from an Order

# Get all Orders for a User 

# Get all Products for an Order



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)
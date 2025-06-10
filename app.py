from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column, String, select, DateTime
from marshmallow import ValidationError
from typing import List, Optional

app = Flask(__name__) 

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Hawaii2024*@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Base(DeclarativeBase): 
    pass 

db = SQLAlchemy(model_class=Base) 
db.init_app(app) 
ma = Marshmallow(app) 

# ----- Models ----- 

# User-Orders Association Table
user_orders = Table(
    "user_orders", 
    Base.meta, 
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("order_id", ForeignKey("orders.id"), primary_key=True)
)


# Order-Products Association Table 
order_products = Table(
    "order_product", 
    Base.metadata, 
    Column("order_id", ForeignKey("orders.id"), primary_key=True),
    Column("product_id", ForeignKey("products.id"), primary_key=True)
)


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    address: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(200), unique=True) 
    
    # One-to-Many Relationship with Orders (one user can place many orders)
    orders: Mapped[List["Orders"]] = relationship("Orders", secondary=user_orders, back_populates='customers')
    
    
class Orders(Base):
    __tablename__ = "orders"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    order_date: Mapped[DateTime] = mapped_column(DateTime(), nullable=False) # Come back and check this one
    user_id: Mapped[int] = mapped_column(ForeignKey()) # Check this   
    
    # One-to-Many with User (one user many orders) 
    customers: Mapped[List["User"]] = relationship("User", secondary=user_orders, back_populates='orders')
    # Many to Many with Products
    products: Mapped[List['Product']] = relationship(secondary=order_products, back_populates="orders") 
    

class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(float(50), nullable=False) 
    
    # many to many with orders
    orders: Mapped[List['Orders']] = relationship(secondary=order_products, back_populates='products')
    
    

# ----- Schemas ----- 

# User Schema 
class UserSchema(ma.SQLAlchemyAutoSchema):
     class Meta:
        model = User
         
# Order Schema
class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Orders
        # add user_id as FK 
        

# Product Schema
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta: 
        model = Product
        

# ----- instances of schemas 
user_schema = UserSchema() # individual user
users_schema = UserSchema(many=True) # many users 

order_schema = OrderSchema() # single order 
orders_schema = OrderSchema(many=True) # many orders 

product_schema = ProductSchema() # single product
products_schema = ProductSchema(many=True) # many products




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)
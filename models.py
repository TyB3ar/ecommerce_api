from sqlalchemy import Table, Column, String, DateTime, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional

# Base Class 
class Base(DeclarativeBase):
    pass

# ----- Models ----- 

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
    
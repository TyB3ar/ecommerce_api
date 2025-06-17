# 🛍️ E-Commerce API

## Overview
This API provides functionality to manage users, products, and orders in an e-commerce system. It supports CRUD operations for users and products, as well as order placement and product association.

## Features
- 🔐 **User Management** – Create, read, update, and delete users
- 📦 **Product Management** – Manage product catalog and pricing
- 🛒 **Order Processing** – Place orders and associate products
- ✅ **Input Validation** – Enforced via Marshmallow schemas
- 🗄️ **Database Integration** – Uses SQLAlchemy ORM with MySQ


## Technologies Used
- Python 3.x
- Flask
- Flask-SQLAlchemy
- Marshmallow (for serialization & validation)
- MySQL (database)

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/TyB3ar/ecommerce_api.git

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt

3. **Configure the Database**:
    Update SQLALCHEMY_DATABASE_URI in app.py with your database credentials.

4. **Run the Application**:
    python app.py


# API Endpoints

## Users
| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| GET | /users | Retrieve all users | 
| GET | /users/<id> | Retrieve a specific user | 
| POST | /users | Create a new user | 
| PUT | /users/<id> | Update user details | 
| DELETE | /users/<id> | Delete a user | 

## Products
| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| GET | /products | Retrieve all products | 
| GET | /products/<id> | Retrieve a specific product | 
| POST | /products | Create a new product | 
| PUT | /products/<id> | Update product details | 
| DELETE | /products/<id> | Delete a product | 

## Orders 
| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| POST | /orders | Create a new order | 
| PUT | /orders/<order_id>/add_product/<product_id> | Add a product to an order | 
| DELETE | <order_id>/remove_prudct/<product_id> | Remove a product from an order | 
| GET | /orders/user/<user_id> | Retrieve all orders for a user | 
| GET | /orders/<order_id>/products | Retrieve all products in an order | 

# Example: Creating a User 
## POST /users 

### Request 
```bash
{
  "name": "Alice",
  "address": "123 Main St",
  "email": "alice@example.com"
}
```
### Response 
```bash
{
  "id": 1,
  "name": "Alice",
  "address": "123 Main St",
  "email": "alice@example.com"
}
```


# Schema Overview 

## Models: 
- User: Represents a customer with an address and email 
- Product: Stores product details including price 
- Order: Links users to purchased products and stores order dates 

## Validation: 
- Uses Marshmallow to validate incoming requests and ensure proper data formatting

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you’d like to change.

## Author
Developed by Tyler Wronski, for Coding Temple project. 

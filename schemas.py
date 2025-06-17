from marshmallow import fields
from models import User, Order, Product
from extensions import ma  


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
    order_date = fields.DateTime(format="%Y-%m-%dT%H:%M:%S")
        
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

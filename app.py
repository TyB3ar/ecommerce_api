from flask import Flask
from extensions import db, ma
from routes import register_routes


# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:<YOUR_PASSWORD>@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init extensions
db.init_app(app)
ma.init_app(app)

# Register routes
register_routes(app)

# Create tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

from flask_sqlalchemy import SQLAlchemy

# Create an instance of SQLAlchemy
db = SQLAlchemy()

# Define the Product model
class Product(db.Model):
    __tablename__ = 'product'  # Define the table name explicitly

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    name = db.Column(db.String(100), nullable=False)  # Product name
    price = db.Column(db.Float, nullable=False)  # Product price
    description = db.Column(db.String(255), nullable=True)  # Product description

    def __repr__(self):
        return f"<Product {self.name}>"

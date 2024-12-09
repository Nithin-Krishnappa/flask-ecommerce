from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ecommerce import db



app = Flask(__name__)

DATABASE_URI = 'postgresql://ecommerce_x3sw_user:Nz7jALs8WLp5rY62YsdVfSKo7sRWQG6V@dpg-ctbjlolds78s739c8f4g-a:5432/ecommerce_x3sw'

# Set up the database connection
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
# Database Models

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)


# Routes
@app.route('/')
def index():
    try:
        products = Product.query.all()
        return render_template('index.html', products=products)
    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        new_product = Product(name=name, price=float(price), description=description)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_product.html')


if __name__ == '__main__':
    app.run(debug=True)

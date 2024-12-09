from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine




app = Flask(__name__)

# Database configuration with hardcoded values
HOSTNAME = 'dpg-ctbjlolds78s739c8f4g-a'
PORT = 5432
DATABASE = 'ecommerce_x3sw'
USERNAME = 'ecommerce_x3sw_user'
PASSWORD = 'Nz7jALs8WLp5rY62YsdVfSKo7sRWQG6V'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'postgresql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable SQLAlchemy event system for better performance

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import the Product model
from model import Product




# Routes
@app.route('/')
def index():
    try:
        products = Product.query.all()
        return render_template('templates/index.html', products=products)
    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('templates/product.html', product=product)
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        new_product = Product(name=name, price=float(price), description=description)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('templates/index'))
    return render_template('templates/add_product.html')


if __name__ == '__main__':
    app.run()

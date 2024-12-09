from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

app = Flask(__name__)

# Database configuration with environment variables
import os

HOSTNAME = os.getenv('HOSTNAME', 'dpg-ctbjlolds78s739c8f4g-a')
PORT = os.getenv('PORT', 5432)
DATABASE = os.getenv('DATABASE', 'ecommerce_x3sw')
USERNAME = os.getenv('USERNAME', 'ecommerce_x3sw_user')
PASSWORD = os.getenv('PASSWORD', 'Nz7jALs8WLp5rY62YsdVfSKo7sRWQG6V')

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
        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
            <title>E-Commerce</title>
        </head>
        <body>
            <nav>
                <a href="/">Home</a>
                <a href="/add">Add Product</a>
            </nav>
            <div class="content">
                <h1>Products</h1>
                <ul>
                    {% for product in products %}
                        <li>
                            <a href="{{ url_for('product_detail', product_id=product.id) }}">
                                {{ product.name }} - ${{ product.price }}
                            </a>
                        </li>
                    {% endfor %}
                </ul>
            </div>
        </body>
        </html>
        '''
        return render_template_string(html, products=products)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
        <title>{{ product.name }}</title>
    </head>
    <body>
        <nav>
            <a href="/">Home</a>
            <a href="/add">Add Product</a>
        </nav>
        <div class="content">
            <h1>{{ product.name }}</h1>
            <p>{{ product.description }}</p>
            <p>Price: ${{ product.price }}</p>
            <a href="/">Back to Home</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, product=product)

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
    
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
        <title>Add Product</title>
    </head>
    <body>
        <nav>
            <a href="/">Home</a>
            <a href="/add">Add Product</a>
        </nav>
        <div class="content">
            <h1>Add Product</h1>
            <form method="POST">
                <label>Name:</label>
                <input type="text" name="name" required>
                <label>Price:</label>
                <input type="text" name="price" required>
                <label>Description:</label>
                <textarea name="description"></textarea>
                <button type="submit">Add Product</button>
            </form>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

if __name__ == '__main__':
    app.run()

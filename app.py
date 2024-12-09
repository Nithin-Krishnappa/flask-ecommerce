from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
hostname = 'dpg-ctbjlolds78s739c8f4g-a'
port = 5432
database = 'ecommerce_x3sw'
username = 'ecommerce_x3sw_user'
password = 'Nz7jALs8WLp5rY62YsdVfSKo7sRWQG6V'

# Configure the database URI for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{database}'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
        return f"Found {len(products)} products"
    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return {'products': [{'id': p.id, 'name': p.name, 'price': p.price, 'description': p.description} for p in products]}

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

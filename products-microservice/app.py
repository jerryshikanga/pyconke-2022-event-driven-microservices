import logging
import random

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import HOST, PORT, SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config['DEBUG'] = True
app.logger.setLevel(logging.DEBUG)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    stock_balance = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        return dict(id=self.id, name=self.name, stock_balance=self.stock_balance, price=self.price)


@app.route('/product/<product_id>')
def product_details(product_id):
    product = db.session.query(Product).filter_by(id=product_id).first()
    if product:
        return jsonify(product.to_dict())
    else:
        return {}, 404


@app.route('/product/order', methods=["POST"])
def order_product():
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity')
    if not product_id or not quantity:
        return dict(error="Invalid request data"), 400
    product = db.session.query(Product).filter_by(id=product_id).first()
    if not product:
        return {}, 404
    if quantity > product.stock_balance:
        return dict(error="Insufficient stock"), 400
    product.stock_balance -= quantity
    db.session.commit()
    return jsonify(product.to_dict())


@app.route('/products')
def all_products():
    products = db.session.query(Product).all()
    products = [product.to_dict() for product in products]
    return jsonify(products)


@app.route('/seeder', methods=['POST'])
def seeder():
    products_to_create = int(request.json['products_to_create'])
    min_price = int(request.json['min_price'])
    max_price = int(request.json['max_price'])
    min_stock = int(request.json['min_stock'])
    max_stock = int(request.json['max_stock'])
    for i in range(products_to_create):
        name = f"Product {i}"
        product = Product(stock_balance=random.randint(min_stock, max_stock),
                          price=random.randint(min_price, max_price), name=name)
        db.session.add(product)
        db.session.flush()
    db.session.commit()
    return all_products(), 201


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)

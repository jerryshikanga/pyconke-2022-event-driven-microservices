from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
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


if __name__ == "__main__":
    app.run()

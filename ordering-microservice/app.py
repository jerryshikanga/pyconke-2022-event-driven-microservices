from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import DEFAULT_CURRENCY_CODE, HOST, PORT
from utils import process_order_request
from exceptions import RequestsException, UserNotFoundError, InactiveUserError, ProductNotFoundError, \
    InsufficientStockError, InsufficientBalanceError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False, default=0)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    total_cost = db.Column(db.Integer, nullable=False, default=0)
    currency = db.Column(db.String, nullable=False, default="KES")

    def to_dict(self):
        return dict(id=self.id, user_id=self.user_id, balance=self.balance, currency=self.currency)


@app.route('/order/<order_id>')
def order_details(order_id):
    order = db.session.query(Order).filter_by(id=order_id).first()
    if order:
        return jsonify(order.to_dict())
    else:
        return {}, 404


@app.route('/order', methods=["POST"])
def order():
    product_id = request.json.get('product_id')
    user_id = request.json.get('user_id')
    quantity = request.json.get('quantity')
    currency = request.json.get('currency')

    if not product_id or not quantity:
        return dict(error="Invalid request data"), 400

    if currency != DEFAULT_CURRENCY_CODE:
        return dict(error="Invalid currency"), 400

    try:
        order = process_order_request(user_id, product_id, quantity, currency)
        return order.to_dict()
    except (RequestsException, InsufficientBalanceError) as e:
        return jsonify(dict(error=str(e))), 400
    except UserNotFoundError:
        return jsonify(error=f"User {user_id} not found.")
    except InactiveUserError:
        return jsonify(dict(error=f"User {user_id} is inactive."))
    except ProductNotFoundError:
        return jsonify(dict(error=f"Product {product_id} not found."))
    except InsufficientStockError:
        return jsonify(dict(error=f"Product {product_id} is out of stock for order quantity {quantity}."))


@app.route('/orders')
def all_orders():
    orders = db.session.query(Order).all()
    orders = [order.to_dict() for order in orders]
    return jsonify(orders)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)

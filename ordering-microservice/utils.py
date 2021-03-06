import requests

from config import USER_MICROSERVICE_URL, PRODUCT_MICROSERVICE_URL, ACCOUNTING_MICROSERVICE_URL
from exceptions import UserNotFoundError, InactiveUserError, ProductNotFoundError, InsufficientStockError, \
    InsufficientBalanceError


def get_user_details(user_id):
    url = f"{USER_MICROSERVICE_URL}/user/{user_id}"
    response = requests.get(url)
    if response.status_code // 100 == 2:
        return response.json()


def get_product_details(product_id):
    url = f"{PRODUCT_MICROSERVICE_URL}/product/{product_id}"
    response = requests.get(url)
    if response.status_code // 100 == 2:
        return response.json()


def get_account_details(user_id):
    url = f"{ACCOUNTING_MICROSERVICE_URL}/accounts/user/{user_id}"
    response = requests.get(url)
    if response.status_code // 100 == 2:
        return response.json()


def charge_account(account_id, amount):
    url = f"{ACCOUNTING_MICROSERVICE_URL}/account/charge"
    response = requests.post(url, json=dict(account_id=account_id, amount=amount))
    if response.status_code // 100 == 2:
        return response.json()


def create_stock_move(product_id, quantity):
    url = f"{PRODUCT_MICROSERVICE_URL}/product/order"
    response = requests.post(url, json=dict(product_id=product_id, quantity=quantity))
    if response.status_code // 100 == 2:
        return response.json()


def process_order_request(user_id, product_id, quantity, currency):
    from flask import current_app as app
    from app import Order, db

    user_details = get_user_details(user_id)
    if not user_details:
        app.logger.warn(f"User {user_id} not found.")
        raise UserNotFoundError
    if not user_details.get('active', False):
        app.logger.warn(f"User {user_id} inactive.")
        raise InactiveUserError

    product_details = get_product_details(product_id)
    if not product_details:
        app.logger.warn(f"Product {product_id} not found.")
        raise ProductNotFoundError
    if quantity > product_details.get('stock_balance', 0):
        app.logger.warn(f"Product {product_id} quantity of {product_details.get('stock_balance', 0)}"
                        f" insufficient for request of {quantity}.")
        raise InsufficientStockError

    account_details = get_account_details(user_id)
    if not account_details:
        app.logger.warn(f"Account for user {user_id} not found.")
        raise UserNotFoundError

    total_cost = quantity * product_details.get('price')
    if total_cost > account_details['balance']:
        message = f"Account {account_details['id']} for user {user_id} has insufficient balance of" \
                  f" {account_details['balance']} for order of cost {total_cost}."
        app.logger.warn(message)
        raise InsufficientBalanceError(message)
    charge_response = charge_account(account_details['id'], total_cost)
    app.logger.info(f"Charge account {account_details['id']} for order response {charge_response}")
    stock_move_response = create_stock_move(product_id, quantity)
    app.logger.info(f"stock_move_response {stock_move_response}")

    order = Order(user_id=user_id, product_id=product_id, quantity=quantity,
                  total_cost=total_cost, currency=currency)
    db.session.add(order)
    db.session.commit()
    return order

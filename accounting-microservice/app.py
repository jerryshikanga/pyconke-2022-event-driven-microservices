import logging
import random

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import HOST, PORT, SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.logger.setLevel(logging.DEBUG)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['DEBUG'] = True


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    balance = db.Column(db.Integer, nullable=False, default=0)
    currency = db.Column(db.String, nullable=False, default="KES")

    def to_dict(self):
        return dict(id=self.id, user_id=self.user_id, balance=self.balance, currency=self.currency)


@app.route('/accounts/user/<user_id>')
def account_details(user_id):
    account = db.session.query(Account).filter_by(user_id=user_id).first()
    if account:
        return jsonify(account.to_dict())
    else:
        return {}, 404


@app.route('/account/charge', methods=['POST'])
def charge_account():
    account_id = request.json['account_id']
    amount = request.json['amount']
    account = db.session.query(Account).filter_by(id=account_id).first()
    if not account:
        return {}, 404
    if account.balance < amount:
        return jsonify(dict(error="Insufficient funds")), 400
    account.balance -= amount
    db.session.commit()
    return jsonify(account.to_dict())


@app.route('/accounts')
def all_accounts():
    accounts = db.session.query(Account).all()
    accounts = [account.to_dict() for account in accounts]
    return jsonify(accounts)


@app.route('/seeder', methods=['POST'])
def seeder():
    accounts_to_create = int(request.json['accounts_to_create'])
    min_balance = int(request.json['min_balance'])
    max_balance = int(request.json['max_balance'])
    for i in range(accounts_to_create):
        balance = random.randint(min_balance, max_balance)
        account = Account(user_id=i, balance=balance)
        db.session.add(account)
    db.session.commit()
    return all_accounts()


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)

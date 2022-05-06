import random

from app import Account, db


def create_accounts():
    for i in range(100):
        balance = random.randint(100, 999)
        account = Account(user_id=i, balance=balance)
        db.session.add(account)
    db.session.commit()


if __name__ == "__main__":
    create_accounts()

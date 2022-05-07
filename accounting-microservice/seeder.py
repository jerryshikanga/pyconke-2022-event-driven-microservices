import random

from app import Account, db
from config import ACCOUNTS_TO_CREATE


def create_accounts():
    for i in range(ACCOUNTS_TO_CREATE):
        balance = random.randint(10000, 99999)
        account = Account(user_id=i, balance=balance)
        db.session.add(account)
    db.session.commit()


if __name__ == "__main__":
    create_accounts()

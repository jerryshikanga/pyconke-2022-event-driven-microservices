import random

from app import Product, db
from config import PRODUCTS_TO_CREATE


def create_products():
    for i in range(PRODUCTS_TO_CREATE):
        name = f"Product {i}"
        product = Product(name=name, stock_balance=random.randint(10000, 100000),
                          price=random.randint(1, 5))
        db.session.add(product)
    db.session.commit()


if __name__ == "__main__":
    create_products()

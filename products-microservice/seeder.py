import random

from app import Product, db


def create_products():
    for i in range(100):
        name = f"Product {i}"
        product = Product(name=name, stock_balance=random.randint(10, 50),
                          price=random.randint(50, 150))
        db.session.add(product)
    db.session.commit()


if __name__ == "__main__":
    create_products()

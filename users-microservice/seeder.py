import random

from app import User, db


def create_users():
    for i in range(100):
        user = User(name=f"User {i}", active=random.choice([True, False]))
        db.session.add(user)
    db.session.commit()


if __name__ == "__main__":
    create_users()

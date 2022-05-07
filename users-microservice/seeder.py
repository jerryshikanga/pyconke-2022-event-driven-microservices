import random

from app import User, db
from config import USERS_TO_CREATE


def create_users():
    for i in range(USERS_TO_CREATE):
        user = User(name=f"User {i}", active=True)
        db.session.add(user)
    db.session.commit()


if __name__ == "__main__":
    create_users()

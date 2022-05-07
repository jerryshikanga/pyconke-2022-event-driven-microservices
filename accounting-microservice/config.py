import os

HOST = os.environ.get("HOST", "0.0.0.0")
PORT = os.environ.get("PORT", 5004)
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///app.db')

ACCOUNTS_TO_CREATE = int(os.environ.get('ACCOUNTS_TO_CREATE', '100'))

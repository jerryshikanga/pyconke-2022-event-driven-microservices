import os

HOST = os.environ.get("HOST", "0.0.0.0")
PORT = os.environ.get("PORT", 5003)
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///app.db')

ACCOUNTS_TO_CREATE = int(os.environ.get('ACCOUNTS_TO_CREATE', '100'))

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', "rabbitmq")
RABBIT_PORT = os.environ.get('RABBIT_PORT', "6739")
RABBITMQ_DEFAULT_QUEUE_NAME = os.environ.get('RABBITMQ_DEFAULT_QUEUE_NAME', 'worker')

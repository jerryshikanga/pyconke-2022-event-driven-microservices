import os

USER_MICROSERVICE_URL = os.environ.get("USER_MICROSERVICE_URL")
ACCOUNTING_MICROSERVICE_URL = os.environ.get("ACCOUNTING_MICROSERVICE_URL")
PRODUCT_MICROSERVICE_URL = os.environ.get("PRODUCT_MICROSERVICE_URL")
DEFAULT_CURRENCY_CODE = os.environ.get("DEFAULT_CURRENCY_CODE", "KES")

HOST = os.environ.get("HOST", "0.0.0.0")
PORT = os.environ.get("PORT", 5001)

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///app.db')

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', "localhost")
RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT', "5672")
RABBITMQ_DEFAULT_QUEUE_NAME = os.environ.get('RABBITMQ_DEFAULT_QUEUE_NAME', 'worker')

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)

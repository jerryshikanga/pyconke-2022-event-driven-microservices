import json

import pika
from config import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_DEFAULT_QUEUE_NAME


def callback(ch, method, properties, body):
    body = json.loads(body)
    print(f"Received {body}")


def consume_messages():
    parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_DEFAULT_QUEUE_NAME)
    channel.basic_consume(queue=RABBITMQ_DEFAULT_QUEUE_NAME, auto_ack=True, on_message_callback=callback)
    print(f"Started listening on {RABBITMQ_HOST}:{RABBITMQ_PORT}")
    channel.start_consuming()


if __name__ == "__main__":
    consume_messages()


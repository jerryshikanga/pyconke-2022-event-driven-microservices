import random

from locust import HttpUser, task


class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        payload = {
            "user_id": random.randint(1, 100),
            "product_id": random.randint(1, 100),
            "quantity": random.randint(1, 5),
            "currency": "KES"
        }
        self.client.post("/order", json=payload)

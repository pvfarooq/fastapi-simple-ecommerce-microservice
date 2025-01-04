import time

import pika

from .constants import RABBITMQ_HOST


class RabbitMQHelper:
    _instances = {}

    def __new__(cls, queue_name):
        if queue_name not in cls._instances:
            cls._instances[queue_name] = super().__new__(cls)
            cls._instances[queue_name]._initialized = False
        return cls._instances[queue_name]

    def __init__(self, queue_name):
        if self._initialized:
            return

        self.queue_name = queue_name
        self._retry_connection()
        self._initialized = True

    def _retry_connection(self):
        max_retries = 5
        retries = 0

        while retries < max_retries:
            try:
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(RABBITMQ_HOST)
                )
                self.channel = self.connection.channel()
                self.channel.queue_declare(queue=self.queue_name)
                print(f"Connected to RabbitMQ on queue: {self.queue_name}")
                return
            except Exception as e:
                retries += 1
                print(
                    f"Failed to connect to RabbitMQ. Retrying {retries}/{max_retries}... Error: {e}"
                )
                time.sleep(5)

        raise ConnectionError(
            f"Failed to connect to RabbitMQ after {max_retries} retries."
        )

    def publish(self, message):
        try:
            self.channel.basic_publish(
                exchange="",
                routing_key=self.queue_name,
                body=message,
                properties=pika.BasicProperties(delivery_mode=2),
            )
            print(f"Message published to {self.queue_name}: {message}")
        except Exception as e:
            print(f"Failed to publish message to {self.queue_name}. Error: {e}")

    def consume(self, callback):
        def wrapper(ch, method, properties, body):
            try:
                callback(body)
            except Exception as e:
                print(f"Error processing message: {e}")

        try:
            self.channel.basic_consume(
                queue=self.queue_name, on_message_callback=wrapper, auto_ack=True
            )
            print(f"Started consuming from {self.queue_name}")
        except Exception as e:
            print(f"Failed to start consuming from {self.queue_name}. Error: {e}")

    def start_consuming(self):
        try:
            print(f"Listening to queue: {self.queue_name}")
            self.channel.start_consuming()
        except Exception as e:
            print(f"Error while consuming messages from {self.queue_name}. Error: {e}")

    def close(self):
        try:
            self.connection.close()
            print(f"Closed connection to {self.queue_name}")
        except Exception as e:
            print(f"Failed to close connection to {self.queue_name}. Error: {e}")

    @classmethod
    def get_instance(cls, queue_name):
        return cls(queue_name)

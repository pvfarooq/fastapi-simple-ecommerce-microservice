import json
import logging

import pika

from .constants import RABBITMQ_HOST, STOCK_DEDUCTION_QUEUE

logger = logging.getLogger(__name__)


class StockDeductionPublisher:
    def __init__(self):
        self.connection = None
        self.channel = None

    def connect(self):
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=STOCK_DEDUCTION_QUEUE, durable=True)

    def publish_stock_deduction(self, product_id: int, quantity: int):
        try:
            self.connect()
            message = {"product_id": product_id, "quantity": quantity}
            self.channel.basic_publish(
                exchange="",
                routing_key=STOCK_DEDUCTION_QUEUE,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2  # make message persistent
                ),
            )
            logger.info(f"Published stock deduction request: {message}")
        except Exception as e:
            logger.error(f"Error publishing message: {e}")
            raise
        finally:
            if self.connection and not self.connection.is_closed:
                self.connection.close()

import json
import logging

import pika

from .constants import RABBITMQ_HOST, STOCK_DEDUCTION_QUEUE

logger = logging.getLogger(__name__)


class StockDeductionConsumer:
    def __init__(self, stock_service):
        self.stock_service = stock_service
        self.connection = None
        self.channel = None

    def connect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=STOCK_DEDUCTION_QUEUE, durable=True)

    def process_message(self, ch, method, properties, body):
        try:
            message = json.loads(body)
            self.stock_service.deduct_stock(
                product_id=message["product_id"], quantity=message["quantity"]
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    def start_consuming(self):
        try:
            self.connect()
            self.channel.basic_qos(prefetch_count=1)
            self.channel.basic_consume(
                queue=STOCK_DEDUCTION_QUEUE, on_message_callback=self.process_message
            )
            logger.info("Started consuming stock deduction messages")
            self.channel.start_consuming()
        except Exception as e:
            logger.error(f"Consumer error: {e}")
            if self.connection and not self.connection.is_closed:
                self.connection.close()

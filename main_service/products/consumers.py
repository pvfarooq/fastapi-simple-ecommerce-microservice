from core.db import SessionLocal
from shared.messaging.config import STOCK_DEDUCTION_QUEUE, Message
from shared.messaging.consumer import Consumer

from .crud import deduct_product_stock


def handle_stock_deduction(message: Message):
    if message.event_type == "stock_deduction_requested":
        db = SessionLocal()
        try:
            deduct_product_stock(
                db,
                product_id=message.data["product_id"],
                quantity=message.data["quantity"],
            )
            db.commit()
        except Exception as e:
            db.rollback()
            raise
        finally:
            db.close()


def start_stock_consumer():
    consumer = Consumer(queue=STOCK_DEDUCTION_QUEUE, callback=handle_stock_deduction)
    consumer.start_consuming()

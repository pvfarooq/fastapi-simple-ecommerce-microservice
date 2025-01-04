import json

from core.db import session_local
from messaging import product_queue
from products.crud import get_product_by_id


def process_product_events(event):
    event = json.loads(event)
    if event["event"] == "product_stock_reduction":
        print("Processing event: product_stock_reduction")

        quantity = event["quantity"]
        product_id = event["product_id"]
        order_id = event["order_id"]

        with session_local() as session:
            product = get_product_by_id(session, product_id)

            if not product:
                print(f"Product with ID {product_id} not found.")
                failure_event = {
                    "event": "product_not_found",
                    "product_id": product_id,
                    "order_id": order_id,
                }
                product_queue.publish(json.dumps(failure_event))
                return

            if product.stock < quantity:
                failure_event = {
                    "event": "stock_unavailable",
                    "product_id": product_id,
                    "order_id": order_id,
                }
                product_queue.publish(json.dumps(failure_event))
                print("Stock not available. Cancelling the order.")
            else:
                product.stock -= quantity
                session.commit()

                success_event = {
                    "event": "stock_deducted",
                    "product_id": product_id,
                    "quantity": quantity,
                    "order_id": order_id,
                }
                product_queue.publish(json.dumps(success_event))
                print(f"Stock deducted for product {product_id}")

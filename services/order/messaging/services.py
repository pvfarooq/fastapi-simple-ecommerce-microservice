import json

from core.db import session_local
from messaging import product_queue
from order import crud
from order.models import Order


def publish_product_stock_reduction(order: Order):
    event = {
        "event": "product_stock_reduction",
        "quantity": order.quantity,
        "product_id": order.product_id,
        "order_id": order.order_id,
    }
    product_queue.publish(json.dumps(event))


def process_order_events(event):
    event = json.loads(event)
    event_type = event["event"]

    print(f"Processing event: {event_type}")
    order_id = event["order_id"]

    if event_type == "stock_unavailable":
        print(f"Stock unavailable for order: {order_id}")
        print("Cancelling order")
        with session_local() as session:
            crud.cancel_order(order_id, session)

    elif event_type == "stock_deducted":
        print(f"Stock deducted for order: {order_id} in User-Poduct Service 🎉")

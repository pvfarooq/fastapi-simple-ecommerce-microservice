import json

import requests
from core.db import session_local
from messaging import product_queue
from order import crud
from order.models import Order

from .constants import USER_PRODUCT_SERVICE_URL


def publish_product_stock_reduction(order: Order):
    event = {
        "event": "product_stock_reduction",
        "quantity": order.quantity,
        "product_id": order.product_id,
        "order_id": order.id,
    }
    product_queue.publish(json.dumps(event))


def validate_product_stock(order_details):
    product_id = order_details["product_id"]
    url = f"{USER_PRODUCT_SERVICE_URL}/products/{product_id}"
    response = requests.get(url)
    if response.status_code == 200:
        product = response.json()
        if product["stock"] < order_details["quantity"]:
            return {"message": "Product out of stock", "in_stock": False}
        else:
            return {"message": "Product available", "in_stock": True}
    else:
        return {"message": "Product not found"}


def process_order_events(event):
    event = json.loads(event)
    event_type = event["event"]

    print(f"Processing event: {event_type}")
    order_id = event["order_id"]

    if event_type == "stock_unavailable":
        print(f"Stock unavailable for order: {order_id} in User-Product Service")
        print("Cancelling order")
        with session_local() as session:
            crud.cancel_order(order_id, session)

    elif event_type == "stock_deducted":
        print(f"Stock deducted for order: {order_id} in User-Poduct Service 🎉")

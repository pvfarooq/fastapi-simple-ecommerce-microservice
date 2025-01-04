import threading

from fastapi import FastAPI

from messaging import order_queue
from messaging.services import process_order_events
from order.routes import router as order_router

app = FastAPI(
    title="Order Service",
)

app.include_router(order_router)


def start_order_consumer():
    order_queue.consume(process_order_events)
    order_queue.start_consuming()


@app.on_event("startup")
async def startup_event():
    consumer_thread = threading.Thread(target=start_order_consumer, daemon=True)
    consumer_thread.start()

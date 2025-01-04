import threading

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from messaging import product_queue
from messaging.services import process_product_events
from products.routes import router as products_router
from users.routes import router as users_router

app = FastAPI(
    title="Main Service",
)

app.include_router(users_router)
app.include_router(products_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def start_product_queue_consumer():
    product_queue.consume(process_product_events)
    product_queue.start_consuming()


@app.on_event("startup")
async def startup_event():
    consumer_thread = threading.Thread(target=start_product_queue_consumer, daemon=True)
    consumer_thread.start()

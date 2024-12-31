import threading

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from messaging.consumer import StockDeductionConsumer
from products.routes import router as products_router
from products.services import StockService
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


@app.on_event("startup")
async def startup_event():
    stock_service = StockService()
    consumer = StockDeductionConsumer(stock_service)
    consumer_thread = threading.Thread(target=consumer.start_consuming, daemon=True)
    consumer_thread.start()

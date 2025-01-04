from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from users.routes import router as users_router

app = FastAPI(
    title="User Service",
)

app.include_router(users_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from core.db import get_session
from fastapi import APIRouter, Depends
from order import crud

from .schemas import OrderRequest

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/create")
def create_order(request: OrderRequest, session=Depends(get_session)):
    current_user = 1
    order = crud.create_order(current_user, session, request)
    return {"message": "Order placed successfully", "order_id": order.order_id}

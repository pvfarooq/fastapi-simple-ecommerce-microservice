from core.db import get_session
from fastapi import APIRouter, Depends
from messaging.services import publish_product_stock_reduction, validate_product_stock
from order import crud

from .schemas import OrderRequest

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/create")
def create_order(request: OrderRequest, session=Depends(get_session)):
    current_user = 1
    is_stock_available = validate_product_stock(request.dict())
    if not is_stock_available["in_stock"]:
        return {"message": is_stock_available["message"]}

    order = crud.create_order(current_user, session, request)
    publish_product_stock_reduction(order)
    return {"message": "Order placed successfully"}


@router.get("/cancel/{order_id}")
def cancel_order(order_id: int, session=Depends(get_session)):
    order = crud.get_order_by_id(order_id, session)
    return {"order": order}
    # if order:
    #     crud.cancel_order(order, session)
    #     return {"message": "Order cancelled successfully"}
    # return {"message": "Order not found"}

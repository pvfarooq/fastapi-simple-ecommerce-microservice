from core.db import get_session
from core.token import verify_token
from fastapi import APIRouter, Depends, HTTPException, Request
from messaging.services import publish_product_stock_reduction
from order import crud
from order.services import validate_product_stock

from .schemas import OrderRequest

router = APIRouter(
    prefix="/orders", tags=["Orders"], dependencies=[Depends(verify_token)]
)


@router.post("/create")
def create_order(
    request: Request, request_data: OrderRequest, session=Depends(get_session)
):
    current_user = request.state.user

    try:
        is_stock_available = validate_product_stock(
            request_data.dict(), request.state.bearer_token
        )
        if not is_stock_available["in_stock"]:
            return {"message": is_stock_available["message"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    order = crud.create_order(current_user, session, request_data)
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

from messaging.publisher import StockDeductionPublisher
from sqlalchemy.orm import Session

from .models import Order
from .schemas import OrderRequest
from .utils import generate_order_id


def create_order(current_user, session: Session, order: OrderRequest):
    new_order = Order(
        user_id=current_user,
        product_id=order.product_id,
        quantity=order.quantity,
    )
    new_order.order_id = generate_order_id(session)
    session.add(new_order)
    session.commit()

    stock_publisher = StockDeductionPublisher()
    stock_publisher.publish_stock_deduction(
        product_id=order.product_id, quantity=order.quantity
    )

    return new_order

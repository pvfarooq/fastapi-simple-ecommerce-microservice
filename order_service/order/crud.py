from sqlalchemy.orm import Session

from .models import Order
from .schemas import OrderRequest
from .utils import generate_order_id


def create_order(current_user, session: Session, order: OrderRequest) -> Order:
    new_order = Order(
        user_id=current_user,
        product_id=order.product_id,
        quantity=order.quantity,
        status="confirmed",
    )
    new_order.order_id = generate_order_id(session)
    session.add(new_order)
    session.commit()
    return new_order


def cancel_order(order_id: int, session: Session) -> Order:
    order = get_order_by_id(order_id, session)
    order.status = "cancelled"
    session.commit()
    return order


def get_order_by_id(order_id: int, session: Session) -> Order:
    query = session.query(Order).filter(Order.id == order_id)
    return query.first()

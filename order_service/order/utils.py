from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Order


def generate_order_id(session: Session) -> int:
    query = select(Order.id).order_by(Order.id.desc()).limit(1)
    result = session.execute(query).fetchone()
    if result:
        return result[0] + 1
    return 1

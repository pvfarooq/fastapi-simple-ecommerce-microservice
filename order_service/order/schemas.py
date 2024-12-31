from pydantic import BaseModel


class OrderRequest(BaseModel):
    product_id: int
    quantity: int

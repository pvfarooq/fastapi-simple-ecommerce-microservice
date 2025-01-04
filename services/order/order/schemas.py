from pydantic import BaseModel


class OrderRequest(BaseModel):
    product_id: str
    quantity: int

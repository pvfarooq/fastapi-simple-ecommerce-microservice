import requests

from core.constants import PRODUCT_SERVICE_URL


def validate_product_stock(order_details: dict, bearer_token: str):
    product_id = order_details["product_id"]
    url = f"{PRODUCT_SERVICE_URL}/api/products/{product_id}"
    response = requests.get(url, headers={"Authorization": f"Bearer {bearer_token}"})
    status_code = response.status_code

    if status_code == 401 or status_code == 403:
        raise Exception("Unauthorized request")

    elif status_code == 200:
        response = response.json()
        product = response["data"]
        if product["stock"] < order_details["quantity"]:
            return {"message": "Product out of stock", "in_stock": False, "code": 200}
        else:
            return {"message": "Product available", "in_stock": True, "code": 200}

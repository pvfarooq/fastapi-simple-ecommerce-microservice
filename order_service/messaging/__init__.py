from .base import RabbitMQHelper
from .constants import ORDER_QUEUE, PRODUCT_QUEUE

order_queue = RabbitMQHelper(ORDER_QUEUE)
product_queue = RabbitMQHelper(PRODUCT_QUEUE)

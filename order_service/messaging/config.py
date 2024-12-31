import json
from dataclasses import dataclass
from typing import Any, Dict

RABBITMQ_HOST = "rabbitmq"
STOCK_DEDUCTION_QUEUE = "stock_deduction"
ORDER_STATUS_QUEUE = "order_status"


@dataclass
class Message:
    event_type: str
    data: Dict[str, Any]

    def to_json(self) -> str:
        return json.dumps({"event_type": self.event_type, "data": self.data})

    @classmethod
    def from_json(cls, json_str: str) -> "Message":
        data = json.loads(json_str)
        return cls(event_type=data["event_type"], data=data["data"])

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

@dataclass
class OrderItem:
    product_id: UUID
    product_name: str
    quantity: int = 0
    price: int = 0
    created_at: datetime = datetime.now(tz=timezone.utc)

    def __post_init__(self):
        if self.quantity < 0:
            raise ValueError("Quantity must be greater than zero.")
        if self.price < 0:
            raise ValueError("Price must be greater than zero.")
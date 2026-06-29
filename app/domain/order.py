from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.order_item import OrderItem

@dataclass
class Order:
    id: UUID
    user_id: UUID
    items: list[OrderItem]
    status: str = 'на рассмотрении'
    price: int = 0
    created_at: datetime = datetime.now(tz=timezone.utc)

    def __post_init__(self):
        if self.price < 0:
            raise ValueError('Order price cannot be negative')
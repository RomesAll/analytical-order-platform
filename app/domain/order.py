from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID
from enum import Enum

class Status(Enum):
    CREATED = "created"
    CONFIRMED = "confirmed"
    PAYMENT = "payment"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

@dataclass
class OrderItem:
    product_id: UUID
    product_name: str
    quantity: int
    price_unit: int

    @property
    def price(self):
        return self.price_unit * self.quantity

    def dict(self):
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'quantity': self.quantity,
            'price_unit': self.price_unit,
            'price': self.price,
        }

@dataclass
class Order:
    id: UUID
    user_id: UUID
    order_items: list['OrderItem']
    status: Status = Status.CREATED
    created_at: datetime = datetime.now(tz=timezone.utc)

    @property
    def order_price(self) -> int:
        return sum([item.price for item in self.order_items])

    def dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'order_items': [item.dict() for item in self.order_items],
            'order_price': self.order_price,
            'status': self.status.value,
            'created_at': self.created_at,
        }
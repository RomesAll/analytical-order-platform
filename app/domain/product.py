from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

@dataclass
class Product:
    id: UUID
    name: str
    quantity: int
    price_unit: int
    created_at: datetime = datetime.now(tz=timezone.utc)

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if self.price_unit < 0:
            raise ValueError("Price must be greater than zero.")

    @property
    def price(self) -> int:
        return self.price_unit * self.quantity

    def is_quantity_equable(self, amount: int) -> bool:
        return self.quantity >= amount

    def increment_quantity(self, quantity: int) -> int:
        self.quantity += quantity
        return self.quantity

    def decrement_quantity(self, quantity: int) -> int:
        if not self.is_quantity_equable(quantity):
            raise ValueError("Quantity must be greater than zero.")
        self.quantity -= quantity
        return self.quantity

    def dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "quantity": self.quantity,
            "price_unit": self.price_unit,
            "price": self.price,
            "created_at": self.created_at,
        }
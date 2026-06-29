from abc import ABC, abstractmethod
from uuid import UUID
from .order import Order

class OrderRepository(ABC):
    @abstractmethod
    def get_by_id(self, order_id: UUID) -> Order:
        pass

    @abstractmethod
    def save(self, order: Order):
        pass
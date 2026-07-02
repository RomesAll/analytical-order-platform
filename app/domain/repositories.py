from abc import ABC, abstractmethod
from datetime import datetime, date
from uuid import UUID
from .events import OrderEvent
from .order import Order
from .product import Product

class OrderRepository(ABC):
    @abstractmethod
    def get_by_id(self, order_id: UUID) -> Order:
        pass

    @abstractmethod
    def save(self, order: Order) -> Order:
        pass

class ProductRepository(ABC):
    @abstractmethod
    def get_by_id(self, product_id: UUID) -> Product:
        pass

    @abstractmethod
    def save(self, product: Product) -> Product:
        pass

    @abstractmethod
    def increment_count_product(self, product_id: UUID, amount: int) -> tuple[int, int]:
        pass

    @abstractmethod
    def decrement_count_product(self, product_id: UUID, amount: int) -> tuple[int, int]:
        pass

class EventRepository(ABC):
    @abstractmethod
    def save(self, event: OrderEvent):
        pass

    @abstractmethod
    def get_order_history(self, order_id: UUID):
        pass

    @abstractmethod
    def get_analytics(self, date_analyze: date):
        pass
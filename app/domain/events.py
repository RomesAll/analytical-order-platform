from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID

"""
# USECASE (синхронно, сразу):
# 1. ORDER_CREATED         — создание заказа
# 2. PAYMENT_RECEIVED      — успешная оплата
# 3. PAYMENT_FAILED        — ошибка оплаты
# 4. ORDER_CANCELLED       — отмена заказа
# 5. STOCK_RELEASED        — возврат товаров
# 6. ORDER_SHIPPED         — отправка заказа
# 7. ORDER_DELIVERED       — доставка заказа

# CELERY: process_order_created (асинхронно):
# 1. PROCESSING_STARTED    — начало обработки
# 2. STOCK_RESERVED        — списание товаров
# 3. ORDER_CONFIRMED       — подтверждение
# 4. CACHE_UPDATED         — обновление кеша
# 5. ERROR_OCCURRED        — ошибка (если что-то пошло не так)

# CELERY: send_notification (асинхронно):
# 1. EMAIL_SENT            — уведомление отправлено
# 2. EMAIL_FAILED          — ошибка отправки
# 3. ERROR_OCCURRED        — ошибка задачи
"""

class EventType(str, Enum):
    """Типы событий заказа"""
    ORDER_CREATED = "order_created"
    PAYMENT_RECEIVED = 'payment_received'
    ORDER_SHIPPED = 'order_shipped'
    ORDER_DELIVERED = 'order_delivered'
    PROCESSING_STARTED = "processing_started"
    STOCK_RESERVED = 'stock_reserved'
    ORDER_CONFIRMED = 'order_confirmed'
    CACHE_UPDATED = 'cache_updated'
    EMAIL_SENT = 'email_sent'
    EMAIL_FAILED = 'email_failed'
    STOCK_RELEASED = 'stock_released'
    ORDER_CANCELLED = 'order_cancelled'
    PAYMENT_FAILED = 'payment_failed'
    ERROR_OCCURRED = 'error_occurred'

@dataclass
class OrderEvent:
    """Доменная модель события заказа"""
    event_id: UUID
    order_id: UUID
    event_type: EventType
    timestamp: datetime = field(default_factory=datetime.utcnow)
    actor: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_mongo_document(self) -> dict:
        """Преобразование в документ MongoDB"""
        return {
            'event_id': str(self.event_id),
            'order_id': str(self.order_id),
            'event_type': self.event_type.value,
            'timestamp': self.timestamp,
            'actor': self.actor or 'system',
            'data': self.data,
            'metadata': {
                **self.metadata,
                'version': '1.0',
                'created_at': self.timestamp
            }
        }
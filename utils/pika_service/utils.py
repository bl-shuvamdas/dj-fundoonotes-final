from typing import Any

from django.conf import settings


class SingletonMeta(type):
    _instance = {}

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        """Singleton Design Pattern"""
        if cls not in cls._instance:
            cls._instance[cls] = super(cls.__class__, cls).__call__(*args, **kwds)
            return cls._instance[cls]


class RabbitMQConfig(metaclass=SingletonMeta):
    def __init__(self) -> None:
        if settings.PIKA_CONFIG.get('queue') is None and settings.PIKA_CONFIG.get('host') is None:
            raise ValueError("queue cannot be None")

        self.queue = settings.PIKA_CONFIG.get('queue')
        self.host = settings.PIKA_CONFIG.get('host')
        self.exchange = settings.PIKA_CONFIG.get('exchange')

from typing import Any, Dict

import pika

from utils.pika_service.utils import RabbitMQConfig


class RabbitMq:
    __slots__ = ['server', '_channel', '_connection']

    def __init__(self):
        """
        :param server: Object of class RabbitMQConfig
        """
        self.server = RabbitMQConfig()
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.server.host))  # type: ignore
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.server.queue)

    def __enter__(self):
        return self

    def publish(self, payload: Dict[str, Any]):  # noqa
        """
        :param payload: JSON payload
        :return: None
        """
        try:
            self._channel.basic_publish(exchange=self.server.exchange,
                                        routing_key=self.server.queue,
                                        body=str(payload))
            print('published Message: {}'.format(payload))
            return True
        except Exception:
            return False

    def __exit__(self, *args, **kwargs):
        self._connection.close()

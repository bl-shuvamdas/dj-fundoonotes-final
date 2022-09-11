import ast

import pika

from utils.email_service import Email
from utils.pika_service.utils import RabbitMQConfig


class RabbitMQServer:
    def __init__(self) -> None:
        """
        :param server: Object of RabbitMQServerConfig
        """
        self.server = RabbitMQConfig()
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.server.host))  # type: ignore
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.server.queue)

    @staticmethod
    def send_email(email):
        Email.verify_user(email)

    def callback(self, ch, method, properties, body):
        payload = ast.literal_eval(body.decode('utf-8'))

        if isinstance(payload, dict) and 'send' in payload:
            self.send_email(email=payload['email'])

        print(" [x] Received %r" % payload)

    def __call__(self):
        self._channel.basic_consume(queue=self.server.queue, on_message_callback=self.callback, auto_ack=True)
        print(' [*] Waiting for messages, To exit press CTRL+C')
        self._channel.start_consuming()

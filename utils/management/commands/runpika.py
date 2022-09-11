from django.core.management.base import BaseCommand
from utils.pika_service import RabbitMQServer


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        server = RabbitMQServer()
        server()
        self.stdout.write(self.style.SUCCESS('Successfully closed poll'))

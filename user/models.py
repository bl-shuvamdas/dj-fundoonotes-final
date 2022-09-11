from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from utils import JWT
from utils.pika_service import RabbitMq


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_verify = models.BooleanField(default=False)

    class Meta:
        db_table = 'user'
        ordering = ('id',)

    @property
    def token(self) -> str:
        return JWT.encode({'user_id': self.pk, 'email': self.email})


@receiver(signal=post_save, sender=User)
def send_verify_email(instance, created,  **kwargs):
    if instance.is_verify is False and created is True:
        with RabbitMq() as rm:
            rm.publish(payload={'email': instance.email, 'send': True})

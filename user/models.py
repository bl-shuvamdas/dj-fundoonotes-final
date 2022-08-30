from django.contrib.auth.models import AbstractUser
from django.db import models

from utils import JWT


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

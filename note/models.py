from django.db import models


# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    collaborator = models.ManyToManyField('user.User', related_name='collaborator')

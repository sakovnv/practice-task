from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    computation_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class Computation(models.Model):
    author = models.ForeignKey('User', on_delete=models.PROTECT)
    image_array = models.JSONField('ImageArray')
    results = models.JSONField('Results')
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.results}'
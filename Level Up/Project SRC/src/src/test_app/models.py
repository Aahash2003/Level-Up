
from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    height = models.FloatField()
    weight = models.FloatField()

    def __str__(self):
        return self.username

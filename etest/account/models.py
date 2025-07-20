from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

    




# class UserToken(models.Model):
#     user = models.OneToOneField(User ,on_delete=models.CASCADE)
#     token = models.CharField(max_length=64)


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()


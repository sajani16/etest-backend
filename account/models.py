from django.db import models
from django.contrib.auth.models import AbstractUser 

# Create your models here.


class CustomUser(AbstractUser):
    pass

# class UserToken(models.Model):
#     user = models.OneToOneField(User ,on_delete=models.CASCADE)
#     token = models.CharField(max_length=64)



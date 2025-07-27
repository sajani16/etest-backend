from django.db import models
from django.contrib.auth.models import AbstractUser 

# Create your models here.


class CustomUser(AbstractUser):
    otp_code = models.CharField(max_length=10, blank=True, null=True, help_text="Temporary OTP for email verification")

# class UserToken(models.Model):
#     user = models.OneToOneField(User ,on_delete=models.CASCADE)
#     token = models.CharField(max_length=64)



from django.contrib.auth.models import User
from django.db import models
from lab_cryptography.fields import encrypt


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = encrypt(models.CharField(verbose_name="phone_number", max_length=10))

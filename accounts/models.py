from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class ConfirmCode(models.Model):
    code = models.CharField(max_length=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

from django.contrib.auth.models import User
from django.db import models


class OneTimeCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=6, blank=True, null=True)

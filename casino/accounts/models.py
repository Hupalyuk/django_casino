from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=1000)  # стартовий баланс

    def __str__(self):
        return f"{self.user.username} — {self.balance}"

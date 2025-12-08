from django.db import models
from django.contrib.auth.models import User

class CoinFlipResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result = models.CharField(max_length=10)  # "Орёл" або "Решка"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} — {self.result}"

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Kana(models.Model):
    hira = models.CharField(max_length=2)
    kata = models.CharField(max_length=2)
    romaji = models.CharField(max_length=10, unique=True)
    base_weight = models.IntegerField(default=5)

    def __str__(self):
        return f"{self.hira}/{self.kata} ({self.romaji})"


class KanaProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kana = models.ForeignKey(Kana, on_delete=models.CASCADE)
    weight = models.IntegerField(null=True, blank=True)
    errors = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'kana')

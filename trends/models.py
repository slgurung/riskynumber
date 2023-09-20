from django.db import models
from stocks.models import Stock

# Create your models here.

class Trending(models.Model):
    ticker = models.CharField(max_length = 10)
    updown = models.CharField(max_length = 10, blank = True, null = True)

    def __str__(self):
        return self.ticker

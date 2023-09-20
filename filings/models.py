from django.db import models

from stocks.models import Stock
# Create your models here.

class Filling(models.Model):
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE)
    description = models.CharField(max_length = 200, null = True)
    form_name = models.CharField(max_length = 50, null = True)
    documentUrl = models.URLField()
    filling_date = models.DateField(null = True)

    def __str__(self):
        return self.filling_date + ': ' + self.description

from django.db import models

# Create your models here.

# class StkIndex(models.Model):
#     symbol = models.CharField(max_length = 20, primary_key = True)
#     name = models.CharField(max_length = 50)

#     def __str__(self):
#         return self.name

# class Exchange(models.Model):
#     name = models.CharField(max_length = 50, primary_key=True)
#
#     def __init__(self):
#         return self.name

class Stock(models.Model):
    ticker = models.CharField(max_length = 10, primary_key = True)
    cik = models.CharField(max_length=10)
    name = models.CharField(max_length = 250)
    exchange = models.CharField(max_length=250, blank = True, null=True)
    sector = models.CharField(max_length = 250, blank = True, null=True)
    website = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=20, null=True)
    stk_index = models.CharField(max_length=100, blank=True, null=True)
    

    def __str__(self): # for python 2, use __unicode__ too
        return self.ticker + ': ' + self.name

# class Financial(models.Model):
#     stock = models.ForeignKey(Stock, related_name='financials', on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     date = models.DateField()
#
#
#     def __str__(self):
#         return self.title +': ' + self.date

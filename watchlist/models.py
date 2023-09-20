from django.db import models
# from django.contrib.auth.models import User
from django.utils.text import slugify # to make string with spaces to use in url
# import misaka

# able to make user object of currently logged in user
from django.contrib.auth import get_user_model
User = get_user_model() # currently logged in user object in session

from stocks.models import Stock
# Create your models here.

# # OneToMany relations
# class WatchList(models.Model):
#     name = models.CharField(max_length=40, unique=False, default="myList")
#     user = models.OneToOneField(User, related_name="watchlist", on_delete=models.CASCADE)
#     # looks like this should be in Stock
#     # stock = models.ForeignKey(Stock, related_name='watchlists', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.name

    # class Meta:
    #     ordering = ["stock"]


class WatchList(models.Model):
    # user = models.ForeignKey(User, related_name="watchlists", on_delete=models.CASCADE)
    user = models.OneToOneField(User, related_name="watchlist", primary_key=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, unique=False, blank=False, default="Watchlist")
    slug = models.SlugField(allow_unicode=True, unique=False, blank=False, default="Watchlist")
    # description = models.TextField(blank=True, default='')
    # description_html = models.TextField(editable=False, default='', blank=True)
    stocks = models.ManyToManyField(Stock, related_name="watchlists")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        # self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse("watchlist:single", kwargs={"slug": self.slug})

    class Meta:
        ordering = ("name",)
        # unique_together = ("user", "name")

# ### we don't need this intermediate model
# class WatchListStock(models.Model):
#     watchlist = models.ForeignKey(WatchList, related_name="watchlist_stocks", on_delete=models.CASCADE)
#     stock = models.ForeignKey(Stock, related_name='watchlists', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.stock.ticker
#
#     class Meta:
#         unique_together = ("watchlist", "stock")
#         ordering = ["watchlist"]

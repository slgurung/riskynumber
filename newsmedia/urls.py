from django.urls import path

from newsmedia import views

app_name = 'newsmedia'

# for ajax call to /newsmedia/stock_news/
urlpatterns = [
    path('stock_news/', views.stock_news, name = 'stock_news'),
]

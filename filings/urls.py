from django.urls import path, re_path

from filings import views

app_name = 'filings'

urlpatterns = [
    path('sec_filing/', views.sec_filing, name = 'sec_filing'),
]

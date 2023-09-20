"""riskynumber URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from django.conf.urls import url    # older version
from . import views  # . is for current directory which is riskynumber

########### extremely important #######
# the url is checked top to bottom and when match is found remaining URLs are
# not checked. So, this might have some effect how pattern are listed
# pattern at bottom might be matched at top so, intended url might not be
# reached..
##################
urlpatterns = [
    #url(r'^admin/', admin.site.urls), # older version
    path('admin/', admin.site.urls),
    #url(r'^$', views.HomePage.as_view(), name='home'), # older version of below
    path('', views.HomePage.as_view(), name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('stocks/', include('stocks.urls', namespace='stocks')),
    path('filings/', include('filings.urls', namespace='filings')),
    ## for ajax call
    path('newsmedia/', include('newsmedia.urls', namespace='newsmedia')),
    path('watchlist/', include('watchlist.urls', namespace='watchlist')),
    path('about/', views.AboutView.as_view(), name="about"),
    path('disclaimer/', views.DisclaimerView.as_view(), name="disclaimer"),
    path('howto/', views.HowtoView.as_view(), name="howto"),
]

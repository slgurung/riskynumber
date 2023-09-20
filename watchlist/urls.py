from django.urls import path, re_path

from watchlist import views

app_name = "watchlist"

urlpatterns = [
    #don't put '/' at begining
    path('', views.WatchList_List.as_view(), name="watchlist_list"),
    path('create_watchlist/', views.CreateWatchList.as_view(), name="create_watchlist"),
    #path('stocks/in/<slug:slug>/', views.SingleWatchlist.as_view(), name="watchlist_detail"),
    ##this is called from ajax call
    path('watchlist_stocks/', views.watchlist_stocks, name="watchlist_stocks"),
    path('remove_ticker/', views.remove_ticker, name="remove_ticker"),
    path('add_ticker/', views.add_ticker, name="add_ticker"),

]

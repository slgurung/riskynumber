from django.urls import path, re_path

from stocks import views

app_name = 'stocks'

########### extremely important #######
# the url is checked top to bottom and when match is found remaining URLs are
# not checked. So, this might have some effect how pattern are listed
# pattern at bottom might be matched at top so, intended url might not be
# reached..
##################

urlpatterns = [
    path('symbol/suggested_tickers/', views.suggested_tickers, name='suggested_tickers'),
    path('symbol/hdata/', views.hdata, name='hdata'),
    path('<ticker>/', views.IntradayQuote.as_view(), name="intraday_quote"),
    path('symbol/intraday/', views.intraday, name='intraday'), # for ajax
    path('symbol/search/', views.symbol_search, name='symbol_search'), # for ajax
    path('stkindex/<ticker>', views.StkIndexView.as_view(), name="stkindex"),
    ########################## carefull using <var> with path #############################
    # '<ticker>/' matches with 'suggested_tickers/', 'intraday/' , or 'quote/' if it is placed on the top.
    # So, these urls actually calls below url. To solve this either change it to
    # 'summary/<ticker>/' or place it at bottom. or use re_path()
    #path('<ticker>/', views.Summary.as_view(), name='summary'),
    # or re method
    #re_path(r'^(?P<ticker>[\^\w]+)/$', views.Summary.as_view(), name='summary'),
    #### This is for non ajax call & it is not using now #########
    #path('summary/<ticker>/', views.Summary.as_view(), name='summary'),
    ####################################################################################
    #path('updateData/', views.updateData, name='updatedata'), # replaced by intraday/

]

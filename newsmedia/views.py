import feedparser
import requests
import pandas as pd

from stocks.models import Stock
from django.http import JsonResponse

p_key = 'UP72PBB1TUSTYMHK'
# Create your views here.

## used for ajax call to /newsmedia/stock_news/ 
def stock_news(request):
    data = {}
    ticker = request.POST.get('ticker').upper()
    data['ticker'] = ticker
    if ticker not in ['^GSPC', '^DJI', '^IXIC']:
        try:
            anews = alpha_news(ticker)
            ynews = yahoo_news(ticker)
            news_df = pd.concat([ynews, anews], ignore_index=True)
            news_df.sort_values('date',  ascending=False, inplace=True)
            news_df = news_df.loc[:, ['title', 'link']].iloc[:40]

        except Exception as e:
            data['result'] = 'no_news'
        else:
            data['news_list'] = news_df.to_dict('records')
            data['result'] = 'gotIt'
    else:
        data['result'] = 'invalid'
    
    return JsonResponse(data)

def alpha_news(symbol, key=p_key):
    url = "https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=" + symbol + "&apikey=" + key
    data = requests.get(url).json()['feed']
    data = [{'date':d['time_published'], 'title':d['title'], 'link':d['url']}  for d in data]
    data = pd.DataFrame(data)
    data.date = pd.to_datetime(data.date, utc = True)

    return data

def yahoo_news(symbol):    
    rss_yahoo = 'http://finance.yahoo.com/rss/headline?s=' + symbol.lower()
    stockfeed = feedparser.parse(rss_yahoo)
    stockfeed = stockfeed.entries[:20]

    # stockPosts = []
    # for post in stockfeed:
    #     date = post.published
    #     title = post.title
    #     link = post.link
    #     stockPosts.append({'date': date, 'title': title, 'link': link})   
    ######## list conprehension instead of for loop
    stockPosts = [{'date': d['published'], 'title':d['title'], 'link':d['link']} for d in stockfeed]
    stockPosts = pd.DataFrame(stockPosts)
    stockPosts.date = pd.to_datetime(stockPosts.date)
    
    # anews = alpha_news(symbol)
    # stockPosts = pd.concat([stockPosts, anews], ignore_index=True)
    # stockPosts.sort_values('date',  ascending=False, inplace=True)

    # stockPosts = stockPosts.loc[:, ['title', 'link']].iloc[:size]
    
    return stockPosts
import pandas as pd
#import numpy as np
#from pandas_datareader import data as web
#import datetime, re

import os #, random
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'riskynumber.settings')

import django
django.setup()

from stocks.models import  Stock

def add_ticker(tik, cik, name, ex=None, sec=None, web=None, ty=None, si=None):
    tic = Stock.objects.get_or_create(ticker=tik, cik=cik, name=name, exchange=ex,
                                      sector=sec, website=web, type=ty, stk_index=si)[0]
    tic.save()

tickers = pd.read_csv('sec_cik.csv')
tickers.apply(lambda r: add_ticker(r['ticker'], r['cik'], r['title']), axis=1)

# stockNum = len(tickers)

# for i in range(stockNum):
#     #if (re.match(r'^[\w]+$', tickerDf.ix[i, 0])):
#     #ex = Exchange.objects.get_or_create(name = tikCikDf.ix[i, 'Exchange'])[0]
#     add_ticker(tickers.loc[i, 'iexId'], tickers.loc[i, 'symbol'], tickers.loc[i, 'cik'], tickers.loc[i, 'name'], tickers.loc[i, 'exchange'],\
#                tickers.loc[i, 'sector'],tickers.loc[i, 'industry'], tickers.loc[i, 'website'],tickers.loc[i, 'tags'], tickers.loc[i, 'type'])

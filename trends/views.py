#from django.shortcuts import render

import pandas as pd
import requests

p_key = 'UP72PBB1TUSTYMHK'

def trending(key=p_key):
    url = 'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey=' + key
    data = requests.get(url).json()
    data = pd.DataFrame(data['most_actively_traded'])
    data.change_percentage = data.change_percentage.map(lambda x: float(x.split('%')[0]))
    # data.sort_values('change_percentage', inplace=True)

    trendDict = {}
    for t, v in zip(data.ticker.to_list(), data.change_percentage.to_list()):
        if v < 0:
            trendDict[t] = 'red'
        elif v > 0:
            trendDict[t] = 'green'
        else:
            trendDict[t] = 'white'


    return trendDict


# def iex_trending():

#     # url1 = "https://cloud.iexapis.com/v1/stock/market/list/mostactive"
#     # #"https://api.iextrading.com/1.0/stock/market/list/mostactive"
#     # url2 = "https://api.iextrading.com/1.0/stock/market/list/gainers"
#     # url3 = "https://api.iextrading.com/1.0/stock/market/list/losers"

#     # mostactive = pd.DataFrame(requests.get(url1).json())[['changePercent', 'latestVolume','symbol']]
#     # gainers = pd.DataFrame(requests.get(url2).json())[['changePercent', 'latestVolume','symbol']]
#     # losers = pd.DataFrame(requests.get(url3).json())[['changePercent', 'latestVolume','symbol']]
#     # mostactive = pd.DataFrame(stk.get_market_most_active(token=textval))[['changePercent', 'latestVolume','symbol']]
#     # gainers = pd.DataFrame(stk.get_market_gainers(token=textval))[['changePercent', 'latestVolume','symbol']]
#     # losers = pd.DataFrame(stk.get_market_losers(token=textval))[['changePercent', 'latestVolume','symbol']]
#     # trendingDict = {}
#     # for s in list(mostactive.symbol):
#     #     if list(mostactive.loc[mostactive.symbol == s].changePercent)[0] < 0:
#     #         trendingDict[s] = 'red'
#     #     else:
#     #         trendingDict[s] = 'green'

#     # for s in list(gainers.symbol):
#     #     trendingDict[s] = 'green'

#     # for s in list(losers.symbol):
#     #     trendingDict[s] = 'red'

#     # #tickerOfDay = choice(list(mostactive.symbol))

#     return {} #trendingDict #, tickerOfDay

# def get_trending_tickers():
#     # nasdaq = 'http://www.nasdaq.com/markets/most-active.aspx'
#     # nyse = 'http://www.nasdaq.com/markets/most-active.aspx?exchange=NYSE'
#     # amex = 'http://www.nasdaq.com/markets/most-active.aspx?exchange=AMEX'

#     # mostActiveList = []
#     # mostAdvancedList = []
#     # mostDeclinedList = []
#     # trendDict = {}

#     # response = requests.get(nasdaq)
#     # soup = bs(response.content, "lxml")

#     # #activeStocks = response.css('div#_active a.mostactive')
#     # # mostActive = soup.find('div', id='_active')
#     # mostAdvanced = soup.find('div', id='_advanced')
#     # mostDeclined = soup.find('div', id='_declined')
#     # #print(mostAdvanced.prettify())
#     # # mostActive = mostActive.find_all('h3')[1:2]
#     # mostAdvanced = mostAdvanced.find_all('h3')[1:13]
#     # mostDeclined = mostDeclined.find_all('h3')[1:13]

#     # # for h in mostActive:
#     # #     symbol = h.string
#     # #     mostActiveList.append(symbol)
#     # for h in mostAdvanced:
#     #     symbol = h.string
#     #     trendDict[symbol] = 'green'
#     #     mostAdvancedList.append(symbol)
#     # for h in mostDeclined:
#     #     symbol = h.string
#     #     trendDict[symbol] = 'red'
#     #     mostDeclinedList.append(symbol)

#     # ### NYSE
#     # response = requests.get(nyse)
#     # soup = bs(response.content, "lxml")

#     # #mostActive = soup.find('div', id='_active')
#     # mostAdvanced = soup.find('div', id='_advanced')
#     # mostDeclined = soup.find('div', id='_declined')
#     # #print(mostAdvanced.prettify())
#     # #mostActive = mostActive.find_all('h3')[1:1]
#     # mostAdvanced = mostAdvanced.find_all('h3')[1:5]
#     # mostDeclined = mostDeclined.find_all('h3')[1:5]

#     # # for h in mostActive:
#     # #     symbol = h.string
#     # #     mostActiveList.append(symbol)
#     # for h in mostAdvanced:
#     #     symbol = h.string
#     #     trendDict[symbol] = 'green'
#     #     mostAdvancedList.append(symbol)
#     # for h in mostDeclined:
#     #     symbol = h.string
#     #     trendDict[symbol] = 'red'
#     #     mostDeclinedList.append(symbol)

#     # ### AMEX
#     # response = requests.get(amex)
#     # soup = bs(response.content, "lxml")

#     # #mostActive = soup.find('div', id='_active')
#     # mostAdvanced = soup.find('div', id='_advanced')
#     # mostDeclined = soup.find('div', id='_declined')
#     # #print(mostAdvanced.prettify())
#     # #mostActive = mostActive.find_all('h3')[1:2]
#     # mostAdvanced = mostAdvanced.find_all('h3')[1:2]
#     # mostDeclined = mostDeclined.find_all('h3')[1:2]

#     # # for h in mostActive:
#     # #     symbol = h.string
#     # #     if Stock.objects.filter(ticker__iexact=symbol).exists():
#     # #         mostActiveList.append(symbol)
#     # for h in mostAdvanced:
#     #     symbol = h.string
#     #     if Stock.objects.filter(ticker__iexact=symbol).exists():
#     #         trendDict[symbol] = 'green'
#     #         mostAdvancedList.append(symbol)
#     # for h in mostDeclined:
#     #     symbol = h.string
#     #     if Stock.objects.filter(ticker__iexact=symbol).exists():
#     #         trendDict[symbol] = 'red'
#     #         mostDeclinedList.append(symbol)

#     # #set1 = set(mostAdvancedList + mostDeclinedList)
#     # #set2 = set(mostActiveList)
#     # #trendSet = set1 #set2.union(set1)
#     # tikCikDf = pd.read_csv('stocks_cik.csv', dtype = {'cik': str})
#     # symbols = set(tikCikDf.symbol)

#     # #trendList = list(trendSet & symbols)
#     # trendDict= {k:v for k, v in trendDict.items() if k in symbols}
#     # #stockOfDay = choice(list(trendDict.keys()))

#     return {} #trendDict #, stockOfDay #trendList # mostActiveList, mostAdvancedList, mostDeclinedList

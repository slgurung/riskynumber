from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
import pandas as pd
import numpy as np
#from datetime import date, timedelta
import datetime as dt
import requests

from stocks.models import Stock
from trends.views import  trending


from django.contrib.auth import get_user_model
User = get_user_model() # currently logged in user object in session

p_key = 'UP72PBB1TUSTYMHK'
token = "pk_d7c57280919e44538cb671a1e8eda58e"
# Create your views here.
stkIndex = {'^GSPC': 'S&P 500', '^DJI': 'Dow Jones Industrial' , '^IXIC': 'Nasdaq Composite'}

# this is called by ajax from js file
def suggested_tickers(request):
    stock_list =  []
    starts_with = ''

    if request.method == 'GET':
        starts_with = request.GET['suggestion']
        #print('suggestion start with:---> ', starts_with)
    stock_list = get_ticker_list(15, starts_with)

    # make list of obj to sortable
    return render(request, 'stocks/ticker.html', {'stocks': stock_list})

# helper function for suggested_tickers()
def get_ticker_list(max_results = 0, starts_with = ''): # check if list is shorted
    stock_list = []
    if starts_with:
        # ticker__istartswith -> ticker is a field in Stock
        stock_list = Stock.objects.filter(ticker__istartswith = starts_with)
    if max_results > 0:
        if len(stock_list) > max_results:
            stock_list = stock_list[:max_results]
    return stock_list
######################################################
#This views for non-ajax call and is not using now.
#intraday is used for ajax call for this view
class IntradayQuote(TemplateView):
    template_name = 'stocks/intraday.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticker = self.kwargs.get('ticker').upper() #getting <ticker> value in url
        ##getting watchlist stock list if logged-in
        user_name = self.request.user.username
        if user_name:
            watchlist_user = User.objects.prefetch_related('watchlist').get(username__iexact=self.request.user.username)
            context['stock_list'] = watchlist_user.watchlist.stocks.all()
            context['watchlist_name'] = watchlist_user.watchlist.name
        else:
            context['stock_list'] = []
            context['watchlist_name'] = ''
        try:
            trend_dict = trending()
        except:
            trendDict = {}
        #to get name and realtime quote info

        try:
            stkObj = Stock.objects.get(ticker__iexact=ticker) # return object with exact match of ticker but case insensitive
            #stkObj = Stock.objects.filter(ticker__iexact=ticker) #return queryset
        except:
            context['result'] = 'error'
            return context
        else:
            # for stk in stkObj: #for queryset obj
            #     context['name'] = ' '.join(stk.name.split(" ")[:2])
            context['name'] = ' '.join(stkObj.name.split(" ")[:2])
            context['ticker'] = ticker
            context['indexTickers'] = ['^GSPC', '^DJI', '^IXIC']

            
        ##########################################
        try:
            quote = delay_intraday(ticker)
            #slicing one day intraday data
            quote = quote.loc[quote.index[-1].date(): ] #quote.loc[quote[-1:].index.date[0]: ]

            context['date'] = list(quote.index.strftime("%Y-%m-%d %H:%M:%S"))
            context['start'] = context['date'][0]
            context['end'] = context['date'][-1] #context['start'].split(' ')[0] + ' 16:00:00'
            context['result'] = 'success'
            #this is for invoking intradayChart() in js file
            #when new page is loaded but this is not for ajax call
            context['data_type'] = 'intraday'
            context['tickpos'] = ''
            context['tick_text'] = ''
            context['chartperiod'] = '1D'
        except:
            try:
                quote = daily(ticker, period='6m')
                #quote = iex_daily(ticker, period='6m')
                context['date'] = list(quote.index.strftime("%b %d, %y"))
                step = len(context['date'])/5
                tickdf = quote.iloc[[step, step*2, step*3, step*4]]
                context['tickpos'] = list(tickdf.index.strftime(("%b %d, %y")))
                context['tick_text'] = context['tickpos']
                context['start'] = context['date'][0]
                context['end'] = context['date'][-1]
                context['result'] = 'success'
                #this is for invoking hIntradayChart() in js file
                #when new page is loaded but this is not for ajax call
                context['data_type'] = 'daily'
                context['chartperiod'] = '6M'

            except:
                context['result'] = 'error'
                return context  #return early

        context['close'] = list(quote.close)
        context['open'] = list(quote.open)
        context['high'] = list(quote.high)
        context['low'] = list(quote.low)

        minClose = min(context['close']) # min() is build-in fn
        context['max'] = max(context['high'])
        context['min'] = minClose - ((context['max'] - minClose) * .25)

        maxVol = quote.volume.max() # quote.volume is Series and use series fn max()
        minVol = quote.volume.min()

        y = (max(context['low']) + quote.high.min()) * 0.5 #quote['adj close'].max() #quote.high.min()
        x = context['min'] * 0.9 + minClose * 0.1

        context['vol'] = list(((quote.volume - minVol) * ((y-x)/(maxVol - minVol))) + x)
        
        # switched to ajax
        #context['stockNews'] = news(ticker).to_dict('records') # save this for quick download
        #context_dict['stkIndexList']  = stkIndexList

        context['trending'] = list(trend_dict.keys())
        context['trendType'] = list(trend_dict.values())

        ########### 
        # lprice = quote.tail(1).close[0]
        # ldate = quote.tail(1).index[0]
        qinfo = quote_info(ticker, quote)

        if qinfo['changePercent'] < 0:
            context['changecolor'] = '#ff0000'
            context['changesymbol'] = 'glyphicon glyphicon-arrow-down'
        else:
            context['changecolor'] = '#009900'
            context['changesymbol'] = 'glyphicon glyphicon-arrow-up'

        context['changePercent'] = str(round(qinfo['changePercent'] * 100, 2)) + '%'
        context['change'] = round(qinfo['change'], 2)
        context['lastClose'] = qinfo['lastClose']
        context['latestPrice'] = qinfo['latestPrice']
        context['latestTime']= dt.datetime.strftime(qinfo['latestTime'], '%I:%M %p, %a')
        
        context['week52High'] = qinfo['week52High']
        context['week52Low'] = qinfo['week52Low']

        return context
####################################################################
class StkIndexView(TemplateView):
    template_name = 'stocks/stkindex.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticker = self.kwargs.get('ticker').upper() #getting <ticker> value in url

        user_name = self.request.user.username
        if user_name:
            watchlist_user = User.objects.prefetch_related('watchlist').get(username__iexact=self.request.user.username)
            context['stock_list'] = watchlist_user.watchlist.stocks.all()
            context['watchlist_name'] = watchlist_user.watchlist.name
        else:
            context['stock_list'] = []
            context['watchlist_name'] = ''

        try:
            trend_dict = trending()
        except:
            trendDict = {}

        ############# getting quote #########################
        try:
            quote = delay_intraday(ticker)
            #slicing one day intraday data
            quote = quote.loc[quote.index[-1].date(): ] #quote.loc[quote[-1:].index.date[0]: ]

            context['date'] = list(quote.index.strftime("%Y-%m-%d %H:%M:%S"))
            context['start'] = context['date'][0]
            context['end'] = context['date'][-1] #context['start'].split(' ')[0] + ' 16:00:00'
            context['result'] = 'success'
            #this is for invoking intradayChart() in js file
            #when new page is loaded but this is not for ajax call
            context['data_type'] = 'intraday'
            context['tickpos'] = ''
            context['tick_text'] = ''
            context['chartperiod'] = '1D'

        except:
            try:
                quote = daily(ticker, period='6m')
                #return string date format
                context['date'] = list(quote.index.strftime("%b %d, %y"))
                step = len(context['date'])/5
                tickdf = quote.iloc[[step, step*2, step*3, step*4]]
                context['tickpos'] = list(tickdf.index.strftime(("%b %d, %y")))
                context['tick_text'] = context['tickpos']
                context['start'] = context['date'][0]
                context['end'] = context['date'][-1]
                context['result'] = 'success'
                #this is for invoking hIntradayChart() in js file
                #when new page is loaded but this is not for ajax call
                context['data_type'] = 'daily'
                context['chartperiod'] = '6M'

            except:
                context['result'] = 'error'
                return context  #return early

        context['close'] = list(quote.close)
        context['open'] = list(quote.open)
        context['high'] = list(quote.high)
        context['low'] = list(quote.low)

        minClose = min(context['close']) # min() is build-in fn
        context['max'] = max(context['high'])
        context['min'] = minClose - ((context['max'] - minClose) * .25)

        maxVol = quote.volume.max() # quote.volume is Series and use series fn max()
        minVol = quote.volume.min()

        y = (max(context['low']) + quote.high.min()) * 0.5 #quote['adj close'].max() #quote.high.min()
        x = context['min'] * 0.9 + minClose * 0.1

        context['vol'] = list(((quote.volume - minVol) * ((y-x)/(maxVol - minVol))) + x)

        # switched to ajax
        #context['stockNews'] = news(ticker).to_dict('records') # save this for quick download

        context['trending'] = list(trend_dict.keys())
        context['trendType'] = list(trend_dict.values())

        context['ticker'] = ticker
        context['name'] = stkIndex[ticker]
        context['indexTickers'] = ['^GSPC', '^DJI', '^IXIC']
        #### trending row realtime quote ########
        try:
            context['latestTime'] = dt.datetime.strftime(quote.index[-1], "%I:%M %p")
        except:
            context['latestTime'] = dt.datetime.strftime(quote.index[-1], "%b %d") + " close price"
        #volume is float type
        context['latestVolume'] = f"{int(context['vol'][-1]):,d}"
        context['latestPrice'] = context['close'][-1]

        return context

# for ajax call
def intraday(request):
    data={}
    
    # need GET capitalized
    ticker = request.GET.get('ticker').strip().upper()
    data['ticker'] = ticker
    if ticker in stkIndex:
        data['name'] = stkIndex[ticker]
    else:
        try:
            stkObj = Stock.objects.filter(ticker__iexact=ticker)
        except:
            data['result'] = 'error'
            return JsonResponse(data)
        else:
            for stk in stkObj:
                data['name'] = ' '.join(stk.name.split(" ")[:2])

            
    if data['name']:
        try:
            quote = delay_intraday(ticker)
            data['result'] = 'success'
        except Exception as e:
            data['result'] = 'error'
        else:
            data['indexTickers'] = list(stkIndex.keys())
            # timeseries slicing for today's data
            # quote[-1:].index.date[0] return today's date
            quote = quote.loc[quote.index[-1].date(): ] #quote.loc[quote[-1:].index.date[0]: ]
            # stkObj = Stock.objects.get(ticker = ticker).name.split(" ")[:2] # no error if list has one element
            #
            # if len(stkObj) > 1:
            #     data['name'] = stkObj[0] + " " +stkObj[1]
            # else:
            #     data['name'] = stkObj[0]

            data['date'] = list(quote.index.strftime("%Y-%m-%d %H:%M:%S"))
            data['start'] = data['date'][0]
            data['end'] = data['date'][-1] #data['start'].split(' ')[0] + ' 16:00:00'

            data['close'] = list(quote.close)
            data['open'] = list(quote.open)
            data['high'] = list(quote.high)
            data['low'] = list(quote.low)

            minClose = min(data['close']) # min() is build-in fn
            data['max'] = max(data['high'])
            data['min'] = minClose - ((data['max'] - minClose) * .25)

            maxVol = quote.volume.max() # quote.volume is Series and use series fn max()
            minVol = quote.volume.min()

            y = (max(data['low']) + quote.high.min()) * 0.5 #quote['adj close'].max() #quote.high.min()
            x = data['min'] * 0.9 + minClose * 0.1

            data['vol'] = list(((quote.volume - minVol) * ((y-x)/(maxVol - minVol))) + x)
            
            # lprice = quote.tail(1).close[0]
            # ldate = quote.tail(1).index[0]
            qinfo = quote_info(ticker, quote)
            
            if qinfo['changePercent'] < 0:
                data['changecolor'] = '#ff0000'
                data['changesymbol'] = 'glyphicon glyphicon-arrow-down'
            else:
                data['changecolor'] = '#009900'
                data['changesymbol'] = 'glyphicon glyphicon-arrow-up'

            data['changePercent'] = str(round(qinfo['changePercent'] * 100, 2)) + '%'
            data['change'] = round(qinfo['change'], 2)
            data['lastClose'] = qinfo['lastClose']
            data['latestPrice'] = qinfo['latestPrice']
            data['latestTime']= dt.datetime.strftime(qinfo['latestTime'], '%I:%M %p, %a')
            
            data['week52High'] = qinfo['week52High']
            data['week52Low'] = qinfo['week52Low']
            #timestamp in microsecond, fromtimestamp() expect in second
            #datetime.datetime.fromtimestamp(q['extendedPriceTime']/1e3).strftime('%Y-%m-%d %H:%M:%S')
            # datetime.datetime.utcnow()
            # datetime.datetime.now()
    else:
        data['result'] = 'not_found'

    return JsonResponse(data)

def hdata(request):
    data = {}
    # fix exact number of days based on time it is accessed (off by 1 now)
    # chartPeriodDict = {'5D': 6, '1M': 30, '2M':60, '3M': 90,
    #                     '6M': 180, '1Y': 365, '2Y':730, '5Y': 1825}
    # will call this ajax only if chartPeriod is different
    chartPeriod = request.GET.get('chartPeriod')
    ticker = request.GET.get('ticker').strip()
    
    if chartPeriod == '5D':
        try:
            quote = delay_intraday(ticker)
        except:
            data['result'] = 'error'
            return JsonResponse(data) # so it doesn't evaluate bottom codes
        else:
            # timeseries dataFrame slicing, but need here coz, max data is 5 days
            #quote = quote.loc[dt.date.today() - dt.timedelta(6): ]
            data['date'] = list(quote.index.strftime("%b, %d %H:%M"))
            # following give 3 or 4 tick values
            # data['tickpos'] = data['date'][::len(data['date'])//5][1:-1]
            # data['tick_text'] = list(quote.index.strftime("%a, %I:%M %p"))[::len(data['date'])//5][1:-1]
            ## instead this give exact 4 ticks for all intervals
            step = len(data['date'])/5
            tickdf = quote.iloc[[step, step*2, step*3, step*4]]
            data['tickpos'] = list(tickdf.index.strftime("%b, %d %H:%M"))
            data['tick_text'] = list(tickdf.index.strftime("%a, %I:%M %p"))
            data['start'] = data['date'][0]
            data['end'] = data['date'][-1]
            data['result'] = 'success'
    elif chartPeriod == '1D':
        try:
            quote = delay_intraday(ticker)
        except:
            data['result'] = 'error'
            return JsonResponse(data)
        else:
            # even if start day is saturday or sunday and not in df
            # it would give rows that would come after the start day.
            quote = quote.loc[quote.index[-1].date(): ] #quote.loc[quote[-1:].index.date[0]: ]
            data['date'] = list(quote.index.strftime("%Y-%m-%d %H:%M:%S"))
            data['start'] = data['date'][0]
            data['end'] = data['date'][-1] #data['start'].split(" ")[0] + ' 16:00:00'
            data['result'] = 'success'
    else:
        try: ################## change this
            if ticker in stkIndex:
                quote = daily(ticker, period=chartPeriod)
            else:
                quote = daily(ticker, period=chartPeriod)
                #quote = iex_daily(ticker, period=chartPeriod.lower()) # if saving use df otherwise use quote direct
                # for iex , don't need slicing but for alpha this is needed
        except:
            data['result'] = 'error'
            return JsonResponse(data)
        else:
            #print(ticker, ': success')
            data['date'] = list(quote.index.strftime("%b %d, %y"))
            # data['tickpos'] = data['date'][::len(data['date'])//5][1:-1]
            # data['tick_text'] = data['tickpos']
            step = len(data['date'])/5
            tickdf = quote.iloc[[step, step*2, step*3, step*4]]
            data['tickpos'] = list(tickdf.index.strftime(("%b %d, %y")))
            data['tick_text'] = data['tickpos']
            data['start'] = data['date'][0]
            data['end'] = data['date'][-1]
            data['result'] = 'success'

    data['ticker'] = ticker
    data['close'] = list(quote.close)
    data['open'] = list(quote.open)
    data['high'] = list(quote.high)
    data['low'] = list(quote.low)

    minClose = quote.close.min() #min(data['close']) # min() is build-in fn
    data['max'] = quote.high.max() #max(data['high'])
    data['min'] = minClose - ((data['max'] - minClose) * .25)

    maxVol = quote.volume.max()
    minVol = quote.volume.min()
    y = (max(data['low']) + quote.high.min()) * 0.5
    x = data['min'] * 0.9 + minClose * 0.1

    data['vol'] = list(((quote.volume - minVol) * ((y-x)/(maxVol - minVol))) + x)

    #data['realVol'] = list(quote.volume)

    # for json data, np numeric type need to be float64, np.float32 is not json serializable
    return JsonResponse(data)

#### this is being replaced by intraday() in rnchartjs.js file
def symbol_search(request): # need this view for pressing enter after ticker input
    data = {}
    ticker = request.GET.get('ticker').upper()
    query = Stock.objects.filter(ticker__iexact=ticker)
    if query:
        data['result'] = 'success'
        #intraday(request)
    else:
        data['result'] = 'not_found'

    return JsonResponse(data)
###########################################

def financials(request):
    data = {}
    ticker = request.POST.get('ticker').upper()
    data['ticker'] = ticker
    try:
        financial_info = iex_financials(ticker)
    except:
        data['result'] = 'error'
    else:
        data['result'] = 'gotIt'
        data['reportDates'] = [r['reportDate'] for r in financial_info]
        for rd, r in zip(data['reportDates'], financial_info):
            data[rd] = r

    return JsonResponse(data)

### old version
# def alpha_intraday(symbol, interval = '1min'):
#     url = ('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&' +\
#         'symbol=' + symbol.upper() + '&interval=' + interval + '&outputsize=full' +\
#                 '&apikey=M3FRVGYYWC9JK7DK&datatype=csv')

#     df = pd.read_csv(url)
#     # to reverse the order
#     df = df[::-1]
#     # change timestamp from object type to datetime type
#     df.loc[:,'timestamp'] = pd.to_datetime(df['timestamp'])
#     # setting timestamp as index
#     df.set_index('timestamp', inplace = True)
#     return df

def alpha_intraday(symbol, outputsize='full', interval='1min', key=p_key, ):
    symbol = symbol.replace('.', '-').upper()
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + symbol+ "&interval=" + interval + "&outputsize="+outputsize+"&apikey=" + key
    # data = pd.DataFrame(requests.get(url).json())
    data = requests.get(url).json()
    data = data[list(data)[1]]
    data = pd.DataFrame(data.values(), index=list(data), dtype=np.float32)
    data.columns = [c.split(' ')[1] for c in list(data.columns)]
    data.index = pd.to_datetime(data.index, format='%Y-%m-%d %H:%M:%S')
    data = data[-1::-1] # reverse order to from old to latest
    return data

# def iex_daily(symbol, period = '1m'):
#     #url = "https://api.iextrading.com/1.0/stock/" + symbol + "/chart/" + period
#     #ochlcv = ['open', 'close','high', 'low', 'change', 'volume']
#     #data = pd.DataFrame(requests.get(url).json())
#     #df = data[ochlcv]
#     #df.index = pd.to_datetime(data.date)
#     df = pd.DataFrame()
#     return df

def alpha_daily(symbol, outputsize = 'full', key=p_key):
    symbol = symbol.replace('.', '-').upper()
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=" + symbol + "&outputsize="+ str(outputsize) +"&apikey=" + key
    # data = pd.DataFrame(requests.get(url).json())
    data = requests.get(url).json()
    try:
        data = data[list(data)[1]]
    except:
        print(symbol)
    
    data = pd.DataFrame(data.values(), index=list(data), dtype=np.float64)
    data.columns = [c.split(' ')[1] for c in list(data.columns)]
    data.index = pd.to_datetime(data.index, format='%Y-%m-%d')
            
    if sum(data.split != 1.0) > 0:
        adjust_split(data)
        
    data.sort_index(inplace=True)
    data['change_percent'] = data.close.pct_change().fillna(0) 
    data['change'] = data['change_percent'] * data.close.shift(fill_value = 0)
    
    # data.to_csv('data/' + symbol + '.csv')
    
    return data

def adjust_split(df):
   
    weight = df.split.cumprod().shift(fill_value=1.0)
        
    df.loc[:,'open'] = df.open / weight
    df.loc[:,'high'] = df.high / weight
    df.loc[:,'low'] = df.low / weight
    df.loc[:,'close'] = df.close / weight
    df.loc[:,'volume'] = (df.volume * weight).round(0)
    df.loc[:,'dividend'] = df.dividend / weight

def daily(symbol, period = '2Y'):
    chartPeriodDict = {'5D': 6, '10D': 13, '1M': 30, '2M':60, '3M': 90,
                        '6M': 180, '1Y': 365, '2Y':730, '5Y': 1825}
    # url = ('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&' +
    #     'symbol=' + symbol.upper() + '&outputsize=full' + '&apikey=M3FRVGYYWC9JK7DK&datatype=csv')

    # df = pd.read_csv(url)
    # # to reverse the order
    # df = df[::-1]

    # # change timestamp from object type to datetime type
    # df['timestamp'] = pd.to_datetime(df['timestamp'])
    # # setting timestamp as index
    # df.set_index('timestamp', inplace = True)
    df = alpha_daily(symbol)
    
    if period != 'YTD':
        df = df.loc[dt.date.today() - dt.timedelta(chartPeriodDict[period]): ]
    else:
        df = df.loc[str(dt.date.today().year) + '-01-01':]

    return df

def iex_financials(symbol):
    url = "https://api.iextrading.com/1.0/stock/" + symbol + "/financials"
    data = requests.get(url).json()
    #metrics = list(data['financials'][0].keys())

    return data['financials']

def delay_intraday(symbol, outputsize='full', interval='1min', key=p_key):
    symbol = symbol.replace('.', '-').upper()
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + symbol+ "&interval=" + interval + "&outputsize="+outputsize+"&entitlement=delayed&apikey=" + key
    # data = pd.DataFrame(requests.get(url).json())
    data = requests.get(url).json()
    data = data[list(data)[1]]
    data = pd.DataFrame(data.values(), index=list(data), dtype=np.float64)
    data.columns = [c.split(' ')[1] for c in list(data.columns)]
    data.index = pd.to_datetime(data.index, format='%Y-%m-%d %H:%M:%S')
    data = data[-1::-1] # reverse order to from old to latest
    ## for one day slicing
    # data = data.loc[data.index[-1].date():]

    return data

def quote(symbol, key=p_key):
    '''    
    Parameters
    ----------
    symbol : string
        Stock symbol.

    Returns
    -------
    data : dictionary

    '''
    symbol = symbol.replace('.', '-').upper()
    url = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=" + symbol +"&apikey=" + key
    # data = pd.DataFrame(requests.get(url).json())
    data = requests.get(url).json()
    # data = data[list(data)[1]]
    # data = pd.DataFrame(data.values(), index=list(data))
    # data.columns = [c.split(' ')[1] for c in list(data.columns)]
    data = {i.split('. ')[1]:j for i, j in list(data.values())[0].items()}
    
    
    return data

def quote_info(symbol, latestQ):
    df = daily(symbol)
    df = df.iloc[-252:]
    low52, high52 = df.low.min(), df.high.max() 
    lclose = df.close.iloc[-1]
    lprice = latestQ.close.iloc[-1]
    ldate = latestQ.index[-1]

    pchange = lprice - lclose

    data = {'change': pchange,
            'changePercent': pchange/lclose,
            'lastClose': lclose,
            'latestPrice': lprice,
            'latestTime': ldate,#.strftime(format="%Y-%m-%d %H:%M:%S"), 
            'week52High': high52, 
            'week52Low': low52}

    return data



# return dictionary of realtime quates for given symbol
# def iex_rtquote(symbol):
#     #url = "https://api.iextrading.com/1.0/stock/" + symbol + "/quote"
#     #data = requests.get(url).json()
#     # metric= ['changePercent','latestPrice', 'latestSource', 'latestTime', 'latestVolume', 'week52High', 'week52Low']
#     ### new version ###
#     data = {'changePercent':.1,'latestPrice':10, 'latestSource':'close', 'latestTime':'2023-09-08 11:30:45', 'latestVolume':1000, 'week52High':20, 'week52Low':5}
#     return data

def visitor_cookie_handler(request): # for old-> , response):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(dt.datetime.now()))
    last_visit_time = dt.datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    if (dt.datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(dt.datetime.now())
    else:
        visits = 1
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits

def get_server_side_cookie(request, cookie, default_val = None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

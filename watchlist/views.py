#from django.shortcuts import render, get_object_or_404
import datetime as dt
from random import choice
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.urls import reverse
from django.views import generic
from django.http import Http404, JsonResponse
# able to make user object of currently logged in user
from django.contrib.auth import get_user_model
User = get_user_model() # currently logged in user object in session

from watchlist.models import WatchList
from trends.views import trending
from stocks.views import delay_intraday, daily, quote_info
from stocks.models import Stock
from newsmedia.views import news
# Create your views here.

stkIndex = {'^GSPC': 'S&P 500', '^DJI': 'Dow Jones Industrial' , '^IXIC': 'Nasdaq Composite'}

class CreateWatchList(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description')
    model = WatchList
    template_name = 'watchlist/create_watchlist.html' # default is 'group_list.html'

# class SingleWatchlist(generic.DetailView):
#     model = WatchList
#     template_name = 'watchlist/watchlist_detail.html'

# for ajax call for tickers in watchlist
def watchlist_stocks(request):
    data = {}
    ticker = request.GET.get('ticker')
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
            # df[-1:].index.date[0] return today's date
            quote = quote.loc[quote.index[-1].date(): ]

            # stkObj = Stock.objects.get(ticker = ticker).name.split(" ")[:2] # no error if list has one element
            #
            # if len(stkObj) > 1:
            #     data['name'] = stkObj[0] + " " +stkObj[1]
            # else:
            #     data['name'] = stkObj[0]

            data['date'] = list(quote.index.strftime("%Y-%m-%d %H:%M:%S"))
            data['start'] = data['date'][0]
            data['end'] = data['date'][-1]

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

            ########## rt quote
            qinfo = quote_info(ticker, quote)
            # for m in metrics:
            #     data[m] = qinfo[m]
            if qinfo['changePercent'] < 0:
                data['changecolor'] = '#ff0000'
                data['changesymbol'] = 'glyphicon glyphicon-arrow-down'
            else:
                data['changecolor'] = '#009900'
                data['changesymbol'] = 'glyphicon glyphicon-arrow-up'

            data['changePercent'] = str(round(qinfo['changePercent'] * 100, 2)) + '%'
            data['change'] = qinfo['change']
            data['lastClose'] = qinfo['lastClose']
            data['latestPrice'] = qinfo['latestPrice']
            data['latestTime']= dt.datetime.strftime(qinfo['latestTime'], '%I:%M %p, %a')
            
            data['week52High'] = qinfo['week52High']
            data['week52Low'] = qinfo['week52Low']
            
    else:
        data['result'] = 'not_found'

    return JsonResponse(data)
#ajax call for removing ticker from watchlist
def remove_ticker(request):
    data = {}
    ticker = request.GET.get("ticker")
    try:
        #stkObj = Stock.objects.filter(ticker__iexact=ticker) #return queryset
        stkObj = Stock.objects.get(ticker__iexact=ticker) # return Stock object
        #this is user object
        userObj = User.objects.prefetch_related('watchlist').get(username__iexact=request.user.username)
        wl_obj = userObj.watchlist #this is WatchList obj
        # print(wl_obj.name)
        # print(wl_obj.stocks.all())
        # removing stkObj from watchlist
        wl_obj.stocks.remove(stkObj)
    except:
        data['result'] = "error"
    else:
        data['wl_name'] = wl_obj.name
        data['stock_list'] =  [ s.ticker for s in wl_obj.stocks.all()]
        # print(data['stock_list'])
        data['result'] = "success"
    return JsonResponse(data)
#ajax call for adding ticker to watchlist
def add_ticker(request):
    data = {}
    ## user_name for adding ticker in realtime quote
    data['user_name'] = request.user.username
    if data['user_name'] != '':
        ticker = request.GET.get("ticker")
        try:
            stkObj = Stock.objects.get(ticker__iexact=ticker) # return Stock object not queryset
            userObj = User.objects.prefetch_related('watchlist').get(username__iexact=request.user.username)
            wl_obj = userObj.watchlist #this is WatchList obj
            data['wl_name'] = wl_obj.name
        except:
            data['result'] = 'error'
        else:
            if stkObj not in wl_obj.stocks.all():
                #adding or associating stkObj with wl_obj if not already associated
                wl_obj.stocks.add(stkObj)
                data['result'] = 'success'
            else:
                data['result'] = 'already listed!'

        data['stock_list'] =  [ s.ticker for s in wl_obj.stocks.all()]
        #print(data['stock_list'])
    else:
        data['result'] = 'not_logged'
    return JsonResponse(data)
#### not in use: /stock/<ticker>/ or IntradayQuote taking the call
class WatchList_List(LoginRequiredMixin, generic.ListView):
    model = WatchList
    template_name = 'watchlist/watchlist_list.html' # default is 'group_list.html'
    context_object_name = 'stock_list'
    
    def get_queryset(self):
        try:
            # "self.request.user.username" returns username of currently logged in user
            self.watchlist_user = User.objects.prefetch_related('watchlist').get(username__iexact=self.request.user.username)
        except User.DoesNotExist:
            raise Http404
        else:
            return self.watchlist_user.watchlist.stocks.all()
            #if watchlist is not created when signup for accoutn then need to check if watchlist exist
            # if hasattr(self.watchlist_user, 'watchlist'): #to Check if watchlist is created for user
            #     return self.watchlist_user.watchlist.stocks.all()
            # else:
            #     return []
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['watchlist_name'] = self.watchlist_user.watchlist.name
        #if watchlist is not created when signup####
        # if hasattr(self.watchlist_user, 'watchlist'):
        #     context['watchlist_name'] = self.watchlist_user.watchlist.name
        # else:
        #     context['watchlist_name'] = ''
        try:
            trend_dict = trending()
        except:
            trendDict = {}

        if trend_dict:
            ticker = choice(list(trend_dict.keys()))
        else:
            ticker = 'AMD' # default dicker

        #to get name and realtime quote infp
        try:
            stkObj = Stock.objects.get(ticker__iexact=ticker) #return object
            #stkObj = Stock.objects.filter(ticker__iexact=ticker) #return queryset
        except:
            context['result'] = 'error'
            return context
        else:
            # for stk in stkObj:
            #     context['name'] = ' '.join(stk.name.split(" ")[:2])
            context['name'] = ' '.join(stkObj.name.split(" ")[:2])
            context['ticker'] = ticker
            context['indexTickers'] = ['^GSPC', '^DJI']
            
        ##########################################
        try:
            quote = delay_intraday(ticker)
            #slicing one day intraday data
            quote = quote.loc[quote.index[-1].date(): ]

            context['date'] = list(quote.index.strftime("%Y-%m-%d %H:%M:%S"))
            context['start'] = context['date'][0]
            context['end'] = context['start'].split(' ')[0] + ' 16:00:00'
            context['result'] = 'success'
            context['data_type'] = 'intraday'
            context['tickpos'] = ''
            context['tick_text'] = ''
            context['chartperiod'] = '1D'
        except:
            try:
                quote = daily(ticker, period='6m')
                context['date'] = list(quote.index.strftime("%b %d, %y"))
                step = len(context['date'])/5
                tickdf = quote.iloc[[step, step*2, step*3, step*4]]
                context['tickpos'] = list(tickdf.index.strftime(("%b %d, %y")))
                context['tick_text'] = context['tickpos']
                context['start'] = context['date'][0]
                context['end'] = context['date'][-1]
                context['result'] = 'success'
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

        context['businessNews'], context['stockNews'] = news(ticker) # save this for quick download
        #context_dict['stkIndexList']  = stkIndexList

        context['trending'] = list(trend_dict.keys())
        context['trendType'] = list(trend_dict.values())

        qinfo = quote_info(ticker, quote)
            
        if qinfo['changePercent'] < 0:
            context['changecolor'] = '#ff0000'
            context['changesymbol'] = 'glyphicon glyphicon-arrow-down'
        else:
            context['changecolor'] = '#009900'
            context['changesymbol'] = 'glyphicon glyphicon-arrow-up'

        context['changePercent'] = str(round(qinfo['changePercent'] * 100, 2)) + '%'
        context['change'] = qinfo['change']
        context['lastClose'] = qinfo['lastClose']
        context['latestPrice'] = qinfo['latestPrice']
        context['latestTime']= dt.datetime.strftime(qinfo['latestTime'], '%I:%M %p, %a')
        
        context['week52High'] = qinfo['week52High']
        context['week52Low'] = qinfo['week52Low']

        return context

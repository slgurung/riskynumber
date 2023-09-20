from django.views.generic import TemplateView
import datetime as dt
from random import choice
from trends.views import trending 
from stocks.views import daily , delay_intraday, quote_info

from stocks.models import Stock
from newsmedia.views import news

from django.contrib.auth import get_user_model


User = get_user_model() # currently logged in user object in session


class AboutView(TemplateView):
    template_name = "about.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            trend_dict = trending()#iex_trending()
        except:
            trend_dict = {}

        context['trending'] = list(trend_dict.keys())
        context['trendType'] = list(trend_dict.values())
        context['data_type'] = "abouthowto"
        return context

class HowtoView(TemplateView):
    template_name = "howto.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            trend_dict = trending() #iex_trending()
        except:
            trend_dict = {}

        context['trending'] = list(trend_dict.keys())
        context['trendType'] = list(trend_dict.values())
        context['data_type'] = "abouthowto"
        return context

class HomePage(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        default_ticker = ['AMD', 'AMZN', 'GOOG', 'AAPL']
        user_name = self.request.user.username
        if user_name:
            watchlist_user = User.objects.prefetch_related('watchlist').get(username__iexact=self.request.user.username)
            context['stock_list'] = watchlist_user.watchlist.stocks.all()
            context['watchlist_name'] = watchlist_user.watchlist.name
        else:
            context['stock_list'] = []
            context['watchlist_name'] = ''

        try:
            trend_dict = trending()#iex_trending()
        except:
            trend_dict = {}

        # if trend_dict:
        #     ticker = choice(list(trend_dict.keys()))
        # else:
        #     ticker = default_ticker
        ##############################

        ticker = choice(default_ticker)
        #to get name and realtime quote infp
        try:
            stkObj = Stock.objects.get(ticker__iexact=ticker) #return object with exact match with ticker but case insensitive
            #stkObj = Stock.objects.filter(ticker__iexact=ticker) #return queryset
        except:
            context['result'] = 'error'
            return context
        else:
            # for stk in stkObj:
            #     context['name'] = ' '.join(stk.name.split(" ")[:2])
            context['name'] = ' '.join(stkObj.name.split(" ")[:2])
            context['ticker'] = ticker.lower()
            context['indexTickers'] = ['^GSPC', '^DJI']
            
            
        ############## Getting stock data ############################
        try:
            
            quote = delay_intraday(ticker)
            #slicing one day intraday data
            quote = quote.loc[quote.index[-1].date(): ]

            context['date'] = list(quote.index.strftime("%Y-%m-%d %H:%M:%S"))
            context['start'] = context['date'][0]
            context['end'] = context['date'][-1] # context['start'].split(' ')[0] + ' 16:00:00'
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
           

        context['close'] = list(quote.close.round(2))
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

        ##### latest quote ########
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
        

# -*- coding: utf-8 -*-
"""
Created on Mon May 31 23:39:18 2021

@author: mars
"""
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# import seaborn as sns
# premium api
# UP72PBB1TUSTYMHK

# keys= [ 'M3FRVGYYWC9JK7DK', 'YQ5YQ1A0BXWSDG2M', 'XL0YEZ35RX2G1D5B', 'AH998A0QGGTXHVDW', 
#        '35PQ93AC1LY1CVZF', 'RCCCBP6U7Z7Q12AM', 'HYZ45XR4GBLMTSAQ', 'CH0U1CSCETX5FTSI', 'GIEXO1UE5UV2ZJOK']
p_key = 'UP72PBB1TUSTYMHK'

'''
To access 15-minute delayed US stock market data, please append entitlement=delayed to the data request. For example:
https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&entitlement=delayed&apikey=UP72PBB1TUSTYMHK
'''

def intraday(symbol, key=p_key, interval='1min'):
    symbol = symbol.replace('.', '-').upper()
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + symbol+ "&interval=" + interval + "&outputsize=full&apikey=" + key
    # data = pd.DataFrame(requests.get(url).json())
    data = requests.get(url).json()
    data = data[list(data)[1]]
    data = pd.DataFrame(data.values(), index=list(data), dtype=np.float32)
    data.columns = [c.split(' ')[1] for c in list(data.columns)]
    data.index = pd.to_datetime(data.index, format='%Y-%m-%d %H:%M:%S')
    data = data[-1::-1] # reverse order to from old to latest
    return data


def delay_intraday(symbol, key=p_key, interval='5min'):
    symbol = symbol.replace('.', '-').upper()
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + symbol+ "&interval=" + interval + "&entitlement=delayed&apikey=" + key
    # data = pd.DataFrame(requests.get(url).json())
    data = requests.get(url).json()
    data = data[list(data)[1]]
    data = pd.DataFrame(data.values(), index=list(data) , dtype=np.float32)
    data.columns = [c.split(' ')[1] for c in list(data.columns)]
    data.index = pd.to_datetime(data.index, format='%Y-%m-%d %H:%M:%S')
    data = data[-1::-1] # reverse order to from old to latest
    ## slicing for one day
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

def add_today(df, price):
    ###########
    # currently it don't save price into the stock csv file
    # if it saves, need to adjust the latest updated index in daily_update()
    ######################
    t = pd.Timestamp.today()   
    i = pd.to_datetime(t.date(), format = '%Y-%m-%d')
    df.loc[i, ['volume']]= int(df.tail(100).volume.mean())
    df.loc[i, ['open', 'close', 'high', 'low']]=price
    # new_row = pd.DataFrame(df.tail(1).values, index= [i], columns= df.columns)
    # new_df = df.append(new_row)
    df.loc[i, ['change', 'change_percent']]=0
    return df
    

def get_latest_trading_day(symbol='AAPL'):
    t = pd.Timestamp.today()    
    # th = get_trading_holiday()
    ltd = pd.read_csv('latest_trading_day.csv', parse_dates=['latest_trading_day', 'expire_date'])
    
        
    if t > ltd['expire_date'].to_list()[0]:
        try:
            q = quote(symbol) # returns 15-min delay data
        except:
            print('error thrwon by quote()')
            
        ltd.loc[0, 'latest_trading_day'] = q['latest trading day']
        expire_date = ltd['latest_trading_day'].to_list()[0]
        
        if expire_date.weekday() == 4:
            expire_date += timedelta(days=3)
        else: 
            expire_date += timedelta(days=1)
            
        # adjust trading holiday
        if expire_date in get_trading_holiday():
            expire_date += timedelta(days=1)
            
        #for 15-delay data    
        expire_date = expire_date.replace(hour=16, minute=15, second=0)        
        
        ltd.loc[0, 'expire_date'] = expire_date        
        ltd.to_csv('latest_trading_day.csv', index=False)
          
    return ltd['latest_trading_day'].to_list()[0]

    
    
def get_trading_holiday():
    # for 2023, but need to expand
    nyd = pd.to_datetime('2023-01-02', format='%Y-%m-%d')
    mld = pd.to_datetime('2023-01-16', format='%Y-%m-%d')
    wbd = pd.to_datetime('2023-02-20', format='%Y-%m-%d')
    gf = pd.to_datetime('2023-04-07', format='%Y-%m-%d')
    md = pd.to_datetime('2023-05-29', format='%Y-%m-%d')
    jt = pd.to_datetime('2023-06-19', format='%Y-%m-%d')
    ind = pd.to_datetime('2023-07-04', format='%Y-%m-%d')
    ld = pd.to_datetime('2023-09-04', format='%Y-%m-%d')
    tgd = pd.to_datetime('2023-11-23', format='%Y-%m-%d')
    cd = pd.to_datetime('2023-12-25', format='%Y-%m-%d')
    
    trading_holiday = [nyd, mld, wbd, gf, md, jt, ind, ld, tgd, cd]
    
    return trading_holiday
    
def is_updated(symbol):
    tickers = pd.read_csv('stock_list.csv', index_col=0)
    symbol = symbol.upper()
    
    if symbol not in tickers.symbol.to_list():
        return -1
    else:
        data = pd.read_csv('data/' + symbol + '.csv', index_col=0, parse_dates=True)
        latest_updated_index = data.index[-1] 
        ltd = get_latest_trading_day()
        
        if ltd.weekday() == 0:
            days_to_update = ltd - latest_updated_index - timedelta(days=2)
        else:
            days_to_update = ltd - latest_updated_index
            
    return days_to_update.days

def daily_updated(symbol, days_to_update):    
    # tickers = pd.read_csv('stock_list.csv', index_col=0)
    # symbol = symbol.upper()    
    # days_to_update = is_updated(symbol)
    symbol = symbol.replace('.', '-').upper()
    
    if days_to_update == -1:
        # print('not found') 
        tickers = pd.read_csv('stock_list.csv', index_col=0)       
        data = daily(symbol) #[['open', 'adjusted','high', 'low', 'volume','change', 'changePercent']]
        #data.rename(columns= {'adjusted':'close'}, inplace=True)
        data.to_csv('data/' + symbol + '.csv')
        
        # tickers = pd.concat([tickers, pd.DataFrame({'symbol': [symbol]})], ignore_index=True)
        tickers.loc[len(tickers.index)] = [symbol]
        tickers.to_csv('stock_list.csv')
    else:
        # # print('found')
        # data = pd.read_csv('data/' + symbol + '.csv', index_col=0, parse_dates=True) 
        
        # # checking if last row is intraday or final closing price if add_today() save price
        # # latest_updated_index = data.index[-1] if ck_vals['hour'] >= 16 else data.index[-2]
        # ######################################
        # latest_updated_index = data.index[-1] 
        
        # ltd = get_latest_trading_day()
        
        # if ltd.weekday() == 0:
        #     days_to_update = ltd - latest_updated_index - timedelta(days=2)
        # else:
        #     days_to_update = ltd - latest_updated_index
        
        ##### upload full data everytime ####
        data = daily(symbol) #[['open', 'adjusted','high', 'low', 'volume','change', 'changePercent']]
        #data.rename(columns= {'adjusted':'close'}, inplace=True)
        data.to_csv('data/' + symbol + '.csv') 
        #################################
                   
        # if days_to_update >= 99: #timedelta(days=99):
        #     data = daily(symbol) #[['open', 'adjusted','high', 'low', 'volume','change', 'changePercent']]
        #     #data.rename(columns= {'adjusted':'close'}, inplace=True)
        #     data.to_csv('data/' + symbol + '.csv')   
            
        # elif days_to_update >= 1: #timedelta(days=2):
            
        #     df = daily_limit(symbol, days_to_update) #[['open', 'adjusted','high', 'low', 'volume','change', 'changePercent']]
        #     #df.rename(columns= {'adjusted':'close'}, inplace=True)
            
        #     #removing the not updated last row if any
        #     if data.index[-1] == df.index[0]:
        #         data = data[:-1]
                
        #     data = pd.concat([data, df])
        #     data.to_csv('data/' + symbol + '.csv')   
                
        # elif days_to_update == 1: #timedelta(days=1):
        #     # print('111111111')
        #     try:
        #         q = quote(symbol)
        #     except:
        #         print(symbol)
        #     qdate = pd.to_datetime(q['latest trading day'], format='%Y-%m-%d')
        #     data.loc[qdate] = 0
        #     data.loc[qdate, 'close'] = float(q['price'])
        #     data.loc[qdate, 'adjusted'] = float(q['price'])
        #     data.loc[qdate, 'open'] = float(q['open']) 
        #     data.loc[qdate, 'high'] = float(q['high']) 
        #     data.loc[qdate, 'low'] = float(q['low']) 
        #     data.loc[qdate, 'volume'] = int(q['volume'])
        #     data.loc[qdate, 'split'] = 1.0
        #     data.loc[qdate, 'change'] = float(q['change'])
        #     data.loc[qdate, 'change_percent'] = round(float(q['change'])/float(q['previous close']), 6)
        
        #     data.to_csv('data/' + symbol + '.csv')
                
    return data    

def highlowlas(symbol, key=p_key):
    df = daily(symbol)
    df = df.tail(252)
    low52, high52 = df.low.min(), df.high.max() 
    lclose = df.tail(1).close[0]
    
    return high52, low52, lclose 



def daily(symbol, key=p_key, outputsize = 'full'):
    symbol = symbol.replace('.', '-').upper()
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=" + symbol + "&outputsize="+ str(outputsize) +"&apikey=" + key
    # data = pd.DataFrame(requests.get(url).json())
    data = requests.get(url).json()
    try:
        data = data[list(data)[1]]
    except:
        print(symbol)
    
    data = pd.DataFrame(data.values(), index=list(data), dtype=np.float32)
    data.columns = [c.split(' ')[1] for c in list(data.columns)]
    data.index = pd.to_datetime(data.index, format='%Y-%m-%d')
            
    if sum(data.split != 1.0) > 0:
        adjust_split(data)
        
    data.sort_index(inplace=True)
    data['change_percent'] = data.close.pct_change().fillna(0) 
    data['change'] = data['change_percent'] * data.close.shift(fill_value = 0)
    
    # data.to_csv('data/' + symbol + '.csv')
    
    return data

def daily_limit(symbol, outputsize = 100, key=p_key): # max outputsize = 100
    symbol = symbol.replace('.', '-').upper()
    # don't have split column
    # url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + symbol+ "&apikey=" + key
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=" + symbol+ "&apikey=" + key
    # data = pd.DataFrame(requests.get(url).json())
    data = requests.get(url).json()
    data = data[list(data)[1]]
    
    data = pd.DataFrame(data.values(), index=list(data), dtype=np.float32)
    data.columns = [c.split(' ')[1] for c in list(data.columns)]
    data.index = pd.to_datetime(data.index, format='%Y-%m-%d')
    
    if sum(data.split != 1.0) > 0:
        adjust_split(data)
            
    data.sort_index(inplace=True)
    data['change_percent'] = data.close.pct_change().fillna(0) 
    data['change'] = data['change_percent'] * data.close.shift(fill_value = 0)
    
    return data.tail(outputsize) #.iloc[-outputsize:]

def adjust_split(df):
   
    weight = df.split.cumprod().shift(fill_value=1.0)
        
    df.loc[:,'open'] = df.open / weight
    df.loc[:,'high'] = df.high / weight
    df.loc[:,'low'] = df.low / weight
    df.loc[:,'close'] = df.close / weight
    df.loc[:,'volume'] = (df.volume * weight).round(0)
    df.loc[:,'dividend'] = df.dividend / weight

#################################Old###############################################

def add_row(index_date, df):
    # pd.to_datetime('2022-02-08', format="%Y-%m-%d")
    # values is np array, df is updating
    i = pd.to_datetime(index_date, format = '%Y-%m-%d')
    new_row = pd.DataFrame(df.tail(1).values, index= [i], columns= df.columns)
    new_df = df.append(new_row)
    return new_df


    
def read_data(symbol):
    df = pd.read_csv('data/' + symbol + '.csv', index_col=0, parse_dates=True)
    
    return df

def plot_stock(symbol, period=None):
    df = pd.read_csv('data/'+ symbol + '.csv', index_col=0)
    df['ma20'] = df.close.rolling(window=20).mean()
    df['ma50'] = df.close.rolling(window=50).mean()
    df['ema20'] = df.close.ewm(span=20, adjust=False).mean()
    df['ema12'] = df.close.ewm(span=12, adjust=False).mean()
    df['ema26'] = df.close.ewm(span=26, adjust=False).mean()
    df['macd'] = df['ema12'] - df['ema26']
    df['signal'] = df.macd.ewm(span=9, adjust=False).mean()
    # df['rsi'] = calc_rsi(df.close)
    # print(df.tail())
    
    plt.close()
    fig, ax = plt.subplots()
    ax.plot(df.index, df['macd'], label='MACD', color='red')
    ax.plot(df.index, df['signal'], label='signal', color='blue')
    # ax.plot(df.index, df['rsi'], label='rsi', color='black')
    ax2 = ax.twinx()
    ax2.plot(df.index, df.close)
    ax.legend(loc='upper left')
    ax.grid(True)
    ax.set_xticklabels(df.index[::1], rotation=90)
    plt.show()
        
def calc_rsi(col):
    delta = col.diff()
    up = delta.clip(lower=0)
    down = delta.clip(upper=0).abs()
    ema_up = up.ewm(com=13, adjust=False).mean()
    ema_down = down.ewm(com=13, adjust=False).mean()
    rs = ema_up/ema_down
    rsi = 100 - (100/(1 + rs))
    
    return rsi

def rsi(symbol, interval='daily'):
    symbol = symbol.replace('.', '-').upper()
    url = 'https://www.alphavantage.co/query?function=RSI&symbol=' + symbol.upper()+'&interval='+ interval + '&time_period=14&series_type=close&apikey=' + p_key
    data = requests.get(url).json()['Technical Analysis: RSI']  
    data = pd.DataFrame(data.values(), index=data.keys())
    return data

def on_balance_vol(df):
    obv = [0]
    for i in range (1, len(df)):
        if df.change[i] > 0:
            obv.append(obv[-1] + df.volume[i])
        elif df.change[i] < 0:
            obv.append(obv[-1] - df.volume[i])
        else:
            obv.append(obv[-1])
            
    df['obv'] = obv
    df['obv_ema'] = df['obv'].ewm(span=20).mean()
    
    # return df
            
    

def calc_macd(df):
    # df['ma20'] = df.close.rolling(window=20).mean()
    # df['ma50'] = df.close.rolling(window=50).mean()
    df['ema20'] = df.close.ewm(span=20, adjust=False).mean()
    df['ema12'] = df.close.ewm(span=12, adjust=False).mean()
    df['ema26'] = df.close.ewm(span=26, adjust=False).mean()
    df['macd'] = df['ema12'] - df['ema26']
    df['signal'] = df.macd.ewm(span=9, adjust=False).mean()
    df['rsi'] = calc_rsi(df.close)
    # # normalizing in macd period
    # df['rsi_norm'] = (df.macd.max() - df.macd.min()) * ((df.rsi - df.rsi.min())/(df.rsi.max() - df.rsi.min())) + df.macd.min()

def calc_ma(df):
    df['ma5'] = df.close.rolling(window=5).mean().fillna(method='bfill').round(2)
    df['ma10'] = df.close.rolling(window=10).mean().fillna(method='bfill').round(2)
    df['ma20'] = df.close.rolling(window=20).mean().fillna(method='bfill').round(2)
    df['ma50'] = df.close.rolling(window=50).mean().fillna(method='bfill').round(2)
    df['ma100'] = df.close.rolling(window=100).mean().fillna(method='bfill').round(2)
    df['ma200'] = df.close.rolling(window=200).mean().fillna(method='bfill').round(2)
    df['ma300'] = df.close.rolling(window=300).mean().fillna(method='bfill').round(2)
    
  
    # return df[['ma5','ma10','ma20','ma50','ma100','ma200']]

def calc_ema(df):
    df['ema5'] = df.close.ewm(span=5, adjust=False).mean().round(2)
    df['ema10'] = df.close.ewm(span=10, adjust=False).mean().round(2)
    df['ema20'] = df.close.ewm(span=20, adjust=False).mean().round(2)
    df['ema50'] = df.close.ewm(span=50, adjust=False).mean().round(2)
    df['ema100'] = df.close.ewm(span=100, adjust=False).mean().round(2)
    df['ema200'] = df.close.ewm(span=200, adjust=False).mean().round(2)
    df['ema500'] = df.close.ewm(span=500, adjust=False).mean().round(2)

def get_ticker(kw):
    url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords='+ kw + '&apikey=' + p_key
    r = requests.get(url)
    data = r.json()
    return data
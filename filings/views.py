
from django.http import JsonResponse

from stocks.models import Stock
# Create your views here.

import requests
import pandas as pd

def sec_filing(request):
    data = {}
    ticker = request.POST.get('ticker').upper()
    data['ticker'] = ticker
    if ticker not in ['^GSPC', '^DJI', '^IXIC']:
        try:
            stk_cik = Stock.objects.get(ticker = ticker).cik
        except Exception as e:
            #print("error is : ", e)
            data['result'] = 'no_cik'
        else:
            data['filing_list'] = get_filings(stk_cik)
            data['result'] = 'gotIt'
    else:
        data['result'] = 'invalid'

    return JsonResponse(data)

  

def get_filings(cik, number=100):
    
    cik10 = f'{cik:0>10s}'
    url = 'https://data.sec.gov/submissions/CIK' + cik10 + '.json'
    headers = { "User-Agent": "phewataal@outlook.com"}
    filings = requests.get(url, headers=headers).json()['filings']['recent']
    filings = pd.DataFrame(filings)
    data_link = 'https://www.sec.gov/Archives/edgar/data/' + cik + '/' 
    filings['url'] = filings.apply(lambda r: data_link + ''.join(r['accessionNumber'].split('-')) + '/' + r['primaryDocument'], axis=1)
    


    filings = filings.loc[:,['filingDate', 'form', 'primaryDocDescription', 'url']].iloc[:number]

    filings.rename(columns={'filingDate': 'filing_date', 'primaryDocDescription': 'description'}, inplace=True)
    filings = filings.to_dict('records')
    
    return filings



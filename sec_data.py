# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 12:24:37 2023

@author: mars
"""
import requests
import pandas as pd

def get_latest_filings(symbol):
   
    ###################### SEC resources ##############
    # Apple CIK: 320193
    # accessing doc using link
    # link = https://www.sec.gov/Archives/edgar/data/<cik>/<accessionNumber without - >/<primaryDocument >
    # ticker with cik file
    # https://www.sec.gov/include/ticker.txt
    # ticker, company name and cik
    # https://www.sec.gov/files/company_tickers.json
    #############################################################################
    
    cik = get_cik(symbol)
    cik10 = f'{cik:0>10s}'
    url = 'https://data.sec.gov/submissions/CIK' + cik10 + '.json'
    headers = { "User-Agent": "phewataal@outlook.com"}
    filings = requests.get(url, headers=headers).json()['filings']['recent']
    filings = pd.DataFrame(filings)
    data_link = 'https://www.sec.gov/Archives/edgar/data/' + cik + '/' 
    filings['url'] = filings.apply(lambda r: data_link + ''.join(r['accessionNumber'].split('-')) + '/' + r['primaryDocument'], axis=1)
    
    return filings

def get_cik(symbol):
    # return cik col as 10 character long string because of dtype='object'
    df = pd.read_csv('sec_cik.csv', dtype='object')
    cik = str(df.loc[df['ticker'] == symbol.upper(), 'cik'].to_list()[0])
    return cik
    
def download_cik():
    '''
       Returns dataframe of cik
    -------
    cik : TYPE
        DESCRIPTION.

    '''
    url = 'https://www.sec.gov/files/company_tickers.json'
    headers = { "User-Agent": "suryagrg@hotmail.com"}
    df = requests.get(url, headers=headers).json()
    df = [ v for k, v in df.items() ]
    df = pd.DataFrame(df)
    df.rename(columns={'cik_str': 'cik'}, inplace=True)
    # changing all cik to 10 characters long string and need to change to dtype to "object" when reading the file
    # df.cik = df.cik.map(lambda x: f'{x:0>10d}')
    # when reading this file need to put dtype to 'object' in order to prevent automatice convert cik col to int
    df.to_csv('sec_cik.csv', index= False)
    


if __name__ == "__main__":
    download_cik()

# Import libraries
from lxml import html
from selenium import webdriver
import requests
import time


def clean_value(val):
    ret = 0
    if 'B' in val:
        ret  = float(val.replace("B", "")) * 1000000000
    elif 'M' in val:
        ret  = float(val.replace("M", "")) * 1000000
    if ret == 0:
        print(f'Error on cleaning the data, try it later or with another ticker [current val = {val} ]')
    return ret


def get_data(ticker, verbose= False): 
    #make request
    page = requests.get('https://finance.yahoo.com/quote/'+ticker+'/key-statistics?p='+ticker,headers={'User-Agent': 'Custom'})
    if (page.status_code != 200):
        print(f'Error screaping the website try it later or with another ticker [response status code: {page.status_code}]')
        return 0
        
    #parse content 
    tree = html.fromstring(page.content)
    
    try:
        EV_EBITDA = float(tree.xpath('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[9]/td[2]/text()')[0])
    except:
        print('Error screaping the website try it later or with another ticker')
        return 0
    if verbose: 
        print(f'EV_EBITDA = {EV_EBITDA}')
   

    try:
        d = str(tree.xpath('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[5]/div/div/table/tbody/tr[3]/td[2]/text()')[0])
    except:
        print('Error screaping the website try it later or with another ticker')
        return 0
    Debt = clean_value(d)
    if Debt == 0:
        return 0
    if verbose: 
        print(f'Debt = {Debt}')
    
    
    try:
        s = str(tree.xpath('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[2]/div/div[2]/div/div/table/tbody/tr[3]/td[2]/text()')[0])
    except:
        print('Error screaping the website try it later or with another ticker')
        return 0

    share_outstanding = clean_value(s)
    if share_outstanding == 0:
        return 0
    if verbose: 
        print(f'Share_outstanding = {share_outstanding}')
    
    
    try:
        e = str(tree.xpath('//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[4]/div/div/table/tbody/tr[5]/td[2]/text()')[0])
    except:
        print('Error screaping the website try it later or with another ticker')
        return 0
    
    EBITDA = clean_value(e)
    if EBITDA == 0:
        return 0
    if verbose: 
        print(f'EBITDA = {EBITDA}')
    
    
    try:
        real_P = float(tree.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div[1]/fin-streamer[1]/text()')[0].replace(",", ""))
    except:
        print('Error screaping the website try it later or with another ticker')
        return 0
    if verbose: 
        print(f'Real price = {real_P}')
    
    return [EV_EBITDA, Debt,  share_outstanding, EBITDA, real_P]

def caclulate_price(data): 

    #Calculate price
    EV = data[3] * data[0]
    Price = (EV - data[1]) / data[2]
    
    print(f'Share price: **{Price:0.2f}**$ vs real price: {data[4] :0.2f} (diff {(Price/data[4] -1)*100:0.2f}%)')
    return 
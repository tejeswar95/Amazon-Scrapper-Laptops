import pandas as pd
from bs4 import BeautifulSoup
import requests

def GetRequest(URL):
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0 AtContent/100.5.5924.25-619As:','Accept-Language': 'en-US, en;q=0.5'})
    webpage = requests.get(URL,headers=HEADERS)
    while webpage.status_code !=200:
        print(webpage.status_code)
        webpage = requests.get(URL)
    return webpage

def GetDF():
    html = GetRequest('https://www.cpubenchmark.net/cpu_list.php')
    soup = BeautifulSoup(html.text,'lxml')
    res = soup.find_all('table')[1].find('tbody').find_all('tr')
    #print(res)
    CPU = {'Model':[],'Performance':[]}
    for r in res:
        temp=r.find('a')
        if(temp != None):
            CPU['Model'].append(temp.text)
        temp=r.find_all('td')[1]
        if(temp != None):
            CPU['Performance'].append(int(temp.text.replace(",","")))
    
    df = pd.DataFrame(CPU)
    df = df.sort_values(by='Performance',ascending=False)
    df.index = range(len(df))
    for i in range(len(df)):
        model=df.loc[i,'Model']
        if model.find('AMD') == -1 and model.find('Intel') == -1 :
            df=df.drop(i)
    
    df.index = range(len(df))
    return df

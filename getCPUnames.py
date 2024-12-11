import pandas as pd
from bs4 import BeautifulSoup
import requests

def GetRequest (URL):
    webpage = requests.get(URL)
    while webpage.status_code !=200:
        webpage = requests.get(URL)
    return webpage

def GetProcessor(CPU):
    if(CPU == "Intel"):
        URL="https://en.wikipedia.org/wiki/Intel_Core"
    else:
        URL="https://en.wikipedia.org/wiki/List_of_AMD_Ryzen_processors"
    d = GetRequest(URL)
    soup = BeautifulSoup(d.text,'lxml')
    tables = soup.find_all('table', class_="wikitable sortable")
    
    for i in range(len(tables)):
        tables[i] = tables[i].tbody
    
    result=[]
    
    for table in tables:
        res= table.find_all('tr')
        for r in res:
            t=r.find('a',class_ = "external text")
            if t != None:
                if t.text.find('PRO')!= -1 or t.text.find('Z1')!= -1:
                    continue
                result.append(t.text)
    
    return result

def GetDF():
    List=GetProcessor('AMD')+GetProcessor('Intel')
    return pd.DataFrame({"Processors": List})

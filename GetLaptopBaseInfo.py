import pandas as pd
from bs4 import BeautifulSoup
import requests

def GetRequest (URL):
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0 AtContent/100.5.5924.25-619As:','Accept-Language': 'en-US, en;q=0.5'})
    webpage = requests.get(URL, headers=HEADERS)
    while webpage.status_code !=200:
        webpage = requests.get(URL, headers=HEADERS)
    return webpage

def GetUrlList(URL):
    UrlList=[]
    webpage = GetRequest(URL)
    UrlList.append(URL)
    
    soup =BeautifulSoup(webpage.text,'html.parser')
    limit = int(soup.find('span',class_="s-pagination-item s-pagination-disabled").text)
    
    for i in range(limit):
        data = soup.find('a',class_="s-pagination-item s-pagination-next s-pagination-button s-pagination-button-accessibility s-pagination-separator")
        URL = 'https://www.amazon.in'+ data['href']
        UrlList.append(URL)
    
    return UrlList

URL="https://www.amazon.in/s?k=laptop&i=computers&rh=p_36%3A3000000-5000000&s=exact-aware-popularity-rank&qid=1732688673&rnid=7252027031&ref=sr_st_exact-aware-popularity-rank&ds=v1%3AyIcZ7pT8Ozr4kZ7t7KctRaEH9KLwCLwvCadOaskcTow"

dict = {'Name':[],"Link":[],"Price":[]}

for url in GetUrlList(URL):
    webpage = GetRequest(url)
    soup =BeautifulSoup(webpage.text,'html.parser')
    data = soup.find_all('div',class_="sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16")
    products =[]

    for d in data:
        products.append(soup.find('a',class_="a-link-normal s-no-hover s-underline-text s-underline-link-text s-link-style a-text-normal"))
        temp = d.find('div',class_="puisg-col puisg-col-4-of-12 puisg-col-8-of-16 puisg-col-12-of-20 puisg-col-12-of-24 puis-list-col-right")
        t=''
        
        try:
            t=temp.find('a', class_ = "a-link-normal s-no-hover s-underline-text s-underline-link-text s-link-style a-text-normal").span.span.text
        except AttributeError:
            continue
        
        dict['Link'].append('https://www.amazon.in'+temp.find('a')['href'])
        dict['Name'].append(temp.find('a').span.text)
        dict['Price'].append(t.replace('₹', '').replace(',', ''))
        
df=pd.DataFrame(dict)
df.to_csv('laptops.csv',header=True,index=False)




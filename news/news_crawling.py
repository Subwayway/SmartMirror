import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

url = 'https://m.news.naver.com/rankingList.nhn'
response=urllib.request.urlopen(url)
soup=BeautifulSoup(response,'html.parser')
results=soup.select("div.commonlist_tx_headline")
i=1
for result in results:
    print(str(i)+ ". " +result.string)
    i+=1
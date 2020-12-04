import urllib.request
import urllib.parse
from bs4 import BeautifulSoup



def news_update():
    global news_value
    news_value = []

    i = 0

    url = 'https://m.news.naver.com/rankingList.nhn'
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response, 'html.parser')
    results = soup.select("div.commonlist_tx_headline")

    for result in results:
        #print(str(i) + ". " + result.string)

        news_value.append(str(i) + ". " + result.string)

        i += 1

#-----test code-----
#news_update()
#print(news_value[0])
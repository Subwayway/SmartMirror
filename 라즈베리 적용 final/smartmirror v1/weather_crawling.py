from urllib.request import urlopen, Request
import urllib
import bs4


def weather_read(loc):  #loc = str자료형
    global location
    global temp
    global climate

    location = loc
    enc_location = urllib.parse.quote(location + '+날씨')

    url = 'https://search.naver.com/search.naver?ie=utf8&query=' + enc_location

    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = bs4.BeautifulSoup(html, 'lxml')  # html5lib오류 발생시 lxml로 변경
    print('현재 ' + location + ' 날씨는 ' +
          soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text
          + "˚ " + soup.find('p', class_='cast_txt').text)


    #날씨 데이터 저장
    temp = soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text

    split_info = soup.find('p', class_='cast_txt').text
    climate = split_info.split(",") #climate[0] = 기후

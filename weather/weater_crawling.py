from urllib.request import urlopen, Request
import urllib
import bs4

location = '성남시'
enc_location = urllib.parse.quote(location + '+날씨')

url = 'https://search.naver.com/search.naver?ie=utf8&query='+ enc_location

req = Request(url)
page = urlopen(req)
html = page.read()
soup = bs4.BeautifulSoup(html,'lxml') #html5lib오류 발생시 lxml로 변경
print('현재 ' + location + ' 날씨는 ' +
      soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text
      + "˚ " + soup.find('p',class_='cast_txt').text  )

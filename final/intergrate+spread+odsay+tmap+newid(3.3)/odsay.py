import json
import requests


Departure_longitude = 0
Departure_latitude = 0
arrival_longitude = 0
arrival_latitude = 0

resultdata = ''


def req_direction():
    global Departure_longitude
    global Departure_latitude
    global arrival_longitude
    global arrival_latitude
    global resultdata

    URL_direction = 'https://api.odsay.com/v1/api/searchPubTransPathR'
    params_direction = {'apiKey': '',
              'lang': '0',
              'output': 'json',
              'SX': str(Departure_longitude),   # 출발 경도
              'SY': str(Departure_latitude),    # 출발 위도
              'EX': str(arrival_longitude),   # 도착 경도
              'EY': str(arrival_latitude),    # 도착 위도
              'OPT': '0',   # 최단거리
              'SearchType': '0',    # 도시내 이동
              'SearchPathType': '0'  # 지하철 + 버스 모두

    }
    response_direction = requests.get(URL_direction, params=params_direction)

    # status코드 200 == 요청완료
    if response_direction.status_code == 200 :
        print('Direction Request Success')

    jsonbuffer = response_direction.json()

    databuff1 = jsonbuffer['result']['path'][0]
    resultdata = '소요시간 : ' + str(databuff1['info']['totalTime']) + '분\n'

    for i in databuff1['subPath']:
        if i['trafficType'] == 1:
            resultdata += i['startName'] + ' ' + i['endName'] + ' ' + i['lane'][0]['name'] + "\n"
        if i['trafficType'] == 2:
            resultdata += i['startName'] + ' ' + i['endName'] + ' ' + i['lane'][0]['busNo'] + '번 버스\n'

    print(resultdata)


def req_departureset(place):
    global Departure_longitude
    global Departure_latitude

    URL_departureset = 'https://api.odsay.com/v1/api/searchStation'
    params_departureset = {'apiKey': '',
                          'lang': '0',
                          'output': 'json',
                          'stationName': place,  # 검색할 정류장 최소 2글자
                          'stationClass': '1:2'  # 버스, 지하철 정류장
                          }
    response_departureset = requests.get(URL_departureset, params=params_departureset)

    if response_departureset.status_code == 200:
        print('Departure_location Request Success')

    # print(response_transitstop.json())

    jsonbuffer = response_departureset.json()

    Departure_longitude = jsonbuffer['result']['station'][0]['x']

    Departure_latitude = jsonbuffer['result']['station'][0]['y']

def req_transitstop(place):
    global arrival_longitude
    global arrival_latitude

    URL_transitstop = 'https://api.odsay.com/v1/api/searchStation'
    params_transitstop = {'apiKey': 'EtTFZAyS+gZ+vjskaSisH3uAvML7lt9xnvEc8OoYNHU',
              'lang': '0',
              'output': 'json',
              'stationName': place,  # 검색할 정류장 최소 2글자
              'stationClass': '1:2'  # 버스, 지하철 정류장
    }
    response_transitstop = requests.get(URL_transitstop, params=params_transitstop)

    if response_transitstop.status_code == 200 :
        print('Arrival_location Request Success')

    # print(response_transitstop.json())

    jsonbuffer = response_transitstop.json()

    arrival_longitude = jsonbuffer['result']['station'][0]['x']

    arrival_latitude = jsonbuffer['result']['station'][0]['y']


def result(arrival, departure):
    req_departureset(str(arrival))
    req_transitstop(str(departure))
    req_direction()

# ---test code---
# result('가천대역', '인천터미널')

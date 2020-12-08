import json
import urllib.request
import requests
import ssl

result = ''

def car_info_print(): # 필요값 출력 함수
    global result

    sign = None                                             # 교통상황을 저장할 변수
    sign_text = ['정보없음', '원활', '서행', '지체', '정체']

    wholeDict = None                                        # 전체 딕셔너리값

    with open("tmap/Agent_Transit_Directions.json","r") as transitJson :
        wholeDict = dict(json.load(transitJson))            # json을 로드

    path = wholeDict["features"]
    tollgateFare = path[0]["properties"]["totalFare"]    # 톨게이트 요금 출력
    duration_sec = path[0]["properties"]["totalTime"]    # 총 걸리는시간 출력

    result += ('총시간: ' + str(float(duration_sec)//60) + '분 '
           + str(float(duration_sec)%60) + '초')
    result += ('요금 : ' + str(tollgateFare) + '원' + '\n')

    j = len(path)

    roadname_buff = ''
    sign_buff = 5

    for i in range(0, j):                                    # 도로이름, 교통정보 출력을 위한 for문
        DriveList = path[i]["properties"]
        roadname = DriveList['name']                        # 도로이름 변수
        trafficList = path[i]["geometry"]

        if 'traffic' in trafficList and trafficList['traffic'] != []:  # traffic 딕셔너리 구분문
            tList = trafficList['traffic']                  # traffic 딕셔너리가 있는경우만 값을 가져옴
            if tList[0][2] == 0:
                sign = 0  # '정보없음'
            elif tList[0][2] == 1:
                sign = 1  # '원활'
            elif tList[0][2] == 2:
                sign = 2  # '서행'
            elif tList[0][2] == 3:
                sign = 3  # '지체'
            elif tList[0][2] == 4:
                sign = 4  # '정체'

            if roadname == roadname_buff:
                if sign_buff <= sign:
                    sign_buff = sign
            else:
                if sign_buff != 5:
                    result += roadname_buff
                    result += (': ' + sign_text[sign_buff] + '\n')

                roadname_buff = roadname
                sign_buff = sign

        if i == (j-1):
            result += roadname_buff
            result += (': ' + sign_text[sign_buff] + '\n')

            # print(roadname)
            # print(sign)

def car_info_load(start, depart):
    start_location_c = start.split(' ')[0]  # 출발지 설정코드
    depart_location_c = depart.split(' ')[0]
    start_lo_c = urllib.parse.quote(start_location_c)  # 한글을 url에서 입력하기위한 utf-8변환
    depart_lo_c = urllib.parse.quote(depart_location_c)

    start_location_g = start.split(' ')[1]
    depart_location_g = depart.split(' ')[1]
    start_lo_g = urllib.parse.quote(start_location_g)
    depart_lo_g = urllib.parse.quote(depart_location_g)

    start_location_d = start.split(' ')[2]
    depart_location_d = depart.split(' ')[2]
    start_lo_d = urllib.parse.quote(start_location_d)
    depart_lo_d = urllib.parse.quote(depart_location_d)

    start_location_da = start.split(' ')[3]
    depart_location_da = depart.split(' ')[3]
    start_lo_da = urllib.parse.quote(start_location_da)
    depart_lo_da = urllib.parse.quote(depart_location_da)

    URL_a = 'https://apis.openapi.sk.com/tmap/geo/geocoding?version=1&city_do=' + str(start_lo_c) \
            + '&gu_gun=' + str(start_lo_g) + '&dong=' + str(start_lo_d) + '&detailAddress=' + str(start_lo_da) \
            + '&coordType=WGS84GEO&appKey='
    # 위도, 경도받아오는 url 1

    URL_b = 'https://apis.openapi.sk.com/tmap/geo/geocoding?version=1&city_do=' + str(depart_lo_c) \
            + '&gu_gun=' + str(depart_lo_g) + '&dong=' + str(depart_lo_d) + '&detailAddress=' + str(depart_lo_da) \
            + '&coordType=WGS84GEO&appKey='
    # 위도, 경도받아오는 url 2

    response_a = requests.get(URL_a)  # 위도, 경도를 json에서 가져오는 코드
    data_a = response_a.json()
    lat_a = data_a['coordinateInfo']['lat']
    lon_a = data_a['coordinateInfo']['lon']

    response_b = requests.get(URL_b)
    data_b = response_b.json()
    lat_b = data_b['coordinateInfo']['lat']
    lon_b = data_b['coordinateInfo']['lon']

    version = "1"  # 자동차 경로 파라미터 값 대입
    tollgateFareOption = "16"
    endX = str(lon_b)
    endY = str(lat_b)
    startX = str(lon_a)
    startY = str(lat_a)
    detailPosFlag = '0'
    trafficInfo = 'Y'
    key = ""

    # 경로 url
    url = "https://apis.openapi.sk.com/tmap/routes?version=" + version \
          + "&tollgateFareOption=" + tollgateFareOption \
          + "&endX=" + endX \
          + "&endY=" + endY \
          + "&startX=" + startX \
          + "&startY=" + startY \
          + "&detailPosFlag=" + detailPosFlag \
          + "&trafficInfo=" + trafficInfo \
          + "&appkey=" + key

    request = urllib.request.Request(url)  # url 요청
    context = ssl._create_unverified_context()  # 의존성 추가코드
    response = urllib.request.urlopen(request, context=context)
    responseText = response.read().decode('utf-8')  # url open
    responseJson = json.loads(responseText)

    with open("tmap/Agent_Transit_Directions.json", "w") as rltStream:
        json.dump(responseJson, rltStream)

def car_result(start, depart):
    car_info_load(start, depart)   # '수원시 영통구 영통동 영통역', '성남시 수정구 복정동 가천대학교'
    car_info_print()
    print(result)


#---test code___
# car_result('수원시 영통구 영통동 영통역', '성남시 수정구 복정동 가천대학교')

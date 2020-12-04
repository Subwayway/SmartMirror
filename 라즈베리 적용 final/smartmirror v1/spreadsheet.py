import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]

json_file_name = 'spread/spreadsheet-267309-2a78d4b64574.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1gR5iVoZiSYu9Uh4gQYA5xiDt0QNobOo2nM8kTSHp6l8/edit#gid=0'
# 스프레스시트 문서 가져오기 

global doc
doc = gc.open_by_url(spreadsheet_url)
# 시트 선택하기

saved_json = 0
saved_newid_json = 0

# 시트 범위내용 출력
def read_rangedata():
    global doc
    worksheet = doc.worksheet('시트2')
    range_list = worksheet.range('A2:D2')
    for cell in range_list:
        print(cell.value)

# 시트 셀내용 출력
def read_celldata(sheet, cell):
    global doc
    worksheet = doc.worksheet(sheet)
    cell_data = worksheet.acell(cell).value
    return cell_data

# 시트 전체 내용 읽기
def read_alldata(sheet):
    global doc
    worksheet = doc.worksheet(sheet)
    cell_data = worksheet.get_all_values()
    return cell_data

# 시트 데이터 입력
def ins_data(sheet, cell, data):
    global doc
    worksheet = doc.worksheet(sheet) # seet = '시트1'
    worksheet.update_acell(cell, data)

# 시트 데이터행 입력
def ins_datarow(sheet, data1, data2, data3, cell_row):
    global doc
    worksheet = doc.worksheet(sheet)
    worksheet.insert_row([data1, '', data2, data3], cell_row)


# 출퇴근 기록 저장
def ins_dataform(id, time, status):
    cell_check = int(read_celldata('시트1', 'J2')) + 1

    ins_datarow('시트1', id, time, status, cell_check)


# 시트 전체 내용 json 파일로 저장(시트2)
def save_dataall():
    global saved_json
    global saved_newid_json

    # id 정보 저장 json
    cell_buff = 1
    sheet_buff = read_alldata('시트2')
    # print(sheet_buff)
    spread_idinfo_data = dict()
    while True:
        try:
            spread_idinfo_data[sheet_buff[cell_buff][0]] = {'name': sheet_buff[cell_buff][0],
                                                            'department': sheet_buff[cell_buff][1],
                                                            'location_transport': sheet_buff[cell_buff][2],
                                                            'location_car': sheet_buff[cell_buff][3],
                                                            'favorite': sheet_buff[cell_buff][4],
                                                            'user_option': sheet_buff[cell_buff][5]
                                                            # 1=transport, 2=car
                                                            }
            cell_buff = cell_buff + 1
        except IndexError:
            break

    # 신규가입 id 저장 json
    cell_buff = 1
    sheet_buff2 = read_alldata('시트3')
    # print(sheet_buff2)
    spread_idinfo_data2 = dict()
    while True:
        try:
            spread_idinfo_data2[sheet_buff2[cell_buff][0]] = {'name': sheet_buff2[cell_buff][1]}
            cell_buff = cell_buff + 1
        except IndexError:
            break

    # json파일 저장
    with open('spread\sheet2_saved_data.json', 'w', encoding='utf-8') as make_file:
        json.dump(spread_idinfo_data, make_file, ensure_ascii=False, indent="\t")

    with open('spread\sheet2_saved_data.json', "r", encoding='utf-8') as file_json:
        saved_json = json.load(file_json)

    with open('spread\sheet3_saved_newid.json', 'w', encoding='utf-8') as make_file:
        json.dump(spread_idinfo_data2, make_file, ensure_ascii=False, indent="\t")

    with open('spread\sheet3_saved_newid.json', "r", encoding='utf-8') as file_json:
        saved_newid_json = json.load(file_json)

def ins_newid(slot_id):
    i = 2

    while read_celldata('시트3', 'A' + str(i)) != '':
        i += 1

    ins_data('시트3', 'A' + str(i), 'NewUser_' + slot_id)

    return (i-2)

def del_newid():
    i = 2
    
    while read_celldata('시트3', 'A' + str(i)) != '':
        if read_celldata('시트3', 'B' + str(i)) != '':
            ins_data('시트3', 'A' + str(i), '')
            ins_data('시트3', 'B' + str(i), '')
        i += 1
    
# ---test code---
# ins_data('시트2', 'A10', 'test')
# ins_dataform('최현준', '2020-02-17 09:00', '출근')

# ins_dataform('aa', 'cc', 'dd')
# print(ins_newid())



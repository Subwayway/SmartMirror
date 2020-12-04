import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]

json_file_name = 'spreadsheet-267309-2a78d4b64574.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1gR5iVoZiSYu9Uh4gQYA5xiDt0QNobOo2nM8kTSHp6l8/edit#gid=0'
# 스프레스시트 문서 가져오기 

global doc
doc = gc.open_by_url(spreadsheet_url)
# 시트 선택하기


# 시트 범위내용 출력
def print_rangedata():
    global doc
    worksheet = doc.worksheet('시트1')
    range_list = worksheet.range('A1:E2')
    for cell in range_list:
        print(cell.value)


# 시트 셀내용 출력
def read_celldata(sheet, cell):
    global doc
    worksheet = doc.worksheet(sheet)
    cell_data = worksheet.acell(cell).value
    return cell_data


# 시트 데이터 입력
def ins_data(sheet, cell, data):
    global doc
    worksheet = doc.worksheet(sheet) # seet = '시트1'
    worksheet.update_acell(cell, data)


# 출퇴근 기록 저장
def ins_dataform(id, time, status):
    cell_check = 1

    # 비어있는 셀 확인
    while read_celldata('시트1', 'A' + str(cell_check)) != '' :
        cell_check = cell_check+1

    ins_data('시트1', 'A' + str(cell_check), id)  # 아이디
    ins_data('시트1', 'C' + str(cell_check), time)    # 출퇴근 시간
    ins_data('시트1', 'D' + str(cell_check), status)  # 출퇴근 상태 업데이트

# 해당 id의 목적지, 관심사등 등록된 정보 읽기
def read_dataform(id):
    cell_check = 1

    # id에 일치하는 셀 확인
    while read_celldata('시트2', 'A' + str(cell_check)) != id :
        cell_check = cell_check+1

    # 목적지, 뉴스관심사 반환
    return  read_celldata('시트2', 'C' + str(cell_check)), read_celldata('시트2', 'D' + str(cell_check))


# ---test code---
# ins_data('시트2', 'A3', 'test')
# ins_dataform('최현준', '2020-02-17 09:00', '출근')
# aa, bb = read_dataform('최현준')
# print(aa)
# print(bb)

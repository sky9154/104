from dotenv import load_dotenv
from datetime import datetime
from requests import request
from json import dumps
from os import getenv
from notification import line
from get import access_token


load_dotenv()

CLIENT_ID = getenv('CLIENT_ID')
CLIENT_SECRET = getenv('CLIENT_SECRET')

def upload (card_data: list, end_day: str):
  '''
  上傳打卡資料
  '''

  url = 'https://apis.104api.com.tw/prohrm/1.0/hrmapi/external/transferCard'

  payload = dumps(card_data)

  headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {access_token(CLIENT_ID, CLIENT_SECRET)}'
  }

  response = request('POST', url, headers=headers, data=payload)

  date = datetime.strptime(end_day, '%Y%m%d %H:%M:%S.000')
  date = datetime.strftime(date, '%Y%m%d_%H%M%S')

  notification = ''

  if response.status_code == 200:
    with open(f'log/user/{date}.log', 'w+', newline='', encoding='utf-8') as txt:
      for data in card_data:
        message = f"員工編號: {data['empNo']}\n打卡時間: {datetime.fromtimestamp (data['cardTime'] / 1000)}\n"

        print(message, file=txt)
    
    with open(f'log/system/{date}.log', 'w+', newline='') as txt:
      response_dict = response.json()
      response_json = dumps(response_dict, indent=4)

      print(response_json, file=txt)

    notification = f'時間: {date}\n狀態: 上傳完畢'
  elif response.status_code == 401:
    notification = f'時間: {date}\n狀態: 用戶端識別碼或密鑰錯誤'
  elif response.status_code == 400:
    with open(f'log/user/{date}.log', 'w+', newline='', encoding='utf-8') as txt:
      print('未取得打卡資料', file=txt)
  
    notification = f'時間: {date}\n狀態: 未取得打卡資料'

  line(f'\n{notification}')

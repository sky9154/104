from dotenv import load_dotenv
from datetime import datetime
from time import strftime
from toast import toast
from requests import request
from os import getenv
from json import dumps
import get


load_dotenv()

CLIENT_ID = getenv('CLIENT_ID')
CLIENT_SECRET = getenv('CLIENT_SECRET')
AUTO = getenv('AUTO')
BEGIN_DATE = getenv('BEGIN_DATE')
END_DATE = getenv('END_DATE')

card_data = None

if AUTO in ['TRUE', 'True', 'true', 't']:
  begin_day, end_day = get.begin_end_day()

  card_data = get.card_data(begin_day, end_day)
elif AUTO in ['FALSE', 'False', 'false', 'f']:
  if BEGIN_DATE == '' or END_DATE == '':
    toast('需填入開始與結束日期')
  else:
    card_data = get.card_data(BEGIN_DATE, END_DATE)
 
if card_data:
  url = 'https://apis.104api.com.tw/prohrm/1.0/hrmapi/external/transferCard'

  payload = dumps(card_data)

  headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {get.access_token(CLIENT_ID, CLIENT_SECRET)}'
  }

  response = request('POST', url, headers=headers, data=payload)

  if response.status_code == 200:
    date = strftime('%Y%m%d_%H%M%S')

    with open(f'log/user/{date}.log', 'w+', newline='', encoding='utf-8') as txt:
      for data in card_data:
        message = f"員工編號: {data['empNo']}\n打卡時間: {datetime.fromtimestamp (data['cardTime'] / 1000)}\n"

        print(message, file=txt)
    
    with open(f'log/system/{date}.log', 'w+', newline='') as txt:
      response_dict = response.json()
      response_json = dumps(response_dict, indent=4)

      print(response_json, file=txt)

    toast('上傳完畢')
else:
  toast('未取得打卡資料')

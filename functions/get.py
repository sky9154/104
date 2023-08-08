from base64 import b64encode
from dotenv import load_dotenv
from datetime import datetime, timedelta
from requests import request
import os
import pymssql


load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
ON_SQL_PATH = os.getenv('ON_SQL_PATH')
OFF_SQL_PATH = os.getenv('OFF_SQL_PATH')

def access_token (id: str, secret: str) -> str:
  '''
  取得 Access Token
  '''

  url = 'https://apis.104api.com.tw/oauth2/token'

  credentials = b64encode(f'{id}:{secret}'.encode('utf-8')).decode('utf-8')

  headers = {
    'Authorization': f'Basic {credentials}',
    'Content-Type': 'application/x-www-form-urlencoded'
  }

  payload = {
    'grant_type': 'client_credentials',
    'scope': 'prohrm'
  }

  response = request('POST', url, headers=headers, data=payload)

  if response.ok:
    result = response.json()

    return result['access_token']
  else:
    return ''


def card_data (now_time: str, startDate: str, endDate: str) -> list:
  '''
  取得打卡資料
  '''
  
  try:
    db = pymssql.connect(
      server=DB_HOST,
      database=DB_NAME
    )

    cursor = db.cursor(as_dict=True)

    with open(ON_SQL_PATH if (now_time) == '22:00:00' else OFF_SQL_PATH, encoding='utf8') as sql:
      sql = ''.join(sql.readlines())

    sql = sql.replace('_BEGINDATE_', startDate)
    sql = sql.replace('_ENDDATE_', endDate)

    cursor.execute(sql)
    print(startDate, endDate)
    return [{
      'empNo': str(result['員工編號']).zfill(6),
      'cardTime': int((result['打卡時間'] - timedelta(hours=8) - datetime(1970, 1, 1)).total_seconds() * 1000)
    } for result in cursor]
  except Exception as e:
    pass


def begin_end_day (date: str, time: str) -> tuple[str, str]:
  '''
  取得開始日期及結束日期
  '''

  time_list = ['00:00:00', '09:00:00', '09:10:00', '09:30:00', '10:00:00', '22:00:00']

  return f'{date} {time_list[time_list.index(time) - 1]}.001', f'{date} {time}.000'


def upload_list (now_date, now_time):
  '''
  取得上傳清單
  '''

  folder = os.listdir('log/user')
  folder.sort(reverse=True)

  file_name = os.path.splitext(folder[0])[0]
  last_date = file_name.split('_')[0]

  date1 = datetime.strptime(last_date, '%Y%m%d')
  date2 = datetime.strptime(now_date, '%Y%m%d')

  if date1 != date2:
    if date1 > date2:
      date1, date2 = date2, date1

    date_list = []
    current_date = date1
    while current_date <= date2:
      date_list.append(current_date)
      current_date += timedelta(days=1)
  else:
    date_list = [date2]

  datetime_list = []
  time_list = ['09:00:00', '09:10:00', '09:30:00', '10:00:00', '22:00:00']

  for date in date_list:
    date = date.strftime('%Y%m%d')
    for time in time_list:
      datetime_list.append(f'{date} {time}')

      if now_date == date and now_time == time:
        break

  remove_datetime_list = [datetime.strptime(os.path.splitext(file)[0], '%Y%m%d_%H%M%S') for file in folder]
  remove_datetime_list = [remove_datetime.strftime('%Y%m%d %H:%M:00') for remove_datetime in remove_datetime_list]
  datetime_list = [date for date in datetime_list if date not in remove_datetime_list]
  
  return datetime_list

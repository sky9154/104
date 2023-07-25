from base64 import b64encode
from dotenv import load_dotenv
from datetime import datetime, timedelta
from requests import request
from time import localtime, strftime
from os import getenv
import pymssql


load_dotenv()

DB_HOST = getenv('DB_HOST')
DB_NAME = getenv('DB_NAME')
SQL_PATH = getenv('SQL_PATH')

db = pymssql.connect(
  server=DB_HOST,
  database=DB_NAME
)

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

def card_data (startDate: str, endDate: str) -> list:
  '''
  取得打卡資料
  '''

  cursor = db.cursor(as_dict=True)

  with open(SQL_PATH, encoding='utf8') as sql:
    sql = ''.join(sql.readlines())

  sql = sql.replace('_BEGINDATE_', startDate)
  sql = sql.replace('_ENDDATE_', endDate)

  cursor.execute(sql)

  return [{
    'empNo': str(result['員工編號']).zfill(6),
    'cardTime': int((result['打卡時間'] - timedelta(hours=8) - datetime(1970, 1, 1)).total_seconds() * 1000)
  } for result in cursor]

def begin_end_day (time: str) -> tuple[str, str]:
  '''
  取得開始日期及結束日期
  '''

  local_time = localtime()

  date = strftime('%Y%m%d', local_time)

  time_list = ['00:00:00', '09:00:00', '09:10:00', '09:30:00', '10:00:00', '22:00:00']

  return f'{date} {time_list[time_list.index(time) - 1]}.001', f'{date} {time}.000'

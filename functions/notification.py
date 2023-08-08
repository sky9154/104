from dotenv import load_dotenv
from os import getenv
from requests import request


load_dotenv()

LINE_TOKEN = getenv('LINE_TOKEN')

def line (message: str):
  '''
  發送 Line 通知
  '''

  url = 'https://notify-api.line.me/api/notify'

  if LINE_TOKEN != '':
    headers = {
      'Authorization': f'Bearer {LINE_TOKEN}',
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    payload = {
      'message': f'\n{message}'
    }

    request('POST', url, headers = headers, data = payload)

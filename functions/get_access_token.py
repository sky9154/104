from dotenv import load_dotenv
from base64 import b64encode
import requests
import os


load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


def get_access_token (id: str, secret: str) -> str:
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

  response = requests.request('POST', url, headers=headers, data=payload)

  if response.ok:
    result = response.json()
    
    return result['access_token']
  else:
    return ''
  
print(get_access_token(CLIENT_ID, CLIENT_SECRET))
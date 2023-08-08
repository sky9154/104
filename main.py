from dotenv import load_dotenv
from time import sleep
from datetime import datetime
from os import getenv
from functions.transfer_card import upload
import functions.get as get


load_dotenv()

CLIENT_ID = getenv('CLIENT_ID')
CLIENT_SECRET = getenv('CLIENT_SECRET')
AUTO = getenv('AUTO')
BEGIN_DATE = getenv('BEGIN_DATE')
END_DATE = getenv('END_DATE')

card_data = None


if AUTO in ['TRUE', 'True', 'true', 't']:
  while True:
    now_date = datetime.now().strftime('%Y%m%d')
    now_time =  datetime.now().strftime('%H:%M:%S')

    if now_time in ['09:00:00', '09:10:00', '09:30:00', '10:00:00', '22:00:00']:
      if __name__ == '__main__':
        for dt in get.upload_list(now_date, now_time):
          date = dt.split(' ')[0]
          time = dt.split(' ')[1]

          begin_day, end_day = get.begin_end_day(date, time)
          print(begin_day, end_day)

          card_data = get.card_data(now_time, begin_day, end_day)
          upload(card_data, end_day)

    sleep(1)
elif AUTO in ['FALSE', 'False', 'false', 'f']:
  if __name__ == '__main__':
    card_data = get.card_data(BEGIN_DATE, END_DATE)
    upload(card_data)

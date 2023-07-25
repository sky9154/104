from dotenv import load_dotenv
from time import localtime, sleep, strftime
from os import getenv
from transfer_card import upload
import get


load_dotenv()

CLIENT_ID = getenv('CLIENT_ID')
CLIENT_SECRET = getenv('CLIENT_SECRET')
AUTO = getenv('AUTO')
BEGIN_DATE = getenv('BEGIN_DATE')
END_DATE = getenv('END_DATE')

card_data = None


if AUTO in ['TRUE', 'True', 'true', 't']:
  while True:
    local_time = localtime()
    time = strftime('%H:%M:%S', local_time)

    if time in ['09:00:00', '09:10:00', '09:30:00', '10:00:00', '22:00:00']:
      if __name__ == '__main__':
        begin_day, end_day = get.begin_end_day(time)

        card_data = get.card_data(begin_day, end_day)

        upload(card_data)

    sleep(1)
elif AUTO in ['FALSE', 'False', 'false', 'f']:
  card_data = get.card_data(BEGIN_DATE, END_DATE)

  if __name__ == '__main__':
    upload(card_data)

from time import sleep
from sys import argv
from datetime import datetime

from database import Data
from constants import API_TOKEN
from requests import get

schedule_time = argv[1]
chat = argv[2]

while True:
    nowt = datetime.now().time()
    now = nowt.strftime('%H:%M')
    if now == schedule_time and Data(chat).days[datetime.weekday(datetime.now())]:
        get(f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={chat}&text={Data(chat).message}")
    sleep(60-nowt.second)

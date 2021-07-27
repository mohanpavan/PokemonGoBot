import requests
import json
import re
import time
from datetime import datetime, timedelta

pattern = re.compile('.*\((\d+%)\).*Level: ([3]\d).*')

channel_ids = {'trapinch': '416893323434000384',
               'beldum': '416797898718576640',
               'gible': '579186338432024576',
               'level35': '416797870986100738',
               'iv100': '302491007382061057',
               'iv95': '324096818549882883',
               'iv90': '416890211604103169'
               }

def check_iv(iv):
    iv_num = int(iv.rstrip('%'))
    return True if iv_num > 70 else False


def check_level(level):
    level_num = int(level.strip())
    return True if level_num > 30 else False

def pokemon_filtered(iv, level):
    return True if check_iv(iv) and check_level(level) else False

def filter_on_time(current_time, msg_time):
    datetimeObj = datetime.strptime(msg_time[:-6], '%Y-%m-%dT%H:%M:%S.%f')
    datetimeObj += timedelta(hours=5, minutes=30) # change to IST
    print('spawn-time:', datetimeObj)
    diff = current_time - datetimeObj
    if ((diff.seconds % 3600) // 60) < 19: # return true if time-difference is less than 19mins
        return True
    else:
        False

def retrieve_messages(channel_id, current_time):
    headers = {
        'authorization': ''
    }

    r = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages?limit=50', headers=headers)
    data1 = json.loads(r.text)
    for value in data1:
        match_data = pattern.match(value['content'])
        if match_data:
            if pokemon_filtered(match_data.group(1), match_data.group(2)) and filter_on_time(current_time, value['timestamp']):
                print('\n\n', value['content'])

cur_time = datetime.now()
print('current-time: ' , cur_time)
retrieve_messages('416797870986100738', cur_time)
# for channel, channel_id in channel_ids.items():
#     retrieve_messages(channel_id, cur_time)

import requests
import json
import re
import time
import datetime;

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
    return True if iv_num > 80 else False


def check_level(level):
    level_num = int(level.strip())
    return True if level_num > 30 else False

def pokemon_filtered(iv, level):
    return True if check_iv(iv) and check_level(level) else False

def retrieve_messages(channel_id, current_time):
    headers = {
        'authorization': ''
    }

    r = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages?limit=50', headers=headers)
    data1 = json.loads(r.text)
    for value in data1:
        match_data = pattern.match(value['content'])
        if match_data:
            if pokemon_filtered(match_data.group(1), match_data.group(2)):
                print(value['timestamp'], '\n\n', value['content'])

for channel, channel_id in channel_ids.items():
    cur_time = datetime.datetime.now()
    print(cur_time)
    retrieve_messages(channel_id, cur_time)

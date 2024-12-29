import json

with open('Parsing-Media-From-JVID_clone.json', 'r') as fh:
    now = json.load(fh)
with open('Parsing-Media-From-JVID_clone_before.json', 'r') as fh:
    before = json.load(fh)
    
latest = dict(before)
if 'count_past_to_last_2_weeks_ago' not in latest.keys():
    latest['count_past_to_last_2_weeks_ago'] = 0
if 'uniques_past_to_last_2_weeks_ago' not in latest.keys():
    latest['uniques_past_to_last_2_weeks_ago'] = 0
if 'count_total' not in latest.keys():
    latest['count_total'] = 0
if 'uniques_total' not in latest.keys():
    latest['uniques_total'] = 0

timestamps = {latest['clones'][i]['timestamp']: i for i in range(len(latest['clones']))}
for i in range(len(now['clones'])):
    timestamp = now['clones'][i]['timestamp']
    if timestamp in timestamps:
        latest['clones'][timestamps[timestamp]] = now['clones'][i]
    else:
        latest['clones'].append(now['clones'][i])

if len(latest["clones"]) > 14:
    temp_list = latest["clones"][:-14]
    latest["clones"] = latest["clones"][-14:]
    for i in temp_list:
        latest['count_past_to_last_2_weeks_ago'] += i['count']
        latest['uniques_past_to_last_2_weeks_ago'] += i['uniques']

latest['count'] = sum(map(lambda x: int(x['count']), latest['clones']))
latest['uniques'] = sum(map(lambda x: int(x['uniques']), latest['clones']))
latest['count_total'] = latest['count_past_to_last_2_weeks_ago'] + latest['count']
latest['uniques_total'] = latest['uniques_past_to_last_2_weeks_ago'] + latest['uniques']

with open('Parsing-Media-From-JVID_clone.json', 'w', encoding='utf-8') as fh:
    json.dump(latest, fh, ensure_ascii=False, indent=4)
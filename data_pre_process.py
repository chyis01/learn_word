import csv
import datetime
import random
import json, yaml

with open('config.yml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

save_file_path = config['learning_dictionary']
origin_file_path = config['pre_process_origin_file_path']

def csv_to_dict(file_path):
    head = ['word', 'answer', 'options']
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        dict_list = [
            {head[i]: row[i] for i in range(len(headers))} for row in reader
        ]
    return dict_list

def get_today():
    return datetime.date.today().strftime('%Y-%m-%d')

def list_dict_to_json_file(list_dict, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(list_dict, file, ensure_ascii=False, indent=4)

today = get_today()

l=csv_to_dict(origin_file_path)

options_list = [
'adj. 充足的；适当的；胜任的',
'vt. 保证；担保；使确信；弄清楚',
"vt. 背诵；叙述；列举"
]

# today = (datetime.date.today() - datetime.timedelta(days=4)).strftime('%Y-%m-%d')

# 遍历列表中的每个字典并添加新字段
for item in l:
    # 要添加的字段
    new_fields = {
        "id": l.index(item),
        "options": list(options_list),
        "memory_level": 40 + random.randint(0, 20),
        "lastday_learn": today,
        "learned": 0,
        "today_correct": 0,
        "update_day": today,
    }
    item.update(new_fields)
    options_list.append(item['answer'])
    options_list = options_list[1:]

list_dict_to_json_file(l, save_file_path)
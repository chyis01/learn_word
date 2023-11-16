import datetime
import random
import json, yaml

with open('config.yml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

def save_learn_result(learn_word_list, word_list):
    for item in learn_word_list:
        for item1 in word_list:
            if item['word'] == item1['word']:
                item1.update(item) 
                break

def get_learn_word_list(dictionary_word_list, learn_word_num):
    '''从dictionary_word_list中选取learned字段为0的前learn_word_num个单词'''
    learn_word_list = []
    for item in dictionary_word_list:
        if item['learned'] == 0:
            learn_word_list.append(item)
        if len(learn_word_list) == learn_word_num:
            break
    return learn_word_list

def choice_learn_word(learn_word_list):
    '''遍历list,每调用一次函数,返回一个元素'''
    return learn_word_list.pop()

def get_review_word_list(dictionary_word_list, learn_word_num):
    '''从dictionary_word_list中选取learned字段为0的前learn_word_num个单词'''
    review_word_list = []
    for item in dictionary_word_list:
        if item['learned'] == 1:
            review_word_list.append(item)
        if len(review_word_list) == learn_word_num:
            break
    return review_word_list

def choice_review_word(review_word_list):
    '''遍历list,每调用一次函数,返回一个元素'''
    return review_word_list.pop()



def date_diff(date1, date2):
    try:
        date1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
        date2 = datetime.datetime.strptime(date2, "%Y-%m-%d")
        return (date2 - date1).days
    except Exception:
        return 0

def day_mem_level_map(day_diff):
    if day_diff <3:
        return 3*day_diff
    elif day_diff <5:
        return 2*(day_diff-2) + 6
    elif day_diff <7:
        return 1*(day_diff-4) + 10
    else:
        return 12

def init_loadlist(dictionary_word_list):
    # print('导入时候执行')
    today = datetime.date.today().strftime('%Y-%m-%d')
    # 循环遍历，获得每个单词的lastday_learn，计算和今天的差值，更新memory_level
    for item in dictionary_word_list:
        day_diff = date_diff(item['update_day'],today)
        item['memory_level'] -= day_mem_level_map(day_diff)
        item['update_day'] = today
        if day_diff > 0:
            item['today_correct'] = 0
    return dictionary_word_list

file_path = config['learning_dictionary']
learn_word_num = config['learn_word_num']


with open(file_path, 'r', encoding='utf-8') as file:
    dictionary_word_list = json.load(file)
    dictionary_word_list = init_loadlist(dictionary_word_list)

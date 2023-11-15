import tkinter as tk
import random
import copy
import word_process
import json
import yaml
import datetime


current_word = ""
correct_translation = ""
showing_answer = False
question_count = 0
today = datetime.date.today().strftime('%Y-%m-%d')


config = word_process.config
file_path = config['learning_dictionary']
learn_word_num = config['learn_word_num']
memory_level_correct = config['memory_level_correct']
memory_level_wrong = config['memory_level_wrong']
dictionary_word_list = word_process.dictionary_word_list

# with open(file_path, 'r', encoding='utf-8') as file:
#     dictionary_word_list = json.load(file)


'''数据类函数'''
def save_word_to_file(list_dict, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(list_dict, file, ensure_ascii=False, indent=4)


'''展示类函数'''
def get_learn_word_list():
    global learn_word_list
    learn_word_list = word_process.get_learn_word_list(dictionary_word_list, learn_word_num)

def get_review_word_list():
    global review_word_list
    dictionary_word_list_review = sorted(dictionary_word_list, key=lambda x: x['memory_level'])
    review_word_list = word_process.get_review_word_list(dictionary_word_list_review, learn_word_num)

def provide_learn_word():
    word_item = word_process.choice_learn_word(learn_word_list)  
    options = copy.deepcopy(word_item['options'])
    options.append(word_item['answer'])
    return word_item['word'], word_item['answer'], options

def provide_review_word():
    word_item = word_process.choice_review_word(review_word_list)  
    options = copy.deepcopy(word_item['options'])
    options.append(word_item['answer'])
    return word_item['word'], word_item['answer'], options

def display_word():
    global current_word, correct_translation, showing_answer, question_count
    # 检查是否已经答够题
    if question_count >= learn_word_num:
        result_label.config(text="已完成%d道题，请点击结束按钮返回主页面。"% learn_word_num)
        return

    # 选择一个单词
    current_word, correct_translation, options = provide_learn_word()

    # 随机打乱选项
    random.shuffle(options)

    # 更新标签显示的单词
    word_label.config(text=current_word)

    # 更新选项按钮的文本
    for i in range(4):
        option_buttons[i].config(text=options[i])

    showing_answer = False

def show_answer():
    global showing_answer
    if not showing_answer:
        result_label.config(text=f"正确答案是：{correct_translation}")
        showing_answer = True

def next_word():
    global question_count
    question_count += 1
    if question_count >= learn_word_num:
        result_label.config(text="已完成%d道题，请点击结束按钮返回主页面。" % learn_word_num)
    else:
        display_word()
        result_label.config(text="")

def check_answer(selected_option):
    global dictionary_word_list
    if showing_answer or question_count >= learn_word_num:
        return
    # 检查用户的答案
    if selected_option == correct_translation:
        result_label.config(text="正确！")
        add_memory_level = memory_level_correct
        learned = 1
    else:
        result_label.config(text=f"错误，正确答案是：{correct_translation}")
        add_memory_level = memory_level_wrong
        learned = 0

    for item in dictionary_word_list:
        if item['word'] == current_word:
            item['learned'] = learned
            item['memory_level'] += add_memory_level
            item['lastday_learn'] = today
            item['update_day'] = today
            break
    

def display_word_review():
    global current_word, correct_translation, showing_answer, question_count
    if question_count >= learn_word_num:
        result_label_review.config(text="已完成%d道题，请点击结束按钮返回主页面。"% learn_word_num)
        return

    current_word, correct_translation, options = provide_review_word()
    random.shuffle(options)

    word_label_review.config(text=current_word)

    for i in range(4):
        option_buttons_review[i].config(text=options[i])

    showing_answer = False

def show_answer_review():
    global showing_answer
    if not showing_answer:
        result_label_review.config(text=f"正确答案是：{correct_translation}")
        showing_answer is True

def next_word_review():
    global question_count
    question_count += 1
    if question_count >= learn_word_num:
        result_label_review.config(text="已完成%d道题，请点击结束按钮返回主页面。" % learn_word_num)
    else:
        display_word_review()
        result_label_review.config(text="")

def check_answer_review(selected_option):
    global dictionary_word_list
    if showing_answer or question_count >= learn_word_num:
        return
    # 检查用户的答案
    if selected_option == correct_translation:
        result_label_review.config(text="正确！")
        add_memory_level = memory_level_correct
        today_correct = 1
    else:
        result_label_review.config(text=f"错误，正确答案是：{correct_translation}")
        add_memory_level = memory_level_wrong
        today_correct = 0

    for item in dictionary_word_list:
        if item['word'] == current_word:
            item['memory_level'] += add_memory_level
            item['today_correct'] = today_correct
            item['lastday_learn'] = today
            item['update_day'] = today
            break

def start_learn():
    get_learn_word_list()
    global question_count
    question_count = 0
    display_word()
    main_window.withdraw()
    learn_window.deiconify()

def end_learn():
    global question_count
    question_count = 0
    result_label.config(text="已结束一轮学习。")
    learn_window.withdraw()
    main_window.deiconify()

def start_review():
    get_review_word_list()
    global question_count
    question_count = 0
    display_word_review()
    main_window.withdraw()
    review_window.deiconify()

def end_review():
    global question_count
    question_count = 0
    result_label_review.config(text="已结束一轮复习。")
    review_window.withdraw()
    main_window.deiconify()

def count_learned():
    count = 0
    for item in dictionary_word_list:
        if item['learned'] == 1:
            count += 1
    return count

def count_reviewed():
    count = 0
    for item in dictionary_word_list:
        if item['today_correct'] == 1:
            count += 1
    return count

def count_word():
    learned_num = count_learned()
    reviewed_num = count_reviewed()
    all_num = len(dictionary_word_list)
    word_count_label.config(text=f"已学习{learned_num}个单词，\n今日复习{reviewed_num}个单词，\n共{all_num}个单词。")

main_window = tk.Tk()
main_window.title("主页面")
main_window.geometry("100x100")

start_button = tk.Button(main_window, text="开始学习", font=("Arial", 18), command=start_learn)
start_button.pack()

review_button = tk.Button(main_window, text="复习", font=("Arial", 18), command=start_review)
review_button.pack()

learn_window = tk.Toplevel(main_window)
learn_window.title("学习")
learn_window.geometry("600x600")

word_label = tk.Label(learn_window, text="", font=("Arial", 24))
word_label.pack()

option_buttons = []
for i in range(4):
    button = tk.Button(learn_window, text="", font=("Arial", 18),
                       command=lambda i=i: check_answer(option_buttons[i].cget("text")))
    option_buttons.append(button)
    button.pack()

result_label = tk.Label(learn_window, text="", font=("Arial", 18))
result_label.pack()

show_answer_button = tk.Button(learn_window, text="显示答案", font=("Arial", 18), command=show_answer)
show_answer_button.pack()
next_word_button = tk.Button(learn_window, text="下一个", font=("Arial", 18), command=next_word)
next_word_button.pack()

end_button = tk.Button(learn_window, text="结束学习", font=("Arial", 18), command=end_learn)
end_button.pack()

review_window = tk.Toplevel(main_window)
review_window.title("复习")
review_window.geometry("600x600")

word_count_label = tk.Label(main_window, text="")
word_count_label.pack()

update_word_count_button = tk.Button(main_window, text="学习进度", command=count_word)
update_word_count_button.pack()

word_label_review = tk.Label(review_window, text="", font=("Arial", 24))
word_label_review.pack()

option_buttons_review = []
for i in range(4):
    button = tk.Button(review_window, text="", font=("Arial", 18),
                       command=lambda i=i: check_answer_review(option_buttons_review[i].cget("text")))
    option_buttons_review.append(button)
    button.pack()

result_label_review = tk.Label(review_window, text="", font=("Arial", 18))
result_label_review.pack()

show_answer_button_review = tk.Button(review_window, text="显示答案", font=("Arial", 18), command=show_answer_review)
show_answer_button_review.pack()
next_word_button_review = tk.Button(review_window, text="下一个", font=("Arial", 18), command=next_word_review)
next_word_button_review.pack()

end_button_review = tk.Button(review_window, text="结束复习", font=("Arial", 18), command=end_review)
end_button_review.pack()

main_window.mainloop()

save_word_to_file(dictionary_word_list, file_path)

import requests
import datetime
import urllib.request
import json
import re
import matplotlib.pyplot as plt
import html
from matplotlib import style
import numpy as np
from collections import defaultdict
def vk_api(method, **kwargs): #для api vk
    api_request = 'https://api.vk.com/method/'+method + '?'
    api_request += '&'.join(['{}={}'.format(key, kwargs[key]) for key in kwargs])
    return json.loads(requests.get(api_request).text)
def text_cleaning(text): #более-менее очищает текст постов и комментов, делит на слова
    text = re.sub(r'\W^\s|http.+?|vk.com.+?|docs.+?|<.?br>|,|\.|\)|\(|-|"|\?|!|:|;|-|\*|_|\/|\+|goo+?|www+?|.+?\.ru|com|org|de.+?|\[.+?\]|form.+?|[01-9].+?|•|\\u.+', '', text)
    text = re.sub('\n', ' ', text)
    arr_post = text.split(' ')
    return (len(arr_post)) #возврашает длину поста или коммента
def bdate(user_info): #требует переменную при обращении api vk; fields = bdate
    bdata = [user['bdate'] for user in user_info['response'] if 'bdate' in user if len(user['bdate']) > 5] #если год указан, то дата состоит более чем из 5 символов
    if bdata != '':
        for el in bdata:
            el = (el.split('.'))
            age_day = str((datetime.date.today()) - (datetime.date(int(el[2]), int(el[1]), int(el[0]))))
            age_day = int(age_day[:age_day.find('d') - 1]) #высчитываем точный возраст
            years_old = str(int(age_day / 365.25))
            return str(years_old) #возвращает возраст строкой
def cities(user_info): #на входе требует переменную, получающуюся при обращении к api vk; fields=city
    citydata = [user['city']['title'] for user in user_info['response'] if 'city' in user]
    for el in citydata: #возвращает город проживания
        return el
def average(array_els): #берем массив всех длин и считаем среднее арифметическое
    for el in array_els:
        el = int(el)
    cou = sum(array_els)
    aver = int(cou)/int(len(array_els))
    aver = round(aver) #округление для красоты
    return aver
style.use('ggplot')
def simple_graph(data_arr): #зависимость длин постов к длинам комментариев
    sort_data_arr = sorted(data_arr, key=lambda x: x[0]) #чтобы координаты в массиве с кортежами соединялись в график последовательно
    keys = [el[0] for el in sort_data_arr]
    values = [el[1] for el in sort_data_arr]
    plt.plot(keys, values)
    plt.xlabel(r'Длина поста')
    plt.ylabel(r'Средняя длина комментов')
    plt.title(r'Студенческий городок Дубки')
    plt.grid(True)
    plt.show()
    plt.close()
def bar_chart(data_dict): #написано, но уж очень долго работает; внизу то же самое без функции; на входе берет словарь "возраст/город : средние длины"
    for values in data_dict:
        av_data_dict = average(data_dict[values])
        data_dict[values] = av_data_dict
    sort_data = sorted(data_dict)
    bar_keys = np.arange(len(data_dict))
    bar_values = [int(data_dict[key]) for key in data_dict]
    bar_sticks = [str(key) for key in data_dict]
    plt.bar(bar_keys, bar_values, align='center')
    plt.ylabel('Длина постов/комментариев')
    plt.title('Студенческий городок Дубки')
    plt.xticks(bar_keys, bar_sticks)
    plt.show()
    plt.close()

def exam_none_or_not(string, dict_length, com_length):
    dict_length.setdefault(string, []).append(com_length)

group_info = vk_api('groups.getById', group_id='dubki', v='5.63') #айди группы
group_id = group_info['response'][0]['id']
posts = []
item_count = 200 #хочу скачать 200 штук в будущем
result = vk_api('wall.get', owner_id=-group_id, v='5.63', count=100)
posts += result["response"]["items"]
comms = []
arr = []
length = []
age_len = {}
city_len = {}
fw = open('postscomments.txt', 'a', encoding='UTF-8')
while len(posts) < item_count:
    result = vk_api('wall.get', owner_id=-group_id, v='5.63', count=100, offset=len(posts)) #качаю посты
    posts += result['response']["items"]

    for i in posts: #ковыряю текст из массива информации о скачанных постах
        post = html.escape(i['text'])
        fw.write('Пост: \n' + post + '\n') #попутно записываю всё
        len_post = text_cleaning(post) #возвращает длину поста
        user_info = vk_api('users.get', user_ids=i['from_id'], fields='bdate,city',
                           v='5.63', count=100) #информация о написавшем
        age = bdate(user_info) #его дата рождения и возраст
        live = cities(user_info)
        if age == None:
            continue
        else:
            exam_none_or_not(age, age_len,len_post) #словарь возраст - длина написанного; нет возраста - не считаю!
        if live == None:
            continue
        else:
            exam_none_or_not(live, city_len, len_post) #то же самое и с городом
        if i['comments']['count'] == 0: #с нулями в комментариях хочется разобраться сразу
            arr.append((len_post, 0))
            fw.write('Комментарии: 0 \n')
        else:
            comments = vk_api('wall.getComments', owner_id=-group_id, post_id=i['id'], v='5.63') #информация о комментариях
            comms += comments['response']['items']
            fw.write('Комментарии: ' + str(i['comments']['count']) + '\n')
            for c in comms: #информация о комментаторах по массиву комментов
                userfo = vk_api('users.get', user_ids=i['from_id'], fields='bdate,city',
                                   v='5.63', count=100)
                ages = bdate(userfo) #шаги, аналогичные тем же действиям для авторов постов
                live = cities(userfo)
                fw.write(c['text'] + '\n')
                length_coms = text_cleaning(c['text'])
                if ages == None:
                    continue
                else:
                    exam_none_or_not(ages, age_len, length_coms) #добавление длин комментов в общий словарь для возраста
                if live == None:
                    continue
                else:
                    exam_none_or_not(live, city_len, length_coms) #добавление длин комментов в общий словарь для города
                length.append(length_coms)
                aver_coms = average(length)
                arr.append((len_post, aver_coms)) #кортеж с координатами внутри массива для длин постов и средней длины комментов к ним
            comms = []
fw.close()



#рисую графики вне функции
for values in age_len:
    av_age_dict = average(age_len[values]) #среднее для значений в словаре по каждому возрасту
    age_len[values] = av_age_dict   #новые соответствия
bar_keys = np.arange(len(age_len))
bar_values = [(age_len[key]) for key in age_len]
bar_sticks = [str(key) for key in age_len] #что будет в подписи к колонкам гистограммы: количество лет
plt.bar(bar_keys, bar_values, align='center')
plt.ylabel('Длина постов/комментариев')
plt.title('Студенческий городок Дубки')
plt.xticks(bar_keys, bar_sticks)
plt.show()
plt.close()

simple_graph(arr)
#bar_chart(age_len)
#bar_chart(city_len)
for values in city_len:
    av_city_dict = average(city_len[values])
    city_len[values] = av_city_dict

bar_keys = np.arange(len(city_len))
bar_values = [int(city_len[key]) for key in city_len]
bar_sticks = [str(key) for key in city_len]
plt.bar(bar_keys, bar_values, align='center')
plt.ylabel('Длина постов/комментариев')
plt.title('Студенческий городок Дубки')
plt.xticks(bar_keys, bar_sticks)
plt.show()
plt.close()

#многие вещи упрощены, не такая активная группа, т.к. слабый компьютер очень долго грузит даже такое количество информации
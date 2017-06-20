# -*- coding: utf-8 -*-
import telebot
import re
import conf
import flask
import requests
import json
import datetime
import html
from rutermextract import TermExtractor
import random

term_extractor = TermExtractor()
WEBHOOK_URL_BASE = 'https://{}:{}'.format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = '/{}/'.format(conf.TOKEN)
VK = '{}'.format(conf.VK_TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)  # создаем экземпляр бота
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
app = flask.Flask(__name__)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)

#Ну куда ж без стикеров! На три установленных случая три массива со стикерами.
hello_sticks = ['CAADAgADnwIAApkvSwpAf6KT3FrhngI', 'CAADAgADnCMAAp7OCwABDB7UT2xaCJoC', 'CAADAgADFgADa-18CgcoBnIvq3DlAg',
                'CAADAgADQAMAAswJPAYQgJuqZKrD9QI', 'CAADAgADpgEAAzigCq4JkXkjpi0lAg', 'CAADBAAD3BwAAnbrwwABAisTQN37TKsC',
                'CAADAgAD_QIAAm4y2AABP7tCb382qgcC']
search_sticks = ['CAADAgADNQADdwaaArqisIt4ddTFAg', 'CAADAgADmQIAAqw3HQcdaBAYb5pDJQI', 'CAADAgADkQADI1wKCLnjuRIykR5rAg',
                 'CAADAgADiAADaJpdDPse3-G2WIWxAg', 'CAADAgADWQADaJpdDKzTfkbpQ8XpAg', 'CAADAgADbwADhC64BiDIKx5R2WOdAg',
                 'CAADAgADEwEAAjbsGwXj2-2f4C8x4AI', 'CAADAgAD8AIAApb6EgWulnIni8WH5wI',
                 'CAADAgADBgMAApb6EgU1SJdVQao9gwI']
help_sticks = ['CAADAgADeAQAAnlc4glIXtyFvEqChwI', 'CAADAgADhgEAAo5EEQLjBYmgPxbYOQI', 'CAADAgADGwADa-18CrkXEinIu91YAg',
               'CAADAgADEAADa-18Co7vmgzcTYOdAg', 'CAADAgADHAMAAs7Y6At2whpp37AWwwI', 'CAADAgADcgcAApkvSwo2mDheWobRcAI',
               'CAADAgADwSMAAp7OCwABId3cUYDusUgC']


def vk_api(method, **kwargs):
    api_request = 'https://api.vk.com/method/' + method + '?'
    api_request += '&'.join(['{}={}'.format(key, kwargs[key]) for key in kwargs])
    return json.loads(requests.get(api_request).text)

#Информация о возрасте пользователя: если указан, то ок. Но если не указан, тоже что-то скажет!
def bdate(user_info):  # требует переменную при обращении api vk; fields = bdate
    bdata = [user['bdate'] for user in user_info['response'] if 'bdate' in user if
             len(user['bdate']) > 5]  # если год указан, то дата состоит более чем из 5 символов
    if bdata != '':
        for el in bdata:
            el = (el.split('.'))
            age_day = str((datetime.date.today()) - (datetime.date(int(el[2]), int(el[1]), int(el[0]))))
            age_day = int(age_day[:age_day.find('d') - 1])  # высчитываем точный возраст
            years_old = str(int(age_day / 365.25))
            mes_age = '\nВозраст нужен, говоришь?.. Ну... ' + str(years_old)
            return (mes_age)  # возвращает возраст строкой
    for user in user_info['response']:
        if 'bdate' in user and len(user['bdate']) < 5:
            years_hidden = ('\nНе могу посчитать возраст, года нет! :(')
            return (str(years_hidden))
    if 'bdate' not in user:
        all_hidden = '\nАноним скрыл свою дату рождения...'
        return (all_hidden)

#Город и образование. Берет на входе два файла с разбором пользовательских данных (так удобнее было просто...)
def city_edu(info, res):
    for c in info['response']:
        if 'city' in c:
            city = c['city']['title']
            leben = '\nХм, а откуда твой юзер? Ах, да, ' + city
        else:
            leben = '\nУвы, никто не знает, где живет пользователь...'
    for j in res['response']:
        if 'university_name' in j:
            uni = j['university_name']
            edu = '\nОбразование: ' + uni
        else:
            edu = '\nУчился ли он где-то?.. Неизвестно..'
        return leben, edu

#Работа. Здесь только с токеном и никак иначе. Либо название работы, либо название соответствующей группы ВК
def search_job(result, token):
    for k in result['response']:
        if 'career' in k:
            if k['career'] != []:
                try:
                    work = k['career'][0]['company']
                    arbeit = '\nЧто по работе? ' + work
                except:
                    work = k['career'][0]['group_id']
                    work_group = requests.get('https://api.vk.com/method/groups.getById?group_ids=' + str(
                        work) + '&access_token=' + token).text
                    work_group = json.loads(work_group)
                    work_name = work_group['response'][0]['name']
                    arbeit = '\nЮзер работает тут: ' + work_name
            else:
                arbeit = '\nКажется, пользователь безработный!..'
    return arbeit

#КЛЮЧЕВЫЕ СЛОВА! Кое-что чищу (ссылки на др. пользователей, например)
#с помощью установленной библиотеки rutermextract - ключевые слова для русского
#установлен лимит на N слов для каждого поста
def posts_words(ids, VKtoken):
    limit = 10
    posts = []
    key_words = []
    result = vk_api('wall.get', owner_id=ids, access_token=VKtoken, filter='owner', v='5.63', count=20)  # качаю посты
    posts += result['response']["items"]

    for i in posts:  # ковыряю текст из массива информации о скачанных постах
        post = html.unescape(i['text'])
        post = re.sub('id.+?\||[1-90]|[a-zA-Z]', '', post)
        for term in term_extractor(post, limit):
            t = str(term.normalized)
            arr = t.split(' ')
            for el in arr:
                key_words.append(el)
        arr = []
        #множество по срезу. Зачем юзеру в телеграме слишком много ключевых слов, ну?
        if len(key_words) > 20:
            key_set = set(key_words[:20])
        else:
            key_set = set(key_words)
        if len(key_words) == 0:
            key_text = '\nПользователь ничего не пишет на стене! :('
        else:
            set_key_text = ', '.join(key_set)
            key_text = '\nВот о чем пользователь пишет в последнее время: ' + set_key_text
    key_words = []
    key_set = {}
    return key_text


@app.route('/')
def index():
    return ('Hello! Write @olgarudina for more details if you want.')

#Приветствую. Присылаю стикер.
@bot.message_handler(commands=['start'])
def send_first_hello(message):
    bot.send_message(message.chat.id, 'Приветик! Отправь мне ссылку на пользователя вк :) \nПосмотрим, что получится!')
    bot.send_sticker(message.chat.id, random.choice(hello_sticks))

#На случай, если нужна помощь. Тоже со стикером :)
@bot.message_handler(commands=['help'])
def hilfe(message):
    bot.send_message(message.chat.id,
                     'Оуу... Требуется помощь?\n\nЯ создан, чтобы выдавать тебе информацию о пользователе ВКонтакте.\n\nЧто я умею:\n-Считать друзей;\n-Находить город пользователя;\n-Работает он или учится? И где? Разберемся!\n-О чем пишет твой товарищ в последнее время? Выдам ключевые слова!\n\nЯ пока молод и горяч, поэтому и не работаю без ошибок.\nЕсли что - пиши @olgarudina. Это её рук дело. \nУдачки! :)')
    bot.send_sticker(message.chat.id, random.choice(help_sticks))

#Отвечает на ссылку от пользователя. И стикеры :)
@bot.message_handler(content_types=["text"])  # reacts to any text message
def id_vk(message):
    string = message.text.split(' ')
    for el in string:
        el = el.lower()
        take_ids = re.search('vk.com/(.+)', el) #регулярка для отбора ника
        if take_ids != None:
            ids = take_ids.group(1)
            user_info = vk_api('users.get', user_ids=ids, fields='city,bdate,education,career', v='5.63')
            first = user_info['response'][0]['first_name'] #Имя и фамилия в самом начале
            last = user_info['response'][0]['last_name']
            age = bdate(user_info) #Возраст
            idu = user_info['response'][0]['id'] #для дальнейших манипуляций извлечем айди
            result = requests.get('https://api.vk.com/method/users.get?user_id=' + str(
                idu) + '&access_token=' + VK + '&fields=education,career').text
            resul = json.loads(result) #сорри, я не знаю как штуку с токеном провернуть в функции с кварками. Поэтому так.
            count_friends = vk_api('friends.get', user_id=idu, v='5.63') #подсчет френдов
            friends_number = count_friends['response']['count']
            friends = '\nКоличество друзей: ' + str(friends_number) #Вся фраза с подсчетом друзей
            wohnen, ausbildung = city_edu(user_info, resul) #образование, город
            job = search_job(resul, VK) #все что касается места работы
            key = posts_words(idu, VK) #все по ключевым словам

            #далее все склеиваю в классный текст с абзацами и тд.
            bot.send_message(message.chat.id,
                             first + ' ' + last + age + friends + wohnen + ausbildung + job + '\n\n' + key)
            #И отправляю стикер :)
            bot.send_sticker(message.chat.id, random.choice(search_sticks))


@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


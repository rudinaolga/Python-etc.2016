from pymorphy2 import MorphAnalyzer
import re
import random
import flask
import telebot
import conf
# @broken_or_bot - логин бота в телеграме
morph = MorphAnalyzer()


WEBHOOK_URL_BASE = 'https://{}:{}'.format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = '/{}/'.format(conf.TOKEN)



bot = telebot.TeleBot(conf.TOKEN, threaded=False)  # создаем экземпляр бота
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
app = flask.Flask(__name__)
def parsed_text(path): #путь к файлу
    f = open(path, 'r', encoding = 'utf-8')
    words = f.read(100000)
    f.close()
    words = re.sub(r'[^\w\s]+|[\d]+', r'', words)
    arr_words = words.split()
    return arr_words

def parsed_words_dictionary(arr_words):
    dict_words = {}
    for i in arr_words:
        ana = morph.parse(i) # морфологическая разметка каждого слова в словаре 
        first = ana[0] # берем первый, самый частотный, разбор
        p = str(first.tag.POS)
        if p == 'NPRO':
            g = str(first.tag.gender) #чтобы вместо одного местоимения не выдавалось совсем другое (тк иные показатели)
            dict_words.setdefault(str(p + ',' + g), []).append(str(first.word))
        else:
            gram = str(first.tag)
            gram = gram.split(' ')
            post = gram[0].split(',') # постоянные признаки разделены запятой, отделены от изменяемых пробелом
            post_set = (set(post))
            dict_words.setdefault(str(post_set), []).append(str(first.word)) #постоянные признаки становятся объединяющим ключом для словаря с массивом подходящих слов
    return dict_words

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return('Hello! Write @olgarudina for more details if you want.')




file_name = '/home/wittmann/mysite/1grams-3.txt'
all_words = parsed_text(file_name) #массив слов из словаря НКРЯ
morph_dict = parsed_words_dictionary(all_words) #словарь с морфологич разметкой слов НКРЯ

@bot.message_handler(func=lambda m: True)
def send_len(message):
    mes = message.text.split()
    total = []
    for word in mes:
        mes_p = morph.parse(word) # разметка каждого слова пользователя
        first1 = mes_p[0]
        gram = str(first1.tag)
        gram = gram.split(' ')
        post = gram[0].split(',') # также получаем изменяемые и неизм признаки
        post_set = (set(post))
        str_post_set = str(post_set)
        if str_post_set in morph_dict:
            r = random.choice(morph_dict[str_post_set]) #рандомный выбор из массива слов, подходящих по признакам
            p_r = morph.parse(r)[0] # разбираем это слово
            try:
                changed = gram[1].split(',')
                changed_set = (set(changed))
                p_r = p_r.inflect(changed_set) #ставим в неизменяемую форму соотв слова пользователя
                total.append(p_r.word) 
            except:
                total.append(r) # если слово изменить нельзя
        else:
            total.append(word) #если для слова аналогии не удалось найти
    myString = ' '.join(total) #объединяем наш ответ в строку
    total = []
    reply_string = myString.capitalize() #делаем обращение с большой буквы
    bot.send_message(message.chat.id, reply_string)


@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)




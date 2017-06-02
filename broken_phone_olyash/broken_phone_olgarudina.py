from pymorphy2 import MorphAnalyzer
import re
import random
import flask
import telebot
import conf

morph = MorphAnalyzer()


WEBHOOK_URL_BASE = 'https://{}:{}'.format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = '/{}/'.format(conf.TOKEN)



bot = telebot.TeleBot(conf.TOKEN, threaded=False)  # создаем экземпляр бота
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
app = flask.Flask(__name__)
def parsed_text(path):
    f = open(path, 'r', encoding = 'utf-8')
    words = f.read(100000)
    f.close()
    words = re.sub(r'[^\w\s]+|[\d]+', r'', words)
    arr_words = words.split()
    return arr_words

def parsed_words_dictionary(arr_words):
    dict_words = {}
    for i in arr_words:
        ana = morph.parse(i)
        first = ana[0]
        p = str(first.tag.POS)
        if p == 'NPRO':
            g = str(first.tag.gender)
            dict_words.setdefault(str(p + ',' + g), []).append(str(first.word))
        else:
            gram = str(first.tag)
            gram = gram.split(' ')
            post = gram[0].split(',')
            post_set = (set(post))
            dict_words.setdefault(str(post_set), []).append(str(first.word))
    return dict_words

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return('Hello! Write @olgarudina for more details if you want.')




file_name = '/home/wittmann/mysite/1grams-3.txt'
all_words = parsed_text(file_name)
morph_dict = parsed_words_dictionary(all_words)

@bot.message_handler(func=lambda m: True)
def send_len(message):
    mes = message.text.split()
    total = []
    for word in mes:
        mes_p = morph.parse(word)
        first1 = mes_p[0]
        gram = str(first1.tag)
        gram = gram.split(' ')
        post = gram[0].split(',')
        post_set = (set(post))
        str_post_set = str(post_set)
        if str_post_set in morph_dict:
            r = random.choice(morph_dict[str_post_set])
            p_r = morph.parse(r)[0]
            try:
                changed = gram[1].split(',')
                changed_set = (set(changed))
                p_r = p_r.inflect(changed_set)
                total.append(p_r.word)
            except:
                total.append(r)
        else:
            total.append(word)
    myString = ' '.join(total)
    total = []
    reply_string = myString.capitalize()
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




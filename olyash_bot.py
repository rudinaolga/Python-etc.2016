import flask
import telebot  
import conf     
import re
#нужен сервер pythonanywhere - olgarudina.pythonanywhere.com
WEBHOOK_URL_BASE = 'https://{}:{}'.format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = '/{}/'.format(conf.TOKEN)

app = flask.Flask(__name__)
@app.route('/')
def index():
    return('Hello! Write @olgarudina for more details if you want.')
# создаем экземпляр бота
bot = telebot.TeleBot(conf.TOKEN, threaded=False)  # создаем экземпляр бота
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)

# функция, которая даст нужный падеж к числительному; x - number, y - list
def get_words(x, y):
    inumber = x % 100
    if inumber >= 11 and inumber <=19:
        y = y[2]
    else:
        iinumber = inumber % 10
        if iinumber == 1:
            y = y[0]
        elif iinumber == 2 or iinumber == 3 or iinumber == 4:
            y = y[1]
        else:
            y = y[2]
    return y

# приветствие и список команд
@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Привет, дорогой друг! \nЯ пока немного ленивый бот Оляш и всё, что я умею, - это считать длину сообщений, которые ты отправишь мне.\nМои команды: \n/howto - как именно я считаю слова? Лучше или хуже ворда? \n/help -  узнай, кому написать, если что-то пошло не так. \n/start - хорошо, давай начнём всё заново. \nУдачи! ")
# получить помощь и написать мне
@bot.message_handler(commands=['help'])
def send_help(message):
	bot.send_message(message.chat.id, "Оууу... Что-то случилось? \n Напиши @olgarudina, она попробует разобраться.")
#подробности о работе бота
@bot.message_handler(commands=['howto'])
def send_howto(message):
	bot.send_message(message.chat.id, "Знаешь, как я работаю? \nЯ считаю словом всё, где есть хотя бы одна буква и нет пробела. \nТы, конечно, можешь попробовать меня обмануть и вводить только знаки препинания... \nИли много пробелов... \nНо поверь, тебе не удастся меня провести. \nNB: Несмотря на значение эмоджи в современном мире, для меня это всё-таки эмоции, но не слова! :)")

#подсчёт слов в месседже, как он это делает - поясняет через /howto
@bot.message_handler(func=lambda m: True)  
def send_len(message):
    word = [' слово.', ' слова.', ' слов.']
    d = re.sub('[^\w\s]*_*', '', message.text)
    d = d.split()
    case = get_words(len(d), word)
    bot.send_message(message.chat.id, 'В вашем сообщении '+(str(len(d)))+case)

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

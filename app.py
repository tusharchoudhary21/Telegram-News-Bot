import logging
from dialogflow_v2.proto import context_pb2

from flask import Flask, request
from telegram import Bot, Update, ReplyKeyboardMarkup
from telegram.ext import Updater,Dispatcher,CommandHandler,Filters,MessageHandler,CallbackContext

from utils import *


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "2132784233:AAEp7cvwU7sPX3uoh5oQWlohOm4XeUV3-Ko"

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello!"


@app.route(f'/{TOKEN}', methods=['GET', 'POST'])
def webhook():

    update = Update.de_json(request.get_json(), bot)
   
    dp.process_update(update)
    return "ok"

def reply_text(update=Update,context=CallbackContext):
    intent,reply = get_reply(update.message.text, update.message.chat_id)
    if intent == "get_news":
        articles = fetch_news(reply)
        for article in articles:
            context.bot.send_message(chat_id=update.message.chat_id, text=article['link'])
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=reply)

def echo_sticker(update,context):
    context.bot.send_sticker(chat_id=update.message.chat_id , sticker=update.message.sticker.file_id)

def error(bot,update):
    logger.error("Update '%s' has caused error '%s' ", update, update.error)
def greeting(update: Update,context: CallbackContext):
    first_name = update.to_dict()['message']['chat']['first_name']



    update.message.reply_text("hi {}".format(first_name))
    

def _help(update: Update,context: CallbackContext):
    help_text="hey! this is a help text"
    context.bot.send_message(chat_id=update.message.chat_id, text= help_text)

def message_handler(update: Update,context: CallbackContext):
    text = update.to_dict()['message']['text']
    update.message.reply_text(text)
def news(update= Update ,context=CallbackContext):
     context.bot.send_message(chat_id=update.message.chat_id, text="Choose a category",
                     reply_markup=ReplyKeyboardMarkup(keyboard=topics_keyboard, one_time_keyboard=True))

bot = Bot(TOKEN)
try:
    bot.set_webhook("https://t-r-news.herokuapp.com/" + TOKEN)
except Exception as e:
    print(e)    

dp = Dispatcher(bot, None)
dp.add_handler(CommandHandler("start", greeting))
dp.add_handler(CommandHandler("help", _help))
dp.add_handler(CommandHandler("news", news))
dp.add_handler(MessageHandler(Filters.text, reply_text))
dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
dp.add_error_handler(error)

if __name__ == "__main__":

    app.run(port=8443)
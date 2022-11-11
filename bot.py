import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging
import os

TOKEN = '5600897776:AAFtRZ3K4ynX2-T-btPg7Jb9BywbUM2BoE8'
path = '/mnt/share'

bot = telegram.Bot(TOKEN)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def count_kickboard_data(date):
    try:
        dir_list = os.listdir(f'{path}/{date[:4]}-{date[4:6]}-{date[6:]}')
        count = len(dir_list)
    except:
        count = 0

    return count

def show_kickboard_data(date, id):
    global bot
    try:
        dir_list = os.listdir(f'{path}/{date[:4]}-{date[4:6]}-{date[6:]}')
        dir_list.sort()
        dir_list.reverse()
    except:
        return False
    photo_list = []
    if len(dir_list) > 10:
        for file in dir_list[:10]:
            photo_list.append(telegram.InputMediaPhoto(open(f'{path}/{date[:4]}-{date[4:6]}-{date[6:]}/{file}', 'rb')))
    else:
        for file in dir_list:
            photo_list.append(telegram.InputMediaPhoto(open(f'{path}/{date[:4]}-{date[4:6]}-{date[6:]}/{file}', 'rb')))
    bot.sendMediaGroup(chat_id=id, media=photo_list)

    return True





def echo(update: Update, context: CallbackContext) -> None:
    dict = update.to_dict()
    # import pdb; pdb.set_trace()
    id = dict['message']['chat']['id']
    message = update.message.text
    try:
        date, message = message.split()
        print(message)
    except:
        message = 'false'
    if message == 'count':
        count = count_kickboard_data(date)
        reply = str(count)
        # update.message.reply_photo(photo=open('/mnt/share/2H2NMM~K.JPG', 'rb'))
    elif message == 'show':
        if show_kickboard_data(date, id):
            reply = 'here'
        else:
            reply = 'None'
    else:
        reply = 'please send another message'
    update.message.reply_text(reply)


updater = Updater(TOKEN)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text, echo))
updater.start_polling()
updater.idle()
import logging
import requests
import re
import telegram
from telegram import Update, Bot, ParseMode
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.ext import MessageHandler, Filters


from special_report.app.proccess import invokeGetReport

users = [] #(phone, chat_id)
#baseList = ["a", "b", "c"]
#outsideList = ["x", "y", "z"]
logger = logging.getLogger(__name__)

INTERVAL = 20

def action_start(bot: Bot, update: Update):
        print("chat_id started", update.message.chat_id)

        if update.message.chat_id not in [chat_id for (phone, chat_id) in users]:
                contact_keyboard = telegram.KeyboardButton(text="send_contact", request_contact=True)
                custom_keyboard = [[ contact_keyboard ]]
                reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
                bot.send_message(chat_id=update.message.chat_id, text="what's your number?", reply_markup=reply_markup)

        

def callback_minute(bot, job):
        #print("minute")
        for (phone,chat_id) in users:
                [baseList, outsideList] = invokeGetReport(phone)
                bot.send_message(chat_id=chat_id, text='Inside the base:')
                text = ""
                for person in baseList:
                        text += person + "\n"
                
                if text:
                        bot.send_message(chat_id=chat_id, text=text)
                bot.send_message(chat_id=chat_id, text='Outside the base:')

                text = ""
                for person in outsideList:
                        text += person + "\n"
                
                if text:
                        bot.send_message(chat_id=chat_id, text=text)

def _error(bot: Bot, update: Update, e: BaseException):
        logger.error(e.message)

def contact_callback(bot, update):
        contact = update.effective_message.contact
        phone = contact.phone_number
        if phone not in [phone for (phone, chat_id) in users]:
                users.insert(0,(phone,update.message.chat_id))
                print(phone)
        contact_keyboard = telegram.KeyboardButton(text="", request_contact=False)
        custom_keyboard = [[ contact_keyboard ]]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=update.message.chat_id, text="", reply_markup=reply_markup)

def start_bot():
        updater = Updater('892444494:AAFCYNd48UN2CdH1T6Ck7hVIXHympFGYk6c')
        
        job_minute = updater.job_queue.run_repeating(callback_minute, interval=INTERVAL, first=0)

        # Add handlers
        updater.dispatcher.add_handler(CommandHandler('start', action_start))
        updater.dispatcher.add_error_handler(_error)
        updater.dispatcher.add_handler(MessageHandler(Filters.contact, contact_callback))

        updater.start_polling()
        # updater.idle()

        while True:
                pass

if __name__ == '__main__':
    start_bot()
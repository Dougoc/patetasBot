# -*- coding: utf-8 -*
##
## Make by Dod
## To 3 patetas group
## Validate Role
## Requirement: python3
##
import logging
import os
from random import randrange
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

botToken = os.getenv('TOKEN')

if not botToken:
    print("You need environment variable TOKEN")
    exit(1)

updater = Updater(token=botToken, use_context=True)

dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Bando de nerd. To de olho em vocês")
    logging.info("Send msg to %s" % update.message.chat_id)

def filter(update, context):
    msgRaw = str(update.message.text.lower())
    usrRaw = str(update.message.chat.first_name)

    palabras = ['beber', 'cheirar', 'putas', 'drugs', 'drogas', 'mulheres']

    for boa in palabras:
        if msgRaw.find(boa) >= 0:
            logging.info(f"achei a palavra {boa}")
            msg = beber()
            context.bot.send_message(chat_id=update.message.chat_id, text=f"Topo {boa}, {usrRaw}! {msg}")

    if msgRaw.find('porn') >= 0:
        path = randrange(9999999999)
        context.bot.send_message(chat_id=update.message.chat_id, text=f"Aqui teu porn do dia danado:\nhttps://beeg.com/{path}")
        logging.info("Send porn link to %s" % update.message.chat_id)


    logging.info("Send msg to %s" % update.message.chat_id)
    #context.bot.send_message(chat_id=update.message.chat_id, text=f"hello {usrRaw}, you say {msgRaw}")

def beber():
    return "Mas Thiago não vai"

def mulher():
    pass


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

filter_handler = MessageHandler(Filters.text, filter)
dispatcher.add_handler(filter_handler)

updater.start_polling()

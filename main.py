# -*- coding: utf-8 -*
##
## Make by Dod
## To 3 patetas group
## Validate Role
## Requirement: python3
##
import logging
import requests
import json
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
    logging.info("Received message from %s" % str(update.message.from_user.first_name))


def filter(update, context):
    msgRaw = str(update.message.text.lower())
    usrRaw = str(update.message.from_user.first_name)

    palabras = ['beber', 'cheirar', 'putas', 'drugs', 'drogas', 'mulheres']

    for boa in palabras:
        if msgRaw.find(boa) >= 0:
            logging.info(f"Achei a palavra {boa}")
            msg = beber()
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text=f"Topo {boa}, {usrRaw}! {msg}")

    if msgRaw.find('porn') >= 0:
        path = randrange(9999999999)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=f"Aqui teu porn do dia danado:\nhttps://beeg.com/{path}")
        logging.info("[%s] Enviando link porno" % usrRaw)

    if msgRaw.find('chover') >= 0:
        temp = clima()
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=f"A temperatura hoje é de: {temp}")
        logging.info("[%s] Enviando temperatura" % usrRaw)

    logging.info("[%s] Respondendo mensagem" % usrRaw)


def clima():
    tempoToken = os.getenv('CLIMA', '131e182a78f3cd2a3a010a7a5dfdcfc1')
    if not tempoToken:
        return 'Não sou adivinho demonio.\n(brinks, fatal o token).'

    url = 'http://apiadvisor.climatempo.com.br'

    Id = cityId(url, tempoToken)

    path2 = f'/api-manager/user-token/{tempoToken}/locales'
    requests.put(url + path2, f'localeId[{Id}]')

    path = f'/api/v1/forecast/locale/{Id}/hours/72?token={tempoToken}'
    r = requests.get(url + path)
    if r.status_code == 200:
        data = r.content['data']

        for info in data:
            graus = info['temperature']['temperature']
            return graus
    else:
        return f"não deu: {r.content}"


def cityId(url, token):
    city = 'Rio de Janeiro'
    state = 'RJ'

    path = f'/api/v1/locale/city?name={city}&state={state}&token={token}'
    r = requests.get(url + path)

    content = json.loads(r.content)[0]

    return content['id']


def registryCity(id, url, token):
    logging.info("Status %s" % r.status_code)


def beber():
    return "Mas Thiago não vai"


def mulher():
    pass


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

filter_handler = MessageHandler(Filters.text, filter)
dispatcher.add_handler(filter_handler)

updater.start_polling()

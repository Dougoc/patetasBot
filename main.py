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
from datetime import datetime
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
            msg = beber()
            logging.info("[%s] Respondendo devido a palavra %s" % (usrRaw, boa))
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text=f"Topo {boa}, {usrRaw}! {msg}")

    if msgRaw.find('porn') >= 0:
        path = randrange(9999999999)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=f"Aqui teu porn do dia danado:\nhttps://beeg.com/{path}")
        logging.info("[%s] Enviando link porno" % usrRaw)

    if msgRaw.find('graus') or  msgRaw.find('chover') >= 0:
        logging.info("[%s] Enviando temperatura" % usrRaw)
        temp = clima()

        if temp < 30:
            context.bot.send_message(chat_id=update.message.chat_id,
                                    text=f"Para Carioca, hoje ta um frio da porra: {temp}°C")
        else:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text=f"Quente como seu rabo: {temp}°C")


def clima():
    tempoToken = os.getenv('CLIMA', '131e182a78f3cd2a3a010a7a5dfdcfc1')
    url = 'http://apiadvisor.climatempo.com.br'
    if not tempoToken:
        return 'Não sou adivinho demonio.\n(brinks, fatal o token).'

    cityId = getCity(url, tempoToken)

    register = registryCity(cityId, tempoToken, url)

    if not register:
        return 'Failed'

    path = '/api/v1/forecast/locale/%s/hours/72?token=%s' % (cityId, tempoToken)
    r = requests.get(url + path)

    if r.status_code == 200:

        today = datetime.now()
        now = today.strftime("%Y-%m-%d %H:00:00")

        data = json.loads(r.content)['data']

        temp = [i['temperature']['temperature'] for i in data if i['date'] == now]
        return temp[0]

    else:
        return f"não deu: {r.content}"


def getCity(url, token):
    city = 'Rio de Janeiro'
    state = 'RJ'

    path = '/api/v1/locale/city?name=%s&state=%s&token=%s' % (city, state, token)
    r = requests.get(url + path)

    content = json.loads(r.content)[0]

    return content['id']


def registryCity(cityid, token, url):
    path2 = '/api-manager/user-token/%s/locales' % (token)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'localeId[]': '%s' % cityid
    }

    r = requests.put(url + path2, headers=headers, data=data)

    content = json.loads(r.content)['locales']

    if content:
        return int(content[0])
    else:
        return 'Failed'


def beber():
    return "Mas Thiago não vai"


def mulher():
    pass


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

filter_handler = MessageHandler(Filters.text, filter)
dispatcher.add_handler(filter_handler)

updater.start_polling()

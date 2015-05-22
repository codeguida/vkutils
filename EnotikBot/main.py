#!/usr/bin/env python3
#-*- coding: UTF-8 -*-
import vk, os
from time import sleep
import requests as req
from lxml import html
from random import randint

def bash(id, mode='u'):
    try:
        r = req.get('http://bash.im/random')
        doc = html.document_fromstring(r.text)
        bash = '\n'.join(doc.xpath('//*[@id="body"]/div[3]/div[@class="text"]/text()'))
        if mode == 'c':
            vkapi.messages.send(chat_id=id, message=bash)
        else:
           vkapi.messages.send(user_id=id, message=bash)
    except Exception as e:
        print(e)

def cgra(id, mode='u'):
    try:
        r = req.get('http://codeguida.com/')
        doc = html.document_fromstring(r.text)
        last_article = doc.xpath('/html/body/div[3]/section/div[1]/div[1]/article[1]/div/a/@href')[0]
        last_id = int(last_article.split('/')[-2])
        random_id = randint(1, last_id)
        r = req.get('http://codeguida.com/post/{}/'.format(random_id))
        doc = html.document_fromstring(r.text)
        title = doc.xpath('/html/body/div[3]/div[2]/section/h1/text()')[0]
        message = '{0}\n\nhttp://codeguida.com/post/{1}/'.format(title, random_id)
        if mode == 'c':
            vkapi.messages.send(chat_id=id, message=message)
        else:
           vkapi.messages.send(user_id=id, message=message)
    except Exception as e:
        print(e)

def print_help(id, mode='u'):
    try:
        message = """=== Система \"Єнотик\" ===
        Дотсупні команди:
        &#_9989; ~bash~ -- випадкова цитата з bash.im 
        &#_9989; ~cgra~ -- випадкова стаття з Codeguida
        &#_9989; ~help~ -- показує цю довідку

        Автор: OlegWock, 2015, спеціально для Codeguida"""
        if mode == 'c':
            vkapi.messages.send(chat_id=id, message=message)
        else:
           vkapi.messages.send(user_id=id, message=message)
    except Exception as e:
        print(e)


login = os.environ["VK_LOGIN"]
password = os.environ["VK_PASS"]

# Авторизація
vkapi = vk.EnterCaptchaAPI('4766382', login, password)
print('Успішно авторизувався')

messages = vkapi.messages.get(count=1)
last = messages['items'][0]['id']

while True:
    try:
        messages = vkapi.messages.get(last_message_id=last, timeout=5)
    except Exception as e:
        print(e)
        sleep(4)
        continue
    if not messages['items']:
        sleep(4)
        continue
    last = messages['items'][0]['id']
    for message in messages['items']:
        if "~bash~" in message['body']:
            if 'chat_id' in message:
                bash(message['chat_id'], 'c')
            else:
                bash(message['user_id'])
        if "~cgra~" in message['body']:
            if 'chat_id' in message:
                cgra(message['chat_id'], 'c')
            else:
                cgra(message['user_id'])
        if "~help~" in message['body']:
            if 'chat_id' in message:
                print_help(message['chat_id'], 'c')
            else:
                print_help(message['user_id'])
    sleep(4)
    
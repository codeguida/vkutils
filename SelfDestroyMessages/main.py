#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

from PIL import Image, ImageDraw, ImageFont
import vk, json, textwrap, os
from time import sleep
import requests as req

def getUserId(link):
    id = link
    if 'vk.com/' in link:
        id = link.split('/')[-1]
    if not id.replace('id', '').isdigit():
        id = vkapi.utils.resolveScreenName(screen_name=id)['object_id']
    else:
        id = id.replace('id', '')
    return int(id)

vkapi = vk.API(access_token=os.environ["OLEG_VK_TOKEN"])
sl = lambda: sleep(0.4)
fnt = ImageFont.truetype('courier.ttf', 18)

read_time = 60 * 1

user_to_send = getUserId(input("Введіть посилання на користувача: "))
text = input("Введіть ваше повідомлення: ")



im = Image.new("RGBA", (800, 800), color=(255, 255, 255))
imd = ImageDraw.Draw(im)
text_lines = textwrap.wrap(text, width=72)
for i, line in enumerate(text_lines):
    imd.text((0, i*18), line, font=fnt, fill=(0, 0, 0))
del imd
im = im.crop((0, 0, 800, 18*len(text_lines)))
im.save("output.jpg", "jpeg")


photo_server = vkapi.photos.getMessagesUploadServer()
sl()
files = {'photo': open('output.jpg', 'rb')}
data = {k.split('=')[0]: k.split('=')[1] for k in photo_server['upload_url'].split('?')[1].split('&')}
r = req.post(photo_server['upload_url'], data, files=files)
data = json.loads(r.text)
buf = vkapi.photos.saveMessagesPhoto(server=data['server'], photo=data['photo'], hash=data['hash'])[0]
sl()
photo_id = 'photo{}_{}'.format(buf['owner_id'], str(buf['id']))

vkapi.messages.send(user_id=user_to_send, attachment=photo_id)
sleep(read_time)
vkapi.photos.delete(owner_id=buf['owner_id'], photo_id=str(buf['id']))
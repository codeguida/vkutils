from colorama import Fore, Style, init
from pprint import pformat
import vk
from time import  sleep
import os, sys

formating = {"green": Fore.GREEN,
             "red": Fore.RED,
             "white": Fore.WHITE,
             "blue": Fore.BLUE,
             "cyan": Fore.CYAN,
             "yellow": Fore.YELLOW,
             "bold": Style.BRIGHT,
             "reset": Style.RESET_ALL}

mes_statuses = {1: "{bold}{blue}прочитане{reset} ==".format(**formating),
                0: "{bold}{red}непрочитане{reset} ==".format(**formating)}

term_size = 109

init()

if sys.platform == 'win32': # бо смайлики викликають ексепшн
    os.system('chcp 65001')

MESSAGE_AUTHOR = "{cyan}{first_name} {last_name}{reset} == {green}(https://vk.com/id{bold}{red}{id}{reset}{green}){reset} == "
FWD_MESSAGE_AUTHOR = ">> {yellow}{first_name} {last_name}{reset} == {green}(https://vk.com/id{bold}{red}{id}{reset}{green}){reset}"


def format(str, *args, **kw): # власні милиці, без них ніяк
    buf = kw.copy() if kw else {}
    buf.update(formating)
    return str.format(*args, **buf)

def printMessages(messages, outfile=sys.stdout):
    for mes in messages:
        if "from_id" in mes:
            user = vkapi.users.get(user_ids=mes['from_id'])[0]
        else:
            user = vkapi.users.get(user_ids=mes['user_id'])[0]
        print(format(MESSAGE_AUTHOR, **user), end='', file=outfile)
        print(mes_statuses[mes['read_state']], file=outfile)
        print(mes['body'], file=outfile)
        if 'fwd_messages' in mes:
            for fwd_mes in mes['fwd_messages']:
                fwd_user = vkapi.users.get(user_ids=fwd_mes['user_id'])[0]
                print(format(FWD_MESSAGE_AUTHOR, **fwd_user), file=outfile)
                print(">>> {body}".format(**fwd_mes), file=outfile)
                sleep(0.25)
        if 'attachments' in mes:
            print(format("{yellow}{bold}Attachments:{reset}"), file=outfile)
            for a in mes['attachments']:
                print("=== Type: {type}".format(**a), file=outfile)
                print(pformat(a), file=outfile)
        print(format("{bold}{0}{reset}", "="*term_size))
        sleep(0.25)


def showDialogs(**kw):
    dialogs = vkapi.messages.getDialogs(**kw)
    printMessages([i['message'] for i in dialogs['items']])

def showDialog(**kw):
    messages = vkapi.messages.getHistory(**kw)
    printMessages(messages['items'][::-1])

def sendMessage(**kw):
    if 'user_id' in kw:
        user = vkapi.users.get(user_ids=kw['user_id'], name_case='dat')[0]
        print("Відправити повідомлення {first_name} {last_name}".format(**user))
    if 'message' not in kw:
        message = input(">> ")
        vkapi.messages.send(message=message, **kw)
    else:
        vkapi.messages.send(**kw)

    if 'user_id' in kw:
        yn = input("Відкрити діалог з користувачем? [y,т/n,н][n]: ")
        if 'yes' in yn.lower() or 'y' in yn.lower() or 'т' in yn.lower() or 'так' in yn.lower():
            showDialog(vkapi, count=10, user_id=kw['user_id'])

def copyLiked(count=1, mode="posts"):
    likes = ''
    for i in range(count):
        if mode == "posts":
            liked = vkapi.fave.getPosts(count=100, offset=i*100)
        elif mode == "photos":
            liked = vkapi.fave.getPhotos(count=100, offset=i*100)
        for like in liked['items']:
            if mode == 'posts':
                likes += "vk.com/wall{owner_id}_{id}\n".format(**like)
            elif mode == "photos":
                likes += "vk.com/photo{owner_id}_{id}\n".format(**like)
        sleep(0.25)
    return likes

def copyGroups(count):
    groups = ''
    raw = vkapi.groups.get(count=count, extended=1, fields="screen_name")
    for group in raw['items']:
        groups += 'vk.com/{screen_name}\n'.format(**group)
    return groups

def copyMessages(id, count, filename=None):
    messages = []
    user = vkapi.users.get(user_ids=id)[0]
    cur_user = vkapi.users.get()[0]
    users = {cur_user['id']: cur_user,
             user['id']: user}
    for i in range(count):
        buf = vkapi.messages.getHistory(user_id=id, count=200, offset=i*200)
        for m in buf['items']:
            messages.append(m)
        sleep(0.25)
    messages = messages[::-1]
    if filename == None:
        f = open(str(id) + "-messages.txt", 'w', encoding='utf-8')
    else:
        f = open(filename, 'w', encoding='utf-8')
    printMessages(messages, outfile=f)
    f.close()

def loadMessagees(filename):
    with open(filename, encoding='utf-8') as f:
        print(f.read())


vkapi = vk.API(access_token='')

while 1:
    try:
        print(exec(input(">>> ")))
    except Exception as e:
        print(e)
        continue





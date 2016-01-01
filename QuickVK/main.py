from colorama import Fore, Style, init
from pprint import pformat
import vk
from time import  sleep
import os, sys
from datetime import datetime

sl = lambda: sleep(0.4)
formating = {"green": Fore.GREEN,
             "red": Fore.RED,
             "white": Fore.WHITE,
             "blue": Fore.BLUE,
             "cyan": Fore.CYAN,
             "yellow": Fore.YELLOW,
             "bold": Style.BRIGHT,
             "reset": Style.RESET_ALL}

mes_statuses = {1: "{bold}{blue}readed{reset} ==".format(**formating),
                0: "{bold}{red}unreaded{reset} ==".format(**formating)}

term_size = 100

init()

if sys.platform == 'win32': # because smiles cause exception
    os.system('chcp 65001')

MESSAGE_AUTHOR = "{cyan}{first_name} {last_name}{reset} == {green}(https://vk.com/id{bold}{red}{id}{reset}{green}){reset} == "
FWD_MESSAGE_AUTHOR = ">> {yellow}{first_name} {last_name}{reset} == {green}(https://vk.com/id{bold}{red}{id}{reset}{green}){reset}"


def format(str, *args, **kw):
    buf = kw.copy() if kw else {}
    buf.update(formating)
    return str.format(*args, **buf)

def printMessages(messages, outfile=sys.stdout):
    for mes in messages:
        if "chat_id" in mes:
            print(format("{green}[chat {0}]{reset} {1}", mes['chat_id'], mes['title']))
        
        if "from_id" in mes:
            user = vkapi.users.get(user_ids=mes['from_id'], fields="online")[0]
        else:
            user = vkapi.users.get(user_ids=mes['user_id'], fields="online")[0]

        sl()
        online = "{green}[✔]{reset} " if user['online'] else "{red}[✖]{reset} "
        print(format(online + MESSAGE_AUTHOR, **user), end='', file=outfile)
        print(mes_statuses[mes['read_state']], file=outfile, end='')
        print(" {} ==".format(datetime.fromtimestamp(mes['date']).strftime('%H:%M %d.%m.%Y')), file=outfile)
        print(mes['body'], file=outfile)
        if 'fwd_messages' in mes:
            for fwd_mes in mes['fwd_messages']:
                fwd_user = vkapi.users.get(user_ids=fwd_mes['user_id'])[0]
                print(format(FWD_MESSAGE_AUTHOR, **fwd_user), file=outfile)
                print(">>> {body}".format(**fwd_mes), file=outfile)
                sl()
        if 'attachments' in mes:
            print(format("{yellow}{bold}Attachments:{reset}"), file=outfile)
            for a in mes['attachments']:
                print("=== Type: {type}".format(**a), file=outfile)
                print(pformat(a), file=outfile)
        print(format("{bold}{0}{reset}", "="*term_size), file=outfile)
        sl()


def showFriends(only_online=False, **kw):
    if not "fields" in kw:
        kw['fields'] = 'online'
    else:
        kw['fields'] += ", online"
    if not "order" in kw:
        kw['order'] = 'hints'
    frs = vkapi.friends.get(**kw)['items']
    if only_online:
        frs = list(filter(lambda x: x['online'], frs))
    max_no_symbs = len(str(len(frs)))

    for i, fr in enumerate(frs):
        if fr['online']:
            print(format("{green}[{0}][✔]", str(i+1).zfill(max_no_symbs)), end=" ")
        else:
            print(format("[{0}][✖]", str(i+1).zfill(max_no_symbs)), end=" ")
        print("{first_name} {last_name} (https://vk.com/id{id})".format(**fr), end="")
        print(format("{reset}"))




def showDialogs(**kw):
    dialogs = vkapi.messages.getDialogs(**kw)
    printMessages([i['message'] for i in dialogs['items']])

def showDialog(**kw):
    messages = vkapi.messages.getHistory(**kw)
    printMessages(messages['items'][::-1])

def sendMessage(**kw):
    if 'user_id' in kw:
        user = vkapi.users.get(user_ids=kw['user_id'], name_case='dat')[0]
        print("Send a message to {first_name} {last_name}".format(**user))
    if 'message' not in kw:
        message = input(">> ")
        vkapi.messages.send(message=message, **kw)
    else:
        vkapi.messages.send(**kw)

    if 'user_id' in kw:
        yn = input("Open dialogue with the user? [y,т/n,н][n]: ")
        if 'yes' in yn.lower() or 'y' in yn.lower() or 'т' in yn.lower() or 'так' in yn.lower():
            showDialog(count=10, user_id=kw['user_id'])

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
    sl()
    cur_user = vkapi.users.get()[0]
    sl()
    users = {cur_user['id']: cur_user,
             user['id']: user}
    for i in range(count):
        buf = vkapi.messages.getHistory(user_id=id, count=200, offset=i*200)
        for m in buf['items']:
            messages.append(m)
        sl()
    messages = messages[::-1]
    if filename == None:
        f = open(str(id) + "-messages.txt", 'w', encoding='utf-8')
    else:
        f = open(filename, 'w', encoding='utf-8')
    printMessages(messages, outfile=f)
    f.close()

def loadMessages(filename):
    with open(filename, encoding='utf-8') as f:
        print(f.read())


vkapi = vk.API(access_token=os.environ["VK_TOKEN"])
if __name__ == "__main__":
    while 1:
        try:
            print(exec(input(">>> ")))
        except Exception as e:
            print(e)
            continue





#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

import vk
from time import sleep

def getUserId(link):
    id = link
    if 'vk.com/' in link:
        id = link.split('/')[-1]
    if not id.replace('id', '').isdigit():
        id = vkapi.utils.resolveScreenName(screen_name=id)['object_id']
    else:
        id = id.replace('id', '')
    return int(id)

def getLikes(user_id, count):
    subscriptions_list = vkapi.users.getSubscriptions(user_id=user_id, extended=0)['groups']['items']
    groups_list = ['-' + str(x) for x in subscriptions_list]

    posts = {}
    newsfeed = vkapi.newsfeed.get(filters='post', source_ids=', '.join(groups_list), count=100, timeout=10)

    posts.update({x['post_id'] : x['source_id'] for x in newsfeed['items']})
    next_from = newsfeed['next_from']

    if count != 1:
        for c in range(count-1):
            newsfeed = vkapi.newsfeed.get(filters='post', source_ids=', '.join(groups_list), count=100, timeout=10, start_from=next_from)
    
            posts.update({x['post_id'] : x['source_id'] for x in newsfeed['items']})
            next_from = newsfeed['next_from']

        

    liked_posts = []

    print('Лайкнуті пости:')
    for post in posts.items():
        try:
            isLiked = vkapi.likes.isLiked(user_id=user_id, item_id=post[0], type="post", owner_id=post[1], timeout=5)['liked']
        except Exception:
            print("ERROR!!! " + 'vk.com/wall{}_{}'.format(post[1], post[0]))
            isLiked = 0
        if isLiked:
            liked_posts.append('vk.com/wall{}_{}'.format(post[1], post[0]))
            print('vk.com/wall{}_{}'.format(post[1], post[0]))
        sleep(0.25)
    return liked_posts

login = ''
password = ''

# Авторизація
vkapi = vk.API('4766382', login, password)

user_id = input('Введіть id користувача або посилання на сторінку: ')
user_id = getUserId(user_id)
getLikes(user_id, 5) # 5 -- глибина пошуку. Кількість постів, що буде перевірена: 100*x = 100*5 = 500
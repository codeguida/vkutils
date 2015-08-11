#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

import vk, os
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


def getUserInfo(user_id):
    template = "\n{first_name} {last_name} (id: {id})"

    info = vkapi.users.get(user_ids=user_id, fields='bdate, home_town', name_case='Nom')
    inf = template.format(**info[0])
    print(inf)
    return info


def getUserAge(user):
    q = "{first_name} {last_name}".format(**vkapi.users.get(user_ids=user)[0])
    age = -1
    for i in range(14, 101):
        results = vkapi.users.search(q=q, age_to=i)
        for result in results['items']:
            if int(result['id']) == user:
                print("Age: {} years".format(i))
                age = i
                break
    
        if age != -1:
            break
        sleep(0.35)
    return age


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

    print('Liked posts:')
    for post in posts.items():
        try:
            isLiked = vkapi.likes.isLiked(user_id=user_id, item_id=post[0], type="post", owner_id=post[1], timeout=5)['liked']
        except Exception:
            print("ERROR!!! " + 'vk.com/wall{}_{}'.format(post[1], post[0]))
            isLiked = 0
        if isLiked:
            liked_posts.append('vk.com/wall{}_{}'.format(post[1], post[0]))
            print('vk.com/wall{}_{}'.format(post[1], post[0]))
        sleep(0.35)
    return liked_posts


# Авторизація
vkapi = vk.API(access_token=os.environ["VK_TOKEN"])

user_id = input('Enter your user id or links to page: ')
user_id = getUserId(user_id)
getUserInfo(user_id)
getUserAge(user_id)
getLikes(user_id, 5) # 5 -- глибина пошуку. Кількість постів, що буде перевірена: 100*x = 100*5 = 500
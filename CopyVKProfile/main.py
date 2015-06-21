#!/usr/bin/python3

import vk
from time import  sleep
import os, sys

###   __          __        _       _                                                  
###   \ \        / /       | |     (_)                                                 
###    \ \  /\  / /__  _ __| | __   _ _ __     _ __  _ __ ___   __ _ _ __ ___  ___ ___ 
###     \ \/  \/ / _ \| '__| |/ /  | | '_ \   | '_ \| '__/ _ \ / _` | '__/ _ \/ __/ __|
###      \  /\  / (_) | |  |   <   | | | | |  | |_) | | | (_) | (_| | | |  __/\__ \__ \
###       \/  \/ \___/|_|  |_|\_\  |_|_| |_|  | .__/|_|  \___/ \__, |_|  \___||___/___/
###                                           | |               __/ |                  
###                                           |_|              |___/                  

def copyInfo(user_id):
	info = vkapi.users.get(user_ids=user_id, fields='sex, bdate, city, country, photo_max, photo_max_orig, photo_id, domain, has_mobile, contacts, connections, site, education, universities, schools, can_post, can_see_all_posts, can_see_audio, can_write_private_message, status, last_seen, common_count, relation, relatives, counters, screen_name, maiden_name, timezone, occupation,activities, interests, music, movies, tv, books, games, about, quotes, personal, friends_status')
    del info['first_name']
    del info['last_name']
    del info['screen_name']
    vkapi.account.saveProfileInfo(**info)



login = os.environ["VK_LOGIN"]
password = os.environ["VK_PASS"]

vkapi = vk.API('4766382', login, password)

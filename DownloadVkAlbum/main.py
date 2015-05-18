#!/usr/bin/env python3.4
#-*- coding: UTF-8 -*-
# Імпортуємо потрібні модулі
from urllib.request import urlretrieve
import vk, os, time, math

# Ваш логін, пароль
login = ''
password = ''

# Авторизація
vkapi = vk.API('4567667', login, password)

url = input("Введіть url альбому: ")
# Магія
album_id = url.split('/')[-1].split('_')[1]
owner_id = url.split('/')[-1].split('_')[0].replace('album', '')

photos_count = vkapi.photos.getAlbums(owner_id=owner_id, album_ids=album_id)['items'][0]['size']

counter = 0 # поточний лічильник
prog = 0 # відсоток завантажених
breaked = 0 # не завантажено через помилку
time_now = time.time() # час старту


# Створимо необхідні папки
if not os.path.exists('saved'):
    os.mkdir('saved')
photo_folder = 'saved/album{0}_{1}'.format(owner_id, album_id)
if not os.path.exists(photo_folder):
    os.mkdir(photo_folder)

for j in range(math.ceil(photos_count / 1000)): # Підсчитуємо скільки раз потрібно отримувати список фото, так як число вийде не ціле -- округлюємо в більшу сторону
    photos = vkapi.photos.get(owner_id=owner_id, album_id=album_id, count=1000, offset=j*1000) # отримуємо список фото
    for photo in photos['items']:
        counter += 1
        url = photo['photo_604'] # Отримуємо адресу зображення
        print('завантажую фото № {} із {}. Прогрес: {} %'.format(counter, photos_count, prog))
        prog = round(100/photos_count*counter,2)
        try:
            urlretrieve(url, photo_folder + "/" + os.path.split(url)[1]) # Завантажуємо та зберігаємо файл
        except Exception:
            print('Відбулася помилка, файл пропущено.')
            breaked += 1
            continue
time_for_dw = time.time() - time_now
print("\nВ черзі було {} файлів. З них вдало завантажено {} файлів, {} не вдалося завантажити. Затрачено часу: {} сек.". format(photos_count, photos_count-breaked, breaked, round(time_for_dw,1)))


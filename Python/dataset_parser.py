#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pymongo import MongoClient
from mylib import *
import sys

#parsed_website_name = 'NatGeogr'
parsed_website_name = sys.argv[1]
clean_db = ''
if len(sys.argv) > 2:
    clean_db = sys.argv[2]

print ' ----- Parser started ----- '

for ws in websites:
    if ws['name'] == parsed_website_name:
        website = ws
name = website['name']
domain = website['domain']
params = website['params']
home_url = website['home_url']

print ' ----- ' + parsed_website_name + ' ----- '
client = MongoClient('mongodb://127.0.0.1:3001/meteor')
db = client['meteor']
dataset_links_collection = db['dataset_links_collection_' + str(website['name'])]
links_for_downloading = []

if clean_db == 'true':
    dataset_links_collection.delete_many({})
    website_link = create_new_link(home_url, name, domain)
    dataset_links_collection.insert_one(website_link)
    links_for_downloading.append(website_link)

# Get downloaded and for downloading links from DB
downloaded_links = ['']
downloaded_links_pointer = dataset_links_collection.find({'downloaded': True})

for link in downloaded_links_pointer:
    downloaded_links.append(link['url'])

for_down_links_pointer = dataset_links_collection.find({'downloaded': False})
for url in for_down_links_pointer:
    links_for_downloading.append(url)

i = 0
while len(links_for_downloading) > 0:

    # Пропускаем уже загруженные страницы
    while links_for_downloading[0]['url'] in downloaded_links:
        del(links_for_downloading[0])
    current_link = links_for_downloading[0]
    current_url = current_link['url']

    # Достаем линки с текущей страницы страницы
    try:
        links = get_links_from_url(current_url, domain, params)
    except Exception as e:
        print e
        links = []

    # Нужно записать линки в базу, чтобы не было повторений
    for url in links:
        new_link = create_new_link(url, name, domain)

        # Перед записью проверяем чтобы этой ссылки не было уже в базе
        found_locally = (url in downloaded_links) or (filter(lambda l: l['url'] == url, links_for_downloading) != [])
        if not found_locally:
            found_in_db = dataset_links_collection.find({'url': url}).count() > 0
            if not found_in_db:
                dataset_links_collection.insert_one(new_link)
                links_for_downloading.append(new_link)

    try:
        title, content, img = get_page_content(current_url, params)
        save_page_in_file(content, title, img, current_url, name)

        i += 1
        if i % 10 == 0:
            print 'Got ' + str(i) + ' pages'
        else:
            print 'Got it'

    except Exception as e: print e

    finally:
        #Что бы ни случилось, убираем страницу из очереди.
        dataset_links_collection.update({'url': current_url}, {'$set': {'downloaded': True}})
        downloaded_links.append(current_url)
        del(links_for_downloading[0])

# Готово! Вы прекрасны
print ' ----- Succsesfully ended ----- '
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mylib import *
import logging
import time
#import resource

import sys

reload(sys)
sys.setdefaultencoding('utf8')

startTime = time.time()
#mem_usage = []


logging.basicConfig(filename='news_parser.log', level=logging.WARNING, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filemode='w')
logging.warning(' ----- Parser started ----- ')

# Connect to MongoDB
summaries_collection = client['meteor']['summaries']
links_collection = client['meteor']['links']

logging.warning(' Getting new links ')
# Полный проход по доступным сайтам и достаем нвоые ссылки с главных страниц

for website in websites:
    # Достаем линки с главной страницы
    name = website['name']
    domain = website['domain']
    home_url = website['home_url']
    params = website['params']

    links = get_links_from_url(home_url, domain, params)

    #mem_usage.append(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000)

    # Нужно записать линки в базу, чтобы не было повторений
    if links: links = set(links)
    for link in links:
        new_link = create_new_link(link, name, domain)
        # Перед записью проверяем чтобы этой ссылки не было уже в базе
        if links_collection.find_one({'url': link}) == None:
            links_collection.insert_one(new_link)
            #logging.warning(new_link)

# Достать и записать тексты по новым линкам, и проставить им флаги, что они уже скачаны
for website in websites:

    name = website['name']
    domain = website['domain']
    home_url = website['home_url']
    params = website['params']

    links_for_downloading = links_collection.find({'downloaded': False, 'source': name})
    logging.warning('--- New links for downloading: ' + str(links_for_downloading.count()) + ' on ' + str(name))

    #mem_usage.append(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000)

    for link in links_for_downloading:
        url = link['url']
        ignore_link = False

        if 'ignore_urls_with' in params:
            if any(pattern in url for pattern in params['ignore_urls_with']):
                ignore_link = True

        if 'ignore_urls_without' in params:
            found = False
            if any(pattern in url for pattern in params['ignore_urls_without']):
                found = True

            if not found:
                ignore_link = True

        if ignore_link:
            logging.warning("Ignore url : " + url)
            continue

        #logging.warning(url)
        try:
            new_summary = get_page_summary(url, name, domain, params)

        except AssertionError as e:
            # Если эта ошибка, значит страница не прошла проверку
            logging.warning(str(e) + " : " + url)

        except Exception as e:
            logging.exception(e)

        else:
            # Если никаких ошибок, записываем саммари в базу и обновляем флаг ссылки на "скачанный"
            summaries_collection.insert_one(new_summary)

        finally:
            links_collection.update({'url': url}, {'$set': {'downloaded': True}})


############ Check user sources
for feed in user_sources:
    name = feed['name'][:18]
    url = feed['url']
    
    if 'youtube.com/user/' in url:
        url = url_extract(url, '/user/', 'https://www.youtube.com/feeds/videos.xml?user=')
    if 'youtube.com/channel/' in url:
        url = url_extract(url, '/channel/', 'https://www.youtube.com/feeds/videos.xml?channel_id=')
    if 'youtube.com/playlist?' in url:
        url = url_extract(url, '?list=', 'https://www.youtube.com/feeds/videos.xml?playlist_id=')

    if 'reddit.com/r/' in url:
        url = url[:url.find('?')] if '?' in url else url
        url = url[:url.find('#')] if '#' in url else url
        url = url + '.rss'

    if 'vk.com' in url:
        url = url_extract(url, '.com/', 'http://feed.exileed.com/vk/feed/')

    if 'twitter.com' in url:
        url = url_extract(url, '.com/', 'http://feed.exileed.com/twitter/feed/')

    if 'facebook.com' in url:
        url = url_extract(url, '.com/', 'http://feed.exileed.com/facebook/feed/')

    if 'instagram.com' in url:
        url = url_extract(url, '.com/', 'http://feed.exileed.com/instagram/feed/')

    if url[:4] != 'http':
        url = 'http://' + url

    try:
        d = feedparser.parse(url)
        if len(d.entries) > 0:
            sources_collection.update_one({'name': feed['name']}, {'$set': {'type': 'rss', 'url': url}})
            rss_feeds.append(feed)
        else:
            logging.warning('Zero entries:')
            logging.warning(feed)
    except:
        logging.warning('Smth went wrong on:')
        logging.warning(feed)
        pass


############ RSS Parsing
for feed in rss_feeds:
    name = feed['name']
    url = feed['url']
    d = feedparser.parse(url)

    logging.warning(str(len(d.entries)) + ' posts on ' + name)

    #mem_usage.append(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000)

    '''
    if 'topics' not in feed or len(feed['topics']) > 1:
        try:
            topics = get_feed_topics(d, 1)
            sources_collection.update_one({'name': feed['name']}, {'$set': {'topics': topics}})
            logging.warning('Topics for ' + feed['name'] + ' : ' + str(topics))

            #mem_usage.append(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000)

        except Exception as e:
            logging.warning('Topics error:' + str(e))
            pass

    '''

    inserted = False

    entries = d.entries if len(d.entries) < 10 else d.entries[:10]

    for entry in entries:
        try:
            link = str(entry.link)

            found = links_collection.find_one({'url': link}) != None
            if not found:
                links_collection.insert_one({'url': link, 'source': name})
            else:
                continue

            clear_html = False if 'reddit' in feed['url'] else True

            title, full_content, thumbnail = extract_entry_info(entry, clear_html)
            full_content = full_content.decode('utf-8')

            content = full_content
            if len(full_content) > 390 and clear_html:
                content = create_summary_text(full_content, title)

            #mem_usage.append(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000)

            if 'reddit' in feed['url']:
                content = img_cleaner.clean_html(content)
                tree = html.fromstring(content)
                #Remove [comments] link
                for elem in tree.xpath('//*[text()="[comments]"]'):
                    elem.getparent().remove(elem)

                #Open links in new tab
                for elem in tree.xpath('//a'):
                    elem.attrib['target'] = "_blank"

                content = etree.tostring(tree)
                if content.find('submitted') > 300:
                    content = create_summary_text(tree.text_content(), title)[:300] + '...' + '<br>' + tree.xpath('//p[contains(text(), "submitted by ")]')[0].tostring()

            title = title.decode('utf-8')
            if len(title) > 90:
                title = title[:90] + (title[90:] and '...')

            if thumbnail == '':
                if 'feed' in d and 'image' in d['feed'] and 'href' in d['feed']['image']:
                    thumbnail = d['feed']['image']['href']

        except Exception as e:
            logging.exception(e)
            pass

        else:
            new_summary = {
                "title": title, #unicode(title, errors='ignore'),
                "url": link,
                "source": name,
                "img_src": thumbnail,
                "text": content, #unicode(content, errors='ignore'),
                "date": (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()
            }
            summaries_collection.update_one({'url': link},{'$set': new_summary}, upsert = True)
            #summaries_collection.insert_one(new_summary)
            inserted = True
            try:
                if len(full_content) > 1000:
                    save_page_in_file(html.fromstring(full_content).text_content(), title, thumbnail, link, name)
            except: pass

    #mem_usage.append(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000)

    if not inserted and 'zero_entries' not in feed:
        sources_collection.update_one({'name': name}, {'$set': {'zero_entries': True}})
    else:
        sources_collection.update_one({'name': name}, {'$set': {'zero_entries': False}})

#print sorted(mem_usage)[-5:]

# Готово! Вы прекрасны. Cron task every hour
logging.warning(' ----- Succsesfully ended ----- ')
logging.warning("Elapsed time: {:.3f} sec".format(time.time() - startTime))

#print "Elapsed time: {:.3f} sec".format(time.time() - startTime)
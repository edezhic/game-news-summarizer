# -*- coding: utf-8 -*-
import requests
from six.moves import cPickle as pickle
from math import e, sqrt, fabs, pow, log, exp
import numpy as np
from rfc3987 import parse
from lxml import html, etree
from lxml.html.clean import Cleaner
from datetime import datetime
import os
from pymongo import MongoClient
from collections import OrderedDict
import feedparser
from urlparse import urlparse, parse_qs

filepath_prefix = '/home/kennivich/Summarizer/Python/'

### Text processing

def word_tokenize(text):
    words = []
    start = -1
    is_word = False
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in range(len(text)):
        try:
            if text[i].isalpha() and not is_word:
                start = i
                is_word = True
        except Exception as e:
            print text[i]

        if not text[i].isalpha() and is_word:
            word = text[start:i].lower()
            if len(word) != 1 or word == 'a' or word in numbers:
                #words.append(word.encode('ASCII', 'ignore'))
                words.append(word.encode('utf-8', 'ignore'))
            is_word = False

    if is_word:
        word = text[start:].lower()
        if len(word) != 1 or word == 'a' or word in numbers:
            words.append(word.encode('utf-8', 'ignore'))
            #words.append(word.encode('ASCII', 'ignore'))

    if 'un' in words: words.remove('un')

    return words

def sent_ending(prev_char, curr_char, next_char):
    sent_endings = ['.', '!', '?']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    is_ending = False

    if curr_char in sent_endings:
        is_ending = True

    if prev_char in numbers and next_char in numbers:
        return False

    if prev_char in numbers and next_char.isalpha():
        return False

    if prev_char.isalpha() and next_char in numbers:
        return False

    return is_ending

def clean_sent_beginning(sentence):
    try:
        while sentence[0] in [' ', ',', '.', ')', '-']:
            sentence = sentence[1:]
        sentence = sentence[0].upper() + sentence[1:]
        return sentence
    except:
        return ''

def sent_tokenize(text):
    sentences = []
    last_sent_end_index = 0
    text_len = len(text)

    for i in range(1, text_len - 1):
        if sent_ending(text[i-1], text[i], text[i+1]) and (i - last_sent_end_index > 3):

            if text[i + 1] in ['"', ')', "'"]:
                i += 1

            sentence = text[last_sent_end_index:i + 1]
            sentence = clean_sent_beginning(sentence)

            if sentence.count('"') % 2 != 0:
                sentence = sentence.replace('"', '')

            if len(sentence) > 8:
                sentences.append(sentence)
            last_sent_end_index = i + 1

    i = text_len - 1
    if text[i] in ['.', '!', '?'] and (i - last_sent_end_index > 3):
        sentence = text[last_sent_end_index:i]
        sentence = clean_sent_beginning(sentence)

        if sentence.count('"') % 2 != 0:
            sentence = sentence.replace('"', '')

        if len(sentence) > 8:
            sentences.append(sentence)

    return sentences

### URLs processing

def youtube_video_id(url):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None

def url_extract(url, start, before='', after=''):
    link_endings = ['/', '&', '?', '#']

    start = url.find(start) + len(start)
    end = min(x for x in [url[start+1:].find(char) for char in link_endings] if x > 0) + start + 1 if any(char in url[start+1:] for char in link_endings) else len(url)
    name = url[start:end]
    return before + name + after

### Summary generation

def get_length_feature(length):
    best_length = 70
    length_feature = -0.003 * fabs(length - best_length) + 1
    if length_feature < 0:
        length_feature = 0
    return length_feature

def get_water_feature(words):
    water = 0
    for word in words:
        if word in stop_words:
            water += 1
    water = 1.0 * water / len(words)
    return water

def depth_feature(i):
    return pow(i, -0.03)

def tf(word, words):
    return (words.count(word) * 1.0 / len(words))

def idf(word):
    try:
        return idf_values[word]
    except Exception as e:
        if word.isalpha():
            return 3
        else:
            return 0.001

def word_vector(word):
    return np.zeros(300)
    #index = dictionary[word]
    #return embeddings[index]

def extract_features(sent_words, text_words, title_words = [], i = 1):

    sent_tf_idf = 0
    vector = np.zeros(300)
    tf_idf = {}

    # Параметр от длины(максимум при best_length знаках
    length_feature = get_length_feature(len(" ".join(sent_words)))

    # Средний TF-IDF слов в предложении
    for word in sent_words:
        if word not in stop_words and word in dictionary:
            # print word
            tf_idf[word] = tf(word, text_words) * pow(10, idf(word))
            if word in title_words:
                tf_idf[word] = tf_idf[word] * 2
            sent_tf_idf += tf_idf[word]

    if len(tf_idf) != 0:
        sent_tf_idf = sent_tf_idf / len(tf_idf)
    else:
        sent_tf_idf = 0

    # Процент воды в предложении
    water = get_water_feature(sent_words)

    # Параметр от расстояния от начала текста
    depth = depth_feature(i)

    # Формула веса предложения
    weight = (-4) * water + (1) * length_feature + (1.5) * depth + (1e-3) * sent_tf_idf

    # Приведение суммы всех тф-идф к единице (работает)
    normalization = 0
    for word in tf_idf:
        normalization += fabs(tf_idf[word])

    for word in tf_idf:
        tf_idf[word] = tf_idf[word] / normalization

    # в этом алгоритме чтото не так, должно типо из центра этих слов
    # смещаться в сторону с большим весом, но выглядит сейчас это иначе
    # разобраться без гаша
    for word in tf_idf:
        if word in dictionary:
            vector += word_vector(word) * tf_idf[word]
    # ^^^^^

    return vector, weight

def create_summary_text(text, title):
    text_words = word_tokenize(text)
    title_words = word_tokenize(title)
    i = 1
    sentences = []
    summary_length = 397
    summary = ''

    # Выделение векторов и весов предложений
    for sentence in sent_tokenize(text):
        #try:
        sent_words = word_tokenize(sentence)
        if len(sent_words) < 1:
            continue
        vector, weight = extract_features(sent_words, text_words, title_words, i)
        sentences.append({'vector': vector, 'weight': weight, 'sentence': sentence, 'i': i})
        i += 1
        #except:
        #    pass

    # Выборка лучших предложений
    best_sentences = []
    while len(summary) < summary_length and len(sentences) > 0:
        max_weight = -1e10
        for i in range(len(sentences)):
            if (sentences[i]['weight'] > max_weight):
                max_weight = sentences[i]['weight']
                index = i
        sentence = sentences[index]['sentence']
        weight = sentences[index]['weight']
        vector = sentences[index]['vector']
        i = sentences[index]['i']

        best_sentences.append({'sentence': sentence, 'i': i})
        summary += ' ' + sentence

        # decrease weights of nearest vectors
        for i in range(len(sentences) - 1):
            if i != index:
                vector2 = sentences[i]['vector']
                dist = np.linalg.norm(vector - vector2)
                decreas = exp(-pow(dist, 2) / 0.3)
                # decreas = 0.2 / pow(dist, 0.5)
                sentences[i]['weight'] -= decreas

        sentences.pop(index)

    #
    # Сортировка лучших предложений по их порядку в реальном тексте
    #
    summary = ''
    while len(summary) < summary_length and len(best_sentences) > 0:
        min_i = 1e10
        for i in range(len(best_sentences)):
            if (best_sentences[i]['i'] < min_i):
                min_i = best_sentences[i]['i']
                index = i

        summary += ' ' + best_sentences[index]['sentence']
        best_sentences.pop(index)

    summary = summary[:summary_length] + (summary[summary_length:] and '...')
    #return summary.encode('ASCII', 'ignore')
    return summary.encode('utf-8', 'ignore')

### Websites parsing

def request_page_tree(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'Accept-Language:en-US,en;q=0.8,ru;q=0.6',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36',
        'Cookie' : "sat=db52003c5ef43f2213a73c0cfd8c1747; device_view=full; AD_SESSION=f; skinSource=giantbomb_white; hycw4hSBtd=true; gebDnVVAmj=136101615611; XCLGFbrowser=CQDqEFcgwq0jB3KrCGc; LDCLGFbrowser=1bedbef3-b4ec-4304-bf1e-7e53c617511d; AMCV_10D31225525FF5790A490D4D%40AdobeOrg=1304406280%7CMCMID%7C87367100744380167012932309239694550977%7CMCAID%7CNONE%7CMCAAMLH-1464768041%7C6%7CMCAAMB-1464768041%7Chmk_Lq6TPIBMW925SPhw3Q; s_vnum=1466755240513%26vn%3D2; JYaH5Y2vxL=true; ads_firstpg=0; QSI_HistorySession=http%3A%2F%2Fwww.giantbomb.com%2Farticles%2Fesa-announces-free-public-e3-live-event%2F1100-5451%2F~1464163256082%7Chttp%3A%2F%2Fwww.giantbomb.com%2F~1464163264151%7Chttp%3A%2F%2Fwww.giantbomb.com%2Farticles%2Fesa-announces-free-public-e3-live-event%2F1100-5451%2F~1464361773855%7Chttp%3A%2F%2Fwww.giantbomb.com%2Freviews%2Fhomefront-the-revolution-review%2F1900-746%2F~1464361793406%7Chttp%3A%2F%2Fwww.giantbomb.com%2Fnews%2F~1464361953089; ssdef094=08cca12951e45e4b88a2716d2d2f6151-1464448858; xcab=1-0; xDUwNzEzYj=1; sptg=%5B%5D; s_sq=cnetcbsiall%3D%2526pid%253Dgiantbomb%25253A%25252F%2526pidt%253D1%2526oid%253DSubmit%2526oidt%253D3%2526ot%253DSUBMIT; s_cc=true; s_getNewRepeat=1464362460610-Repeat; s_lv_giantbomb=1464362460610; s_lv_giantbomb_s=Less%20than%207%20days; s_invisit=true; __utmt=1; __utma=223628573.1373292033.1464163238.1464163238.1464361764.2; __utmb=223628573.5.10.1464361764; __utmc=223628573; __utmz=223628573.1464163238.1.1.utmcsr=reddit.com|utmccn=(referral)|utmcmd=referral|utmcct=/r/gamernews; __utmv=223628573.|2=User%20Type=Anonymous=1^3=Subscription%20Type=None=1; aam_uuid=87483978197898106292947092788954342073; sq4YFvJMK2=1"
    }

    page = requests.get(url, headers=headers)
    page = cleaner.clean_html(page.content)
    return html.fromstring(page)

def get_links_from_url(url, domain, params):

    tree = request_page_tree(url)
    links = []
    for a in tree.xpath('//a'):
        ignore_link = False
        try:
            link = str(a.get('href'))
        except:
            #Link is somehow broken
            link = ''
            ignore_link = True
            pass

        if 'ignore_urls_with' in params:
            if any(pattern in link for pattern in params['ignore_urls_with']):
                ignore_link = True


        if 'ignore_urls_without' in params:
            found = False
            if any(pattern in link for pattern in params['ignore_urls_without']):
                found = True

            if not found:
                ignore_link = True

        if ignore_link:
            continue

        try:
            if '#' in link:
                link = link[:link.find('#')]

            if 'retain_params' not in params and '?' in link:
                link = link[:link.find('?')]

            if parse(link, rule='IRI') and (domain+'/') in link:
                links.append(str(link).encode('ASCII'))

        except ValueError as e:
            if 'http' not in link and 'java' not in link and len(link) > 1 and link != 'None' and link[0] not in  ['?', '#']:
                if str(link).encode('ASCII', 'ignore')[0] != '/':
                    link = '/' + link
                rel_link = 'http://' + domain + link
                try:
                    if parse(rel_link, rule='IRI'):
                        links.append(str(rel_link).encode('ASCII'))
                except: pass
            pass

        except: pass

    return list(set(links))

def get_page_content(url, params, domain):
    title_path = params['title_path'] + '//text()'
    content_path = params['content_path'] + '//text()'

    if 'img_path' in params:
        img_path = params['img_path']
    else:
        img_path = '//meta[@property="og:image"]'

    if 'img_prop' in params:
        img_prop = params['img_prop']
    else:
        img_prop = 'content'

    tree = request_page_tree(url)

    try:
        if 'check_node' in params:
            assert tree.xpath('boolean(' + params['check_node'] + ')') > 0
        elif 'check_path' in params:
            assert tree.xpath(params['check_path'])[0].get(params['check_param']).find(params['check_value']) >= 0
        else:
            assert tree.xpath('boolean(' + content_path + ')')
    except Exception:
        raise AssertionError('Not an article')

    title = ''.join(tree.xpath(title_path)).encode('utf-8', 'ignore')
    content = ''.join(tree.xpath(content_path)).encode('utf-8', 'ignore')

    try:
        img = str(tree.xpath(img_path)[0].get(img_prop))

        if len(img) < 3 or img.find('javascr') >= 0:
            raise Exception

        if img.find('http') < 0:
            if str(img).encode('ASCII')[0] != '/':
                img = '/' + img
            img = 'http://' + domain + img

    except Exception:
        img = ''
        pass

    return title, content, img

def get_page_summary(url, name, domain, params):

    max_title_length = 90

    title, content, img = get_page_content(url, params, domain)

    if len(title) > max_title_length:
        title = title[:max_title_length] + (title[max_title_length:] and '...')

    if len(content) > 400:
        summary = create_summary_text(content, title)
    elif len(content) > 30:
        summary = content
    else: raise AssertionError('Content not found')

    if len(title) < 3: raise AssertionError('Title not found')

    new_summary = {
        "title": unicode(title, errors='ignore'),
        "url": url,
        "source": name,
        "img_src": img,
        "text": unicode(summary, errors='ignore'),
        "date": (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()
    }

    # Additionally save page for future dataset
    try: save_page_in_file(content, title, img, url, name)
    except: pass

    return new_summary

def create_new_link(link, name, domain):
    link = str(link).encode('ASCII')

    if (link[:5] == 'https'):
        link = 'http:' + link[6:]

    new_link = {
        'url': link,
        'source': name,
        'domain': domain,
        'downloaded': False,
        'article': True
    }
    return new_link

### RSS parsing

def get_feed_entries(feed_url):
    d = feedparser.parse(feed_url)
    return d.entries

def get_feed_topics(d, ammount = 0):
    text = d.feed.title
    if 'description' in d.feed:
        text = text + " " + d.feed.description
    for post in d.entries:
        #text = text + " " + post.description + " " + post.title
        text = text + " " + post.title

    text_words = word_tokenize(text)
    text_aver_vector, _ = extract_features(text_words, text_words)

    distances = {}
    for topic in topics:
        distances[topic] = np.linalg.norm(text_aver_vector - word_vector(topic.lower()))
        # print "Distance to " + topic + " = " + str(distances[topic])


    feed_dict = OrderedDict(sorted(distances.items(), key=lambda t: t[1]))

    if ammount != 0:
        for i, k in enumerate(feed_dict):
            if i >= ammount:
                del feed_dict[k]

    feed_topics = []

    for topic in feed_dict:
        feed_topics.append(topic)

    return feed_topics

def extract_entry_info(entry, clear_html = True):
    # Searching entry title
    title = html.fromstring(entry.title).text_content()
    #title = title.encode('ASCII', 'ignore')
    title = title.encode('utf-8', 'ignore')
    title = str(title)


    # Searching entry content
    content = ''
    if 'description' in entry:
        content = entry.description
    if 'content' in entry:
        for piece in entry.content:
            new_piece = piece.value
            if content != new_piece:
                content = content + new_piece

    content_tree = html.fromstring(content)
    if content and clear_html == True:
        content = content_tree.text_content()
    
    #content = content.encode('ASCII', 'ignore')
    content = content.encode('utf-8', 'ignore')

    # Searching entry thumbnail
    imgs = []

    extensions = ['.jpg', '.png', '.gif', '.jpeg', '.webp']
    blacklist = ['.gifv', 'feedburner.com', '/stat?', '-test/', 'pixel.wp.com/b.gif']

    objects_urls = content_tree.xpath('//iframe/@src | //object/@data | //embed/@src')
    for url in objects_urls:
        if 'yout' in url:
            imgs.append('http://img.youtube.com/vi/' + youtube_video_id(url) + '/hqdefault.jpg')

    content_imgs = content_tree.xpath("//*[text()='[link]']/@href | //img/@src")
    for img in content_imgs:
        imgs.append(img)

    img_params = ['enclosures', 'media_thumbnail', 'media_content']
    img_attrs = ['url', 'src', 'href']

    for param in [param for param in img_params if param in entry]:
        for record in entry[param]:
            for attr in [attr for attr in img_attrs if attr in record]:
                imgs.append(record[attr])
            if not [attr for attr in img_attrs if attr in record]:
                imgs.append(str(record))

    filtered_images = [img for img in imgs if any(ext in img for ext in extensions) and not any(string in img for string in blacklist)]

    if filtered_images:
        thumbnail = filtered_images[0]
    else:
        thumbnail = ''

    return title, content, thumbnail

### Work with files and datasets

def save_page_in_file(content, title, img, url, name):
    file_name = url.replace('/', '').replace(':', '')
    file_name = filepath_prefix + 'saved_pages/' + str(name) + '/' + file_name + '.pickle'
    file_name = file_name.encode('ASCII')

    dir = os.path.dirname(file_name)
    if not os.path.exists(dir):
        os.makedirs(dir)

    with open(file_name, 'a+') as file:
        save = {'content': content, 'title': title, 'img': img, 'source': name, 'url': url}
        pickle.dump(save, file, pickle.HIGHEST_PROTOCOL)

def get_content_from_file(file):
    page = pickle.load(open(file, "rb"))
    return page['content']

def delete_wrong_files():
    for website in websites:
        if 'ignore_urls_with' in website['params']:
            dir = filepath_prefix + "saved_pages/" + str(website['name']) + "/"
            for file in os.listdir(dir):
                file_path = dir + file
                page = pickle.load(open(file_path, "a+"))
                if 'url' in page:
                    for pattern in website['params']['ignore_urls_with']:
                        pattern = pattern.replace('/', '')
                        if page['url'].find(pattern) != -1:
                            print file_path, page['url']
                            try:
                                os.remove(file_path)
                            except Exception as e:
                                print e
                                pass

def create_words_dataset(websites):
    words = []
    word_tokenized_dataset = []
    i = 0
    for website in websites:
        dir = filepath_prefix + "saved_pages/" + str(website['name']) + "/"
        try:
            for file in os.listdir(dir):
                file_path = dir + file
                #print(file_path)
                content = get_content_from_file(file_path)
                new_words = word_tokenize(content)
                words.extend(new_words)
                word_tokenized_dataset.append(new_words)

                i += 1
                if i % 1000 == 0:
                    print 'Got ' + str(i) + ' pages, len = ' + str(len(words))

                if i % 100000 == 0:
                    with open(str(i) + '_words_dataset.pickle', 'a+') as file:
                        pickle.dump(words, file, pickle.HIGHEST_PROTOCOL)

                    with open(str(i) + '_word_tokenized_dataset.pickle', 'a+') as file:
                        pickle.dump(word_tokenized_dataset, file, pickle.HIGHEST_PROTOCOL)
                    words = []
                    word_tokenized_dataset = []

        except OSError as e:
            print e
            pass

    with open('last_words_dataset.pickle', 'a+') as file:
        pickle.dump(words, file, pickle.HIGHEST_PROTOCOL)

    with open('last_word_tokenized_dataset.pickle', 'a+') as file:
        pickle.dump(word_tokenized_dataset, file, pickle.HIGHEST_PROTOCOL)

    #return words, word_tokenized_dataset

client = MongoClient('mongodb://127.0.0.1:81/meteor')
sources_collection = client['meteor']['sources']

websites = []
rss_feeds = []
user_sources = []
for source in sources_collection.find({}):
    if source['type'] == 'website':
        if 'domain' in source and 'home_url' in source and 'params' in source and 'title_path' in source['params'] and 'content_path' in source['params']:
            websites.append(source)
    if source['type'] == 'rss':
        rss_feeds.append(source)
    if source['type'] == 'user':
        user_sources.append(source)

dataset_dir = os.path.dirname(os.path.abspath(__file__)) + '/dataset/'

lines = open(dataset_dir+'long_list_stop_words.txt', 'r').readlines()
stop_words = [word[:-1].lower().encode('utf-8', 'ignore') for word in lines if word[-1] == '\n'] + [word.lower().encode('utf-8', 'ignore') for word in lines if word[-1] != '\n']
dictionary = pickle.load(open(dataset_dir+'dictionary.pickle', "rb"))
reverse_dictionary = pickle.load(open(dataset_dir+'reverse_dictionary.pickle', "rb"))
#embeddings = pickle.load(open(dataset_dir+'embeddings.pickle', "rb"))
idf_values = pickle.load(open(dataset_dir+'idf_values.pickle', "rb"))

topics = ['Science', 'Space', 'Astronomy', 'Photo', 'Comics', 'Cooking', 'Neuroscience', 'Politics',
          'Technology', 'Videogames', 'IT', 'Devices', 'Management', 'Marketing', 'Design', 'Food',
          'Startup', 'Console', 'Economics', 'Education', 'YouTube']

cleaner = Cleaner(meta=False, page_structure=False, style=False, kill_tags=['style','script','iframe','video'], safe_attrs_only=False, remove_unknown_tags=False)
img_cleaner = Cleaner(kill_tags=['img'], remove_unknown_tags=False)
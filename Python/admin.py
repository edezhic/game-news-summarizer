# -*- coding: utf-8 -*-
from mylib import *

db = client['meteor']
summaries_collection = db['summaries']
links_collection = db['links']
briefs_collection = db['briefs']
sources_collection = db['sources']
suggestions_collection = db['suggestions']

def del_url(url):
    summaries_collection.delete_one({'url': url})
    links_collection.delete_one({'url': url})

def del_source_summaries(name):
    summaries_collection.delete_many({'source': name})
    links_collection.delete_many({'source': name})

def del_summaries_and_links():
    summaries_collection.delete_many({})
    links_collection.delete_many({})

def set_not_an_article(url):
    links_collection.update_one({'url': url}, {'$set' : {'article': False}})
    summaries_collection.delete_one({'url': url})

def clean_dataset_parser_db():
    for website in websites:
        dataset_links_collection = db['dataset_links_collection_' + str(website['name'])]
        dataset_links_collection.delete_many({})

def default_briefs():

    briefs_collection.delete_many({'type': 'default'})

    default_briefs = [
        ["Home", "BigThink"],
        ["Photo", "500px-Blog", "NASA:ImgOfTheDay", "Astronomy-Images", "CanonRumors", "Envato-Tuts", "NikonRumors", "NG-PhotoOfTheDay", "OneBigPhoto"],
        ["Games", "IndieGames.com", "Eurogamer.net", "GameInformer.com", "GameReactor", "GameSpot", "GiantBomb", "PCGamer", "Polygon", "VG247", "Reddit:Gaming"],
        ["Space", "Astronomy-Images", "HubbleNews", "HubbleSite", "MinutePhysics", "NASA:ImgOfTheDay", "NYT:Space&Cosmos", "SpaceDaily.Com", "WhatIf?", "BBC:Scie&Environm", "BadAstronomy", "Reddit:Space"],
        ["Brain", "PsyBlog", "MindHacks", "AsapSCIENCE"],
        ["Business", "99U99U", "AltucherConf", "BensBlog", "Bloomberg", "BothSidesOfTheTable", "BudgetsAreexy", "BusinessInsider", "CNNMoney.com", "CNN-PersonalFin", "Forbes-PersonalFin"],
        ["Cooking", "101Cookbooks", "ACoupleCooks", "AnniesEats", "AverieCooks", "Apt2B-BakingCo.", "Bakerella.com", "Food52", "SimplyRecipes"],
        ["Devices", "AnandTech", "AndroidPolice", "MacRumors", "SamMobile", "Reddit:Gadgets"],
        ["Startup", "BensBlog", "BothSidesOfTheTable", "Kickstarter", "SiliconBeat", "VentureBeat", "VersionOne"],
        ["Music", "YTube:NewMusic", "YTube:ChillOut", "Reddit:Music"],
        ["Politics", "Reddit:WorldNews", "Reddit:News", "Reddit:IntNews"],
        ["YTube360", "YTube360"]
    ]

    for brief in default_briefs:
        briefs_collection.insert_one({
            'name': brief[0],
            'sources': brief[1:],
            'type': 'default'
        })

    print 'briefs number:' + str(briefs_collection.find({}).count())
    print 'topics number:' + str(len(topics))
    print 'sources number: ' + str(sources_collection.find({}).count())
    print 'summaries number: ' + str(summaries_collection.find().count())

def print_suggestions():
    suggestions = suggestions_collection.find()
    for suggestion in suggestions:
        print suggestion['url'], suggestion['count']


#url = 'https://twitter.com/cnnbrk'
url = 'https://new.vk.com/tproger'
begin = '.com/'
before = 'http://feed.exileed.com/vk/feed/'
print url_extract(url, begin, before)
#print url_extract('https://www.reddit.com/r/startups/new/.rss', '/r/', 'https://www.reddit.com/r/', '/.rss')


#title = 'как поживаешь человек из краснодарска ты странный вообщето'
#print unicode(title, errors='ignore')
#title = title.decode('utf-8')
#if len(title) > 90:
#    title = title[:90] + (title[90:] and '...')

#print title

#print summaries_collection.find_one({'url': 'http://www.anandtech.com/show/10448/adata-introduces-premier-sp550-m2-ssd'})
#print links_collection.find_one({'url': 'http://www.anandtech.com/show/10448/adata-introduces-premier-sp550-m2-ssd'})
#print request_page_tree('http://www.pcgamer.com/beyond-good-evil-2-is-still-happening/')

#del_summaries_and_links()

#print not links_collection.find_one({'url': 'http://www.sciencenews.org/feeds/headlines.rss'})

#default_briefs()


#for source in sources_collection.find({'zero_entries': True}):
#    print source['name']


#del_source_summaries('BothSidesOfTheTable')

#del_summaries_and_links()

#print feedparser.parse('http://feeds.newscientist.com/space')['feed']['image']['href']


#print len(rss_feeds)

#del_summaries_and_links()

#print_suggestions()


#standart_briefs()
#create_words_dataset(websites)

#del_url('http://www.engadget.com/2016/04/25/apple-macbook-review-2016/')

#del_site('InfoWorld')

#url = 'http://www.engadget.com/2016/04/25/apple-macbook-review-2016/'
#print request_page_tree(url)

#with open('full_word_tokenized_dataset.pickle', 'a+') as file:
#    pickle.dump(word_tokenized_dataset, file, pickle.HIGHEST_PROTOCOL)


#with open('word_tokenized_dataset.pickle', 'a+') as file:
#    pickle.dump(words, file, pickle.HIGHEST_PROTOCOL)


#with open('words_dataset.pickle', 'a+') as file:
#    words = pickle.load(file)

#print len(words)
#compute_idf(word_tokenized_dataset, dictionary)

#del_url('http://www.bbc.com/mundo/america_latina/2016/05/160531_venezuela_almagro_oea_que_es_carta_democratica_maduro_ps')

#del_site('PopSci')

#words, word_tokenized_dataset = create_words_dataset(['PopSci', 'BBC' ...])
#idf_values = compute_idf(words, word_tokenized_dataset)


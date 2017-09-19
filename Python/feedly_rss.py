from mylib import *

'''
var script = document.createElement('script');script.src = "https://ajax.googleapis.com/ajax/libs/jquery/1.6.3/jquery.min.js";document.getElementsByTagName('head')[0].appendChild(script); $("div[id*='overview']").each(function() { var child = $(this).children("div[data-uri*='/feed/']"); var uri = $(child).attr('data-uri'); console.log($(this).attr('data-followtitle'));  console.log(uri.substring(uri.indexOf('http')))})
'''

file = open(os.path.dirname(os.path.abspath(__file__)) + '/rss', 'r')
lines = file.readlines()

sources = {}

i = 0
for line in lines:
    if line[0] == ' ':
        line = line[1:]

    if line[-1] == '\n':
        line = line[:-1]

    if i == 0:
        name = line
        i = 1
    else:
        if line.find('gdata.youtube') > -1:
            line = line[line.find('users/') + 6:line.find('/uploads')]
            line = 'https://www.youtube.com/feeds/videos.xml?user=' + line
            name = name + '(YTube)'
            name = name.encode('ASCII', 'ignore')

        if line.find('os/-/') < 0:
            line = line.encode('ASCII', 'ignore')
            sources[line] = name
        i = 0


print len(sources)

urls = []


sources_collection.delete_many({'type': 'rss'})
for url in sources:
    sources_collection.update_one({'name': sources[url]}, {'$set': {'name': sources[url], 'type': 'rss', 'url': url}}, upsert=True)






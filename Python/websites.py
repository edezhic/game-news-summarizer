# -*- coding: utf-8 -*-

'''
MGI = {
    'name': 'MGInformer',
    'domain': 'www.metalgearinformer.com',
    'category': 'Videogames',
    'params': {
        'title_path': '//h1[@class="title single-title"]',
        'content_path': '//div[@class="post-single-content box mark-links"]/p',
        'img_path': '//div[@class="post-single-content box mark-links"]/p//img | //div[@class="post-single-content box mark-links"]/div//img',
        'img_prop': 'src',
        'check_node': '//body[contains(@class, "single-post")]',
        'retain_params': ''
}}


GiantBomb = {
    'name': 'GiantBomb',
    'domain': 'www.giantbomb.com',
    'category': 'Videogames',
    'params': {
        'title_path': '//article//h1[@class="news-title instapaper_title entry-title"]',
        'content_path': '(//article//section[@itemprop="articleBody"]//p | //article//section[@itemprop="description"]//p)',
        'check_node': '//div[@id="default-content"]//article[contains(@class, "content-body")]',
        'ignore_urls_with': ['/forums/', '/profile/']
}}

Steam = {
    'name': 'Steam',
    'domain': 'store.steampowered.com/news',
    'category': 'Videogames',
    'params': {
        'title_path': '//h2[@class="pageheader"]',
        'content_path': '//div[@id="news"]//div[@class="body"]',
        'img_path': '//div[@id="news"]//div[@class="body"]//img',
        'img_prop': 'src',
        'check_path': '//div[@class="headline"]//div[2]',
        'check_param': 'class',
        'check_value': 'date',
}}

PlayStationBlog = {
    'name': 'PlayStationBlog',
    'domain': 'blog.us.playstation.com',
    'category': 'Videogames',
    'params': {
        'title_path': '//div[@class="post-title"]//h1',
        'content_path': '//div[@class="well"]//div[@class="post-entry"]',
        'check_node': '//h1[contains(@id, "comments") and contains(@class, "alignright")]',
}}

Videogamespot = {
    'name': 'Videogamespot',
    'domain': 'www.Videogamespot.com',
    'category': 'Videogames',
    'params': {
        'title_path': '(//h1[@itemprop="name"] | //span[@itemprop="itemreviewed"] | //*[@class="kubrick-info__title"])',
        'content_path': '(//div[@itemprop="articleBody"]//p | //section[@itemprop="description"]//p | //section[@itemprop="articleBody"]//p)',
        'check_node': '//article[contains(@class, "article--one-column")]',
}}

VideogamesRadar = {
    'name': 'VideogamesRadar+',
    'domain': 'www.Videogamesradar.com',
    'category': 'Videogames',
    'params': {
        'title_path': '//h1[@itemprop="name"]',
        'content_path': '(//div[@id="article-body"]//p | //article//div[@id="content-after-image"]//p)',
        'check_node': '//article[contains(@class, "article")]',
}}

EuroGamer = {
    'name': 'EuroGamer',
    'domain': 'www.eurogamer.net',
    'category': 'Videogames',
    'params': {
        'title_path': '//header//h1',
        'content_path': '//article[@class="hd"]//p',
        'check_node': '//article/div[contains(@class, "social")]',
}}

GameReactor = {
    'name': 'GameReactor',
    'domain': 'www.gamereactor.eu',
    'category': 'Videogames',
    'params': {
        'title_path': '//div[@id="main"]//header//h1',
        'content_path': '//div[@class="breadtext"]/div/p',
        'check_node': '//meta[contains(@property, "og:type") and contains(@content, "article")]',
}}

Kotaku = {
    'name': 'Kotaku',
    'domain': 'kotaku.com',
    'category': 'Videogames',
    'params': {
        'title_path': '//header//h1',
        'content_path': '//div[@class="post-content entry-content js_entry-content "]//p',
        'check_node': '//meta[contains(@property, "og:type") and contains(@content, "article")]',
}}

XboxWire = {
    'name': 'XboxWire',
    'domain': 'news.xbox.com',
    'category': 'Videogames',
    'params': {
        'title_path': '//article//h1',
        'content_path': '(//div[@class="entry-content"]/p | //div[@class="entry-content"]/ul)',
        'img_path': '//header/img | //div[@class="entry-content"]//img',
        'img_prop': 'src',

}}

VG247 = {
    'name': 'VG247',
    'domain': 'www.vg247.com',
    'category': 'Videogames',
    'params': {
        'title_path': '//header//h1',
        'content_path': '//article/section/p',
        'check_node': '//div[@id="article"]',
    }
}

Escapist = {
    'name': 'Escapist',
    'domain': 'www.escapistmagazine.com',
    'category': 'Videogames',
    'params': {
        'title_path': '//h1[contains(@class, "headline")]',
        'content_path': '//*[contains(@itemprop, "Body")]/p',
        'check_node': 'not(//*[contains(text(), "Source:")]) and boolean(//*[contains(@itemprop, "Body")]/p)',
    }
}

PopSci = {
    'name': 'PopSci',
    'domain': 'www.popsci.com',
    'category': 'Science',
    'params': {
        'title_path': '//header//h1',
        'content_path': '(//div[@class="content"]//div[@class!="caption-wrapper"]/*/p[not(@class)] | //div[@class="content"]//div[@class!="caption-wrapper"]/*/p[@class="in-content-skip"])',
        'check_node': '//div[@class="field-tags inline"]',
}}

Phys = {
    'name': 'Phys',
    'domain': 'phys.org',
    'category': 'Science',
    'params': {
        'title_path': '//header//h1',
        'content_path': '//section[contains(@class,"content-holder")]//article//p[not(@class)]',
        'check_node': '//header/h5[contains(@class, "data")]'
}}

BBC = {
    'name': 'BBC',
    'domain': 'www.bbc.com',
    'category': 'Global',
    'params': {
        'title_path': '//h1',
        'content_path': '(//div[@property="articleBody"]//p | //div[@class="story-body"]//p)',
        'check_node': '//meta[contains(@property, "og:type") and contains(@content, "article")]',
        'ignore_urls_with': ['/mundo/', '/arabic/', '/zhongwen/', '/indonesia/', '/kyrgyz/', '/portuguese/', '/ukrainian/', '/azeri/', '/afrique/', '/japanese/', '/nepali/', '/russian/', '/swahili/', '/urdu/', '/bengali/', '/hausa/', '/gahuza/', '/pashto/', '/sinhala/', '/tamil/', '/uzbek/', '/burmese/', '/hindi/', '/gahuza/', '/persian/', '/somali/', '/turkce/', '/vietnamese/']
}}

ScienceDaily = {
    'name': 'ScienceDaily',
    'domain': 'www.sciencedaily.com',
    'category': 'Science',
    'params': {
        'title_path': '//h1[@id="headline"]',
        'content_path': '(//div[@id="story_text"]//p[@id="first"] | //div[@id="story_text"]//div[@id="text"]//p)',
        'check_node': '//h1[@id="headline"]',
        'ignore_urls_with': ['/videos/']
}}

NatGeogr = {
    'name': 'NatGeogr',
    'domain': 'nationalgeographic.com',
    'home_url': 'http://science.nationalgeographic.com/science',
    'category': 'Science',
    'params': {
        'title_path': '//h1/span[@itemprop="headline"]',
        'content_path': '//span[@itemprop="articleBody"]//div[@class="text smartbody parbase section"]',
        'check_node': '//meta[contains(@name, "news_keywords") and contains(@content, "science")]',
}}

SciNews = {
    'name': 'SciNews',
    'domain': 'www.sci-news.com',
    'category': 'Science',
    'params': {
        'title_path': '//header//h1',
        'content_path': '//div[@class="entry-content"]/p',
        'check_node': '//header//h1[contains(@class, "title")]',
}}

SciMag = {
    'name': 'SciMag',
    'domain': 'www.sciencemag.org',
    'category': 'Science',
    'params': {
        'title_path': '//header//h1',
        'content_path': '(//div[@class="pane-content"]//p | //div[@class="article__body"]//p)',
        'check_node': '//header//h1[contains(@class, "headline")]'
}}

SciAmerican = {
    'name': 'SciAmerican',
    'domain': 'scientificamerican.com',
    'category': 'Science',
    'params': {
        'title_path': '//header//h1',
        'content_path': '//div[@class="article-block article-text"]/p',
        'check_node': '//header//h1[contains(@class, "header")]',
}}

HackerNews = {
    'name': 'HackerNews',
    'domain': 'thehackernews.com',
    'category': 'IT',
    'params': {
        'title_path': '//article//h1',
        'content_path': '//article//div[@itemprop="articleBody"]//div[not(@class)]',
        'check_node': '//article//h1[@itemprop="headline name"]',
}}

ITNews = {
    'name': 'ITNews',
    'domain': 'www.itnews.com',
    'category': 'IT',
    'params': {
        'title_path': '//header//h1',
        'content_path': '(//div[@itemprop="reviewBody"]//p | //div[@itemprop="articleBody"]//p)',
        'check_node': '//header//h1[contains(@itemprop, "headline")]',
}}

TechNewsWorld = {
    'name': 'TechNewsWorld',
    'domain': 'www.technewsworld.com',
    'category': 'IT',
    'params': {
        'title_path': '//*[@id="story"]//h1',
        'content_path': '//*[@id="story-body"]/p[not(@id)]',
        'img_path': '//*[@id="story"]//img[@alt]',
        'img_prop': 'src',
        'check_node': '//*[@id="story"]//h1[contains(@class, "title")]',
}}

InfoWorld = {
    'name': 'InfoWorld',
    'domain': 'www.infoworld.com',
    'category': 'IT',
    'params': {
        'title_path': '//header//h1',
        'content_path': '//*[@itemprop="articleBody"]/p ',
        'check_node': '//header//h1[contains(@itemprop, "headline")]',
}}

ComputerWeekly = {
    'name': 'ComputerWeekly',
    'domain': 'www.computerweekly.com',
    'category': 'IT',
    'params': {
        'title_path': '//header//h1',
        'content_path': '//section[@id="content-body"]/p',
        'img_path': '//*[@id="main-content"]//img',
        'img_prop': 'src',
        'check_node': '//header//h1[contains(@class, "title")]',
        'ignore_urls_with' : ['/resources/']
}}

TechCrunch = {
    'name': 'TechCrunch',
    'domain': 'techcrunch.com',
    'category': 'IT',
    'params': {
        'title_path': '//article//header//h1',
        'content_path': '//article//div[contains(@class, "article-entry")]/*[not(self::img or self::div or self::small)]'
    }
}

SiliconValley = {
    'name': 'SiliconValley',
    'domain': 'www.siliconvalley.com',
    'category': 'IT',
    'params': {
        'title_path': '//*[contains(@class, "articleBox")]//h1',
        'content_path': '//*[contains(@class, "articleBox")]//*[contains(@id, "articleBody")]/p'
    }
}

SiliconBeat = {
    'name': 'SiliconBeat',
    'domain': 'www.siliconbeat.com',
    'category': 'IT',
    'params': {
        'title_path': '//*[@id="main"]//h1',
        'content_path': '//*[contains(@class,"post-content")]/*[self::p or self::ul]'
    }
}

CNET = {
    'name': 'CNET',
    'domain': 'www.cnet.com',
    'category': 'Global',
    'params': {
        'title_path': '//h1',
        'content_path': '(//div[@itemprop="reviewBody"]//p | //div[@itemprop="articleBody"]//p)',
        'check_node': '//div[@itemprop="reviewBody"] | //div[@itemprop="articleBody"]',
}}

CNN = {
    'name': 'CNN',
    'domain': 'cnn.com',
    'home_url': 'http://edition.cnn.com',
    'category': 'Global',
    'params': {
        'title_path': '//article//h1',
        'content_path': '//section[@id="body-text"]//*[contains(@class, "zn-body__paragraph")]',
        'check_node': '//section[@id="body-text"]//*[contains(@class, "zn-body__paragraph")]',
}}

SkyNews = {
    'name': 'SkyNews',
    'domain': 'news.sky.com',
    'category': 'Global',
    'params': {
        'title_path': '//header//h1',
        'content_path': '//div[contains(@class, "content-column")]/p',
}}

TheGuardian = {
    'name': 'TheGuardian',
    'domain': 'www.theguardian.com',
    'category': 'Global',
    'params': {
        'title_path': '//header//h1',
        'content_path': '//div[@itemprop="articleBody"]/p',
        'check_node': '//div[@itemprop="articleBody"]',
}}

GlobalNews = {
    'name': 'GlobalNews',
    'domain': 'globalnews.ca',
    'category': 'Global',
    'params': {
        'title_path': '//article//h1',
        'content_path': '//*[@itemprop="articleBody"]/p',
}}

TheVerge = {
    'name': 'TheVerge',
    'domain': 'www.theverge.com',
    'category': 'Global',
    'params': {
        'title_path': '//article//h1',
        'content_path': '//article//p',
        'check_node': '//meta[contains(@property, "og:type") and contains(@content, "article")]',
}}

Wired = {
    'name': 'Wired',
    'domain': 'www.wired.com',
    'category': 'Global',
    'params': {
        'title_path': '//main//h1',
        'content_path': '//article/p',
        'check_node': '//article[contains(@class, "body")]',
}}

SamMobile = {
    'name': 'SamMobile',
    'domain': 'www.sammobile.com',
    'category': 'Devices',
    'params': {
        'title_path': '//article//h1',
        'content_path': '//div[@class="article-text"]/p',
        'check_node': '//article[contains(@class, "col")]'
}}

Engadget = {
    'name': 'Engadget',
    'domain': 'www.engadget.com',
    'category': 'Devices',
        'params': {
        'title_path': '//article//header//h1',
        'content_path': '//article//div[contains(@class,"article-text")]/p'
}}

'''

############################## Videogames
PCGamer = {
    'name': 'PCGamer',
    'domain': 'pcgamer.com',
    'topics': ['Videogames'],
    'params': {
        'title_path': '//h1[@itemprop="name"]',
        'content_path': '//div[contains(@id, "article-body") or contains(@id, "content-after-image")]//p',
        'check_node': '//article[contains(@class, "article")]',
}}

PlayOverWatch = {
    'name': 'PlayOverWatch',
    'domain': 'playoverwatch.com',
    'home_url': 'https://playoverwatch.com/en-us/blog/',
    'topics': ['Videogames'],
    'params': {
        'title_path': '//div[@class="blog-wrap"]//h1',
        'content_path': '//div[@class="blog-content"]/div//p',
        'img_path': '//div[@class="blog-header-image"]//img',
        'img_prop': 'src',
        'check_node': '//section[@class="body clearfix"]',
        'ignore_urls_with': ['.com//']
}}


Polygon = {
    'name': 'Polygon',
    'domain': 'www.polygon.com',
    'topics': ['Videogames'],
    'params': {
        'title_path': '(//h1 | //article//header//h2)',
        'content_path': '(//div[@class="m-feature-modern__body"] | //div[@id="review-body"] | //div[@id="article-body"]/p)',
        'check_node': '//div[@class="m-share-buttons"]',
        'ignore_urls_with': ['/forums/', '/login', '/users/']
}}

############################ SCIENCE

HowStuffWorks = {
    'name': 'HowStuffWorks',
    'domain': 'howstuffworks.com',
    'topics': ['Science'],
    'params': {
    'title_path': '//div[@id="page"]//h1',
    'content_path': '//div[@class="infinite-item"]/p'
}}

ScienceNews = {
    'name': 'ScienceNews',
    'domain': 'www.sciencenews.org',
    'topics': ['Science'],
    'params': {
        'title_path': '//header//h1',
        'content_path': '//div[@property="rnews:articlebody schema:articleBody"]//p[not(@class="inst-desc")]',
        'check_node': '//header//h1[@class="node-title"]',
        'ignore_urls_with': ['/blog/', '/topic/', '/editors-picks/']
}}

############################# IT

NBCNews = {
    'name': 'NBCNews',
    'domain': 'www.nbcnews.com',
    'topics': ['Politics'],
    'params': {
        'title_path': '//header//h1',
        'content_path': '//div[@class="article-body"]/p',
        'check_node': '//div[contains(@class, "article-body") and contains(@itemprop, "Body")]',
        'ignore_urls_with': ['/video/']
}}

Independent = {
    'name': 'Independent',
    'domain': 'www.independent.co.uk',
    'topics': ['Politics'],
    'params': {
        'title_path': '//h1[@itemprop="headline"]',
        'content_path': '//*[@itemprop="articleBody"]/p',
        'check_node': '//*[@itemprop="articleBody"]',
}}

websites = [
    PCGamer, PlayOverWatch, Polygon,
    ScienceNews, HowStuffWorks,
    NBCNews, Independent
]



if __name__ == '__main__':
    from pymongo import MongoClient
    client = MongoClient('mongodb://127.0.0.1:3001/meteor')
    db = client['meteor']
    sources_collection = db['sources']
    sources_collection.delete_many({'type': 'website'})

    for website in websites:
        if 'home_url' not in website:
            home_url = ('https://' if 'https' in website else 'http://') + website['domain']
        else:
            home_url = website['home_url']

        query = {'name': website['name']}
        set = {'$set': {'name': website['name'], 'type': 'website', 'domain': website['domain'], 'home_url': home_url, 'params': website['params'], 'topics': website['topics']}}
        sources_collection.update_one(query, set, upsert = True)

    print sources_collection.find({}).count()

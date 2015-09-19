# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join

def strip_text(s):
    return s.strip()


class NewsItem(scrapy.Item):
    url = scrapy.Field()        #url
    title = scrapy.Field()      #标题
    text = scrapy.Field()       #正文


class NewsLoader(ItemLoader):
    url_in = MapCompose(strip_text)
    url_out = TakeFirst()
    
    title_in = MapCompose(strip_text)
    title_out = TakeFirst()

    text_in = MapCompose(strip_text)
    text_out = Join('\n')


import scrapy
import re
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join

def strip_text(s):
    return re.sub(r'\s*', '', s)


class TianyaItem(scrapy.Item):
    url = scrapy.Field()        #路径
    text = scrapy.Field()       #正文


class TianyaLoader(ItemLoader):
    url_in = MapCompose(strip_text)
    url_out = TakeFirst()

    text_in = MapCompose(strip_text)
    text_out = Join('\n')




import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join

def strip_text(s):
    return s.strip()


class TiebaItem(scrapy.Item):
    url = scrapy.Field()        #路径
    title = scrapy.Field()      #标题
    text = scrapy.Field()       #正文


class TiebaLoader(ItemLoader):
    url_in = MapCompose(strip_text)
    url_out = TakeFirst()

    title_in = MapCompose(strip_text)
    title_out = TakeFirst()

    text_in = MapCompose(strip_text)
    text_out = Join('\n')




import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join


def strip_text(s):
    return s.strip()


class TxweiboItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()


class TxweiboLoader(ItemLoader):
    url_in = MapCompose(strip_text)
    url_out = TakeFirst()
    
    title_in = MapCompose(strip_text)
    title_out = TakeFirst()

    text_in = MapCompose(strip_text)
    text_out = Join('\n')



import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join


def strip_text(s):
    return s.strip()


class SinaWeiboItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()


class SinaWeiboLoader(ItemLoader):
    url_in = MapCompose(strip_text)
    url_out = TakeFirst()

    title_in = MapCompose(strip_text)
    title_out = TakeFirst()

    text_in = MapCompose(strip_text)
    text_out = Join('\n')





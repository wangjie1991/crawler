# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join

def strip_text(s):
    t = s.strip()
    t = t.replace(' ', '')
    # last char is } or ; maybe javascript code
    if (1 <= len(t)):
        if ('}' == t[-1]) or \
           ('{' == t[-1]) or \
           (';' == t[-1]):
            return ''

    if (2 <= len(t)):
        if ('//' == t[0:2]):
            return ''

    return t


class TextItem(scrapy.Item):
    path = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()


class TextLoader(ItemLoader):
    #path_in = MapCompose(strip_text)
    path_out = TakeFirst()
    
    title_in = MapCompose(strip_text)
    title_out = TakeFirst()

    text_in = MapCompose(strip_text)
    text_out = Join('\n')



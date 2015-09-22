# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join

def strip_text(s):
    t = s.strip()
    # last char is } or ; maybe javascript code
    if (1 <= len(t)) and (('}' == t[-1]) or (';' == t[-1])):
        return ''
    else:
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
    text_out = Join('')



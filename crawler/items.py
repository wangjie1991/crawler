# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join

def strip_text(s):
    return s.strip()


class TextItem(scrapy.Item):
    path = scrapy.Field()
    text = scrapy.Field()


class TextLoader(ItemLoader):
    #path_in = MapCompose(strip_text)
    path_out = TakeFirst()

    text_in = MapCompose(strip_text)
    text_out = Join('\n')

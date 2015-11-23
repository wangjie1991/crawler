# -*- coding: utf-8 -*-

import re
import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join

pat_stp1 = re.compile(r'\s*')
pat_stp2 = re.compile(r'http:[\w/.#%&?=\-]*')
pat_stp3 = re.compile(r'[@]')

def strip_text(s):
    t = s.strip()
    t = pat_stp1.sub('', t)
    t = pat_stp2.sub('', t)
    t = pat_stp3.sub('', t)

    # last char is } or ; maybe javascript code
    # if (1 <= len(t)):
        # if ('}' == t[-1]) or \
           # ('{' == t[-1]) or \
           # (';' == t[-1]):
            # return None

    # if (2 <= len(t)):
        # if ('//' == t[0:2]):
            # return None 

    if ('' == t):
        return None
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
    text_out = Join('\n')



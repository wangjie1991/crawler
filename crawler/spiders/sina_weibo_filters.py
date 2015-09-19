# -*- coding: utf-8 -*-

import os
import re
#from scrapy import log
from pybloomfilter import BloomFilter


class SinaWeiboBloomFilter():
    
    def __init__(self, domain):
        self.html_tmp = '/tmp/%s_%s' % (domain, 'html_url.bloom')

        if os.path.exists(self.html_tmp):
            self.html_bf = BloomFilter.open(self.html_tmp)
        else:
            self.html_bf = BloomFilter(10000000, 0.001, self.html_tmp)
    
    def filter_html(self, urls):
        new_urls = set()
        
        for url in urls:
            idx = url.find('?')
            if idx != -1:
                head = url[:idx+1]
                tail = ''
                tail_list = re.findall('(page=\d*)', url)
                if tail_list:
                    tail = tail_list[0]
                url = head + tail
            
            #s = '!!!!! url = ' + url
            #log.msg(s, level=log.INFO)
            #http://t.qq.com/kaifulee?page=98
            if not self.html_bf.add(url):
                new_urls.add(url)
        
        return new_urls

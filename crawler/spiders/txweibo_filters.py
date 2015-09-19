# -*- coding: utf-8 -*-

import os
import re
#from scrapy import log
from pybloomfilter import BloomFilter


class WeiboBloomFilter():
    
    def __init__(self, domain):
        self.html_tmp = '/tmp/%s_%s' % (domain, 'html_url.bloom')

        if os.path.exists(self.html_tmp):
            self.html_bf = BloomFilter.open(self.html_tmp)
        else:
            self.html_bf = BloomFilter(10000000, 0.001, self.html_tmp)
    
    def filter_html(self, links):
        new_links = []
        
        for link in links:
            url = link.url
            idx = url.find('?')
            if idx != -1:
                head = url[:idx+1]
                tail = ''
                tail_list = re.findall('&(pi=[0-9]*?)&', url)
                if tail_list:
                    tail = tail_list[0]
                url = head + tail
            
            #s = '!!!!! url = ' + url
            #log.msg(s, level=log.INFO)
            #http://t.qq.com/kaifulee?pi=98
            if not self.html_bf.add(url):
                new_links.append(link)
        
        return new_links

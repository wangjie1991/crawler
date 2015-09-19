# -*- coding: utf-8 -*-

import os
import re
from pybloomfilter import BloomFilter


class UrlFilter():
    
    def __init__(self, domain):
        self.index_tmp = '/tmp/%s_%s' % (domain, 'index_url.bloom')
        self.html_tmp = '/tmp/%s_%s' % (domain, 'html_url.bloom')

        if os.path.exists(self.index_tmp):
            self.index_bf = BloomFilter.open(self.index_tmp)
        else:
            self.index_bf = BloomFilter(10000000, 0.001, self.index_tmp)

        if os.path.exists(self.html_tmp):
            self.html_bf = BloomFilter.open(self.html_tmp)
        else:
            self.html_bf = BloomFilter(10000000, 0.001, self.html_tmp)
    
    def filter_index(self, links):
        new_links = []
        for link in links:
            if not self.index_bf.add(link.url):
                new_links.append(link)
        return new_links

    def filter_html(self, links):
        new_links = []
        for link in links:
            if not self.html_bf.add(link.url):
                new_links.append(link)
        return new_links

    def filter_txweibo(self, links):
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
    
    def filter_sinaweibo(self, urls):
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

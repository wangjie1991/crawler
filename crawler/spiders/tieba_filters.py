# -*- coding: utf-8 -*-

import os
from pybloomfilter import BloomFilter


class MyBloomFilter():
    
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

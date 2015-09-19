# -*- coding: utf-8 -*-

import os
import re
from pybloomfilter import BloomFilter


class LinkFilter():
    
    def __init__(self, domain):
        self.tmp_index = '/tmp/%s_%s' % (domain, 'index.bf')
        self.tmp_html = '/tmp/%s_%s' % (domain, 'html.bf')

        if os.path.exists(self.tmp_index):
            self.bf_index = BloomFilter.open(self.tmp_index)
        else:
            self.bf_index = BloomFilter(10000000, 0.001, self.tmp_index)

        if os.path.exists(self.tmp_html):
            self.bf_html = BloomFilter.open(self.tmp_html)
        else:
            self.bf_html = BloomFilter(10000000, 0.001, self.tmp_html)
    
    def index_filter(self, links):
        new_links = []
        for link in links:
            if not self.bf_index.add(link.url):
                new_links.append(link)
        return new_links

    def html_filter(self, links):
        new_links = []
        for link in links:
            if not self.bf_html.add(link.url):
                new_links.append(link)
        return new_links

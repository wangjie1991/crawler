# -*- coding: utf-8 -*-

import os
import re
from scrapy import log
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
            #log.msg('This is a link : %s' % link, level=log.WARNING)
            if not self.bf_html.add(link.url):
                new_links.append(link)
        return new_links


class BaiduMusicFilter(LinkFilter):

    def url_filter(self, links):
        mdf_links = []
        for link in links:
            link = self.modify_url(link)
            if link:
                mdf_links.append(link)

        return self.html_filter(mdf_links)

    def modify_url(self, link):
        url = link.url
        tag = '%09%20%20%20%20%09/tag/'
        idx1 = url.find('?tag')
        idx2 = url.find(tag)

        if (-1 != idx1):
            return None
 
        if (-1 != idx2):
            head = url[:idx2]
            tail = url[idx2+len(tag):]
            url = head + tail
            url = url.rstrip('%0A++++')
            link.url = url

        return link



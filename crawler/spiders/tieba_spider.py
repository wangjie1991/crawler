# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from tieba.spiders.filters import MyBloomFilter
from tieba.items import TiebaItem, TiebaLoader


class TiebaSpider(CrawlSpider):
    name = 'tieba'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['http://tieba.baidu.com/']
    #start_urls = ['http://tieba.baidu.com/f?kw=%BF%EC%C0%D6%B4%F3%B1%BE%D3%AA']
    mbf = MyBloomFilter('tieba')
    
    rules = [Rule(LinkExtractor(allow=(r'http://tieba.baidu.com/p/[0-9]*$', r'http://tieba.baidu.com/p/[0-9]*\?pn=[0-9]*$')),
                  callback='parse_item', follow=True, process_links=mbf.filter_html),
             Rule(LinkExtractor(allow=(r'http://tieba.baidu.com/f[/\?].*?')), process_links=mbf.filter_index)]
    
    def parse_item(self, response):
        loader = TiebaLoader(item = TiebaItem(), response = response)

        #with open('url.txt', 'a') as f:
        #    u = response.url + '\n'
        #    f.write(u.encode('utf-8'))
        
        # get path
        # path = 'http://娱乐明星/港台东南亚明星/周杰伦/3915073118/1.htm'
        first_class = ''
        second_class = ''
        fname = ''
        sels = response.xpath('//div[contains(@class, "wrap2")]//text()')
        for sel in sels:
            first = sel.re(r'first_class:\s*?"(.*?)"')
            second = sel.re(r'second_class:\s*?"(.*?)"')
            if len(first) and len(second):
                first_class = first[0]
                second_class = second[0]
                break
        
        if response.xpath('//meta//@fname'):
            fname = response.xpath('//meta//@fname').extract()[0]
        
        pid = response.url
        pid = pid[pid.rfind('/')+1:]
        pn = 0
        if pid.find('?pn=') != -1:
            pn = pid[pid.find('?pn=')+4:]
            pid = pid[:pid.find('?')]
        else:
            pn = 1

        nl = [first_class, second_class, fname, pid, str(pn)]
        for i in range(len(nl)):
            if 0 == len(nl[i]):
                nl[i] = '_'
        url = 'http://%s/%s/%s/%s/%s.htm' % (nl[0], nl[1], nl[2], nl[3], nl[4])
        
        loader.add_value('url', url)
        if pn == 0:
            loader.add_xpath('title', '//h1/text()')
        loader.add_xpath('text', '//div[re:test(@class, "d_post_content j_d_post_content[\s\S]*?")]//text()')
        
        return loader.load_item()

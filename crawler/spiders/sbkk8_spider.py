# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from crawler.spiders.pathextractor import PathExtractor
from crawler.spiders.linkfilter import LinkFilter
from crawler.items import TextItem, TextLoader
from crawler import settings


class Sbkk8Spider(CrawlSpider):
    name = 'sbkk8'
    start_urls = ['http://www.sbkk8.cn/']
    allowed_domains = ['www.sbkk8.cn']

    linkfilter = LinkFilter('sbkk8')
    pathextractor = PathExtractor()

    rules = [
                Rule(LinkExtractor(allow=r'http://www\.sbkk8\.cn/.*\.s?html?$'), 
                     callback='parse_item', follow=True, 
                     process_links=linkfilter.html_filter),
                Rule(LinkExtractor(allow=r'http://www\.sbkk8\.cn/.*/$'), 
                     process_links=linkfilter.index_filter)
            ]
    
    def parse_item(self, response):
        loader = TextLoader(item=TextItem(), response=response)

        path = self.pathextractor.host(settings.SBKK8_STORE, response.url)
        loader.add_value('path', path)
        loader.add_xpath('title', '//h1/text()')

        ps = response.xpath('//div[@id="f_article"]//p')
        if not ps:
            ps = response.xpath('//div[@id="f_article"]/div')
        if not ps:
            ps = response.xpath('//div[@id="f_article"]')
        if not ps:
            ps = response.xpath('//div[@id="articleText"]//p')

        for p in ps:
            ts = p.xpath('.//text()').extract()
            text = ''.join(ts)
            loader.add_value('text', text)

        item = loader.load_item()

        # if ('text' not in item) or (item['text'] == ''):
            # with open('url.txt', 'a') as url_file:
                # url = response.url + '\n'
                # url_file.write(url.encode('utf-8'))

        return item



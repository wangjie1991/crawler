# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from crawler.spiders.pathextractors import PathExtractor
from crawler.spiders.linkfilter import LinkFilter
from crawler.items import TextItem, TextLoader


class SinaSpider(CrawlSpider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn']
    linkfilter = LinkFilter('sina')
    
    rules = [# 规则1匹配文本页面，一定做URL去重
             Rule(LinkExtractor(allow=(r'http://news.sina.com.cn/.*?s?html')), 
                  callback='parse_item', follow=True, process_links=linkfilter.html_filter),
             # 规则2匹配新闻索引页面，不提取文本。
             Rule(LinkExtractor(allow=(r'http://news.sina.com.cn/.*?/')), process_links=linkfilter.index_filter)]
             #Rule(LinkExtractor(allow=(r'http://news.sina.com.cn/.*?/')))]
    
    def parse_item(self, response):
        loader = NewsLoader(item=NewsItem(), response=response)

        path = PathExtractor.parse_sina(response.url)
        loader.add_value('path', path)

        # title compatible of new and old page
        # loader.add_xpath('title', '//h1[contains(@id, "artibodyTitle")]//text()')
        h1 = response.xpath('//h1/text()')
        if h1:
            loader.add_xpath('text', '//h1/text()')
        else:
            loader.add_xpath('text', '//th[contains(@class, "f24")]/text()')
        
        # text compatible of new and old page
        t1 = response.xpath('//div[contains(@id, "artibody")]//p//text()')
        t2 = response.xpath('//div[contains(@id, "article")]//p/text()')
        if t1:
            # <p>中会有<strong>修饰文本，也为了最大匹配artibody，保证<p>匹配成功
            loader.add_xpath('text', '//div[contains(@id, "artibody")]//p//text()')
        elif t2:
            # <div id=article>内一些<p>会在里层，而且这里匹配失败会全匹配<p>，容易引入js杂料，所以这里需要匹配最大化
            # 早期网页中一般没有将重要文本放入<p>里层，里层反而有js等。
            loader.add_xpath('text', '//div[contains(@id, "article")]//p/text()')
        else:
            # 旧的网页对<p>敏感度高，一般不会里层包含文本。如果深层获取，还会引入一些js杂料
            loader.add_xpath('text', '//p/text()')
        
        return loader.load_item()

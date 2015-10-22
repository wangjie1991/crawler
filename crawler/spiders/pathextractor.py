# -*- coding: utf-8 -*-

import re
import urllib
from scrapy import log
from crawler import settings


class PathExtractor():
    tieba_first_class = re.compile(r'first_class:\s*?"(.*?)"')
    tieba_second_class = re.compile(r'second_class:\s*?"(.*?)"')

    def host(self, store, url):
        path = url.lstrip('http://')
        path = path[:path.rfind('.')]
        path = '%s/%s.txt' % (store, path)
        return path

    def weibo(self, store, url):
        path = url.lstrip('http://weibo.cn/')
        path = path[:path.rfind('?')]
        path = '%s/%s.txt' % (store, path)
        return path

    def baidumusic(self, url):
        # http://music.baidu.com/tag/%E7%94%B5%E8%A7%86%E5%89%A7?start=200&size=25&third_type=0
        url = urllib.unquote(url)
        url = url.lstrip('http://music.baidu.com/tag/')
        url = url.strip('\t')
        
        p = ''
        f = ''
        idx = url.find('?')
        
        if (-1 == idx):
            p = url
            f = '0'
        else:
            p = url[:idx]
            fl = re.findall('start=([0-9]*)', url)
            if fl:
                f = fl[0]
            else:
                f = 'x'
        
        path = '%s/%s/%s.txt' % (settings.BDYY_STORE, p, f)
        return path

    def tieba(self, store, response):
        # 娱乐明星/港台东南亚明星/周杰伦/3915073118/1.txt'
        body = response.body.decode('utf-8')

        first = '_'
        second = '_'
        first_list = self.tieba_first_class.findall(body)
        second_list = self.tieba_second_class.findall(body)
        if first_list and second_list:
            first = first_list[0]
            second = second_list[0]

        fname = '_'
        fname_list = response.xpath('//meta//@fname')
        if fname_list:
            fname = fname_list[0].extract()
        
        page_id = '_'
        page_num = '_'
        url = response.url
        url = url[url.rfind('/')+1:]
        index = url.find('?pn=')
        if (-1 == index):
            page_id = url
            page_num = '1'
        else:
            page_id = url[:index]
            page_num = url[index+4:]

        path = '%s/%s/%s/%s/%s/%s' % (store, first, second, fname, page_id, page_num)
        return path



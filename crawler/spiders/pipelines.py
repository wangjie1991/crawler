# -*- coding: utf-8 -*-

from news_crawler import settings
import os


class NewsPipeline(object):
    
    def process_item(self, item, spider):
        b_url = 'url' in item and item['url'] != ''
        b_text = 'text' in item and item['text'] != ''
        
        if b_url and b_text :
            # write url list
            #with open('url.txt', 'a') as f:
            #    u = item['url'] + '\n'
            #    f.write(u.encode('utf-8'))

            # get directory and filename
            url = item['url'][7:]
            idx = url.rfind('/')
            d = '%s/%s' % (settings.NEWS_STORE, url[:idx])
            fn = url[idx+1:]
            fn = fn[:fn.rfind('?')]
            fn = fn[:fn.rfind('.')] + '.txt'
            fn = '%s/%s' % (d, fn)
            
            if not os.path.exists(d):
                os.makedirs(d)
            
            with open(fn, 'w') as f:
                if 'title' in item and item['title'] != '':
                    s = item['title'] + '\n'
                    f.write(s.encode('utf-8'))
                s = item['text'] + '\n'
                f.write(s.encode('utf-8'))
        
        return item




from tianya import settings
import os


class TianyaPipeline(object):

    def process_item(self, item, spider):
        b_url = 'url' in item and item['url'] != ''
        b_text = 'text' in item and item['text'] != ''

        if b_url and b_text :
            # get directory and filename
            ulist = item['url'].split('-')
            path = '%s/%s/%s' % (settings.STORE, ulist[1], ulist[2])
            fn = ulist[3]
            fn = fn[:fn.rfind('.')] + '.txt'
            fn = '%s/%s' % (path, fn)

            if not os.path.exists(path):
                os.makedirs(path)

            with open(fn, 'w') as f:
                s = item['text'] + '\n'
                f.write(s.encode('utf-8'))

        return item




from tieba import settings
import os


class TiebaPipeline(object):
    
    def process_item(self, item, spider):
        b_url = 'url' in item and item['url'] != ''
        b_text = 'text' in item and item['text'] != ''
        
        if b_url and b_text :
            # get directory and filename
            url = item['url'][7:]
            idx = url.rfind('/')
            d = '%s/%s' % (settings.STORE, url[:idx])
            fn = url[idx+1:]
            fn = fn[:fn.rfind('?')]
            fn = fn[:fn.rfind('.')] + '.txt'
            fn = '%s/%s' % (d, fn)
            
            if not os.path.exists(d):
                os.makedirs(d)
            
            with open(fn, 'w') as f:
                if 'title' in item and item['title'] != '':
                    s = item['title'] + '\n'
                    f.write(s.encode('utf-8'))
                s = item['text'] + '\n'
                f.write(s.encode('utf-8'))
        
        return item




from txweibo import settings
import os
import re


class TxweiboPipeline(object):
    
    def process_item(self, item, spider):
        b_url = 'url' in item and item['url'] != ''
        b_title = 'title' in item and item['title'] != ''
        b_text = 'text' in item and item['text'] != ''
        
        if b_url and b_title and b_text :
##            with open('url.txt', 'a') as f:
##                s = item['url'] + '\t'
##                s = s + item['title'] + '\n'
##                f.write(s.encode('utf-8'))
            
            # get directory and filename
            path = '%s/%s' % (settings.STORE, item['title'])
            fl = re.findall('&pi=([0-9]*?)&', item['url'])
            fn = 0
            if fl:
                fn = fl[0]
            else:
                fn = 0
            fn = '%s/%s.txt' % (path, fn)
            
            if not os.path.exists(path):
                os.makedirs(path)
            
            with open(fn, 'w') as f:
                s = item['text'] + '\n'
                f.write(s.encode('utf-8'))
        
        return item




from sina_weibo import settings
import os
import re


class SinaWeiboPipeline(object):

    def process_item(self, item, spider):
        b_url = 'url' in item and item['url'] != ''
        b_title = 'title' in item and item['title'] != ''
        b_text = 'text' in item and item['text'] != ''

        if b_url and b_title and b_text:
##            with open('url.txt', 'a') as f:
##                s = item['url'] + '\t'
##                s = s + item['title'] + '\n'
##                f.write(s.encode('utf-8'))

            # get directory and filename
            path = '%s/%s' % (settings.STORE, item['title'])
            fl = re.findall('page=(\d*)', item['url'])
            fn = 1
            if fl:
                fn = fl[0]
            fn = '%s/%s.txt' % (path, fn)

            if not os.path.exists(path):
                os.makedirs(path)

            with open(fn, 'w') as f:
                s = item['text'] + '\n'
                f.write(s.encode('utf-8'))

        return item





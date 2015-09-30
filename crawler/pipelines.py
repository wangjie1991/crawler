# -*- coding: utf-8 -*-

import os


class TextPipeline(object):
    
    def process_item(self, item, spider):
        b_path = 'path' in item and item['path'] != ''
        b_text = 'text' in item and item['text'] != ''
        
        if b_path and b_text:
            path = item['path']
            text = item['text']

            d = path[:path.rfind('/')]
            if not os.path.exists(d):
                os.makedirs(d)
            
            with open(path, 'w') as fout:
                if 'title' in item and item['title'] != '':
                    s = item['title'] + '\n'
                    fout.write(s.encode('utf-8'))
                fout.write(text.encode('utf-8'))
        
        return item


class WeiboPipeline(object):
    
    def process_item(self, item, spider):
        b_path = 'path' in item and item['path'] != ''
        b_text = 'text' in item and item['text'] != ''
        
        if b_path and b_text:
            path = item['path']
            text = item['text']

            d = path[:path.rfind('/')]
            if not os.path.exists(d):
                os.makedirs(d)
            
            with open(path, 'a') as fout:
                fout.write(text.encode('utf-8'))



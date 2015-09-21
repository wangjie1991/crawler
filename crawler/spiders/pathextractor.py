# -*- coding: utf-8 -*-

import re
import urllib
from crawler import settings


class PathExtractor():

    def baidumusic(self, url):
        # http://music.baidu.com/tag/%E7%94%B5%E8%A7%86%E5%89%A7?start=200&size=25&third_type=0
        url = urllib.unquote(url)
        # write url list
        #with open('/home/wangjie/url.txt', 'a') as f:
        #    u = '%s\n%s\n\n' % (url, path)
        #    #f.write(u.encode('utf-8'))
        #    f.write(u)
        url = url.lstrip('http://music.baidu.com/tag/')
        
        p = ''
        f = ''
        idx = url.find('?')
        
        if (-1 == idx):
            p = url
            f = '0'
        else:
            p = url[:idx]
            fl = re.findall('start=([0-9]*?)', url)
            if fl:
                f = fl[0]
            else:
                f = 'x'
        
        path = '%s/%s/%s.txt' % (settings.BDYY_STORE, p, f)
        return path


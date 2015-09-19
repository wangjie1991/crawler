# -*- coding: utf-8 -*-

import os
from crawler import settings


class PathExtractor():

    def parse_sina(self, url):
        path = url.lstrip('http://')
        path = path[:path.rfind('.')]
        path = '%s/%s.txt' % (settings.SINA_STORE, path)
        return path

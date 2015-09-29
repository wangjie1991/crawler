# -*- coding: utf-8 -*-

import urllib
import base64
import re
import binascii
import rsa
import scrapy


class Login():

    def __init__(self, username, pwd, start_urls):
        self.username = username
        self.pwd = pwd
        self.start_urls = start_urls


    def prelogin(self):
        url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack' \
              '&su=%s&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.15)&_=1400822309846' % self.username
        return scrapy.Request(url, callback=self.postData)


    def postData(self, response):
        body = response.body
        servertime = re.findall('"servertime":(.*?),', body)[0]
        nonce = re.findall('"nonce":"(.*?)",', body)[0]
        pubkey = re.findall('"pubkey":"(.*?)",', body)[0]
        rsakv = re.findall('"rsakv":"(.*?)",', body)[0]

        su = urllib.quote(self.username)
        su = base64.encodestring(su)[:-1]

        rsapubkey = int(pubkey, 16)
        key = rsa.PublicKey(rsapubkey, 65537)
        message = servertime + '\t' + nonce + '\n' + self.pwd
        sp = binascii.b2a_hex(rsa.encrypt(message, key))

        data = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'userticket': '1',
            'pagerefer': 'http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D',
            'vsnf': '1',
            'su': su,
            'service': 'miniblog',
            'servertime': servertime,
            'nonce': nonce,
            'pwencode': 'rsa2',
            'rsakv': rsakv,
            'sp': sp,
            'sr': '1680*1050',
            'encoding': 'UTF-8',
            'prelt': '961',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack'
        }

        url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
        return scrapy.FormRequest(url, formdata=data, callback=self.preCrawl)


    def preCrawl(self, response):
        body = response.body
        url = re.findall('location.replace\(\'(.*?)\'\);', body)[0]
        return scrapy.Request(url, callback=self.startCrawl)


    def startCrawl(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url)

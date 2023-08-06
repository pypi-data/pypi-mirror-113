#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import requests
import os
import urllib

def write(filename,text,typename='w',encoding='utf8'):
    dirname = os.path.dirname(filename)
    print(dirname)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(filename,typename,encoding=encoding) as f:
        f.write(text)

def read(filename,typename='r',encoding='utf8'):
    with open(filename,typename,encoding=encoding) as f:
        return f.read()
    return ''

def getHtml(url,retry_count = 5):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3", 
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
    }
    while retry_count > 0:
        try:
            res = requests.get(url, headers=headers,timeout=10)
            if res.apparent_encoding.lower()=='gb2312':
                return res.text.encode("latin1").decode("gbk")
            else:
                res.encoding = res.apparent_encoding
                return res.text
        except Exception as e:
            print(e)
            retry_count -= 1
    return None

def existsWebFile(srcUrl):
    result = False
    with requests.get(srcUrl, stream=True) as r:
        result = r.ok
    return result

def handleURL(uri):
    result = urllib.parse.urlparse(uri)
    url = result.scheme + '://' + result.netloc + result.path
    return url

def escape_string(value):
    _escape_table = [chr(x) for x in range(128)]
    _escape_table[0] = "\\0"
    _escape_table[ord("\\")] = "\\\\"
    _escape_table[ord("\n")] = "\\n"
    _escape_table[ord("\r")] = "\\r"
    _escape_table[ord("\032")] = "\\Z"
    _escape_table[ord('"')] = '\\"'
    _escape_table[ord("'")] = "\\'"
    return value.translate(_escape_table)